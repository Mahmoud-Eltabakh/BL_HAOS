# Requirements: BL-HAOS Production Readiness & Release

**Defined:** 2026-10-28
**Milestone:** v1.1 Production Readiness & Release (closing audited v1.0 gaps)
**Core Value:** Effortless, reliable Home Assistant media playback to Bluetooth speakers.

## v1.0 Feature Requirements

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

## Scoped Bluetooth Reliability Follow-Up

- [x] **PROD-04**: One bounded connection attempt shares adapter ownership across automatic and operator requests, releasing ownership on failure, timeout and cancellation. Locally verified in phase 27; hardware soak pending.
- [x] **PROD-05**: Reconnect recovery preserves pairing and conservative failure pacing without nested retries or automatic link resets. Locally verified in phase 27; hardware soak pending.

These scoped reliability requirements do not mark any playlist requirement complete.

## Deferred Playlist Requirements

- **PL-12**: Resume an in-progress playlist and queue position after Home Assistant or add-on restart.
- **PL-13**: Synchronize one playlist queue across multiple Bluetooth speakers.

## v1.1 Requirements: Production Readiness & Release

Requirements for closing the audited v1.0 packaging, CI, security, host-acceptance, and hardware gaps. Live host/provider, publication, restart, and physical-playback actions require separate explicit authorization; planning these gates does not authorize executing them.

### Packaging and CI

- [x] **PRD-01**: The Home Assistant integration package serves a generated panel bundle built from the reviewed panel source, and package-layout checks verify the queue launch and control UI is present.
- [ ] **PRD-02**: Root, bridge, and integration CI gates pass on their declared runtimes; pull-request validation can run without publishing add-on images or release artifacts.

### Security and Production Acceptance

- [ ] **PRD-03**: The production security threshold is `high`, T-24-15 and T-24-16 are closed with reviewed evidence, and no local override weakens release enforcement.
- [ ] **PRD-04**: On an explicitly authorized HAOS test host, native media browsing, saved playlist resolution, queue launch, and audible playback work on one explicitly selected connected speaker.
- [ ] **PRD-05**: Authorized denial, unavailable-reference, and expired-session cases fail safely without credential, provider, or playable-URL leakage or modification of the shared HA session.
- [ ] **PRD-06**: The packaged panel passes actual HA-shell keyboard, focus, labeling, announcements, contrast, reduced-motion, and responsive acceptance at 375, 768, and 1440 pixels.

### Hardware and Release

- [ ] **PRD-07**: An authorized HAOS reconnect soak verifies bounded retries, pairing retention, recovery after link loss, and stable playback on the supported hardware matrix.
- [ ] **PRD-08**: A release candidate has synchronized versions, passed security/build/test gates, a reviewed evidence bundle, and a tested rollback plan before an explicit go/no-go decision.

## v1.2 Requirements: Native HA UX

- [ ] **NUX-01**: Shuffle and repeat succeed on an active queue and are disabled or harmless when no queue exists; failed queue commands show a safe, specific reason.
- [ ] **NUX-02**: Playlist creation/editing and browse-and-play are available in the integration's native HA UI.
- [ ] **NUX-03**: Pairing, speaker management and settings are available in the integration (config/options flow, services, panel).
- [x] **NUX-04**: The add-on runs as a headless service and its ingress web UI is retired with documented migration notes (locally verified; candidate not published/deployed).
- [x] **NUX-05**: Add-on/integration version compatibility is checked and reported clearly in HA (locally verified; candidate not published/deployed).
- [x] **NUX-07**: The BL-HAOS media/speaker UI is available as a Lovelace dashboard card with Add card discovery; the separate sidebar panel is retired with migration notes. Integration0.2.24 is deployed and the card was placed on the explicitly authorized new Audio dashboard; existing dashboards were preserved. Broader live acceptance remains open.
- [ ] **NUX-06**: v1.2 passes CI and authorized live acceptance, with an explicit go/no-go after evidence review.
- [x] **NUX-08**: All dashboard card views use clean HA-native, light/dark theme-aware styling with consistent hierarchy, responsive card-width layouts and preserved actions, labels, focus, errors and44px interaction targets.

Decision: add-on and integration stay separate packages (the add-on needs privileged BlueZ/D-Bus/audio access that Core cannot provide); only the UI moves.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Direct provider-specific API clients or credentials | Home Assistant media sources remain the catalog and authentication boundary. |
| Importing arbitrary raw URLs as custom playlist entries | This milestone stores HA media references so provider resolution and access remain HA-owned. |
| Synchronized multi-speaker queues | The approved v1.0 workflow targets playback on a selected speaker; synchronized queue semantics need separate design. |
| Restoring the active queue after restart | Playlist definitions persist, but in-progress playback recovery is deferred. |

## Traceability

### v1.0 (unchanged)

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
| PROD-04 | Phase 27 | Locally verified; hardware soak pending |
| PROD-05 | Phase 27 | Locally verified; hardware soak pending |

### v1.1 Production Readiness & Release

| Requirement | Phase | Status |
|-------------|-------|--------|
| PRD-01 | Phase 28 | Locally verified; package parity and SIL passed |
| PRD-02 | Phase 29 | Pending |
| PRD-03 | Phase 30 | Pending |
| PRD-04 | Phase 31 | Pending |
| PRD-05 | Phase 31 | Pending |
| PRD-06 | Phase 32 | Pending |
| PRD-07 | Phase 33 | Pending |
| PRD-08 | Phase 34 | Pending |

### v1.2 Native HA UX

| Requirement | Phase | Status |
|-------------|-------|--------|
| NUX-01 | Phase 35 | Pending |
| NUX-02 | Phase 36 | Pending |
| NUX-03 | Phase 37 | Pending |
| NUX-04 | Phase 38 | Locally verified; candidate not published/deployed |
| NUX-05 | Phase 38 | Locally verified; candidate not published/deployed |
| NUX-07 | Phase 38.1 | Deployed0.2.24; real Add card picker and authorized Audio dashboard verified at375/768/1440; broader acceptance pending |
| NUX-08 | Phase 38.2 | Locally verified through unit, mock-browser, theme/container matrix and package parity; no live acceptance claimed |
| NUX-06 | Phase 39 | Pending |

**Coverage:**
- v1.0 requirements: 11 total
- v1.0 mapped to phases: 11
- v1.1 production-readiness requirements: 8 total
- v1.1 mapped to phases: 8
- v1.1 mappings: PRD-01 -> Phase 28; PRD-02 -> Phase 29; PRD-03 -> Phase 30; PRD-04 and PRD-05 -> Phase 31; PRD-06 -> Phase 32; PRD-07 -> Phase 33; PRD-08 -> Phase 34
- Unmapped or multiply mapped v1.1 requirements: 0

---
*v1.0 requirements defined: 2026-10-10*
*v1.1 requirements defined: 2026-10-28*
*Last updated: 2026-10-29 after Phase 38.2 local/mock UI verification*
