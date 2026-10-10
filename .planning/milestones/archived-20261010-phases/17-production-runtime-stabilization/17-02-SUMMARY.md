---
phase: 17-production-runtime-stabilization
plan: 02
subsystem: runtime
tags: [python, asyncio, bluetooth, bluez, dbus, health, pytest]

requires:
  - phase: 17-production-runtime-stabilization
    provides: canonical health states, failure classifications, and versioned runtime observations from 17-01
provides:
  - single-owner reconnect workers with terminal cleanup
  - bounded stale BlueZ refresh and explicit D-Bus transport recovery observations
  - deterministic successful recovery, exhaustion, and health transition regression coverage
affects: [phase-18-security, phase-19-observability, reconnect-runtime, bluetooth-manager]

actuals:
  tokens: 7600
  tasks: 3
  commits: 0

tech-stack:
  added: []
  patterns: [identity-checked asyncio task ownership cleanup, bounded D-Bus recovery, classified health observations]

key-files:
  created: []
  modified:
    - modules/bridge/backend/bl_haos/bluetooth/reconnect.py
    - modules/bridge/backend/bl_haos/bluetooth/manager.py
    - modules/bridge/backend/bl_haos/health.py
    - modules/bridge/tests/test_auto_reconnect.py
    - modules/bridge/tests/test_bluetooth_manager.py
    - modules/bridge/tests/test_health.py

key-decisions:
  - "Reconnect ownership is released by an identity-checked task done callback so an old worker cannot remove a newer owner."
  - "D-Bus transport loss invalidates manager readiness and publishes DBUS_DISCONNECTED or DBUS_UNAVAILABLE instead of retaining healthy state."
  - "Successful stale recovery resets retry counters and clears obsolete speaker failure metadata; exhaustion continues to preserve its classified failure."

patterns-established:
  - "Normalize speaker addresses before profile, worker, and health ownership decisions."
  - "Bound stale-object refresh to one replacement lookup per connect attempt."

requirements-completed: [PROD-01, PROD-02, PROD-03, PROD-04, PROD-05, PROD-06]

coverage:
  - id: D1
    description: "Reconnect workers have one normalized-address owner and clean ownership after completion or cancellation."
    requirement: PROD-06
    verification:
      - kind: unit
        ref: "modules/bridge/tests/test_health.py and tests/test_auto_reconnect.py; pytest focused reconnect slice"
        status: pass
    human_judgment: false
  - id: D2
    description: "Stale BlueZ objects and D-Bus transport loss are bounded and explicitly classified."
    requirement: PROD-04
    verification:
      - kind: unit
        ref: "modules/bridge/tests/test_bluetooth_manager.py; pytest manager/reconnect slice"
        status: pass
    human_judgment: false
  - id: D3
    description: "Full bridge regression matrix preserves health, lifecycle, API, WebSocket, and degraded dependency contracts."
    requirement: PROD-01
    verification:
      - kind: unit
        ref: "python -m pytest tests/ -q from modules/bridge; 70 passed"
        status: pass
    human_judgment: false

# No task commits were made per user instruction; the parent workflow owns commit/push.
commits: 0
plan_head_before: not-recorded

duration: under 1 hour
completed: 2026-09-23
status: complete
---

# Phase 17 Plan 02: Deterministic reconnect and BlueZ recovery summary

**Reconnect ownership, stale BlueZ recovery, D-Bus loss classification, and deterministic health transitions are now covered by focused and full bridge tests.**

## Performance

- **Duration:** under 1 hour
- **Started:** 2026-09-23
- **Completed:** 2026-09-23
- **Tasks:** 3
- **Files modified:** 6 planned runtime/test files, including the existing health contract file

## Accomplishments

- Added identity-checked `_inflight` cleanup for reconnect success, exception, cancellation, unregister, and shutdown paths.
- Added explicit stale-object classification, one-shot refresh behavior, D-Bus transport invalidation, bounded reinitialization, and duplicate-safe signal subscription.
- Ensured successful stale recovery publishes `connected` and resets retry state, while exhaustion publishes `unavailable` with `reconnect_exhausted`.
- Added RED/GREEN coverage for ownership, stale refresh, D-Bus loss, recovery ordering, health redaction, API/WebSocket compatibility, and degraded-mode isolation.

## TDD Evidence

### RED

- Task 1 initially failed because completed workers remained in `_inflight`.
- Task 2 initially failed because `BluetoothManager` lacked an injectable health registry and D-Bus loss seam.
- Task 3 initially failed because successful stale recovery ended in `BACKOFF` instead of `CONNECTED`.

### GREEN

- Focused reconnect/health slice: `10 passed`.
- Focused manager/reconnect slice: `10 passed`.
- Focused Task 3 regression slice: `17 passed`.
- Full bridge suite from `modules/bridge`: `70 passed, 4 warnings`.
- `git diff --check`: passed.

### REFACTOR

- Kept the public manager and reconnect APIs compatible, removed redundant test assertions/imports, and retained existing asyncio/dbus-fast dependencies.

## Task Commits

No commits were made, per user instruction. The parent workflow owns staging, commit, and push.

## Files Created/Modified

- `modules/bridge/backend/bl_haos/bluetooth/reconnect.py` - terminal worker ownership cleanup and successful stale recovery state handling.
- `modules/bridge/backend/bl_haos/bluetooth/manager.py` - health injection, D-Bus loss/recovery seam, and bounded stale refresh classification.
- `modules/bridge/backend/bl_haos/health.py` - clear obsolete speaker failure metadata after a successful connection.
- `modules/bridge/tests/test_auto_reconnect.py` - ownership and stale recovery transition coverage.
- `modules/bridge/tests/test_bluetooth_manager.py` - stale refresh and D-Bus loss coverage.
- `modules/bridge/tests/test_health.py` - worker cleanup and exhaustion contract coverage.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Critical runtime contract] Extended the existing health registry to clear obsolete speaker failures after successful recovery.**
- **Found during:** Task 3
- **Issue:** A successful stale recovery could publish `connected` while retaining the old stale-object failure, producing contradictory health output.
- **Fix:** Connected observations now clear prior speaker failure metadata when no new failure is supplied; unavailable/exhausted observations still preserve or replace failure classification.
- **Files modified:** `modules/bridge/backend/bl_haos/health.py`
- **Verification:** Focused and full bridge suites passed.

**Total deviations:** 1 auto-fixed (Rule 2).
**Impact on plan:** Required for truthful deterministic health transitions; no new dependency or public API change.

## Issues Encountered

- The repository and bridge submodule contained unrelated dirty and untracked user changes. They were preserved.
- The full suite reports one existing Starlette deprecation warning and three existing unawaited `ConnectionManager.broadcast` warnings in API tests. None point to this plan's modified reconnect or manager code.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Phase 17-02 is ready for parent review and commit/push. The runtime now has bounded reconnect ownership and explicit BlueZ/D-Bus failure observations for Phase 18 security work.

---
*Phase: 17-production-runtime-stabilization*
*Completed: 2026-09-23*

## Self-Check: PASSED

- Summary file and all six plan files exist.
- Focused reconnect/health tests: 11 passed.
- Full bridge suite: 70 passed, 4 warnings.
- `git diff --check`: passed.
