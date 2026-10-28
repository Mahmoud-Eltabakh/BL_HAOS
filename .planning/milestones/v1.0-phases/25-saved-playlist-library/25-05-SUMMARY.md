---
phase: 25-saved-playlist-library
plan: 05
subsystem: ui
tags: [react, typescript, home-assistant, vitest]
requires:
  - phase: 25
    provides: HA-authenticated playlist provider save, rename, and remove commands
provides:
  - Browse-media save action with an editable local name for one exact provider playlist reference
  - Local shortcut rename and confirmed local-only removal controls
  - Provider shortcut component tests for retries, pending states, failures, and focus
affects: [25-06, 26]
actuals:
  tokens: null # Cannot isolate chars/4 from pre-existing dirty and untracked baseline files.
  tasks: 2
  commits: 0
tech-stack:
  added: []
  patterns: [HA-injected callWS for library mutations, server-acknowledged snapshots, native confirmation dialog]
key-files:
  created:
    - .planning/phases/25-saved-playlist-library/25-05-SUMMARY.md
  modified:
    - modules/integration/panel_ui/src/media-panel.tsx
    - modules/integration/panel_ui/src/playlist-library.test.tsx
    - modules/integration/custom_components/bl_haos/panel_static/bl-haos-media-panel.js
key-decisions:
  - "Provider playlists remain opaque Home Assistant references; provider contents are never copied into local entries."
  - "The server response is canonical for shortcut identity and local label, including retry after an uncertain save."
  - "Do not stage, commit, or update STATE/ROADMAP per the explicit run override."
requirements-completed: [PL-05]
coverage:
  - id: D1
    description: Save one browsed HA playlist by exact opaque ID; retain the HA-canonical local name on retry.
    requirement: PL-05
    verification:
      - kind: unit
        ref: "npm --prefix modules/integration/panel_ui test -- --run src/playlist-library.test.tsx"
        status: pass
    human_judgment: false
  - id: D2
    description: Rename and remove only the local provider shortcut, with explicit confirmation and failure retention.
    requirement: PL-05
    verification:
      - kind: automated_ui
        ref: "npm --prefix modules/integration/panel_ui test -- --run"
        status: pass
      - kind: other
        ref: "npm --prefix modules/integration/panel_ui run build"
        status: pass
    human_judgment: false
duration: not-measured
completed: 2026-10-27
status: complete
---

# Phase 25 Plan 05: Provider Playlist Shortcut UI Summary

**Authenticated Browse media shortcuts now save exact HA playlist references, preserve server-owned canonical labels, and support local rename and confirmed removal without editing provider content.**

## Performance

- **Duration:** Not measured
- **Completed:** 2026-10-27
- **Tasks:** 2/2
- **Declared implementation files:** 2
- **Commits:** 0, per explicit override

## Accomplishments

- Added `Save to library` only for playlist browse results. The request uses the original `media_content_id` and injected `hass.callWS`; success is based on the HA response, not optimistic insertion.
- Added an editable local shortcut name before saving, allowing long UTF-8 provider titles to be shortened to the backend's 128-byte bound without changing the opaque media reference.
- Added a saved Home Assistant playlist section with the approved empty copy, local labels, HA-managed-contents identification, local rename, and confirmed local-only removal.
- Added pending/single-flight handling, bounded retry copy, failure retention, accessible dialog focus, and wrapping for long local labels.
- Rename focuses its input on open and restores focus to the Rename shortcut action after success or cancellation; over-limit server validation keeps the draft with corrective guidance.

## TDD Gate Compliance

- **RED:** The focused command failed on the six new provider-flow assertions while the existing 16 tests passed; the missing browse save action, provider section, rename, and removal behavior were the asserted failures.
- **GREEN:** The final focused run passed 23/23 tests. The full panel suite passed 65/65 tests across two files, and the TypeScript/Vite production build succeeded.
- **Commit gate:** RED/GREEN commits were intentionally omitted under the user's no-stage/no-commit override. No evidence or source file outside the declared task scope was added for commit bookkeeping.

## Files Created/Modified

- `modules/integration/panel_ui/src/media-panel.tsx` - Provider shortcut UI and injected HA mutation flows.
- `modules/integration/panel_ui/src/playlist-library.test.tsx` - Exact-ID, idempotent retry, local rename/removal, pending/error, empty-state, focus, and long-label coverage.
- `modules/integration/custom_components/bl_haos/panel_static/bl-haos-media-panel.js` - Rebuilt panel artifact in the pre-existing untracked baseline directory.
- `.planning/phases/25-saved-playlist-library/25-05-SUMMARY.md` - This plan summary.

The build reports its output at `modules/integration/custom_components/bl_haos/panel_static/bl-haos-media-panel.js`, inside the pre-existing untracked baseline directory. It was not staged, committed, or cleaned.

## Verification

- `npm --prefix modules/integration/panel_ui test -- --run src/playlist-library.test.tsx` - 23 passed, 0 failed.
- `npm --prefix modules/integration/panel_ui test -- --run` - 65 passed, 0 failed across 2 files.
- `npm --prefix modules/integration/panel_ui run build` - passed; TypeScript check and Vite production build completed (269.84 kB, gzip 64.79 kB).

## Deviations from Plan

- The required production build writes to the panel's configured static output under the pre-existing untracked `panel_static` directory. The baseline was preserved; no cleanup or staging was performed.
- The estimate's `actuals.tokens` is `null`: pre-existing dirty/untracked files overlap the task outputs, so an exact chars/4 delta cannot be isolated without an available pre-task snapshot. Tasks and commits are recorded exactly.

**Total deviations:** 2 documented execution constraints. No scope expansion.

## Residual Risks

- Verification is local component/build evidence only. No live HA/provider, deployment, restart, playback, queue, or release verification was performed.
- Existing phase-24 production risks remain open; this plan does not establish provider availability or production acceptance.
- The panel build output remains within the user's untracked baseline and was not reviewed or committed as a release artifact.

## Next Phase Readiness

Plan 25-05 is complete for local/mock scope. Plan 25-06 availability behavior remains separate; Phase 26 still owns playlist launch and queue behavior.

---
*Phase: 25-saved-playlist-library*
*Completed: 2026-10-27*