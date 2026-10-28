---
phase: 28-package-panel-bundle-parity
plan: 01
subsystem: testing
tags: [vite, typescript, pytest, home-assistant, package]
requires:
  - phase: 27
    provides: Existing BL-HAOS integration and reconnect behavior retained by the packaged panel.
provides:
  - Fresh temporary Vite build compared byte-for-byte with the tracked panel bundle.
  - Package and Home Assistant SIL assertions for saved-playlist launch and queue-summary markers.
  - Refreshed integration-served panel bundle generated from the reviewed source.
affects: [phase-29-ci, phase-31-ha-acceptance, phase-32-accessibility]
tech-stack:
  added: []
  patterns:
    - Separate static package assertions from Node-dependent isolated-build parity.
    - Build to pytest tmp_path before intentionally refreshing the tracked asset.
key-files:
  created:
    - .planning/phases/28-package-panel-bundle-parity/28-CONTEXT.md
    - .planning/phases/28-package-panel-bundle-parity/28-REVIEW.md
  modified:
    - modules/integration/tests/test_package_layout.py
    - modules/integration/tests/test_panel_registration.py
    - modules/integration/custom_components/bl_haos/panel_static/bl-haos-media-panel.js
    - .planning/phases/28-package-panel-bundle-parity/28-VALIDATION.md
key-decisions:
  - "Keep Node-free package assertions runnable in Python-only CI; Phase 29 owns installing the selected Node/npm toolchain for mandatory CI parity checks."
  - "Use the existing pinned Vite build and isolate parity output from panel_static because the configured build clears its output directory."
patterns-established:
  - "Verify generated assets by building into a fresh temp directory and comparing actual bytes before any intentional refresh."
  - "Test package contents separately from Home Assistant's static-route and unload/reload lifecycle."
requirements-completed: [PRD-01]
coverage:
  - id: D1
    description: The packaged bundle matches a fresh build of the reviewed panel source and contains saved-playlist launch and queue summary behavior.
    requirement: PRD-01
    verification:
      - kind: unit
        ref: modules/integration/tests/test_package_layout.py::test_panel_bundle_matches_fresh_build
        status: pass
      - kind: unit
        ref: modules/integration/panel_ui/src/media-panel.test.tsx
        status: pass
    human_judgment: false
  - id: D2
    description: Home Assistant serves the refreshed bundle and preserves the existing static-route unload/reload lifecycle.
    requirement: PRD-01
    verification:
      - kind: integration
        ref: modules/integration/tests/test_panel_registration.py (WSL SIL, 26 passed)
        status: pass
    human_judgment: false
completed: 2026-10-28
status: complete
---

# Phase 28: Package Panel Bundle Parity Summary

**The integration now serves the reviewed panel source as a reproducible bundle, with byte-level drift detection and Home Assistant route coverage.**

## Accomplishments

- Reviewed the pre-existing panel-source/test changes and confirmed the 73-test panel suite passed before using them as bundle input.
- Added a temporary-output parity check and package markers; proved it detected the stale bundle before the intentional refresh, then passed after refresh.
- Extended the Home Assistant SIL response assertions; the registered route, queue markers, unload, and reload passed.
- Split the static assertions from the Node/Vite-dependent parity check so the Python-only CI job remains runnable; Phase 29 must provision the build toolchain to make parity mandatory in CI.
- Standard-depth code review completed with no Critical or Warning findings.

## Verification

- Panel Vitest: 73 passed.
- Integration package-layout tests: 11 passed.
- Focused fresh-build parity test: 1 passed after refresh; it failed on byte mismatch before refresh as expected.
- WSL panel-registration SIL: 26 passed.
- Local build runtime: Node `v24.19.0`, npm `11.17.0`; these are observations, not CI pins.

## Files Created/Modified

- `modules/integration/tests/test_package_layout.py` - Static queue markers and isolated fresh-build parity.
- `modules/integration/tests/test_panel_registration.py` - Served module response markers with existing lifecycle assertions.
- `modules/integration/custom_components/bl_haos/panel_static/bl-haos-media-panel.js` - Generated bundle refreshed from reviewed source.
- `.planning/phases/28-package-panel-bundle-parity/28-VALIDATION.md` - Passed local Nyquist validation and runtime evidence.
- `.planning/phases/28-package-panel-bundle-parity/28-CONTEXT.md` - Autonomous infrastructure-phase constraints and existing patterns.
- `.planning/phases/28-package-panel-bundle-parity/28-REVIEW.md` - Clean standard-depth code review.

## Decisions and Deviations

- No UI behavior, transport controls, package dependencies, Node pins, CI workflows, or release metadata were changed.
- The parity check is skipped only when Node/npm or the panel Vite/TypeScript dependencies are absent. Phase 29 must install these dependencies in CI so the check runs there.
- No task commits were created because the active project state says not to stage or commit. No live host, publication, restart, playback, provider/session, or hardware actions were performed.

## Next Phase Readiness

Phase 29 can add the panel's selected Node/npm runtime and `npm ci` to the integration CI job, then make the parity test mandatory there. The refreshed bundle remains local and unpublished.

---
*Phase: 28-package-panel-bundle-parity*
*Completed: 2026-10-28*