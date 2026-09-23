# Roadmap: BL-HAOS

## Overview

BL-HAOS is a Home Assistant OS Bluetooth audio platform combining BlueZ, PipeWire, Snapcast, a native Home Assistant media-player integration, and an Ingress UI. The current milestone moves the project from feature completeness to production trustworthiness.

The reference bar is the operational maturity demonstrated by Sendspin Bluetooth Bridge: explicit lifecycle contracts, isolated failure domains, deterministic diagnostics, guided recovery, reproducible test modes, and release governance. BL-HAOS adopts those engineering lessons while retaining native Home Assistant control as its product boundary.

## Production milestone

- [x] **Phase 16: Automated Orchestration & Reporting**
- [x] **Phase 17: Production Runtime Stabilization**
- [x] **Phase 18: Security & Safe Execution Hardening**
- [x] **Phase 19: Diagnostics, Supportability & Observability**
- [>] **Phase 20: Release Quality Gates & Go-Live**

## Phase details

### Phase 16: Automated Orchestration & Reporting
**Goal**: Make the existing validation pipeline reproducible and truthful before runtime hardening begins.
**Depends on**: Phases 14 and 15
**Requirements**: SIL-03, REL-01
**Success Criteria**:
  1. The test runner executes bridge and integration suites in a predictable sequence.
  2. Reports distinguish pass, fail, skipped, unavailable-environment, and not-run states.
  3. Docker image build and test-runner execution are validated, not only configured.
  4. The smoke matrix is checked into the repository and can run locally and in CI.
**Plans**:
- [x] 16-01: Add orchestration to the full test runner and reporting output
- [x] 16-02: Validate the smoke matrix, CI gate expectations, and static contract coverage

### Phase 17: Production Runtime Stabilization
**Goal**: Make runtime behavior deterministic under startup failures, reconnect churn, stale BlueZ objects, and missing audio dependencies.
**Depends on**: Phase 16
**Requirements**: PROD-01, PROD-02, PROD-03, PROD-04, PROD-05, PROD-06
**Success Criteria**:
  1. Startup publishes explicit progress and terminal lifecycle events, including failure and degraded completion.
  2. A canonical health model covers the add-on, BlueZ, PipeWire, Snapcast, HA bridge, adapters, and speakers.
  3. Each speaker has a deterministic state machine with observable transition reasons.
  4. Reconnect attempts have ownership/lease protection so one speaker cannot accumulate duplicate workers.
  5. Stale-device recovery is bounded, classified, and non-destructive by default.
  6. Runtime contracts are versioned at API, event, and any subprocess boundary.
**Plans**:
- [x] 17-01: Lifecycle, health-state, event, and runtime-contract model
- [x] 17-02: Reconnect concurrency, stale-state recovery, and degraded-mode tests

### Phase 18: Security & Safe Execution Hardening
**Goal**: Force user-controlled inputs and privileged actions through strict validation and safe default handling.
**Depends on**: Phase 17
**Requirements**: SAFE-01, SAFE-02, SAFE-03, SAFE-04, SAFE-05
**Success Criteria**:
  1. Device addresses, adapter names, URLs, media types, and command payloads are validated before execution.
  2. Playback URL policy rejects unsafe schemes, malformed values, and disallowed destinations.
  3. Secrets are redacted from logs, diagnostics, support bundles, and error responses.
  4. Auth and privilege boundaries remain strict under restart, failure, and malformed-input scenarios.
  5. Dependencies are pinned and scanned for known vulnerabilities in CI.
**Plans**:
 - [ ] 18-01-PLAN.md: Safe input validation and command guard rails
 - [ ] 18-02-PLAN.md: Secret handling, auth hardening, dependency pinning, and CVE gates

### Phase 19: Diagnostics, Supportability & Observability
**Goal**: Make runtime failure modes visible and diagnosable without SSH guesswork.
**Depends on**: Phase 18
**Requirements**: OBS-01, OBS-02, OBS-03, OPS-01, OPS-02, OPS-03
**Success Criteria**:
  1. Canonical diagnostics and telemetry endpoints expose bounded component, adapter, speaker, sink, startup, and contract status.
  2. Structured events and logs include correlation context, failure classification, transition reason, and recovery outcome.
  3. Operators receive guided next actions for common pairing, sink, reconnect, and integration failures.
  4. A redacted support bundle can be exported without tokens, credentials, or uncontrolled log volume.
  5. A deterministic demo mode exercises the UI and diagnostics without Bluetooth or HA hardware.
**Plans**:
**Plans:** 2 plans
Plans:
- [ ] 19-01-PLAN.md: Unified diagnostics, telemetry, lifecycle events, and support bundle
- [ ] 19-02-PLAN.md: Operator recovery guidance and deterministic demo/test mode

### Phase 20: Release Quality Gates & Go-Live
**Goal**: Create a release gate that proves the project is safe to ship and support.
**Depends on**: Phase 19
**Requirements**: REL-02, REL-03, REL-04, OPS-03
**Success Criteria**:
  1. Startup, connect, disconnect, reconnect, playback failure, upgrade, and rollback smoke checks pass reliably.
  2. Critical state transitions, auth cases, degraded modes, and redaction behavior are enforced in CI.
  3. Builds are reproducible across supported architectures and dependency drift is visible.
  4. Stable/preview support policy, security disclosure process, compatibility matrix, and go-live checklist are documented.
  5. Release evidence is attached to each candidate and a failed gate blocks publication.
**Plans**:
- [ ] 20-01: Release gate checklist, regression matrix, compatibility policy, and CI enforcement
- [ ] 20-02: Final HAOS validation, upgrade/rollback rehearsal, and go-live readout

## Historical context

Phases 1-15 remain the feature-delivery backbone: add-on foundation, audio stack, Bluetooth management, reconnect, API, UI, HA integration, multi-room, live verification, VM testing, and SIL coverage. Phase 16 closes the existing test-orchestration gap before Phases 17-20 harden the platform for production.

---
*Roadmap updated: 2026-09-23 after completing Phase 19; Phase 20 is current