# BL-HAOS Testing Guide

This repository ships three independently testable surfaces — the **bridge add-on** (`modules/bridge`), the **Home Assistant integration** (`modules/integration`), and the **Home Assistant-native panel** (`modules/integration/panel_ui`). Tests are organized into layers with explicit environment requirements so that every developer, on any OS, has a fast feedback loop and CI enforces the same gates.

## The five-layer pyramid

| Layer | Scope | Command | Environment | Gate |
|---|---|---|---|---|
| **L0** Static contracts | `tsc` typecheck, frontend production build, manifest/S6/Dockerfile static tests (inside pytest), tracked-file hygiene (CI job `repo-hygiene`) | `scripts/run-tests.ps1 -Layer L0` / `scripts/run-tests.sh L0` | any OS | exit 0 |
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
| `pytest-homeassistant-custom-component` | `0.13.374` |
| `homeassistant` (Core) | `2026.10.3` |
| `aiohttp` | `3.14.5` (required by Core) |
| `pytest` | `9.0.3` |

Phase 24 rebaseline approved and measured on 2026-10-24: Python 3.14.4 under Ubuntu WSL, 24 actual passes in 4.06s, no skips. From `/mnt/f/Workspace/BL-HAOS/modules/integration`:

```sh
BLHAOS_RUN_SIL=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests/test_panel_registration.py tests/test_ha_integration_sil.py -q -p asyncio --asyncio-mode=auto
```

This local gate is not live panel acceptance. The temporary Task 24-01-02
contract probe was accepted and removed after exactly one authorized restart.
It did not deploy the production panel or prove actual expiry/physical playback.
Task 24-06-01 remains blocked; no demo E2E or Windows skip substitutes for it.
Official Core testing guide: https://contributors.home-assistant.io/core/development/testing/.

### Phase 24 Separate Local Gates

From the repository root use the existing Ubuntu WSL environment (Python
3.14.4, Core 2026.10.3, helper 0.13.374, aiohttp 3.14.5, pytest 9.0.3).
Run real Core and stub units in separate processes, never mixed collection:

```powershell
wsl.exe -d Ubuntu --cd /mnt/f/Workspace/BL-HAOS/modules/integration env BLHAOS_RUN_SIL=1 PYTHONDONTWRITEBYTECODE=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests --ignore=tests/unit -q -p asyncio --asyncio-mode=auto --tb=short --show-capture=no
wsl.exe -d Ubuntu --cd /mnt/f/Workspace/BL-HAOS/modules/integration env PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests/unit -q -p asyncio --asyncio-mode=auto --tb=short --show-capture=no
npm --prefix modules/integration/panel_ui test
npm --prefix modules/integration/panel_ui run build
npm --prefix modules/integration/panel_ui test
npm --prefix modules/integration/panel_ui run build
./scripts/run-tests.ps1 -Layer L1
```

For full Windows bridge checks, change directory to `modules/bridge`, set
`$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'`, then run
`../../.venv/Scripts/python.exe -B -m pytest -c pytest.ini tests -q -p asyncio --asyncio-mode=auto`.
The existing POSIX-only skip is not HA proof. Pure harness validator tests run
from `modules/integration/panel_ui` using `npm run test:host-config`; they never
contact HA or dispatch playback.

### Phase 24 Authorized Target-Host Acceptance (Pending)

Production panel/release 0.2.69 remain undeployed. Do not run host tests until
installation, host access and real playback are separately authorized. This
suite dispatches real play, not a silent probe. The previous one-restart
authorization is exhausted; no restart, radio reset, pairing, shared-session
extraction, expiry or revocation is implied.

Prepare these environment inputs without putting values in source control,
logs, app code or this document:

| Input | Required contract |
|---|---|
| `BLHAOS_HA_URL` | Credential-free HTTP(S) Core 2026.10.3 origin, no path/query/fragment |
| `BLHAOS_HA_STORAGE_STATE` | Absolute external workspace-disposable authenticated Playwright file outside repository roots; harness-only |
| `BLHAOS_HA_TARGET` | Explicit connected BL-HAOS media_player entity, no implicit speaker |
| `BLHAOS_HA_PROVIDER_ID` | Original opaque expandable media-source provider reference |
| `BLHAOS_HA_PLAYLIST_ID` | Original opaque playable playlist reference in that provider |
| `BLHAOS_HA_ALLOW_PLAYBACK` | Exactly `I_AUTHORIZE_REAL_PLAYBACK` for this test environment |
| `BLHAOS_HA_EXPIRY_STORAGE_STATE` | Different external separately authorized disposable expired-session fixture, never the shared/current user |
| `BLHAOS_HA_EXPIRY_CONSENT` | Exactly `I_AUTHORIZE_DISPOSABLE_EXPIRY_OBSERVATION` |
| `BLHAOS_HA_EXPIRY_ATTESTATION` | Exactly `I_ATTEST_SEPARATE_DISPOSABLE_FIXTURE_IS_EXPIRED_READ_ONLY`; its owner attests the fixture session already expired outside the harness, which only reads it |

Use actual opaque references supplied by the operator or discovered through
the public HA UI. No provider-name guesses, raw URL resolution, session-state
extraction or token mutation is part of the harness. Without a safe expiring
fixture, actual expiry remains pending; an invalid sentinel or unauthenticated
context proves denial only, not expiry. The expiry scenario passes only when
the attested fixture reaches the HA login page (`/auth/authorize`) or receives
an HA auth rejection (`/auth/token` 400/401 or `/api/` 401) with no accepted
call. Only origin-local pathnames and status codes are observed. A numeric
connection loss, 403 or `unauthorized` on a live connection is never expiry.
Otherwise the scenario hard-fails and expiry stays unproven.

From `modules/integration/panel_ui`, after those authorizations and prerequisites:

```powershell
npm run test:host
```

The separate `e2e/playwright.config.ts` checks exact Core and the actual HA
`bl-haos-media-panel` shadow root, not a demo. Missing prerequisites hard-fail,
never skip/fake acceptance. Default execution without env must fail before host
access: record an expected precondition failure, not a passed host test.
Traces, HAR, video and automatic failure screenshots are disabled. Explicit
catalog screenshots go under ignored `test-results/ha-catalog` at 375/768/1440
after checking visible content. Never print auth/storage-state contents,
credentials, resolved URLs or raw network payloads. External browser state is
test-harness input only; no application code receives it.

Review all three real HA screenshots and verify keyboard traversal, Escape
focus return, visible focus, labels/polite announcements, contrast, long target
names, 44px hit areas, overflow/overlap and reduced motion. Public-provider
layout, denied/unavailable/unresolvable cases, leakage/fallback, actual natural
session expiry and physical audio need host evidence and a human backstop.
Local validators and fixture screenshots establish none of these. Saved
playlist CRUD (Phase 25) and queues/sequential playback (Phase 26) are not
implemented. Retired Docker E2E is not an acceptance path.

### Upgrading the HA Core pin (deliberate, gated procedure)

1. Bump `homeassistant==` in `requirements-sil.txt` to the target Core release.
2. Bump `pytest-homeassistant-custom-component==` to the version that targets that Core release (check its changelog).
3. Open a PR; the `integration-sil` CI job must pass, plus `integration-unit` and `frontend`.
4. Run the Playwright E2E suite against a demo backend built from the updated venv.
5. Record the new pin + date in this table. Never upgrade Core and the custom-component pin separately.

## CI

| Workflow | Trigger | Jobs |
|---|---|---|
| `.github/workflows/tests.yml` | push to `main`, PRs | `repo-hygiene` (L0), `bridge-unit` (L1), `integration-unit` (L1), `integration-sil` (L2), `frontend` (L3: vitest → build → Playwright) |
| `modules/bridge/.github/workflows/builder.yaml` | push/tags | release gates (bridge L1 + frontend build + audits) → multi-arch add-on image build |

## Writing tests

- **Bridge backend**: plain pytest with `asyncio_mode = auto` — write `async def test_*` without markers. Fakes for D-Bus, processes, and sinks live in each test module; keep fakes local and small.
- **Integration client**: put tests in `modules/integration/tests/unit/`; use the `FakeSession` from `tests/conftest.py` (`session.command_response`, `session.command_status`, then assert on `session.commands`).
- **HA SIL behaviors** (config flows, entity registry, diagnostics redaction) still belong in `test_ha_integration_sil.py` — they need the real runtime.
- **Frontend unit**: colocate as `*.test.ts(x)` next to the component; `vitest.config.ts` picks up `src/**/*.test.{ts,tsx}`.
- **Native panel mock E2E**: panel-only mock Playwright coverage lives under `modules/integration/panel_ui/e2e/` and does not boot the bridge or contact a live HA host. Real-HA browser checks require separate authorization.
- **Never abandon a coroutine.** Both `pytest.ini` files escalate `RuntimeWarning`, so a coroutine that is created but never awaited fails the suite instead of scrolling past as a warning. Schedule it (`asyncio.create_task` behind a "is a loop running?" guard) or close it; a bare `asyncio.create_task` on a synchronous code path both loses the work and trips this gate.

## Live verification scripts

Two operator-facing scripts validate a real installation. Both take every
installation-specific value from the environment, so no host, entity, or
credential is stored in the repository.

| Script | Purpose | Usage |
|---|---|---|
| `ui_check.py` | Retained operational/API probes and Home Assistant `media_player` checks; not an ingress UI check | `set HATOK=<token>` then `python ui_check.py --host host[:port]` (authorized host only) |
| `ingress_probe.py` | Historical pre-retirement probe; not a current headless add-on UI check | Do not use for current Phase 38 candidate acceptance |

`ui_check.py` discovers the native entity from the attributes the bridge
publishes (`bluetooth_address`, `adapter`), so it is correct on any
installation; override with `--entity` / `BLHAOS_ENTITY`. Checks the environment
cannot evaluate are reported as `SKIP`, never as a failure: playback without
`BLHAOS_UI_CHECK_MEDIA`, and playback plus text-to-speech while the speaker is
disconnected (`media_player` state `off`). Exit codes: `0` pass (skips allowed),
`1` failed check, `2` unusable invocation (no token or an unresolvable entity).
Set `BLHAOS_UI_CHECK_MEDIA` to a short audio URL to assert the playback timeline
too, and `--tts` / `BLHAOS_TTS` to choose the TTS entity.

`ingress_probe.py` is a historical tool from before the Phase 38 UI retirement.
It may resolve Supervisor Ingress metadata but does not restore the retired UI or
prove current add-on functionality. Do not treat it as a current acceptance path.

## Coverage

Bridge backend coverage runs with `--cov=backend` when `pytest-cov` is installed:

```powershell
cd modules/bridge
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'
python -m pytest tests -q -p asyncio --asyncio-mode=auto --cov=backend --cov-report=term-missing --cov-fail-under=85
```

Frontend coverage is informational for now (no gate).

## Autonomous Workflow & Mock Strategy

To enable reliable, non-blocking autonomous execution (`/gsd-autonomous`) across all phases (Phases 24, 25, 26, 27) without sacrificing production rigor:

### 1. Full Mock Autonomous Progression
- **Automated Gates (L0-L3)**: Every plan executed autonomously must pass 100% exit 0 on all local gates:
  - **L0**: Types (`tsc`), linter, and static file hygiene.
  - **L1**: Bridge backend tests (`modules/bridge/tests`, 323+ tests, >=85% coverage) + integration client unit tests (`modules/integration/tests/unit` with `ha_stubs`) + frontend Vitest suites.
  - **L2**: Linux/WSL Home Assistant SIL (`modules/integration/tests/test_ha_integration_sil.py` and `test_panel_registration.py`, 127+ tests) running against real Home Assistant Core 2026.10.3 in-process with `pytest-homeassistant-custom-component`.
  - **L3**: Headless Playwright browser tests for the retained native panel using the mock-HA shell harness; the retired bridge Ingress UI and demo harness are not built or tested.
- **Physical Hardware & Live Host Deferral**: Live host acceptance requiring operator authorization, credentials, physical Bluetooth speakers, or host restarts (e.g., Plan 24-06 live target playback, Phase 27 physical speaker soak, and Phase 20 live Pi/VM go-live) is formally staged and deferred to a dedicated post-milestone live verification phase. Automated synthetic mocks and SIL tests serve as the acceptance criteria for milestone feature completion.

### 2. Mocking Boundaries & Fidelity Levels
- **Home Assistant Media Source**: Synthetic mock `media_source` provider fixtures in HA SIL provide multi-level folder hierarchies, playable streams, unresolvable IDs, and permission-denied entries to thoroughly test catalog browsing and playlist item resolution without external network dependencies.
- **Audio Stream Driver**: In-memory controllable audio stream driver in the bridge backend fires natural completion (EOF), errors, and duration-based advancement without spawning real ffmpeg or PipeWire processes.
- **Sequential Playback & Queue Concurrency**: Queue management (advancement, shuffle, repeat, manual skip, stop) is tested via deterministic async event interleaving in pytest. Queue generation tokens and lease ownership prevent race conditions and stale process callbacks without timing flakiness.
- **Panel & Web UI Mock-Shell**: Frontend components are tested at unit level with Vitest, and at browser level with Playwright against a lightweight mock-HA shell simulating the Home Assistant environment (`hass` object, WebSocket `media_source/browse_media`, service calls, and dark Neumorphic theme tokens).

## Historical note

The Docker-Compose live-bridge test harness was retired (see `.github/skills/update-e2e-tests/SKILL.md`); deep validation now flows through L1/L3 locally, L2 in CI, and L4 in the HAOS VM. The retired bridge ingress app and demo Playwright harness are removed; the distinct Home Assistant-native panel mock harness remains. Real-HA browser acceptance belongs to the authorized HAOS VM workflow.
