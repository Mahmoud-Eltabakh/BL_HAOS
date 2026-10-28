---
phase: 37-native-pairing-speaker-settings-ui
plan: 01
subsystem: bridge-api
tags: [fastapi, native-auth, bluetooth, settings, tests]
provides:
  - Authenticated native management endpoints for scan, discovery, pairing, connection, speaker management, adapters, and settings.
  - Whitelisted safe management errors and bounded settings/device projections.
  - Native editing of bridge-managed log_level, default_codec, and auto_reconnect_enabled.
key-decisions:
  - Legacy management routes remain unchanged; all new integration management calls use /native/*.
  - Native settings never serialize native_token; raw BlueZ/D-Bus exception details are not returned.
  - Global auto-reconnect setting gates reconnect-engine registration and scheduled attempts.
requirements-completed: [NUX-03]
status: verified-local-only
---

# Phase 37 Plan 01: Native Bridge Management Summary

Implemented native-authenticated endpoints for scanning, device listing, pairing, connect/disconnect/remove, adapter listing/power, speaker settings, and system settings. Auth is checked before management work. Errors use the safe allowlist; settings expose only approved fields. System updates accept only `log_level`, `default_codec`, and `auto_reconnect_enabled`. Legacy routes were left unchanged.

## Verification

- `py -3.12 -m pytest -q`: **369 passed, 1 skipped** (370 collected). This full bridge run includes native-management, legacy API, reconnect, and addon-config coverage. One existing Starlette/httpx deprecation warning was emitted.
- `git -C modules\bridge diff --check`: passed.

## Not run / limitations

- No live Home Assistant/BlueZ interaction, host access, deployment, restart, or audio playback was performed, as required.
- `default_codec` is stored and editable, but repository inspection found no global playback consumer for this field; changing it does not yet demonstrate an operational playback effect.
