# Requirements

**Project:** BL-HAOS (Bluetooth Audio Adapter for Home Assistant OS)
**Defined:** 2026-09-23
**Milestone:** Production-Level Readiness

## Production Readiness Requirements

### Runtime Reliability & Health (PROD)

- [x] **PROD-01**: Define a canonical runtime health state for the add-on, the Bluetooth manager, PipeWire, Snapcast, and each tracked speaker.
- [x] **PROD-02**: Detect and report degraded and unavailable states when BlueZ, PipeWire, or the sink path is missing or unhealthy.
- [x] **PROD-03**: Ensure each Bluetooth speaker has a deterministic state transition model from `unknown` through `connected`, `disconnected`, `reconnecting`, and `unavailable`.
- [x] **PROD-04**: Recover gracefully from stale BlueZ devices, stale cached objects, and transient D-Bus disconnect events without leaving the app in a silent broken state.
- [x] **PROD-05**: Publish explicit startup and shutdown lifecycle progress, failure, and completion events with bounded status details.
- [x] **PROD-06**: Version runtime event/API contracts and prevent duplicate reconnect workers for the same speaker.

### Security & Safe Execution (SAFE)

- [ ] **SAFE-01**: Validate all incoming device addresses, command payloads, and media URLs before any privileged BlueZ or subprocess action executes.
- [ ] **SAFE-02**: Reject malformed or unsafe playback commands with explicit, user-visible validation errors.
- [ ] **SAFE-03**: Ensure native auth and config tokens are never logged or exposed in support output.
- [ ] **SAFE-04**: Enforce strict privileges and safe default behavior for runtime configuration, speaker control, and system integration points.
- [ ] **SAFE-05**: Pin and scan runtime dependencies, with documented handling for supported stable and preview releases.

### Observability & Supportability (OBS)

- [ ] **OBS-01**: Expose a bounded but useful diagnostics surface covering adapter state, speaker state, sink availability, and last known failure reasons.
- [ ] **OBS-02**: Emit structured logs with speaker address, adapter context, and failure classification for reconnect and playback issues.
- [ ] **OBS-03**: Provide an operational summary for support staff to diagnose a broken speaker, stale state, or restart loop without live SSH access.

### Operator Support & Deterministic Validation (OPS)

- [ ] **OPS-01**: Provide bounded, redacted support-bundle export containing diagnostics, lifecycle status, recent classified failures, and contract versions.
- [ ] **OPS-02**: Provide guided recovery actions for common pairing, sink, reconnect, and native-integration failures.
- [ ] **OPS-03**: Provide a deterministic demo/test mode that exercises UI and diagnostics without Bluetooth hardware or a live Home Assistant host.

### Release Quality & Regression Gates (REL)

- [ ] **REL-01**: Define release smoke checks for startup, connect, disconnect, reconnect, and playback failure paths.
- [ ] **REL-02**: Add CI gates covering the most critical Bluetooth and HA state transitions.
- [ ] **REL-03**: Verify each release with a reproducible regression matrix covering at least reconnect, auth, and degraded-mode scenarios.
- [ ] **REL-04**: Define reproducible multi-architecture build, upgrade, rollback, compatibility, and release-evidence gates.

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| SIL-03 | Phase 16 | Complete (16-01, 16-02) |
| PROD-01 | Phase 17 | Complete (17-01, 17-02) |
| PROD-02 | Phase 17 | Complete (17-01, 17-02) |
| PROD-03 | Phase 17 | Complete (17-01, 17-02) |
| PROD-04 | Phase 17 | Complete (17-01, 17-02) |
| PROD-05 | Phase 17 | Complete (17-01, 17-02) |
| PROD-06 | Phase 17 | Complete (17-01, 17-02) |
| SAFE-01 | Phase 18 | Planned |
| SAFE-02 | Phase 18 | Planned |
| SAFE-03 | Phase 18 | Planned |
| SAFE-04 | Phase 18 | Planned |
| SAFE-05 | Phase 18 | Planned |
| OBS-01 | Phase 19 | Planned |
| OBS-02 | Phase 19 | Planned |
| OBS-03 | Phase 19 | Planned |
| OPS-01 | Phase 19 | Planned |
| OPS-02 | Phase 19 | Planned |
| OPS-03 | Phase 19 | Planned |
| REL-01 | Phase 20 | Planned |
| REL-02 | Phase 20 | Planned |
| REL-03 | Phase 20 | Planned |
| REL-04 | Phase 20 | Planned |

## Out of Scope

- **Microphone / HFP Voice Satellite Input**: Deferred beyond the current A2DP audio playback product scope.
- **Custom Hardware / Driver Forks**: BL-HAOS targets standard supported Home Assistant OS hosts and off-the-shelf Bluetooth adapters.

---
*Requirements updated: 2026-09-23 using Sendspin Bluetooth Bridge production lessons*
