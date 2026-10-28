---
phase: 26-sequential-playback-queue-controls
plan: 01
subsystem: playback
tags: [python, asyncio, queue, process-lifecycle]
requires:
  - phase: 25-saved-playlist-library
    provides: ordered saved media references for a later authenticated queue-start adapter
provides:
  - generation-fenced in-memory playback sessions per normalized speaker
  - bridge queue start, navigation, repeat/shuffle, and URL-free state transitions
affects: [26-02, native-api, ingress-playback]
actuals:
  tokens: 11000
  tasks: 2
  commits: 0
tech-stack:
  added: []
  patterns: [per-speaker generation fencing, strict paired-process natural completion]
key-files:
  created: [.planning/phases/26-sequential-playback-queue-controls/26-01-SUMMARY.md]
  modified:
    - modules/bridge/backend/bl_haos/ha/player.py
    - modules/bridge/backend/bl_haos/api/routes.py
    - modules/bridge/tests/test_media_player.py
    - modules/bridge/tests/test_api.py
key-decisions:
  - "Natural completion advances only when both decoder and player exit with code zero."
  - "Queue invalidation clears playable URLs; standalone play_url remains single-item compatible."
requirements-completed: [PL-07, PL-09, PL-10]
duration: not-measured
completed: 2026-10-28
status: complete
---

# Phase 26 Plan 01: Authenticated Bridge Playback Queue Summary

**One authenticated native queue-start request now reaches a generation-fenced per-speaker session and returns a bounded URL-free playback snapshot.**

## Accomplishments

- Added bounded, transient per-speaker sessions keyed by normalized Bluetooth address, with generation and exact process-pair ownership checks.
- Added ordered queue start, zero/zero-only natural advancement, explicit failure retention, repeat/shuffle, next/previous, pause/resume, retry, and stop semantics.
- Kept queue snapshots allowlisted and URL-free; bounded item count, aggregate payload, display text, and failure status.
- Added deterministic fake-process coverage for replacement, stop, disconnect, shutdown, partial spawn, completion, and standalone playback compatibility.
- Added a strict native `queue_start` request schema with item-count, URL/display-field, and aggregate-payload bounds; dispatch retains native authentication and trusted audio-sink checks.
- Exposed only allowlisted queue display fields in the shared playback envelope and kept queue-start out of sink reconnect/re-execution handling.
- Added a TestClient tracer using a real `MediaPlayerBridge` and deterministic fake subprocesses, proving address normalization, one decoder/player pair, current-session metadata, authentication, and URL-free response state.

## Task Status

- Task 1: Complete. The authenticated queue-start route reaches the normalized speaker session, starts one process pair, and returns a sanitized current-item snapshot; both-zero natural completion and stale/failure outcomes remain covered by deterministic player tests.
- Task 2: Complete. Navigation, modes, pause/resume/retry, and cancellation semantics pass the focused queue lifecycle tests.

## Verification

Working directory: `modules/bridge`.

1. `$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'; python -m pytest tests/test_media_player.py tests/test_api.py -q -k queue` — 23 passed, 123 deselected; one Starlette deprecation warning.
2. `$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'; python -m pytest tests/test_media_player.py tests/test_api.py -q` — 145 passed, 1 existing skip; one Starlette deprecation warning.
3. Focused nested-URL route regression — passed, with sentinels absent from queue/timeline snapshots and logs.
4. VS Code diagnostics for `player.py`, `routes.py`, `test_media_player.py`, and `test_api.py` — no errors.
5. `git diff --check` on the declared queue implementation and tests — passed.

The focused queue selectors verify process lifecycle behavior. The full player/API suite also covers existing playback compatibility. API tests verify oversized item-count and aggregate payload rejection before dispatch, and that queue-start sink failure does not reconnect or retry. No live HA/provider, deployment, restart, physical audio, or release verification was performed.

## Deviations from Plan

- Corrected prior sequencing omission: the earlier executor stopped after the player/session work because its dispatch excluded `routes.py` and `test_api.py`. The current authorization explicitly included the route tracer; those remaining Task 1 files are now implemented and verified. No Plan 26-02 controls/capability work was added.
- The aggregate-size HTTP response remains the application's generic `Invalid request payload`; the model-boundary test confirms the specific aggregate limit is enforced without exposing validation details to callers.
- No STATE.md or ROADMAP.md updates were made. No files were staged and no commits were created, as explicitly requested.

## Git State

- Staged paths: 0.
- Commits created: 0.
- Existing dirty/untracked baseline preserved; only the declared API route and API test were additionally modified for this completion.

## Self-Check: PASSED

- Summary artifact and all four plan implementation/test files exist.
- The exact focused queue selector passes: 23 passed, 123 deselected.
- No files staged, no commits created, and STATE.md/ROADMAP.md remain untouched.