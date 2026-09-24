# BL-HAOS Testing Guide

This repository ships three independently testable surfaces — the **bridge add-on** (`modules/bridge`), the **Home Assistant integration** (`modules/integration`), and the **Ingress web UI** (`modules/bridge/web_ui`). Tests are organized into layers with explicit environment requirements so that every developer, on any OS, has a fast feedback loop and CI enforces the same gates.

## The five-layer pyramid

| Layer | Scope | Command | Environment | Gate |
|---|---|---|---|---|
| **L0** Static contracts | `tsc` typecheck, frontend production build, manifest/S6/Dockerfile static tests (inside pytest) | `scripts/run-tests.ps1 -Layer L0` / `scripts/run-tests.sh L0` | any OS | exit 0 |
| **L1** Unit / API regression | Bridge backend suite (`modules/bridge/tests`, 118+ tests), integration client unit tests (`modules/integration/tests/unit`), frontend vitest | `scripts/run-tests.ps1 -Layer L1` | any OS (Windows OK) | exit 0 |
| **L2** Home Assistant SIL | `modules/integration/tests/test_ha_integration_sil.py` — real HA Core in-process | `scripts/run-tests.sh L2` | **Linux only** (CI or WSL2) | exit 0 |
| **L3** Browser E2E | Playwright against the real backend in demo mode | `scripts/run-tests.ps1 -Layer L3` | any OS with Chromium | exit 0 |
| **L4** HAOS VM validation | Full add-on + integration on a HAOS virtual machine | manual, see `RELEASE-RUNBOOK.md` | HAOS VM | release evidence |

Run everything runnable on your machine: `scripts/run-tests.ps1 -Layer all` (L2 auto-skips with an explanation on Windows).

## Quick start (Windows)

```powershell
# 1. Bridge unit + integration unit + frontend unit
.\scripts\run-tests.ps1 -Layer L1

# 2. Browser E2E (boots the backend in demo mode automatically)
.\scripts\run-tests.ps1 -Layer L3
```

## Quick start (Linux / WSL2 / CI)

```bash
./scripts/run-tests.sh all   # includes the HA SIL suite
```

## Environment matrix

| Surface | Native Windows | WSL2 | Linux CI |
|---|---|---|---|
| Bridge L1 | ✅ | ✅ | ✅ |
| Integration client unit tests | ✅ | ✅ | ✅ |
| Integration HA SIL (L2) | ❌ (`fcntl`) | ✅ | ✅ |
| Frontend unit + build | ✅ | ✅ | ✅ |
| Playwright E2E | ✅ | ✅ (GUI deps) | ✅ |

### Why SIL is Linux-only

Home Assistant Core imports Unix-only standard-library modules (`fcntl`) at import time, which fails on native Windows. The official HA development guidance recommends WSL2 or containers. The suite is **auto-skipped** on Windows (`pytest_ignore_collect` in `modules/integration/tests/conftest.py`) so a plain `pytest` run still passes; set `BLHAOS_RUN_SIL=1` inside WSL2 to force it.

### ha_stubs: client unit tests without the HA runtime

`modules/integration/tests/ha_stubs/` provides a minimal `homeassistant.*` stand-in (task helpers, `async_get_clientsession` returning the injected `FakeSession`). It is activated only for `tests/unit/` via that folder's `conftest.py`, so the full SIL suite always uses the real runtime. This lets `BLHAOSClient` command payloads, error surfacing, and snapshot reconciliation be tested on Windows — previously impossible because the SIL fake rejected every POST.

## Pinned dependencies

### Bridge tests — `modules/bridge/backend/requirements-test.txt`

Installed by both `builder.yaml` (release gate) and `tests.yml` (PR/push CI). Pins `pytest`, `pytest-asyncio`, `pytest-cov`, `dbus-fast`, `PyYAML` on top of `requirements.txt` via `-r`.

> **pytest-asyncio note**: the plugin's entry-point name is `asyncio` (not `pytest_asyncio`), which is why both `pytest.ini` files use `-p asyncio`. `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` is set by the runner scripts to prevent `pytest-homeassistant-custom-component` (installed for SIL) from hijacking bridge-only runs on machines that have it.

### HA SIL — `modules/integration/requirements-sil.txt`

| Pin | Value |
|---|---|
| `pytest-homeassistant-custom-component` | `0.13.366` |
| `homeassistant` (Core) | `2026.9.3` |

### Upgrading the HA Core pin (deliberate, gated procedure)

1. Bump `homeassistant==` in `requirements-sil.txt` to the target Core release.
2. Bump `pytest-homeassistant-custom-component==` to the version that targets that Core release (check its changelog).
3. Open a PR; the `integration-sil` CI job must pass, plus `integration-unit` and `frontend`.
4. Run the Playwright E2E suite against a demo backend built from the updated venv.
5. Record the new pin + date in this table. Never upgrade Core and the custom-component pin separately.

## CI

| Workflow | Trigger | Jobs |
|---|---|---|
| `.github/workflows/tests.yml` | push to `main`, PRs | `bridge-unit` (L1), `integration-unit` (L1), `integration-sil` (L2), `frontend` (L3: vitest → build → Playwright) |
| `modules/bridge/.github/workflows/builder.yaml` | push/tags | release gates (bridge L1 + frontend build + audits) → multi-arch add-on image build |

## Writing tests

- **Bridge backend**: plain pytest with `asyncio_mode = auto` — write `async def test_*` without markers. Fakes for D-Bus, processes, and sinks live in each test module; keep fakes local and small.
- **Integration client**: put tests in `modules/integration/tests/unit/`; use the `FakeSession` from `tests/conftest.py` (`session.command_response`, `session.command_status`, then assert on `session.commands`).
- **HA SIL behaviors** (config flows, entity registry, diagnostics redaction) still belong in `test_ha_integration_sil.py` — they need the real runtime.
- **Frontend unit**: colocate as `*.test.ts(x)` next to the component; `vitest.config.ts` picks up `src/**/*.test.{ts,tsx}`.
- **Browser E2E**: add specs to `modules/bridge/web_ui/e2e/specs/`; the Playwright `webServer` recipe boots the backend in `BLHAOS_DEMO_MODE=true` automatically (override the target with `BLHAOS_E2E_URL`).

## Coverage

Bridge backend coverage runs with `--cov=backend` when `pytest-cov` is installed:

```powershell
cd modules/bridge
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'
python -m pytest tests -q -p asyncio --asyncio-mode=auto --cov=backend --cov-report=term-missing --cov-fail-under=85
```

Frontend coverage is informational for now (no gate).

## Historical note

The Docker-Compose live-bridge test harness was retired (see `.github/skills/update-e2e-tests/SKILL.md`); deep validation now flows through L1/L3 locally, L2 in CI, and L4 in the HAOS VM. The former ad-hoc Playwright specs under `.planning/runtime-validation/` have been promoted into `modules/bridge/web_ui/e2e/`.
