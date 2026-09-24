# Implementation Plan — Refined Test Strategy for BL-HAOS

## [Overview]

Establish a single, layered, environment-aware test strategy that makes the BL-HAOS bridge, HA integration, and web UI testable on any developer machine (Windows included) and enforces the same gates in CI. Today the suites work but are fragile: the bridge pytest run depends on an undocumented `PYTEST_DISABLE_PLUGIN_AUTOLOAD` workaround, the root `pytest.ini` conflicts with `modules/integration` (unknown `asyncio_mode` warning, wrong `pythonpath`), the HA integration SIL suite cannot run on native Windows (`fcntl`) and has zero command-path coverage (`FakeSession.post()` raises on every POST), the frontend has no unit tests and no checked-in E2E harness, and there is no Linux CI job executing the integration SIL suite (pending todo `add-linux-ha-sil-ci.md`).

The high-level approach is a five-layer pyramid, each layer pinned to an explicit environment:

1. **L0 — Static contracts** (any OS): `tsc` typecheck, frontend production build, package-layout / manifest / S6-structure / Dockerfile static tests. Already exists; formalized as a named stage.
2. **L1 — Unit / API regression** (any OS, no host services): the 118-test bridge suite (FastAPI TestClient, fake D-Bus, fake processes) plus new integration-client unit tests that run **without** the Home Assistant runtime by faking `homeassistant` imports, so command paths are covered on Windows too.
3. **L2 — Home Assistant SIL** (Linux only: CI or WSL2): the existing `test_ha_integration_sil.py` suite against a **pinned** Home Assistant Core version via `pytest-homeassistant-custom-component`, executed in a new CI job.
4. **L3 — Browser E2E** (any OS with Playwright): promote the ad-hoc `.planning/runtime-validation/*.spec.js` flows into a permanent, checked-in Playwright suite (`modules/bridge/web_ui/e2e/`) running against the real FastAPI app in demo mode.
5. **L4 — HAOS VM validation** (release-time, documented): existing go-live runbook; out of scope for automation here but referenced as the final evidence tier.

The plan touches configuration, test infrastructure, CI, and documentation. It deliberately does **not** change production code except for two minimal, test-driven cleanups in `ws.py` (tracked broadcast tasks) that remove a persistent test warning.

## [Types]

No new production types. Test-infrastructure types:

- `FakeSession.post()` (integration test fake): change from `raise AssertionError` to a recording dispatcher with `self.commands: list[tuple[str, dict]]` and `self.command_response: dict | Exception | None`.
- Collect-skip guard in `modules/integration/tests/conftest.py` implemented as a `pytest_ignore_collect(collection_path, config)` hook keyed on `sys.platform == 'win32'` and env `BLHAOS_RUN_SIL=1`, so Windows default collection skips SIL files instead of erroring on `fcntl`.
- New `ha_stubs/` package (`modules/integration/tests/ha_stubs/`) providing minimal `homeassistant.*` stand-ins used only by L1 client unit tests; declared in a new `modules/integration/tests/unit/` folder with its own `conftest.py` that inserts `ha_stubs` into `sys.path` **only** when the real Home Assistant is absent.

## [Files]

New files:

| Path | Purpose |
|---|---|
| `modules/bridge/pytest.ini` (modify) | Add `asyncio_mode = auto` (removes the CLI-flag workaround), targeted `filterwarnings` for unawaited-coroutine errors, and a coverage `fail_under = 85` block. |
| `pytest.ini` (root, modify) | Becomes a thin aggregator: `testpaths = modules/bridge/tests`, `pythonpath = modules/bridge`, `asyncio_mode = auto`; integration module gets its own ini. |
| `modules/integration/pytest.ini` (new) | Own config: `testpaths = tests`, `asyncio_mode = auto`, marker `sil` for the HA-runtime suite. |
| `modules/integration/tests/unit/test_client_commands.py` (new) | L1 unit tests for `BLHAOSClient.async_command` and `_async_listen` reconnect logic using `ha_stubs` (Windows-safe). |
| `modules/integration/tests/ha_stubs/**` (new) | Stub package: `__init__.py`, `homeassistant/__init__.py`, `core.py`, `config_entries.py`, `exceptions.py`, `helpers/aiohttp_client.py`. |
| `modules/bridge/web_ui/e2e/playwright.config.ts` (new) | Checked-in Playwright config: `baseURL` from `BLHAOS_E2E_URL` (default `http://127.0.0.1:8099`), Chromium project, retries=1 in CI, webServer recipe booting `uvicorn bl_haos.main:app` with `BLHAOS_DEMO_MODE=true`. |
| `modules/bridge/web_ui/e2e/specs/{dashboard,diagnostics,recovery,volume}.spec.ts` (new) | The three validated flows from `runtime-validation-report.md` plus a new volume-slider flow exercising `POST /api/devices/{address}/volume`. |
| `modules/bridge/web_ui/src/**/*.test.ts(x)` (new, 3–4 files) | Vitest unit tests for `api/client.ts` URL builders and error mapping, `SpeakerCard` volume commit, `RecoveryPanel` result rendering. |
| `modules/bridge/web_ui/vitest.config.ts` (new) | Vitest config reusing `vite.config.ts` plugins, `environment: 'jsdom'`. |
| `.github/workflows/tests.yml` (new) | Jobs: `bridge-unit` (L0+L1, ubuntu py3.12), `integration-sil` (L2, pinned HA Core), `frontend` (vitest + build + Playwright L3). |
| `scripts/run-tests.ps1` + `scripts/run-tests.sh` (new) | One-command local runner with `-Layer L0|L1|L2|L3|all` encoding all plugin/env workarounds. |
| `TESTING.md` (new, repo root) | Documents the five layers, pinned HA Core version + upgrade procedure, environment matrix (Windows / WSL2 / Linux CI). |
| `modules/bridge/backend/requirements-test.txt` (new) | Pinned test deps: `pytest==9.0.3`, `pytest-asyncio==1.4.0`, `pytest-cov==7.1.0`, `dbus-fast`, `PyYAML`. |
| `modules/integration/requirements-sil.txt` (new) | Pinned `pytest-homeassistant-custom-component==0.13.366`, `homeassistant==2026.9.3`. |

Modified files:

| Path | Change |
|---|---|
| `modules/bridge/tests/conftest.py` | Add `pytest_configure` assertion of asyncio mode; keep the Windows dbus-fast socket shim. |
| `modules/integration/tests/conftest.py` | Extend `FakeSession.post` to record commands and return configurable responses; add `pytest_ignore_collect` platform guard. |
| `modules/integration/tests/test_package_layout.py` | Add assertions that the strategy artifacts (`pytest.ini`, `e2e/` config, `TESTING.md`) exist. |
| `modules/bridge/backend/bl_haos/api/ws.py` | Tracked broadcast cleanup in the two websocket endpoints so no orphaned coroutines remain (removes the RuntimeWarning at its source). |
| `modules/bridge/tests/test_ws.py` | +1 regression test: broadcast send-failures are logged and no un-awaited coroutines remain. |
| `modules/bridge/web_ui/package.json` | devDependencies: `vitest`, `jsdom`, `@testing-library/react`, `@playwright/test`; scripts `test`, `test:unit`, `test:e2e`, `test:e2e:install`. |
| `.github/workflows/builder.yaml` | Replace ad-hoc pip install list with `pip install -r backend/requirements-test.txt`. |

Deleted / moved: none. `.planning/runtime-validation/*.spec.js` content is **promoted** into `modules/bridge/web_ui/e2e/`; the temporary folder is documented as obsolete in `TESTING.md`.

## [Functions]

New functions:

- `scripts/run-tests.ps1 -Layer <L0|L1|L2|L3|all>` and `scripts/run-tests.sh <layer>` — set `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`, invoke the right pytest/vitest/playwright entry per layer; L2 prints a clear skip reason on Windows unless `BLHAOS_RUN_SIL=1` (WSL2 path documented).
- `modules/integration/tests/ha_stubs/homeassistant/core.py::HomeAssistant` — supports the subset `client.py` uses: `async_create_task`, `async_create_background_task`, `async_block_till_done`, `config_entries`, `data`, `states`.
- `modules/integration/tests/ha_stubs/helpers/aiohttp_client.py::async_get_clientsession(hass)` — returns the `FakeSession` stashed on `hass.data['bl_haos_test_session']`.
- `modules/integration/tests/conftest.py::pytest_ignore_collect(collection_path, config)` — returns `True` for `test_ha_integration_sil.py` when `sys.platform == 'win32'` and `os.environ.get('BLHAOS_RUN_SIL') != '1'`.
- Playwright specs (`e2e/specs/*.spec.ts`) — `dashboard loads and lists demo speakers`, `diagnostics panel refreshes and shows demo scenario`, `recovery guidance renders via ingress header path`, `volume slider commits to bridge and reports persisted level`; each uses `test.step` boundaries matching `runtime-validation-report.md`.

Modified functions:

- `modules/integration/tests/conftest.py::FakeSession.post` — from unconditional `AssertionError` to recording + configurable response so `async_command` play/pause/stop/set_volume/play_media payloads can be asserted (closes the command-path gap recorded in `20-REVIEW.md`).
- `modules/bridge/backend/bl_haos/api/ws.py::ConnectionManager.broadcast` / both websocket endpoints — no signature change; add defensive socket cleanup in `finally` so disconnect paths never leave orphaned coroutines (keeps `test_ws.py` green under warnings-as-errors).

Removed functions: none.

## [Classes]

New classes:

- `ha_stubs/homeassistant/core.py::HomeAssistant` — attributes `data`, `states`, `config_entries`, `async_create_task`, `async_create_background_task`, `async_block_till_done`; mirrors only what `custom_components/bl_haos/client.py` touches.
- `ha_stubs/helpers/aiohttp_client.py::async_get_clientsession` — test-session provider described above.

Modified classes:

- `conftest.py::FakeSession` — new attributes `commands: list[tuple[str, dict]]`, `command_response: dict | Exception | None`; `post()` records `(url, kwargs['json'])` and returns `FakeResponse(command_response)` or raises when `command_response` is an exception.
- `ws.py::ConnectionManager` — document that callers must track tasks; no behavioral change to `connect`/`disconnect`.

Removed classes: none.

## [Dependencies]

- **Bridge Python (test-only)**: pin in new `backend/requirements-test.txt`: `pytest==9.0.3`, `pytest-asyncio==1.4.0`, `pytest-cov==7.1.0`, `PyYAML>=6.0.2`, `dbus-fast>=2.36`. CI (`builder.yaml` + new `tests.yml`) installs this file instead of ad-hoc pip lists — removes version drift between local and CI.
- **Integration SIL (CI-only)**: `pytest-homeassistant-custom-component==0.13.366`, `homeassistant==2026.9.3` pinned in `modules/integration/requirements-sil.txt`. Upgrade procedure (recorded in `TESTING.md`): bump pin → run L2 in CI → run L1 client unit tests → run L3 browser suite → only then merge.
- **Frontend (dev-only)**: `vitest@^3`, `jsdom@^25`, `@testing-library/react@^16`, `@playwright/test@^1.49` (pinned major). No production dependency changes.
- **Playwright browsers**: CI runs `npx playwright install --with-deps chromium`; local devs run once via `npm run test:e2e:install`.
- No runtime (add-on) dependency changes; `backend/requirements.txt` untouched.

## [Testing]

Layer mapping:

| Layer | Suite | Command | Environments | Gate |
|---|---|---|---|---|
| L0 static | `test_package_layout.py`, `test_addon_config.py`, `test_s6_structure.py`, `test_dockerfile.py`, `tsc`, `vite build` | `run-tests.ps1 -Layer L0` | any | exit 0 |
| L1 unit | all `modules/bridge/tests` (118) + `test_client_commands.py` + vitest unit | `run-tests.ps1 -Layer L1` | any (Windows OK) | exit 0, backend coverage ≥ 85% |
| L2 SIL | `test_ha_integration_sil.py` | `run-tests.sh L2` (Linux/WSL2 only; auto-skip on Windows with reason) | Linux CI / WSL2 | exit 0 |
| L3 E2E | `modules/bridge/web_ui/e2e` | `run-tests.ps1 -Layer L3` | any with Chromium | exit 0 |
| L4 VM | go-live runbook | manual | HAOS VM | evidence attached to release |

Existing test modifications:

- `modules/bridge/tests/test_ws.py`: +1 regression test for tracked broadcasts (L1).
- `modules/integration/tests/test_package_layout.py`: +1 test asserting the strategy artifacts exist.
- New `test_client_commands.py` covers (closes gaps from `20-REVIEW.md`): command payload shape (`{"version":1,"operation":...}`), `detail` extraction on non-200 surfaced into the raised `aiohttp.ClientError`, malformed non-dict JSON body on 200, listener cache update after successful command, and `_async_process_speaker` rejection of non-sink records (WR-03 regression).
- New Playwright specs encode the three previously ad-hoc flows plus the volume feature added in the latest change.

Validation strategy:

- Every layer independently runnable and idempotent; `run-tests.*` is the single documented entry point.
- CI (`tests.yml`) runs L1+L2+L3 on every push to `main` and every PR; `builder.yaml` keeps its release-gate call of L1 before image build.
- Coverage: `pytest --cov=backend --cov-report=term-missing` with `fail_under=85`; frontend coverage informational (no gate in first iteration).
- Warnings-as-errors: `filterwarnings = error::RuntimeWarning` targeted at un-awaited coroutines only (not blanket, to avoid third-party deprecation noise).

## [Implementation Order]

1. **Fix the pytest plumbing first** (no test-behavior change): update `modules/bridge/pytest.ini` (`asyncio_mode = auto`, coverage block, filterwarnings), rewrite root `pytest.ini` as aggregator, create `modules/integration/pytest.ini`, extend `modules/bridge/tests/conftest.py`. Verify plain `python -m pytest tests` (no env vars) works in `modules/bridge`.
2. **Silence the orphaned-coroutine warning at the source**: tracked broadcasts in `ws.py` + new `test_ws.py` regression; confirm `filterwarnings` passes.
3. **Bridge requirements pinning**: add `backend/requirements-test.txt`; update `builder.yaml` to use it.
4. **Integration L1 stubs**: create `ha_stubs/` + `tests/unit/test_client_commands.py`; extend `FakeSession.post`; add the platform guard. Verify L1 green on Windows.
5. **Integration CI pin file**: add `requirements-sil.txt`; document the pin in `TESTING.md`.
6. **Frontend unit tests**: vitest + testing-library, `vitest.config.ts`, 3–4 component/util tests; wire `npm run test`.
7. **Frontend E2E**: `e2e/playwright.config.ts` + 4 specs (promoting `.planning/runtime-validation` flows); `test:e2e` scripts; verify locally against demo-mode uvicorn.
8. **CI workflow**: create `.github/workflows/tests.yml` with `bridge-unit`, `integration-sil`, `frontend` jobs (L2 uses the pin file; sets `BLHAOS_RUN_SIL=1`).
9. **Local runner + docs**: add `scripts/run-tests.ps1` / `.sh`; write `TESTING.md` (layers, environment matrix, HA Core pin + upgrade procedure, WSL2 guidance, retired Docker-harness note). Add `test_package_layout.py` assertions.
10. **Full validation sweep**: run `run-tests.ps1 -Layer all` locally (L2 auto-skips on Windows with a printed reason), confirm CI green on a scratch branch, and mark `.planning/todos/pending/add-linux-ha-sil-ci.md` resolved once the `integration-sil` job passes.



