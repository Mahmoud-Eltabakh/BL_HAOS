---
phase: 09-native-integration-foundation
plan: 01
status: complete
requirements: [NMP-01, NMP-02]
files_modified:
  - config.yaml
  - rootfs/etc/s6-overlay/s6-rc.d/00-init-environment/up
  - backend/ha_integration/custom_components/bl_haos/manifest.json
  - backend/ha_integration/custom_components/bl_haos/const.py
  - backend/ha_integration/custom_components/bl_haos/config_flow.py
  - backend/ha_integration/custom_components/bl_haos/__init__.py
  - backend/ha_integration/custom_components/bl_haos/strings.json
  - tests/test_custom_integration.py
---

# Phase 09 Plan 01: Native Integration Foundation Summary

The add-on now installs only its bundled component using a staged, ownership-scoped replacement and retains a restrictive native bridge credential across restarts.

## Completed Work

- Declared the direct add-on HTTP port without changing unrelated add-on configuration.
- Installed the component below `custom_components/bl_haos` without deleting user-managed Home Assistant configuration or unrelated components.
- Generated a persistent, mode `0600` bridge credential and installed it as the component runtime setting.
- Replaced the MQTT config flow with one validated local HTTP endpoint and a fixed bridge unique ID.
- Stored entry-specific runtime data and removed the manifest's MQTT dependency.

## Verification

`pytest tests/test_custom_integration.py -v` passed: 3 tests.

## Deviations from Plan

None. The requested no-commit constraint leaves the implementation available for orchestrator review.

## Self-Check: PASSED

All planned files exist and focused validation passed.