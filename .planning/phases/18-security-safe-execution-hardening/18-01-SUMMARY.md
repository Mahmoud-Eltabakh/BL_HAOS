---
phase: 18-security-safe-execution-hardening
plan: 01
subsystem: bridge-security
status: complete
tags: [validation, bluetooth, media, subprocess, auth, tdd]
dependency_graph:
  requires: [phase-17-runtime-stabilization]
  provides: [strict-input-validation, safe-media-process-boundary, redacted-validation-errors]
  affects: [native-api, bluetooth-manager, media-player, multiroom-manager]
tech_stack:
  added: []
  patterns: [typed-allowlists, canonical-mac-normalization, argv-only-subprocesses, generic-validation-errors]
key_files:
  created: []
  modified:
    - modules/bridge/backend/bl_haos/api/routes.py
    - modules/bridge/backend/bl_haos/bluetooth/manager.py
    - modules/bridge/backend/bl_haos/health.py
    - modules/bridge/backend/bl_haos/ha/player.py
    - modules/bridge/backend/bl_haos/main.py
    - modules/bridge/backend/bl_haos/multiroom/manager.py
    - modules/bridge/tests/test_api.py
    - modules/bridge/tests/test_bluetooth_manager.py
    - modules/bridge/tests/test_media_player.py
    - modules/bridge/tests/test_multiroom_manager.py
    - modules/bridge/tests/test_native_transport.py
decisions:
  - Centralize strict MAC, adapter, URL, media-type, PIN, identifier, and sink validation in the existing health utility module.
  - Reject malformed request payloads with a stable generic 422 response so untrusted values are never reflected.
  - Keep persisted legacy invalid speaker identifiers from preventing startup, while rejecting them at every active operation boundary.
metrics:
  duration: ongoing-session
  completed: 2026-09-23
  tasks: 3
  commits: 0
plan_head_before: not-applicable
commits: 0
actuals:
  tokens: 9000
  tasks: 3
  commits: 0
---
# Phase 18 Plan 01: Strict validation and safe execution summary
Strict, test-backed Bluetooth/media validation with redacted API errors and argv-only process boundaries.

## Delivered

- Canonical MAC validation accepts colon and hyphen six-octet unicast addresses and rejects malformed, broadcast, multicast, overlong, and control-character values.
- Adapter, PIN, media type, URL, alias, identifier, PipeWire sink, Snapcast endpoint, latency, group, and client inputs are bounded and allowlisted before privileged work or state mutation.
- Native command validation runs before speaker lookup, bridge execution, sink resolution, reconnect, or URL persistence.
- Native authentication uses constant-time token comparison.
- FastAPI validation responses no longer echo rejected URLs, credentials, or other raw payload values.
- Playback stores the last URL only after process startup succeeds; ffmpeg, pw-play, pw-dump, and wpctl remain fixed argv-only subprocess calls.
- Legacy malformed persisted speaker keys are ignored during startup instead of crashing the service, while new operations remain strict.

## TDD Execution

### Task 1 RED/GREEN
- RED: Added unsafe native media rejection and valid URL argv tests; the unsafe request initially reached a 404 before validation.
- GREEN: Added shared media URL validation, pre-lookup request validation, redacted validation handling, and post-start URL persistence.
- Focused result: `16 passed`.

### Task 2 RED/GREEN
- RED: Added MAC, adapter, and inconsistent payload tests.
- GREEN: Added canonical validators to API models and Bluetooth manager entry points; updated auth contract to require constant-time comparison.
- Focused result: `21 passed`.

### Task 3 RED/GREEN
- RED: Added unsafe sink, exact argv/no-shell, and multi-room mutation-boundary tests.
- GREEN: Added sink validation before playback, keepalive, and volume process creation, plus multi-room endpoint and field bounds.
- Focused result: `20 passed`.

## Verification

- `python -m pytest tests/test_api.py tests/test_media_player.py -q`: 16 passed.
- `python -m pytest tests/test_api.py tests/test_bluetooth_manager.py tests/test_native_transport.py -q`: 21 passed.
- `python -m pytest tests/test_media_player.py tests/test_multiroom_manager.py tests/test_bridge_sil.py -q`: 20 passed.
- `python -m pytest tests/ -q`: 80 passed, 4 warnings.
- `git diff --check`: passed for the bridge changes.
- Pylance/VS Code diagnostics: no errors in touched implementation files.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Critical startup compatibility] Ignored invalid legacy persisted speaker identifiers during startup.**
- **Found during:** Task 1 focused verification.
- **Issue:** Existing persisted test/runtime configuration contained a multicast MAC and strict normalization prevented FastAPI lifespan startup.
- **Fix:** Player initialization and reconnect registration now skip malformed persisted keys with bounded warnings; active API and manager operations still reject them.
- **Files modified:** `modules/bridge/backend/bl_haos/ha/player.py`, `modules/bridge/backend/bl_haos/main.py`.

**2. [Rule 2 - Security redaction] Replaced FastAPI default validation detail output.**
- **Found during:** Task 1 focused verification.
- **Issue:** Pydantic's default 422 response reflected the rejected media URL.
- **Fix:** Added a generic application validation handler returning `Invalid request payload`.
- **Files modified:** `modules/bridge/backend/bl_haos/main.py`.

**3. [Rule 2 - Authentication hardening] Updated the native transport contract test.**
- **Found during:** Task 2 verification.
- **Issue:** An existing assertion required the route not to use constant-time credential comparison.
- **Fix:** Changed the assertion to require `hmac.compare_digest`.
- **Files modified:** `modules/bridge/tests/test_native_transport.py`.

No commits were created, per the explicit user instruction. The bridge submodule already contained unrelated dirty changes; those were preserved.

## Known Stubs

None introduced by this plan.

## Blockers

None.

## Self-Check: PASSED

- Summary file exists at `.planning/phases/18-security-safe-execution-hardening/18-01-SUMMARY.md`.
- All three plan verification commands and the full `tests/` suite passed.
- No task or metadata commits were created, as requested by the parent workflow.
