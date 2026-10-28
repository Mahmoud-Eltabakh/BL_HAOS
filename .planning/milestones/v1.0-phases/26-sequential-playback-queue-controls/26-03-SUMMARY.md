---
phase: 26-sequential-playback-queue-controls
plan: 03
subsystem: ha-integration
tags: [home-assistant, playlist-resolution, native-media-player, queue]
requires:
  - phase: 26-02
    provides: versioned bridge queue commands, capability marker, and bounded snapshots
provides:
  - authenticated launch of canonical saved playlists on one explicit speaker
  - ordered resolve-all queue replacement and atomic provider shortcuts
  - capability-gated native queue state and controls
  - single-attempt semantics for ambiguous non-idempotent queue commands
affects: [26-04, 26-05, native-playback, saved-playlists]
tech-stack:
  added: []
  patterns: [resolve-all-before-replace, exact-target-recheck, version-gated-entity-features, single-attempt-queue-commands]
key-files:
  modified:
    - modules/integration/custom_components/bl_haos/client.py
    - modules/integration/custom_components/bl_haos/const.py
    - modules/integration/custom_components/bl_haos/media_player.py
    - modules/integration/custom_components/bl_haos/playlist_library.py
    - modules/integration/tests/test_ha_integration_sil.py
    - modules/integration/tests/test_playlist_library_sil.py
decisions:
  - Queue-start, next, and previous have one transport attempt because an ambiguous acknowledgement must not replay non-idempotent playback changes.
  - Queue capability requires the exact supported version; legacy bridge snapshots retain their existing feature set.
  - Custom records resolve in saved order before one queue_start; provider shortcuts resolve exactly once as one item.
metrics:
  duration: not-measured
  completed: 2026-10-28
status: complete
actuals:
  tokens: null
  tasks: 2
  commits: 0
commits: 0
---

# Phase 26 Plan 03: HA Playlist Resolution and Native Controls Summary

**Home Assistant now resolves saved playlist references completely on the selected entity before sending one versioned queue replacement to the bridge.**

## Accomplishments

- Registered an authenticated playlist-start WebSocket command that accepts only a saved record ID and explicit media-player entity ID, then loads the canonical record from HA storage.
- Resolved custom references sequentially in saved order and submitted a single bounded `queue_start` only after all references resolve and the same speaker remains connected.
- Kept provider shortcuts atomic: one saved media-source reference resolves to one queue item and is never expanded into provider tracks.
- Rejected empty/oversized queues, invalid resolved URLs, and excessive aggregate URL payload before bridge submission; resolver errors expose only a bounded item index.
- Added version-gated Home Assistant next/previous, shuffle, repeat, queue metadata, and playlist state while preserving legacy features when the bridge does not advertise queue version 1.
- Made `queue_start`, `next`, and `previous` single-attempt in the integration client after ambiguous acknowledgements.
- Added value-free call tracing to every function in `playlist_library.py`, satisfying the integration-wide AST tracing gate.

## Verification

- Pinned Core 2026.10.3 SIL, full touched files: `tests/test_playlist_library_sil.py tests/test_ha_integration_sil.py` — 142 passed.
- Plugin-isolated integration unit suite: `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 ... pytest tests/unit` — 77 passed.
- Targeted call-tracing check — 4 passed.
- VS Code diagnostics: no errors in the six touched integration implementation/test files.
- `git -C modules/integration diff --check` — passed.

No live HA/provider, deployment, restart, or physical playback was performed.

## Deviations from Plan

**1. Tightened the integration call-tracing baseline.** The unit gate exposed that all pre-existing functions in the touched playlist-library module lacked the repository-required `@trace_call` decorator. The module now follows the same value-free tracing convention as the rest of the integration.

**2. Added an explicit aggregate resolved-payload check.** References are already bounded in storage, but their resolved URLs can be larger. The integration checks the complete transient payload before calling the bridge, with a regression proving no dispatch occurs over the limit.

## Residuals

- Plan 26-04 still needs to wire the ingress Library launch and queue controls to this authenticated HA command and shared native snapshot.
- Plan 26-05 still owns local mock acceptance and user-facing documentation.
- Live provider resolution, physical playback, deployment, and release acceptance remain unauthorized and unverified.

## Git State

- No files staged; no commits created.
- Existing dirty and untracked integration and bridge work was preserved.
- Phase 26 remains local/mock-only; the temporary local security-threshold override remains release-ineligible.

## Self-Check: PASSED

- Resolve-all ordering, provider atomicity, failure/disconnect atomicity, payload limits, queue capability, native controls, and retry behavior have SIL coverage.
- Full touched SIL and isolated unit suites passed after final edits.