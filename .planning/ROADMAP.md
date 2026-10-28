# Roadmap: BL-HAOS

## Overview

BL-HAOS is a Home Assistant OS Bluetooth audio platform combining BlueZ, PipeWire, Snapcast, a native Home Assistant media-player integration; speaker controls are moving fully into Home Assistant. The current milestone moves the project from feature completeness to production trustworthiness.

The reference bar is the operational maturity demonstrated by Sendspin Bluetooth Bridge: explicit lifecycle contracts, isolated failure domains, deterministic diagnostics, guided recovery, reproducible test modes, and release governance. BL-HAOS adopts those engineering lessons while retaining native Home Assistant control as its product boundary.

The current milestone is v1.1 Production Readiness & Release. The preceding v1.0 Playlist Playback & Management milestone ended at Phase 27 with a `gaps_found` audit; it is not complete. Its local/mock implementation history remains below, and no local/mock result is treated as production acceptance.

## Real-Time Device Discovery milestone

- [x] **Phase 23: Real-Time Device Discovery UI & API**

## Production milestone

- [x] **Phase 16: Automated Orchestration & Reporting**
- [x] **Phase 17: Production Runtime Stabilization**
- [x] **Phase 18: Security & Safe Execution Hardening**
- [x] **Phase 19: Diagnostics, Supportability & Observability**
- [ ] **Phase 20: Release Quality Gates & Go-Live**

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

- [x] 18-01-PLAN.md: Safe input validation and command guard rails
- [x] 18-02-PLAN.md: Secret handling, auth hardening, dependency pinning, and CVE gates

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

- [x] 19-01-PLAN.md: Unified diagnostics, telemetry, lifecycle events, and support bundle
- [x] 19-02-PLAN.md: Operator recovery guidance and deterministic demo/test mode

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

- [x] 20-01: Release gate checklist, regression matrix, compatibility policy, and CI enforcement
- [x] 20-02: Final HAOS validation, upgrade/rollback rehearsal, and go-live readout

## Historical context

Phases 1-15 remain the feature-delivery backbone: add-on foundation, audio stack, Bluetooth management, reconnect, API, UI, HA integration, multi-room, live verification, VM testing, and SIL coverage. Phase 16 closes the existing test-orchestration gap before Phases 17-20 harden the platform for production.

### Phase 21: HAOS VM Validation and Release Evidence

**Goal:** [To be planned]
**Requirements**: TBD
**Depends on:** Phase 20
**Plans:** 0 plans

Plans:

- [ ] TBD (run $gsd-plan-phase 21 to break down)

### Phase 22: Make Home Assistant integration tests runnable on Windows

**Goal:** [To be planned]
**Requirements**: TBD
**Depends on:** Phase 21
**Plans:** 0 plans

- [ ] TBD (run $gsd-plan-phase 22 to break down)

### Phase 23: Real-Time Device Discovery UI & API

**Goal:** Show newly found Bluetooth devices in real time during a scan.
**Requirements**: UX-01, UX-02
**Depends on:** Phase 19
**Plans:** 0 plans

**UI direction:** Convert the ingress dashboard and discovery flow to restrained Neumorphism. Use a cohesive base surface with paired light/dark shadows, raised cards, inset fields and sliders, and pressed states for actions. Keep semantic status colors (connected, warning, error, diagnostics) as accents rather than replacing them with decorative gradients. Preserve focus-visible outlines, keyboard operation, readable contrast, reduced-motion behavior, and responsive card geometry. The detailed design contract is in [23-CONTEXT.md](phases/23-real-time-device-discovery-ui-api/23-CONTEXT.md).

Plans:

- [ ] TBD (run $gsd-plan-phase 23 to break down)

---
*Historical roadmap snapshot updated: 2026-09-23 after Phase 19; Phase 20 was current at that time.*

## Phase 20 — Release quality gates and go-live: HOLD

**Plans:** complete. **Milestone:** hold (not complete).

Go-live blockers: missing full Playwright regression; missing pip-audit/Trivy evidence; incomplete registry/architecture publishing; missing HAOS image and authenticated Home Assistant validation; and no approved hardware. See the Phase 20 summaries, GO-LIVE-READOUT.md, RELEASE-RUNBOOK.md, and release evidence for the validation record and exit criteria.

## Playlist Playback & Management milestone (v1.0)

**Goal:** Let users browse and play Home Assistant provider playlists, create and manage BL-HAOS playlists of Home Assistant media references, and play them sequentially through Bluetooth speakers.
**Depends on:** Phase 23; prior release hold and open Phase 21-22 work remain recorded above.
**Requirements:** PL-01 through PL-11

### Phase 24: HA Media Catalog & Provider Playback

**Goal:** Expose supported Home Assistant media sources and provider playlists through native media players and a secure ingress catalog path.
**Depends on:** Phase 23
**Requirements:** PL-01, PL-02, PL-03
**Plans:** 6/6 plans complete
**Status:** Complete for user-approved local mock progression (2026-10-24). Mock-HA Playwright scenarios and responsive captures passed. This does not verify real-provider authentication, actual session expiry, physical playback, or HA-shell accessibility. PL-01/02/03 remain production-pending; T-24-15 remains OPEN/HIGH and blocks release. Live acceptance is deferred to post-milestone verification.
**Success Criteria:**

1. A connected BL-HAOS media-player entity exposes supported audio media and provider playlists through Home Assistant Browse Media.
2. Selecting a supported provider item or playlist resolves through Home Assistant and begins playback on the selected speaker, with resolution failures reported.
3. The ingress UI can browse the supported HA catalog and launch provider playlists through a secure HA-owned interface; HA credentials are not copied into add-on storage, browser persistence, or logs.
4. Integration and ingress tests cover catalog browsing, provider resolution, unavailable items, and denied/expired access.

Plans:
- [x] 24-01-PLAN.md: SIL Core 2026.10.3 pins and single-restart public-host probe
- [x] 24-02-PLAN.md: Custom media panel shell and Home Assistant registration
- [x] 24-03-PLAN.md: Panel catalog browsing and media resolution
- [x] 24-04-PLAN.md: Target speaker selection and single-attempt playback
- [x] 24-05-PLAN.md: Ingress navigation entry and session boundary hardening
- [x] 24-06-PLAN.md: Headless mock-HA Playwright browser acceptance, responsive captures, and quality gates

### Phase 25: Saved Playlist Library

**Goal:** Let users create and maintain persistent BL-HAOS playlists from Home Assistant media references and save provider playlist references.
**Depends on:** Phase 24
**Requirements:** PL-04, PL-05, PL-06, PL-11
**Status:** Complete for user-approved local/mock progression (2026-10-27; 69/69 verifier score). Production/live HA acceptance remains pending and release-blocking.
**Success Criteria:**

1. Users can create, rename, reorder, edit, and delete custom playlists of ordered Home Assistant media references in the existing authenticated HA panel.
2. Users can save an existing provider playlist reference as a BL-HAOS library shortcut; launching it is owned by Phase 26.
3. Playlist definitions survive Home Assistant and add-on restarts; stale media references are identified rather than shown as playable.
4. Persisted records contain media references and required display/order metadata, never resolved playback URLs or provider credentials.

**Plans:** 7 plans

Plans:
- [x] 25-01-PLAN.md — HA-owned custom-playlist create/list tracer and persistence
- [x] 25-02-PLAN.md — Bounded schema and pure migration tests, concurrency, and fail-closed storage
- [x] 25-03-PLAN.md — Custom playlist editor, ordering, and confirmation flows
- [x] 25-04-PLAN.md — Validated, idempotent provider playlist shortcut persistence
- [x] 25-05-PLAN.md — Provider shortcut save, rename, and local removal UI
- [x] 25-06-PLAN.md — Explicit browse-based availability checks
- [x] 25-07-PLAN.md — Mock-only end-to-end, responsive, and keyboard acceptance

### Phase 26: Sequential Playback & Queue Controls

**Goal:** Play saved playlists in order with automatic advancement, full queue controls, and truthful failure/cancellation state.
**Depends on:** Phase 25
**Requirements:** PL-07, PL-08, PL-09, PL-10
**Status:** Complete for user-approved local/mock progression (5/5 plans; 10/10 scoped truths verified). PL-07 through PL-10 remain production-pending; T-24-15/T-24-16, release, and deployment remain blocked. The generated `panel_static` bundle is unchanged and requires a separately authorized packaging step before HA serves the updated panel source.
**Success Criteria:**

1. Starting a playlist on a selected speaker plays items in order and advances only after successful natural completion of the current item.
2. Users can view the active playlist/item and use next, previous, shuffle, repeat, play, pause, and stop controls in the ingress UI and supported native Home Assistant controls.
3. Stop, replacement playback, or speaker loss cancels queued work; stale process-completion events cannot start another playlist item.
4. Resolution and playback failures are visible, and the queue does not silently skip an item that failed.

**Plans:** 5 plans

Plans:
- [x] 26-01-PLAN.md — Bridge queue session and process lifecycle tracer
- [x] 26-02-PLAN.md — Bounded native/ingress transport, shared snapshot, and capability contract
- [x] 26-03-PLAN.md — HA resolve-all playlist launch and capability-gated native entity
- [x] 26-04-PLAN.md — Authenticated Library launch and ingress queue controls
- [x] 26-05-PLAN.md — Local mock acceptance, API coverage, and user-facing documentation

### Phase 27: Bluetooth Reconnect Reliability

**Goal:** Prevent reconnect storms by removing nested connection retries, sharing connection ownership across automatic and operator requests, and preserving conservative backoff through failure and recovery.
**Requirements**: PROD-04, PROD-05
**Depends on:** Phase 23
**Success Criteria:**

1. One scheduled reconnect performs one bounded connection attempt; busy or failed BlueZ calls cannot trigger immediate nested retries or destructive stale-link recovery.
2. Manual and automatic connection requests share adapter ownership, including cleanup after cancellation and failure; pairing is preserved.
3. Repeated failures use longer exponential backoff and a meaningful circuit-breaker cooldown; recovery, presence events, and busy responses cannot erase accumulated backoff.
4. Deterministic module-local tests verify call counts, concurrent requests, cancellation, backoff, and breaker behavior, with existing Bluetooth and API regressions passing.
5. Release notes and operator documentation describe the change, with real-host soak validation explicitly pending until deployment is authorized.

**Execution scope:** Dedicated autonomous run, phase 27 only. Playlist phases 24-26 remain paused. No live deployment, Bluetooth reset, pairing deletion, branch creation, or commits are authorized by this run.
**Plans:** 1/1 plans complete
**Status:** Locally complete 2026-10-24. Independent review clean; 280 passed, one existing platform skip. HAOS deployment and hardware soak deferred.

Plans:
- [x] 27-01-PLAN.md: Bounded shared connection ownership, conservative scheduler pacing, regression tests and version 0.2.68 guidance.

## v1.0 Requirement Traceability

**Milestone audit:** `gaps_found` in [v1.0-MILESTONE-AUDIT.md](v1.0-MILESTONE-AUDIT.md). Local phase plans are complete, but PL-07 is not available in the unchanged packaged `panel_static` bundle, production requirements remain pending, T-24-15/T-24-16 remain open, and Phase 27 hardware soak is deferred. Do not complete/archive or claim release readiness until separately authorized gates pass.

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

**Coverage:** 11 of 11 v1 requirements mapped; 0 unmapped.

## v1.1 Production Readiness & Release (Current)

**Goal:** Make the audited v1.0 media, playlist, queue, and reconnect capabilities safely shippable through verified packaging, reproducible non-publishing CI, security closure, and explicitly authorized production acceptance.
**Depends on:** Phase 27; the v1.0 milestone remains `gaps_found` and incomplete.
**Requirements:** PRD-01 through PRD-08
**Status:** In progress. Phase 28 is complete for local package/SIL scope; Phase 29 is active with one plan. No production acceptance or release-ready claim is made.

This roadmap is planning only. It does **not** authorize deployment, package or image publication, release-artifact publication, host changes, Home Assistant Core restarts, physical playback, provider or session manipulation, or hardware tests. Local planning and non-publishing checks do not grant any of those permissions. Any live acceptance requires separate explicit authorization and a recorded phase checkpoint defining the approved host, actions, limits, and rollback/stop conditions. Without that authorization, the live phase remains blocked and must not be reported complete.

No `.planning/MILESTONES.md` or completed milestone record exists in this workspace. The v1.0 history and incomplete status above are retained from the existing roadmap and [v1.0-MILESTONE-AUDIT.md](v1.0-MILESTONE-AUDIT.md); no completion record is inferred or fabricated.

## Phases

- [x] **Phase 28: Package Panel Bundle Parity** - Generate and verify the integration-served panel bundle against the reviewed queue UI source. (completed 2026-10-28)
- [x] **Phase 29: PR-Safe Root, Bridge & Integration CI** - Local declared-runtime gates passed; hosted Node 22 pull_request evidence remains deferred until a separate authorized PR check is available.
- [ ] **Phase 30: Security Gate & Finding Closure** - Blocked pending explicit security evidence review and release-threshold authorization.
- [ ] **Phase 31: Authorized HA & Provider Playback Acceptance** - Blocked pending explicit host, provider, and playback authorization.
- [ ] **Phase 32: HA-Shell Accessibility & Responsive Acceptance** - Blocked pending explicit shell-inspection authorization.
- [ ] **Phase 33: Authorized Reconnect Hardware Soak** - Blocked pending explicit support-hardware authorization and soak checkpoint.
- [ ] **Phase 34: Release Candidate Evidence & Go/No-Go Preparation** - Blocked pending completion of the earlier authorized evidence gates.

## Phase Details

### Phase 28: Package Panel Bundle Parity

**Goal**: Home Assistant serves the reviewed panel source as a generated bundle containing the saved-playlist launch and queue controls.
**Depends on**: Phase 27
**Requirements**: PRD-01
**Success Criteria** (what must be TRUE):
  1. The integration package serves a generated bundle produced from the reviewed panel source, not a stale hand-maintained artifact.
  2. Package-layout checks confirm the served bundle contains saved-playlist launch and queue-control behavior.
  3. A reproducible local build/check identifies source-to-bundle drift and fails when the packaged artifact is stale.

**Plans:** 1/1 plans complete

Plans:
- [x] 28-01-PLAN.md - Reviewed panel source to generated-bundle parity and HA serving verification

**UI hint**: yes

### Phase 29: PR-Safe Root, Bridge & Integration CI

**Goal**: Contributors can validate root, bridge, and integration changes through passing pull-request gates without publishing release artifacts.
**Depends on**: Phase 28
**Requirements**: PRD-02
**Success Criteria** (what must be TRUE):
  1. The root CI gate passes on its declared runtime and required checks.
  2. Bridge and integration CI gates pass on their declared runtimes and required checks.
  3. Pull-request validation can run without publishing add-on images, packages, or release artifacts.

**Plans:** 1/1 plans executed

Plans:
- [x] 29-01-PLAN.md - Root PR-safe gates, required panel parity, and declared-runtime verification

### Phase 30: Security Gate & Finding Closure

**Goal**: Release enforcement applies the production high threshold, and the audited security findings have reviewed closure evidence.
**Depends on**: Phase 29
**Requirements**: PRD-03
**Success Criteria** (what must be TRUE):
  1. The effective production security threshold is `high` in the release-enforced configuration.
  2. T-24-15 and T-24-16 are closed with reviewed evidence recorded against each finding.
  3. No local or CI override weakens the release security enforcement below `high`.

**Plans**: 0 (TBD)

Plans:
- [ ] TBD (run $gsd-plan-phase 30 to break down)

### Phase 31: Authorized HA & Provider Playback Acceptance

**Goal**: On an explicitly authorized HAOS test host, users can browse and play saved Home Assistant media safely, including when access or media is unavailable.
**Depends on**: Phase 30
**Requirements**: PRD-04, PRD-05
**Success Criteria** (what must be TRUE):
  1. Before live host, provider, session, or playback actions, a separate explicit authorization and scoped checkpoint records the approved host, test identities, actions, limits, and stop conditions; absent this, no live test is run or marked complete.
  2. On the authorized host, native media browsing, saved-playlist resolution, queue launch, and audible playback succeed on one explicitly selected connected speaker.
  3. Authorized denial, unavailable-reference, and expired-session cases fail safely without leaking credentials, provider data, or playable URLs.
  4. Those negative cases do not modify the shared Home Assistant session or use unapproved provider/session manipulation.

**Plans**: 0 (TBD)

Plans:
- [ ] TBD (run $gsd-plan-phase 31 to break down)

**UI hint**: yes

### Phase 32: HA-Shell Accessibility & Responsive Acceptance

**Goal**: The packaged panel is accessible and usable in the actual Home Assistant shell at the required viewport sizes.
**Depends on**: Phase 31
**Requirements**: PRD-06
**Success Criteria** (what must be TRUE):
  1. Before actual HA-shell acceptance, a separate explicit authorization and checkpoint identifies the host, allowed inspection, and evidence capture; absent this, live acceptance is not performed or marked complete.
  2. At 375, 768, and 1440 pixels, recorded actual-shell evidence shows responsive layout, readable contrast, and no blocking overflow.
  3. Keyboard operation, visible focus, labels, announcements, and reduced-motion behavior pass the agreed acceptance checks in the packaged panel.

**Plans**: 0 (TBD)

Plans:
- [ ] TBD (run $gsd-plan-phase 32 to break down)

**UI hint**: yes

### Phase 33: Authorized Reconnect Hardware Soak

**Goal**: Authorized HAOS hardware demonstrates bounded reconnect recovery, pairing retention, and stable playback across the supported matrix.
**Depends on**: Phase 32
**Requirements**: PRD-07
**Success Criteria** (what must be TRUE):
  1. Before deployment, link-loss simulation, or physical playback, separate explicit authorization and a checkpoint name the host, hardware, duration, actions, and rollback/stop conditions; absent this, no hardware test is run or marked complete.
  2. The approved soak records bounded retry pacing, recovery after link loss, and retained pairing without destructive recovery.
  3. Stable playback and reconnect results are recorded for each approved supported-hardware target, with failures and unavailable targets clearly distinguished.

**Plans**: 0 (TBD)

Plans:
- [ ] TBD (run $gsd-plan-phase 33 to break down)

### Phase 34: Release Candidate Evidence & Go/No-Go Preparation

**Goal**: A release decision can be made from synchronized candidate versions, complete reviewed evidence, passed gates, and a tested rollback plan.
**Depends on**: Phase 33
**Requirements**: PRD-08
**Success Criteria** (what must be TRUE):
  1. Candidate add-on and integration versions are synchronized and verified against the candidate being assessed.
  2. Required security, build, and test gates pass, and a reviewer accepts an evidence bundle linking each release claim to its result.
  3. A rollback plan is rehearsed and its recovery evidence is included with the candidate record.
  4. An explicit go/no-go decision is recorded only after the evidence review; this planning and decision record do not authorize deployment or package/release publication.

**Plans**: 0 (TBD)

Plans:
- [ ] TBD (run $gsd-plan-phase 34 to break down)

## v1.2 Native HA UX (Phases 35-39, planned; runs alongside open v1.1)

**Goal:** All user-facing UI lives in the Home Assistant integration, and the add-on becomes a headless Bluetooth/audio service. v1.1 stays open; its live evidence gates (Phases 30-34) are unchanged and no archiving was done.
**Requirements:** NUX-01 through NUX-06 (see REQUIREMENTS.md)
**Authorization:** Planning only. Deploys, restarts, playback and hardware tests need the same per-action authorization as v1.1.

- [ ] **Phase 35: Queue Control Fix & Real Error Reasons** - Shuffle/repeat work or are disabled when no queue exists; the bridge and integration surface the real failure reason instead of "Native playback command failed".
- [ ] **Phase 36: Native Playlist & Browse-and-Play UI** - Playlist creation/editing and browse-and-play live in the integration's native HA UI.
- [ ] **Phase 37: Native Pairing, Speaker & Settings UI** - Pairing, speaker management and settings move into the integration (config/options flow, services, panel).
- [ ] **Phase 38: Headless Add-on & Ingress UI Retirement** - The add-on exposes only the service API; its ingress web UI is removed with a documented migration.
- [ ] **Phase 39: v1.2 Verification & Release Gates** - Local/SIL parity checks, then authorized live acceptance and go/no-go, after Phase 34.

### Phase 35: Queue Control Fix & Real Error Reasons

**Goal**: Shuffle and repeat never fail opaquely.
**Depends on**: Phase 29
**Requirements**: NUX-01
**Success Criteria** (what must be TRUE):
  1. `media_player.shuffle_set` and `repeat_set` succeed on an active queue.
  2. With no queue (single `play_media`), the integration disables or hides shuffle/repeat, or applies them to the next queue, without raising an error.
  3. A failed queue command shows its safe, specific reason (for example "No active queue") in HA instead of the generic message.
  4. Bridge and integration tests cover the no-queue and active-queue paths.

**Plans**: 0 (TBD)

### Phase 36: Native Playlist & Browse-and-Play UI

**Goal**: Users create playlists and browse-and-play from the integration without the add-on UI.
**Depends on**: Phase 35
**Requirements**: NUX-02
**Success Criteria** (what must be TRUE):
  1. Playlist create, rename, edit and delete work in the integration's native UI.
  2. Browse-and-play uses HA media sources from the integration.
  3. Existing saved playlists remain readable and unchanged.

**Plans**: 0 (TBD)
**UI hint**: yes

### Phase 37: Native Pairing, Speaker & Settings UI

**Goal**: Pairing, speaker management and settings are available in the integration.
**Depends on**: Phase 36
**Requirements**: NUX-03
**Success Criteria** (what must be TRUE):
  1. A speaker can be scanned, paired, connected, removed and renamed from HA.
  2. Settings previously changed in the add-on UI are editable via options flow or services.
  3. Every action has a bridge API endpoint and a test.

**Plans**: 0 (TBD)
**UI hint**: yes

### Phase 38: Headless Add-on & Ingress UI Retirement

**Goal**: The add-on is a headless service with a stable API.
**Depends on**: Phase 37
**Requirements**: NUX-04, NUX-05
**Success Criteria** (what must be TRUE):
  1. The add-on ships without its ingress web UI and with no UI-only endpoints required by users.
  2. Add-on/integration version compatibility is checked and reported clearly in HA.
  3. Upgrade notes cover moving from the old UI to the integration.

**Plans**: 3 plans

Plans:
- [x] 38-01-PLAN.md — Retire ingress UI/static assets and UI-only routes; preserve native/operational contracts and local gates.
- [x] 38-02-PLAN.md — Add authenticated version metadata, shared compatibility checks, HA repairs/diagnostics and recovery tests.
- [x] 38-03-PLAN.md — Document staged migration, bump local candidates to bridge 0.2.71/integration 0.2.22, and verify docs/version parity.

### Phase 39: v1.2 Verification & Release Gates

**Goal**: v1.2 is verified locally, then accepted live under explicit authorization.
**Depends on**: Phase 34, Phase 38
**Requirements**: NUX-06
**Success Criteria** (what must be TRUE):
  1. Bridge, integration, SIL and frontend gates pass in CI.
  2. Authorized live acceptance covers the native UI, pairing, playback, shuffle and repeat.
  3. An explicit go/no-go is recorded after evidence review.

**Plans**: 0 (TBD)

## v1.2 Progress

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 35. Queue Control Fix & Real Error Reasons | 1/1 (inline) | Locally complete: bridge 359 passed; SIL assertion added, awaits CI; not deployed | 2026-10-28 |
| 36. Native Playlist & Browse-and-Play UI | 1/1 | Locally complete: vitest 74, WSL SIL 48, parity 12 passed; not deployed | 2026-10-28 |
| 37. Native Pairing, Speaker & Settings UI | 3/3 | Locally complete: bridge 369, integration unit 92, WSL SIL 97, vitest 76, parity 12 passed; not deployed; `default_codec` has no known playback consumer | 2026-10-28 |
| 38. Headless Add-on & Ingress UI Retirement | 3/3 | Locally complete: bridge 366 passed/1 skipped; integration unit/package/docs 120 passed; WSL SIL 179 passed; panel Vitest 76 passed/build/parity passed. Candidate only; not published/deployed; Phase 39 authority gates remain | 2026-10-28 |
| 39. v1.2 Verification & Release Gates | 0/TBD | Blocked behind Phase 34 and authorization | - |

## v1.1 Progress

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 28. Package Panel Bundle Parity | 1/1 | Complete (local scope) | 2026-10-28 |
| 29. PR-Safe Root, Bridge & Integration CI | 1/1 | Local execution passed; hosted Node 22 PR #1 checks all green | 2026-10-28 |
| 30. Security Gate & Finding Closure | 0/TBD | Blocked pending explicit security-evidence authorization | - |
| 31. Authorized HA & Provider Playback Acceptance | 0/TBD | Blocked pending explicit host and provider authorization | - |
| 32. HA-Shell Accessibility & Responsive Acceptance | 0/TBD | Blocked pending explicit shell-review authorization | - |
| 33. Authorized Reconnect Hardware Soak | 0/TBD | Blocked pending explicit hardware authorization | - |
| 34. Release Candidate Evidence & Go/No-Go Preparation | 0/TBD | Blocked pending completion of earlier authorized gates | - |

**v1.1 coverage:** PRD-01 through PRD-08 are each assigned to exactly one phase. PRD-01 is locally verified; PRD-02 has local evidence and a deferred hosted PR gate; PRD-03 through PRD-08 remain blocked behind explicit authorization and reviewer-approved evidence. Phase 28 and the local execution of Phase 29 are complete for their scoped evidence, while Phases 30-34 remain intentionally blocked rather than reported as complete.

---
*Roadmap updated: 2026-10-28 after Phase 29 local CI gates; hosted PR evidence remains deferred and v1.0 remains `gaps_found`.*
