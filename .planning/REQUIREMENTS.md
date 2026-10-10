# Requirements: BL-HAOS Playlist Playback & Management

**Defined:** 2026-10-10
**Milestone:** v1.0 Playlist Playback & Management
**Core Value:** Effortless, reliable Home Assistant media playback to Bluetooth speakers.

## v1 Requirements

### Home Assistant Media Browsing

- [ ] **PL-01**: Each BL-HAOS media-player entity exposes supported Home Assistant audio sources and provider playlists through the native Browse Media experience.
- [ ] **PL-02**: A supported Home Assistant media item or provider playlist selected for a connected speaker resolves through Home Assistant and starts playback on that speaker.
- [ ] **PL-03**: The ingress UI can browse the Home Assistant media catalog and launch provider playlists through an authenticated HA-owned interface without exposing HA credentials to add-on storage or logs.

### Saved Playlists

- [ ] **PL-04**: Users can create, rename, reorder, edit, and delete custom ingress playlists containing ordered Home Assistant media references.
- [ ] **PL-05**: Users can save existing Home Assistant provider playlist references in the BL-HAOS playlist library.
- [ ] **PL-06**: Saved playlist definitions persist across Home Assistant and add-on restarts; unavailable or stale media references are identified to the user.

### Playback and Queue Controls

- [ ] **PL-07**: Starting a saved playlist on a selected speaker plays its items in order and advances only after the current item completes successfully.
- [ ] **PL-08**: Users can view the active playlist and item, and control playback with next, previous, shuffle, repeat, play, pause, and stop in the ingress UI and supported native Home Assistant controls.
- [ ] **PL-09**: Stop, replacement playback, or speaker loss cancels queued work so late process-completion events cannot advance a stale playlist.
- [ ] **PL-10**: Media resolution or playback failures expose an explicit state and do not silently skip the failed item.

### Data Safety

- [ ] **PL-11**: Saved playlists store Home Assistant media references and required display/order metadata, not resolved playback URLs or provider credentials.

## Future Requirements

- **PL-12**: Resume an in-progress playlist and queue position after Home Assistant or add-on restart.
- **PL-13**: Synchronize one playlist queue across multiple Bluetooth speakers.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Direct provider-specific API clients or credentials | Home Assistant media sources remain the catalog and authentication boundary. |
| Importing arbitrary raw URLs as custom playlist entries | This milestone stores HA media references so provider resolution and access remain HA-owned. |
| Synchronized multi-speaker queues | The approved v1.0 workflow targets playback on a selected speaker; synchronized queue semantics need separate design. |
| Restoring the active queue after restart | Playlist definitions persist, but in-progress playback recovery is deferred. |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| PL-01 | Phase 24 | Pending |
| PL-02 | Phase 24 | Pending |
| PL-03 | Phase 24 | Pending |
| PL-04 | Phase 25 | Pending |
| PL-05 | Phase 25 | Pending |
| PL-06 | Phase 25 | Pending |
| PL-07 | Phase 26 | Pending |
| PL-08 | Phase 26 | Pending |
| PL-09 | Phase 26 | Pending |
| PL-10 | Phase 26 | Pending |
| PL-11 | Phase 25 | Pending |

**Coverage:**
- v1 requirements: 11 total
- Mapped to phases: 11
- Unmapped: 0

---
*Requirements defined: 2026-10-10*
*Last updated: 2026-10-10 after starting milestone v1.0*
