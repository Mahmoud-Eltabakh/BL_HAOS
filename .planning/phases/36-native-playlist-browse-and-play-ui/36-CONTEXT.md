# Phase 36 Context — Native Playlist & Browse-and-Play UI

**Phase goal:** Users create playlists and browse-and-play from the integration without the add-on UI.
**Requirement:** NUX-02
**Planning scope:** Local implementation and verification only. No commit is part of this planning run.

## Decisions

### Locked decisions

- **D-01 — UI/service ownership boundary.** User-facing UI belongs in the Home Assistant integration: `modules/integration/panel_ui/src/media-panel.tsx` is the panel surface and `modules/integration/custom_components/bl_haos/playlist_library.py` owns its authenticated playlist WebSocket services. The add-on remains a separate service because it requires BlueZ, D-Bus, and audio access. Phase 36 must not move this feature back into the bridge.
- **D-02 — Native playlist and browsing behavior.** Playlist creation/editing and browse-and-play must be available in the integration's native HA UI. Existing saved playlists must remain readable and unchanged unless a user explicitly performs a supported mutation.
- **D-03 — Phase 35 is complete locally.** Shuffle/repeat gating and specific playback error reasons have already been implemented locally. Do not redo or broaden Phase 35 work as part of Phase 36.
- **D-04 — Scope fences.** Pairing/speaker/settings UI belongs to Phase 37; retiring the add-on ingress UI belongs to Phase 38. No deployment, publication, live action, or GHCR publishing is authorized or in scope for Phase 36.

## Agent's Discretion

- Follow the existing `MediaPanel` and HA WebSocket contracts; preserve opaque Home Assistant media-source IDs, record identity/revision semantics, and existing stored record shape.
- Make only changes needed to satisfy the Phase 36 acceptance criteria. Reuse existing authenticated HA media-source and playlist-library APIs rather than adding provider-specific clients, credentials, raw-URL playlist entries, or new dependencies.
- Use module-local Vitest and pytest/SIL checks. Regenerate the packaged panel bundle from reviewed source and use the isolated package-parity check.

## Out of Scope

- Pairing, speaker management, and settings UI (Phase 37).
- Add-on ingress UI retirement or migration (Phase 38).
- Deployment, publishing, live HA/provider/playback/hardware actions, and GHCR publication.
- Reworking Phase 35 shuffle/repeat gating or error-reason behavior.

## Existing Implementation References

- Native panel: `modules/integration/panel_ui/src/media-panel.tsx`
- Native panel behavior tests: `modules/integration/panel_ui/src/media-panel.test.tsx` and `modules/integration/panel_ui/src/playlist-library.test.tsx`
- HA-owned library/WebSocket service: `modules/integration/custom_components/bl_haos/playlist_library.py`
- Library SIL coverage: `modules/integration/tests/test_playlist_library_sil.py`
- Packaged panel and parity test: `modules/integration/custom_components/bl_haos/panel_static/bl-haos-media-panel.js` and `modules/integration/tests/test_package_layout.py`
- Bridge web UI is a parity reference only; Phase 36 does not modify it.
