---
phase: 36-native-playlist-browse-and-play-ui
plan: 01
subsystem: ui
tags: [react, vitest, home-assistant, playlist-library, sil, vite, package-parity]

requires:
  - phase: 24
    provides: Native Home Assistant media-source browsing boundary
  - phase: 25
    provides: HA-owned saved playlist library
  - phase: 26
    provides: Saved playlist queue start operation
provides:
  - Mounted native-panel browse-to-save-to-selected-player playlist-start regression test
  - Authenticated persistence/read-shape SIL assertions for custom and provider records
  - Package parity assertions for playlist creation/editing and media browsing actions
affects: [phase-36-verification, phase-37]

actuals:
  tokens: 2602
  tasks: 3
  commits: 0

tech-stack:
  added: []
  patterns:
    - Mounted-panel regression coverage follows exact HA WebSocket command order and opaque media IDs
    - Fresh Vite package parity is checked in an isolated temporary output directory

key-files:
  created:
    - .planning/phases/36-native-playlist-browse-and-play-ui/36-01-SUMMARY.md
  modified:
    - modules/integration/panel_ui/src/playlist-library.test.tsx
    - modules/integration/tests/test_playlist_library_sil.py
    - modules/integration/tests/test_package_layout.py

key-decisions:
  - "No production behavior gap was found; retain the existing integration UI/library implementation and strengthen verification only."
  - "No commits or STATE.md/ROADMAP.md updates were made, per explicit user instruction."

requirements-completed: [NUX-02]
coverage:
  - id: D1
    description: Native panel browses an HA media item, saves its exact reference to a one-item playlist, and starts that saved record on the explicitly selected player.
    requirement: NUX-02
    verification:
      - kind: automated_ui
        ref: modules/integration/panel_ui/src/playlist-library.test.tsx#browses an exact HA reference, saves it, and starts that playlist on the selected speaker
        status: pass
    human_judgment: false
  - id: D2
    description: Authenticated reads and playlist starts preserve existing custom/provider record identity, order, references, shortcut labels, and persisted shape.
    requirement: NUX-02
    verification:
      - kind: integration
        ref: modules/integration/tests/test_playlist_library_sil.py#test_authenticated_library_read_preserves_custom_and_provider_record_shape
        status: pass
      - kind: integration
        ref: modules/integration/tests/test_playlist_library_sil.py#test_custom_playlist_start_resolves_every_reference_before_one_queue_command
        status: pass
    human_judgment: false
  - id: D3
    description: The packaged panel is regenerated and matches an isolated fresh build, with NUX-02 action labels guarded by package tests.
    requirement: NUX-02
    verification:
      - kind: unit
        ref: modules/integration/tests/test_package_layout.py::test_panel_bundle_matches_fresh_build
        status: pass
    human_judgment: false

duration: 7min
completed: 2026-10-28
status: complete
---

# Phase 36 Plan 01: Native Playlist Browse and Play UI Summary

**Native playlist browse-to-save-to-play coverage proves opaque media references reach the selected player through HA-owned services, with saved-record compatibility and packaged-bundle parity verified.**

## Performance

- **Duration:** 7 minutes
- **Started:** 2026-10-28T17:45:21+01:00
- **Completed:** 2026-10-28T17:52:06+01:00
- **Tasks:** 3/3
- **Files modified by this plan:** 3 test files; the generated bundle rebuilt to identical tracked output

## Accomplishments

- Added a mounted-panel test that creates a playlist, browses the HA media-source root, saves one playable leaf without changing its opaque ID, selects Kitchen, and starts the saved record through `bl_haos/playlist_library/start`.
- Added authenticated SIL coverage confirming list reads preserve custom/provider record IDs, entry order, exact references, shortcut label, persisted shape, and stored bytes. Strengthened the save/start SIL path to verify storage remains unchanged by playback launch.
- Extended package checks to require the native `Create playlist`, `Save changes`, and `Browse media` labels in source, packaged output, and a fresh isolated build.
- Ran the pinned panel build (`tsc && vite build`) to regenerate `panel_static/bl-haos-media-panel.js`. The isolated byte-for-byte package parity check passed; the generated bundle had no resulting tracked diff.
- Existing native UI and HA library implementation already provided the required behavior, so no production code changes were necessary.

## Verification Results

| Check | Result |
|---|---|
| `npm --prefix modules/integration/panel_ui test` | **PASS** — 74 tests across 2 files |
| `npm --prefix modules/integration/panel_ui run build` | **PASS** — TypeScript check and Vite build; 1,462 modules transformed |
| `py -3.12 -m pytest -q tests/test_package_layout.py` from `modules/integration` | **PASS** — 12 tests, including isolated fresh-build byte parity |
| WSL Ubuntu SIL command using the cached integration venv | **PASS** — 48 playlist library SIL tests, Python 3.14.4 |
| `py -3.12 -m pytest -q` at repository root | **PASS** — bridge suite: 359 passed, 1 skipped; one Starlette/httpx deprecation warning |
| `git diff --check` in `modules/integration` | **PASS** |

## Not Run / Environment Limits

- The playlist SIL suite could not collect with local Windows `py -3.12` because `homeassistant` is not installed there. It was run successfully in the existing Ubuntu WSL SIL environment instead.
- The full integration pytest suite beyond the requested playlist SIL and package-layout suites was not run.
- No live HA host, provider, playback/audio, hardware, deploy, publish, restart, or GHCR action was attempted. Host `192.168.1.18` was not contacted.

## Task Commits

No commits were made, per explicit user instruction. This also means no plan metadata commit was created.

## Files Created/Modified

- `modules/integration/panel_ui/src/playlist-library.test.tsx` — mounted end-to-end native browse/save/start path.
- `modules/integration/tests/test_playlist_library_sil.py` — authenticated saved-record read and persistence/start invariants.
- `modules/integration/tests/test_package_layout.py` — NUX-02 action-label and bundle parity checks.
- `modules/integration/custom_components/bl_haos/panel_static/bl-haos-media-panel.js` — regenerated with the pinned build; byte-identical to the isolated fresh build and no tracked diff.

## Decisions Made

- Preserve the existing production implementation because the required UI and authenticated HA playlist operations were already present; close the plan's observed gaps through additional regression assertions only.
- Respect the requested no-commit and no-state-update constraints. `STATE.md` and `ROADMAP.md` were not edited by this execution.

## Deviations from Plan

- No production source changes were needed; plan instructions explicitly limited such changes to demonstrated gaps. Existing implementation and coverage already handled playlist lifecycle operations; new assertions close the missing end-to-end and read-preservation coverage.
- Per user instruction, all task/final commits and state/roadmap updates were omitted. No other plan scope was expanded.

## Issues Encountered

- Initial local Windows SIL collection confirmed the missing `homeassistant` dependency. The pre-existing WSL environment had the required Home Assistant test dependencies, and the complete targeted SIL suite passed there.
- The first draft of the new read-compatibility test passed an unsupported revision argument to `async_save_provider`; corrected the test to use the established API signature, then reran the full SIL suite successfully.

## User Setup Required

None. No external service configuration is required for local verification.

## Next Phase Readiness

Phase 36's local NUX-02 UI, playlist persistence, and packaged asset assertions are verified. This is local/mock evidence only and does not imply live acceptance or authorize deployment/publication. No state or roadmap status was advanced.

---
*Phase: 36-native-playlist-browse-and-play-ui*
*Completed: 2026-10-28*
## Self-Check: PASSED

- Summary and all three changed test files exist; the packaged bundle exists.
- The recorded Vitest, WSL SIL, package parity, bridge pytest, and build results correspond to successful runs.
- No plan commits exist because committing was expressly prohibited; STATE.md and ROADMAP.md were left unchanged by this execution.