---
phase: 24-ha-media-catalog-provider-playback
plan: "01"
subsystem: integration
status: complete
completed: "2026-10-24"
requirements-completed: []
provides:
  - Exact Core 2026.10.3 Linux SIL compatibility and public panel/static API checks
  - User-accepted disposable live-host registration and authenticated-call evidence
  - Verified removal of the temporary integration, panel, entity and module files
key-files:
  modified:
    - modules/integration/requirements-sil.txt
    - modules/integration/tests/test_panel_registration.py
    - TESTING.md
  created:
    - .planning/phases/24-ha-media-catalog-provider-playback/host-probe/test_probe.py
affects: [24-02, 24-06]
commits: 0
human_checkpoint: accepted
production_contract: pending-24-02-01
---

# Phase 24 Plan 01: Accepted Public Host Contract

## Scope and Decisions

The user approved rebaselining Core from 2026.9.4 to 2026.10.3, separately approved a disposable live integration probe with at most one Core restart, and then explicitly accepted the resulting host evidence on 2026-10-24. Plan 24-01 is complete. The production panel identity/lifecycle decision in Task 24-02-01 remains pending.

## Linux Evidence

- Exact SIL pins: Home Assistant 2026.10.3, pytest-homeassistant-custom-component 0.13.374, aiohttp 3.14.5 and pytest 9.0.3. Public registry metadata, resolver and pip check were verified. Older test environments were preserved.
- The version regression first rejected the old 2026.9.4 environment as intended: one failed assertion and two deselections.
- In the separate Core 2026.10.3 Ubuntu WSL environment, the focused panel/static and existing integration SIL suites passed 24 tests in 4.06s with zero skips.
- The disposable probe's local real-Core test passed in 1.15s, covering config flow, public panel registration, silent dispatch, duplicate rejection and unload. Its mocked static registration was verified on the real host rather than claimed as local HTTP evidence.

## Accepted Live Observations

| Contract | Observed result |
|----------|-----------------|
| Exact target version | Core 2026.10.3 reported through SSH and injected hass |
| Static serving | Disposable module returned HTTP 200 through public async_register_static_paths |
| Public panel and module loading | Registered panel map entry and actual custom element loaded |
| Authenticated injected browse | hass.callWS media_source/browse_media succeeded; diagnostic output omitted provider payload and URLs |
| Targeted service dispatch | hass.callService media_player.play_media reached only the silent probe entity, recording exactly one call with media type music |
| Denied access | Credentials-omitted REST returned 401; independent invalid WebSocket session returned auth_invalid; current session stayed connected |

The probe used disposable identifiers, not the final production URL, element or package. The silent entity never resolved media, played sound or targeted the real speaker. Actual session expiration was not forced; denied/invalid-session rejection was the accepted authorization branch. Final physical audio/provider acceptance remains in Plan 24-06.

## Authorized Live Changes and Cleanup

Uploaded only the five disposable integration files into a previously absent directory. No configuration YAML or existing integration source was edited. Core initially rejected the undiscovered handler; configuration validation passed and exactly one authorized restart was used.

After observations, the config entry was removed through the public API. Authoritative server checks confirmed no remaining probe entries/entities and the panel was absent. Uploaded files, including generated caches, were removed; the module URL returned HTTP 404 with cache bypassed. The current user session stayed connected, and the shared browser was returned to BL-HAOS.

A browser wait timed out during unload navigation and logged a transient removed-panel error; server checks subsequently established cleanup. No blind second delete or restart was performed. The unloaded static route object stays in memory until a normal future restart, but the removed module is not served.

## Handoff

- Detailed command history, measurements and limitations are retained in 24-VALIDATION.md.
- No production panel source/build, Bluetooth fix deployment, pairing deletion, radio reset, extra restart, commit or branch was performed.
- Plan 24-02 may advance only after its separate production contract decision is accepted. Phase 24 and playlist requirements are not complete.