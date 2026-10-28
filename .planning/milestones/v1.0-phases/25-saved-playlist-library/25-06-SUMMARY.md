---
phase: 25-saved-playlist-library
plan: 06
subsystem: integration/panel
tags: [react, typescript, home-assistant, pytest, vitest]
requires:
  - phase: 25-03
    provides: Custom playlist editor and ordered media-reference rows
  - phase: 25-05
    provides: Saved provider playlist shortcut UI
provides:
  - Explicit transient availability checks for custom and provider references through authenticated HA browse
  - Core SIL coverage for exact-reference browse, denial, preservation, and no resolution/playback
  - Panel coverage for manual checks, per-row pending state, mixed results, and reload reset
affects: [25-07, 26]
actuals:
  tokens: null # Existing dirty/untracked files overlap the plan outputs, so the realized diff cannot be isolated reliably.
  tasks: 2
  commits: 0
commits: 0
plan_head_before: 9ab8f2ead4f5fd96c3515e06f5a384a5fbcb045d
plan_head_after: 9ab8f2ead4f5fd96c3515e06f5a384a5fbcb045d
tech-stack:
  added: []
  patterns: [injected hass.callWS browse, transient row-keyed status, synthetic Core media source]
key-files:
  created:
    - .planning/phases/25-saved-playlist-library/25-06-SUMMARY.md
  modified:
    - modules/integration/panel_ui/src/media-panel.tsx
    - modules/integration/panel_ui/src/playlist-library.test.tsx
    - modules/integration/tests/test_playlist_library_sil.py
key-decisions:
  - "Only an explicit Check availability action calls media_source/browse_media with the unchanged saved ID."
  - "A successful browse is Available at check time regardless of can_play; failures only update transient UI state."
  - "Availability results reset on panel reload and never enter saved records or browser storage."
patterns-established:
  - "Use a single shared polite status region for completion announcements and plain per-row status text."
requirements-completed: [PL-06, PL-11]
coverage:
  - id: D1
    description: Core authenticated browse checks preserve exact custom/provider references and Store bytes without resolution or playback.
    requirement: PL-06
    verification:
      - kind: integration
        ref: "tests/test_playlist_library_sil.py::test_playlist_library_availability_browses_exact_saved_references_without_resolution"
        status: pass
    human_judgment: false
  - id: D2
    description: The panel provides explicit, independent, transient availability actions and statuses for saved references.
    requirement: PL-06
    verification:
      - kind: unit
        ref: "src/playlist-library.test.tsx (26 focused tests)"
        status: pass
      - kind: other
        ref: "npm --prefix modules/integration/panel_ui run build -- --outDir $env:TEMP/bl-haos-plan-25-06-final-build"
        status: pass
    human_judgment: false
duration: not-measured
completed: 2026-10-27
status: complete
---

# Phase 25 Plan 06: Explicit Availability Checks Summary

**Saved custom and provider references now have on-demand, exact-ID HA browse checks with independent transient status and no library mutation or media resolution.**

## Performance

- **Duration:** Not measured
- **Tasks:** 2/2
- **Implementation and test files modified:** 3
- **Commits:** 0, per explicit no-stage/no-commit override
- **Plan metadata commit:** Omitted; no commit was authorized
- **HEAD before/after:** `9ab8f2ead4f5fd96c3515e06f5a384a5fbcb045d` (unchanged)

## Accomplishments

- Added `Check availability` for saved provider shortcuts and custom playlist entries. Each action calls the injected authenticated HA connection with the exact stored `media_content_id`; no browse occurs on load.
- Added row-specific pending/results, duplicate-submit protection, generic unavailable copy, and a shared polite completion announcement. `can_play` is not inspected, entries remain editable, and status is component state only.
- Added a synthetic Core media source SIL check covering successful non-playable browse, denied browse, independent results for two saved records, exact IDs, unchanged serialized Store bytes/order, zero resolver calls, and zero service calls.

## TDD Gate Compliance

- **RED:** The focused panel tests initially failed because the availability actions/statuses were absent. The first SIL selector found no matching availability tests before the contract test was added.
- **GREEN:** Focused panel tests passed 26/26; the focused Core SIL passed 1/1.
- **Full local gates:** Panel Vitest passed 68/68 across two files; the typed production build passed to a temporary output directory.
- **Commit gate:** No files were staged or committed under the explicit override.

## Files Created/Modified

- `modules/integration/panel_ui/src/media-panel.tsx` - Exact-ID check action and transient per-row statuses.
- `modules/integration/panel_ui/src/playlist-library.test.tsx` - Explicit checks, pending isolation, mixed outcomes, no playability inference, duplicate prevention, and reload reset.
- `modules/integration/tests/test_playlist_library_sil.py` - Authenticated synthetic Core browse contract and non-mutation assertions.
- `.planning/phases/25-saved-playlist-library/25-06-SUMMARY.md` - This execution record.

## Verification

- `wsl.exe -d Ubuntu --cd /mnt/f/Workspace/BL-HAOS/modules/integration env BLHAOS_RUN_SIL=1 PYTHONDONTWRITEBYTECODE=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests/test_playlist_library_sil.py -q -p asyncio --asyncio-mode=auto -k "playlist_library_availability"` - 1 passed, 41 deselected.
- `npm --prefix modules/integration/panel_ui test -- --run src/playlist-library.test.tsx` - 26 passed.
- `npm --prefix modules/integration/panel_ui test -- --run` - 68 passed across 2 files.
- `npm --prefix modules/integration/panel_ui run build -- --outDir "$env:TEMP/bl-haos-plan-25-06-final-build"` - TypeScript check passed; Vite transformed 1,462 modules and built a 272.18 kB bundle (65.12 kB gzip) in the temporary directory.

## Deviations from Plan

No functional scope deviation. WSL returned transient `WSAETIMEDOUT` errors before a later identical SIL command passed. The Core test's no-service spy was adjusted to patch the slotted `ServiceRegistry.async_call` class method rather than its read-only instance attribute. The build output was redirected to `%TEMP%` to preserve the existing untracked `panel_static` baseline. Follow-up review found failure copy claiming an unsaved draft was saved; neutral wording and draft-specific coverage were added, then the full panel suite/build passed again.

## Residual Risks

- Verification is local component/build and synthetic Core SIL evidence only. No live provider, Home Assistant host, deployment, restart, playback, queue, or release operation was performed.
- Availability means only that authenticated HA browse succeeded at check time; it does not establish playability or future availability. Existing Phase 24 production risks remain open.
- `actuals.tokens` is unavailable because the overlapping pre-existing dirty/untracked baseline prevents reliable isolation of the realized diff size.

## Next Phase Readiness

Plan 25-06 is complete for local/mock scope. Plan 25-07 may run its phase-level UI and documentation gates; Phase 26 remains responsible for playback and queue behavior.

## Self-Check: PASSED

- Summary and all three declared source/test files exist.
- HEAD is unchanged and the Git index has no staged paths.
- STATE.md and ROADMAP.md were not edited by this execution; their existing dirty baseline was preserved.

---
*Phase: 25-saved-playlist-library*
*Completed: 2026-10-27*
