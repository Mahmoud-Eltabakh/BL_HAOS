---
phase: 09-native-integration-foundation
plan: 02
status: complete
requirements: [NMP-03, NMP-04]
files_modified:
  - backend/bl_haos/api/routes.py
  - backend/bl_haos/api/ws.py
  - backend/bl_haos/main.py
  - backend/ha_integration/custom_components/bl_haos/client.py
  - backend/ha_integration/custom_components/bl_haos/__init__.py
  - backend/ha_integration/custom_components/bl_haos/media_player.py
  - tests/test_native_transport.py
  - tests/test_custom_integration.py
---

# Phase 09 Plan 02: Native Entity Transport Summary

Trusted Bluetooth audio sinks now appear through a credentialed REST snapshot and a separate WebSocket update channel, with entities driven entirely from the integration client cache.

## Completed Work

- Added native bridge identity and trusted-speaker snapshot endpoints protected by constant-time credential comparison.
- Added an isolated credentialed `/ws/native` channel and publishes trusted speaker changes as `speaker_updated` events.
- Added an async client that verifies bridge identity, caches the initial snapshot, validates speaker records, and reconnects its event stream.
- Replaced MQTT media player subscriptions with dynamic entities using normalized MAC-derived identities and Home Assistant device registry metadata.
- Kept entity properties memory-only and deferred playback controls to Phase 10.

## Verification

`pytest tests/test_native_transport.py tests/test_custom_integration.py tests/test_api.py tests/test_ws.py -v` passed: 11 tests.

## Deviations from Plan

None. The requested no-commit constraint leaves the implementation available for orchestrator review.

## Self-Check: PASSED

All planned files exist and the REST, WebSocket, and integration regression suites passed.