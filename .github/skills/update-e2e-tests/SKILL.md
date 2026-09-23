---
name: update-e2e-tests
description: Update the BL-HAOS end-to-end simulation test suite (Docker Compose + live-bridge scenarios) whenever a new feature, API endpoint, demo scenario, or HA entity is implemented. Use this when a PR/change adds or modifies backend routes (modules/bridge/backend/bl_haos/api), the demo runtime (modules/bridge/backend/bl_haos/demo.py), or the Home Assistant integration (modules/integration/custom_components/bl_haos).
---

# Update E2E Tests

## When to use this skill

Use this whenever a change touches any of:
- `modules/bridge/backend/bl_haos/api/routes.py` or `ws.py` (new/changed endpoint, new operation, new validation rule)
- `modules/bridge/backend/bl_haos/demo.py` (new demo scenario, new demo device/behavior)
- `modules/bridge/backend/bl_haos/recovery.py` (new recovery action or guidance entry)
- `modules/integration/custom_components/bl_haos/*` (new entity, new service, new config flow step)

The goal is to keep `tests/integration/tests/test_e2e_live_bridge.py` (real-network,
live-container coverage) and its orchestrators in sync with the actual feature set,
so `tests/integration/scripts/run-e2e-tests.sh` always simulates "everything the
product does" -- not a stale snapshot of it.

## Files involved

| File | Role |
|---|---|
| `tests/integration/docker-compose.e2e.yml` | Brings up a real bridge container (demo mode) + a runner container |
| `tests/integration/scripts/run-e2e-tests.sh` | Orchestrator: loops every demo scenario, (re)starts the bridge, runs the suite, aggregates pass/fail |
| `tests/integration/scripts/run-e2e-scenario.sh` | Runs inside the runner container for exactly one scenario |
| `tests/integration/tests/test_e2e_live_bridge.py` | The actual scenario assertions (real HTTP + real in-process Home Assistant) |
| `modules/bridge/tests/test_bridge_sil.py`, `modules/integration/tests/test_ha_integration_sil.py` | Mocked/white-box SIL suites -- keep these in sync too, they cover paths the demo runtime can't (pairing, scanning, adapter power) |

## Procedure

1. **Identify what changed.**
   - New REST/WS endpoint or operation? -> needs a black-box `httpx` call in `test_e2e_live_bridge.py`.
   - New demo scenario in `DEMO_SCENARIOS` (`demo.py`)? -> add it to `ALL_SCENARIOS` in `run-e2e-tests.sh`, and if it changes expected entity/command behavior, branch on `SCENARIO` in the test file (see existing `if SCENARIO == "healthy":` examples).
   - New recovery action or guidance key? -> add a `test_recovery_*` assertion (valid action succeeds, invalid target/action is rejected).
   - New HA entity/service (media_player attribute, new platform)? -> extend `test_connect_integration_creates_media_player_entity` or add a new `async def test_*(hass):` using the real `hass` fixture and a `MockConfigEntry` pointed at `BRIDGE_URL`/`TOKEN` -- do **not** patch `async_get_clientsession`; that mock is only for the SIL suite. Real E2E tests must exercise the real aiohttp session.
   - New failure mode / edge case (bad payload, unauthorized, unavailable device)? -> add one `test_edge_case_*` per case: assert the exact HTTP status code the route contract promises (422 validation, 401 auth, 404/409 unavailable).

2. **Check demo runtime support.** `modules/bridge/backend/bl_haos/demo.py`'s `DemoRuntime` only implements a fixed single speaker and a few manager methods (`get_adapters`, `get_devices`, `connect_device`, `ensure_device`, `recover_dbus`, `execute`, ...). If your new feature needs a demo-runtime method that doesn't exist yet (e.g. pairing, scanning, adapter power), either:
   - Extend `DemoRuntime` with a safe, deterministic implementation, or
   - Explicitly document in the test file's module docstring that this feature stays covered only by the mocked SIL suite, and do not add a failing E2E assertion for it.

3. **Run it locally before committing:**
   ```bash
   # one scenario, fast iteration
   ./tests/integration/scripts/run-e2e-tests.sh healthy

   # full matrix (all demo scenarios)
   ./tests/integration/scripts/run-e2e-tests.sh
   ```
   Reports land in `tests/integration/reports/e2e-<scenario>-junit.xml`.

4. **Keep assertions structural, not literal.** Match on status codes, key presence, and boolean conditions (e.g. `payload["contract_version"] == 1`, `"guidance" in payload`) rather than exact prose strings, so copy/wording changes in `recovery.py` guidance text don't cause unrelated test churn.

5. **Never assert on secrets.** Any new endpoint that returns diagnostics/support-bundle data must be checked against `test_support_bundle_never_leaks_secrets`-style assertions (`TOKEN not in body`).

6. **Update both suites when behavior is shared.** If a change affects request/response shape used by both the mocked SIL suite and the live E2E suite, update both in the same change so they can't silently diverge.

## Gotcha: `pytest-homeassistant-custom-component` blocks real networking by default

- Every test in this file needs the `socket_enabled` fixture (applied module-wide via `pytestmark`) to make real socket connections at all.
- Home Assistant's test plugin *also* patches `socket.getaddrinfo` to reject any hostname that isn't `localhost`/`127.0.0.1`/a literal IP address ("DNS resolution disabled in tests") -- and `socket_enabled` does **not** undo that specific patch. This means `BRIDGE_URL` must always be a literal IP address, never a Docker Compose service name like `http://bridge:8099`. `run-e2e-tests.sh` resolves the bridge container's real IP via `docker inspect` for this reason -- keep that resolution step if you change the compose topology.
- If you add a new **autouse** fixture that performs real network I/O in its own setup body (like `wait_for_bridge`), it must be **function-scoped** and explicitly take `socket_enabled` as a parameter (`def my_fixture(socket_enabled): ...`), not just rely on `pytestmark`. A module- or session-scoped autouse fixture will run before the function-scoped `socket_enabled` fixture and get blocked.

## Non-goals

This skill does not cover:
- Real Bluetooth/PipeWire hardware testing (out of scope for Docker; remains manual on real hardware, see `test_live_pi.py` / `test_full_pi_workflow.py` at the repo root).
- Full Home Assistant OS boot testing via the QEMU-based `tests/integration/docker-compose.yml` (that stack is separate and unrelated to this demo-mode E2E simulation).
