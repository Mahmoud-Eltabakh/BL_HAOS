---
phase: 10-native-player-control-state-sync
plan: 01
status: complete
requirements: [NMP-05]
files_modified:
  - Dockerfile
  - backend/bl_haos/api/routes.py
  - backend/bl_haos/ha/player.py
  - backend/bl_haos/main.py
  - backend/ha_integration/custom_components/bl_haos/client.py
  - backend/ha_integration/custom_components/bl_haos/media_player.py
  - tests/test_dockerfile.py
  - tests/test_media_player.py
  - tests/test_native_transport.py
---

# Phase 10 Plan 01: Native Playback Control Summary

Authenticated native media-player commands now reach an authoritative per-speaker playback supervisor and return confirmed add-on records.

## Completed Work

- Added the versioned credential-protected native command endpoint with trusted, connected A2DP speaker validation.
- Replaced the bridge stub with structured operations, persistent volume updates, safe URL validation, supervised FFmpeg-to-PipeWire playback, and bounded cleanup.
- Added native entity play, pause, stop, volume, and media-play feature declarations that delegate through the REST client without optimistic local state changes.
- Added one native speaker publication path for bridge state changes and Bluetooth updates.
- Installed FFmpeg in the add-on image and added focused command/runtime safety coverage.

## Verification

`PYTHONPATH=. pytest tests/test_native_transport.py tests/test_media_player.py tests/test_dockerfile.py -v` passed: 9 tests.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Replaced invalid asyncio child-stdout wiring with an explicit PCM pump**
- **Found during:** Task 3 verification review
- **Issue:** `asyncio` subprocess `StreamReader` cannot be passed as the stdin handle of `pw-play`.
- **Fix:** Added an owned asynchronous decoder-to-player PCM copy task while retaining argument-list process launches.
- **Files modified:** `backend/bl_haos/ha/player.py`

## Self-Check: PASSED

All planned implementation files exist and focused tests pass.