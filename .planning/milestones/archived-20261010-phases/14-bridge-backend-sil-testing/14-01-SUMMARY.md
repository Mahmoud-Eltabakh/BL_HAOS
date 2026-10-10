---
phase: 14-bridge-backend-sil-testing
plan: 01
subsystem: bridge-testing
status: complete
tags: [pytest, fastapi, websocket, bluetooth, sil, authentication]
dependency_graph:
  requires: [Phase 13 isolated test harness]
  provides: [SIL-01 bridge REST/WebSocket coverage, CR-01 auth regression coverage]
  affects: [Phase 16 test orchestration]
tech_stack:
  added: []
  patterns: [TestClient lifespan portal injection, deterministic BlueZ-shaped events, bearer-auth contract assertions]
key_files:
  created: [modules/bridge/tests/test_bridge_sil.py]
  modified: [modules/bridge/tests/test_native_transport.py]
decisions:
  - Keep SIL tests in-process and inject events through BluetoothManager callbacks rather than requiring D-Bus or Bluetooth hardware.
  - Route callback injection through TestClient.portal so broadcaster tasks execute on the lifespan event loop.
  - Update stale native transport regression calls to use the configured bearer token now that protected routes enforce CR-01.
metrics:
  duration: 00:20
  completed: 2026-09-23
commits: 0
plan_head_before: not recorded (user requested no commits)
actuals:
  tokens: 3300
  tasks: 3
  commits: 0
---

# Phase 14 Plan 01: Bridge Backend SIL Testing Summary

Deterministic in-process bridge SIL coverage now exercises REST contracts, BlueZ-shaped discovery and property events through the live FastAPI lifespan, and native REST/WebSocket bearer authentication.

## Delivered

- Added `test_bridge_sil.py` with six independent tests covering:
  - device discovery event serialization over `/ws`;
  - health, adapters, devices, and scan start/stop REST contracts;
  - connected-client `device_updated` propagation and connection cleanup;
  - native identity, snapshot, and command rejection for missing/malformed/wrong credentials;
  - valid authenticated native command execution against a connected trusted sink;
  - native WebSocket close code `1008` for unauthorized clients and valid authenticated connection cleanup.
- Updated three stale native transport regression calls to pass the configured token to protected routes.
- No production files, packages, credentials, D-Bus sockets, HAOS VM, PipeWire, or network services were required.

## Verification

- `pytest tests/test_bridge_sil.py -q -k websocket_device_discovery`: 1 passed.
- `pytest tests/test_bridge_sil.py -q -k "rest or websocket"`: 5 passed, 1 deselected.
- `pytest tests/test_bridge_sil.py -q -k "native or auth or cr01"`: 3 passed, 3 deselected.
- `pytest tests/test_bridge_sil.py -q`: 6 passed.
- `pytest tests/test_native_transport.py -q`: 4 passed.
- `pytest tests/ -q`: 61 passed.
- Static diagnostics for both changed test files: no errors.

## Deviations from Plan

### Auto-fixed Issues

**1. Rule 3 - Blocking regression test maintenance**
- **Found during:** Full bridge regression validation.
- **Issue:** Three existing native transport tests called protected native routes without authorization and failed with HTTP 401.
- **Fix:** Added the configured in-process bearer header to those test requests; production authentication behavior was unchanged.
- **Files modified:** `modules/bridge/tests/test_native_transport.py`

No other deviations. No credentials were asserted in response bodies or logs.

## Known Stubs

None.

## Self-Check: PASSED

- Summary file exists.
- Focused SIL and full bridge validations pass.
- No commits or pushes were made, per user request.
