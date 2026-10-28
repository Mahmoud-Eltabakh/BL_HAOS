---
gsd_state_version: "1.0"
milestone: v1.0
current_phase: 27
current_phase_name: Bluetooth Reconnect Reliability
status: blocked
last_updated: "2026-10-28"
last_activity: 2026-10-28
last_activity_desc: v1.0 milestone audit found production and packaged-panel gaps; all local plans complete, no staging or commits
progress:
  total_phases: 4
  completed_phases: 4
  total_plans: 19
  completed_plans: 19
  percent: 100
milestone_name: Playlist Playback & Management
---

# Project State

## Project Reference

See: [PROJECT.md](PROJECT.md) (updated 2026-10-24)

**Core value:** Effortless pairing, high-fidelity audio streaming, and seamless Home Assistant `media_player` playback to any Bluetooth speaker with rock-solid background auto-reconnection, safe degraded-mode behavior, and production-grade operational visibility.
**Current focus:** v1.0 audit is gaps_found; local plans are complete, but packaged Phase 26 panel delivery, production acceptance, security, and hardware gates block milestone completion.

## Current Position

Phase: 27 (Bluetooth Reconnect Reliability) — local implementation complete
Plan: 1 of 1
Status: All local phase plans complete; v1.0 milestone audit gaps_found; production/release blockers remain (no staging or commits in this run)
Last activity: 2026-10-28 — Milestone audit records missing packaged queue UI and pending live/security/hardware acceptance

## Performance Metrics

**Velocity:**
- Total plans completed: 7 in the current milestone (six phase-24 plans plus phase 27)
- Average duration: pending
- Total execution time: pending

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 24. HA Media Catalog & Provider Playback | 6/6 | Complete (Mock E2E passed; live host deferred) | Complete (local/mock) |
| 25. Saved Playlist Library | 7/7 | Locally/mock verified; production acceptance deferred | Complete (local/mock) |
| 26. Sequential Playback & Queue Controls | 5/5 | 10/10 local/mock truths verified; panel bundle packaging and production acceptance deferred | Complete (local/mock) |
| 27. Bluetooth Reconnect Reliability | 1/1 | Locally complete; shared docs fingerprint requires refresh | Hardware soak pending |

## Accumulated Context

### Roadmap Evolution

- 2026-10-24: Phase 27 added: Bluetooth Reconnect Reliability. Run only phase 27 for the requested retry/locking/backoff fix; leave playlist phases 24-26 paused. The user delegated routine decisions while unavailable. No deployment, radio reset, pairing deletion, or commits in this run.

### Decisions

Decisions are logged in [PROJECT.md](PROJECT.md) Key Decisions table.
Recent decisions affecting current work:
- Prioritize real-time feedback over wait-and-batch discovery responses.
- Saved BL-HAOS playlists reference Home Assistant media items; the bridge owns sequential process playback.
- Phase 24: User explicitly approved Core 2026.10.3 instead of 2026.9.4. Exact isolated SIL pins: pytest-homeassistant-custom-component 0.13.374, Core 2026.10.3, aiohttp 3.14.5 (Core-required resolver correction), pytest 9.0.3 (preserved). This does not approve the public-host gate or authorize panel source/build work.
- Phase 24 host probe: User explicitly approved temporary integration installation and at most one Core restart. Configuration check passed; exactly one restart was used. The silent probe targeted only its own test entity, preserved the active user session, and was removed afterward. No additional restart is authorized by this approval.
- Phase 24 Task 24-01-02: User explicitly accepted the recorded host evidence on 2026-10-24. Plan 24-01 is complete. Task 24-02-01 remains a separate decision for final production identities and lifecycle; no deployment or further restart is approved.
- Phase 24 Task 24-02-01: User explicitly supplied approve-contract on 2026-10-24. Module URL /api/bl_haos/catalog/bl-haos-media-panel.js, element bl-haos-media-panel, packaged output panel_static/bl-haos-media-panel.js and entry-owned setup/failure/unload cleanup are approved for local implementation and testing, not live deployment or additional restart. Exact Core inspection found no public static unregister API; disable served assets on final unload/failure and reuse the inert route without private router mutation.
- Phase 24 local implementation: HA-injected catalog, one explicit connected target, metadata-preserving native browsing, single-attempt playback submission, navigation-only ingress entry and URL-free logging are implemented. Plans 24-02 through 24-05 received clean bounded independent reviews. Final static-module unload/failure returns 404; Core's inert public route is reused without private router mutation.
- Prepared local release metadata is bridge 0.2.69 and integration 0.2.20. A package-layout regression verifies the local manifest identity; live add-on remains 0.2.67 and live integration remains 0.2.19. Both local candidates are uncommitted and unpublished; no saved-playlist CRUD or queue controls from phases 25-26 were implemented.
- User selected controlled deployment/test-window planning only. The plan in 24-06-CHECKPOINT.md covers backup/restore verification, version-only amd64 publication, update/Core restart and rollback budgets, explicit playback/session consent and host review. Read-only inventory confirmed live add-on 0.2.67 and installed integration 0.2.19; the installed integration differs from the local candidate. Assign a unique integration candidate version (proposed 0.2.20) before publication and rerun metadata gates. No publishing, backup creation, commit, install, restart or playback was authorized/performed by this planning step.
- Phase 27: The scheduler owns repeated reconnects; manager-level adapter locks serialize automatic/operator connections. Defaults are 10-120 seconds exponential backoff and a 300-second breaker, with no automatic link reset.
- Local mock-progression exception: user explicitly approved phase-25/26 local work while T-24-15 remains OPEN/HIGH. `.planning/config.json` temporarily sets `workflow.security_block_on=critical`; restore it to `high` before live verification, publication, or deployment. This is not risk acceptance, production verification, or release approval.

### Pending Todos

- Design the API streaming/polling mechanism for discovery.
- Update the frontend to incrementally render discovered devices.

### Blockers/Concerns

- Phase 24 Task 24-01-01 rebaselined under Ubuntu WSL Python 3.14.4 in the separate /home/mse/.venvs/bl-haos-sil-2026.10.3 environment: Core 2026.10.3, helper 0.13.374; panel/static and integration SIL passed 24 tests in 4.06s, no skips. Public PyPI metadata verified; corrected resolver dry-run, isolated install, and pip check succeeded. Earlier 2026.9.4 evidence remains historical in 24-VALIDATION.md.
- Phase 24 Task 24-01-02 accepted: All six public-host observations passed on Core 2026.10.3 and were accepted by the user. Actual session expiration was not forced; denied/invalid-session rejection was observed. Probe entry/entity/panel/files were removed and module returned 404 with the active session connected. Plan 24-01 summary records the accepted evidence. Task 24-02-01 final production contract is now approved for local implementation; deployment remains gated.
- Phase 24 canonical verification was refreshed on 2026-10-27 and passed 5/5 for the explicitly authorized local-mock scope. The 42 panel unit tests and five mock browser scenarios passed after the Library-first test-flow repair. Production acceptance remains deferred: actual HA/provider/audio/expiry/HA-shell behavior is not established, PL-01/02/03 remain pending, T-24-15 stays OPEN/HIGH, T-24-16 stays OPEN/MEDIUM, and release/deployment remain blocked.
- Phase 24 mock-only local progression is explicitly user-approved. The five-case mock Playwright suite and three captures are accepted for local sequencing only. Live provider/audio/expiry/HA-shell acceptance remains deferred; PL-01/02/03 remain unverified for production and T-24-15 stays OPEN/HIGH. Release/deployment are blocked. Current read-only browser showed the sole speaker idle/disconnected and media-source browsing unavailable. No candidate publication, install, additional restart, playback or fixture/session manipulation occurred; the previous one-restart probe approval is exhausted.
- Phase 27 verification was refreshed after shared phase-24 release changes and is current passed for local scope: fresh 91 Bluetooth, 2 version and 3 API cases passed; full bridge 323-pass evidence retained. Bridge 0.2.69 remains uncommitted/undeployed. Authorized HAOS deployment and physical-speaker soak remain required before claiming the live fault resolved.

## Deferred Items

| Category | Item | Status | Deferred At | Milestone |
|----------|------|--------|-------------|-----------|
| Hardware validation | Phase 27 reconnect soak | Await deployment authorization; then test power loss/return, busy responses, breaker pacing, pairing retention and playback | 2026-10-24 | v1.0 |
| Production host acceptance | Phase 24 plan 06 | Await deployment/session/playback inputs; actual provider, expiry-fixture rejection, screenshots and accessibility/audio checks remain required | 2026-10-24 | v1.0 |

## Session Continuity

Last session: 2026-10-27T19:00:00Z
Current: Phase plans 24-27 are locally complete; v1.0 audit is gaps_found. Await separate authorization for panel packaging and production gates. Do not stage or commit because task outputs overlap the existing dirty baseline.
Resume file: .planning/v1.0-MILESTONE-AUDIT.md
