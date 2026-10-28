---
phase: 37-native-pairing-speaker-settings-ui
plan: 02
subsystem: home-assistant-integration
tags: [home-assistant, services, options-flow, websocket, panel, tests]
provides:
  - Native client methods, admin-only services and WebSocket commands for speaker and system settings.
  - Per-speaker options flow and a Speakers view in the integration panel.
  - Unit, SIL, and panel interaction coverage.
key-decisions:
  - HA operations use the integration client and authenticated native routes only.
  - Unsafe response details become fixed safe errors; Supervisor credentials are not used.
requirements-completed: [NUX-03]
status: verified-local-only
---

# Phase 37 Plan 02: Home Assistant Speaker Management Summary

Implemented integration client calls and admin-gated HA services/WebSocket commands for scan, pair, connect/disconnect, remove, rename, adapter power, speaker settings, and the three bridge-managed system settings. Added per-speaker options flow and mounted Speakers panel controls. The integration does not call legacy unauthenticated management routes.

## Verification

- Integration unit tests: **92 passed**.
- WSL SIL tests (`test_speaker_management_sil.py` and `test_ha_integration_sil.py`) using the discovered Phase 36 cached venv `/home/mse/.venvs/bl-haos-sil-2026.10.3`: **97 passed**.
- Panel Vitest: **76 passed**.
- The panel build completed successfully.
- No Supervisor token handling was introduced; unsafe bridge error details are mapped to safe integration errors.

## Not run / limitations

- No live HA instance or HA host was contacted; no pairing against physical hardware or audio playback was attempted.
- `default_codec` persistence/editability is verified, but global playback use is not present in the inspected code and remains an operational limitation.
