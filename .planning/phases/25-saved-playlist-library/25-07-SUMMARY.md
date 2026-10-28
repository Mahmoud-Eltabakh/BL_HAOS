---
phase: 25-saved-playlist-library
plan: 07
subsystem: mock-panel
tags: [react, typescript, playwright, pytest, home-assistant]
requires:
  - phase: 25-03
    provides: Custom playlist editor and ordered media-reference rows
  - phase: 25-05
    provides: Saved provider playlist shortcut UI
  - phase: 25-06
    provides: Explicit non-destructive availability checks
provides:
  - Deterministic local playlist-library mock commands, revisions, availability, and failure injection
  - Dedicated mock Playwright coverage for CRUD, shortcuts, keyboard/focus, failure retention, and responsive backstops
  - Scoped documentation claims and contract assertions that retain production blockers
affects: [26, integration docs, bridge docs]
actuals:
  tokens: null # Existing dirty/untracked baseline overlaps declared outputs; isolated chars/4 delta is unavailable.
  tasks: 3
  commits: 0
plan_head_before: 9ab8f2ead4f5fd96c3515e06f5a384a5fbcb045d
plan_head_after: 9ab8f2ead4f5fd96c3515e06f5a384a5fbcb045d
tech-stack:
  added: []
  patterns: [in-memory hass.callWS library model, separate mock Playwright spec selection, local-only docs contract tests]
key-files:
  created:
    - modules/integration/panel_ui/e2e/playlist-library.spec.ts
    - modules/integration/tests/test_phase25_docs.py
    - modules/bridge/tests/test_phase25_docs.py
  modified:
    - modules/integration/panel_ui/mock-harness.html
    - modules/integration/panel_ui/playwright.mock.config.ts
    - modules/integration/README.md
    - modules/bridge/README.md
    - modules/bridge/DOCS.md
    - README.md
key-decisions:
  - "Keep mock-catalog.spec.ts untouched and runnable by selecting both dedicated specs in the mock Playwright config."
  - "Use explicit empty, availability, and responsive scenarios with in-memory records and injectable pre/post-mutation failures."
  - "Redirect the build output to a temporary directory because the configured output would clear the pre-existing untracked panel_static baseline."
  - "No staging, commits, STATE.md updates, or ROADMAP.md updates under the Phase 25 autonomous-run override."
patterns-established:
  - "Mock evidence is origin-restricted and cannot issue live-host requests."
  - "Responsive evidence is local rendered-panel coverage only, not HA-shell or production acceptance."
requirements-completed: [PL-04, PL-05, PL-06, PL-11]
coverage:
  - id: D1
    description: Deterministic browser acceptance covers custom playlist drafts/CRUD/order, provider shortcuts, exact-ID availability, and retained state on failures.
    requirement: PL-04
    verification:
      - kind: e2e
        ref: "npm --prefix modules/integration/panel_ui run test:mock-panel (playlist-library.spec.ts)"
        status: pass
    human_judgment: false
  - id: D2
    description: Keyboard/focus and all ten responsive backstops are asserted at 375px, 768px, and 1440px with ignored local screenshots.
    requirement: PL-06
    verification:
      - kind: automated_ui
        ref: "modules/integration/panel_ui/test-results/playlist-library/playlist-library-{375,768,1440}px.png"
        status: pass
    human_judgment: false
  - id: D3
    description: Integration and bridge docs describe the local candidate while keeping T-24-15/T-24-16 and release/deployment gates open.
    verification:
      - kind: unit
        ref: "modules/integration/tests/test_phase25_docs.py::test_phase25_library_docs"
        status: pass
      - kind: unit
        ref: "modules/bridge/tests/test_phase25_docs.py::test_phase25_library_docs"
        status: pass
    human_judgment: false
  - id: D4
    description: Production HA/provider/accessibility/playback acceptance and release readiness remain unclaimed.
    verification: []
    human_judgment: true
    rationale: Local mock/browser tests cannot establish live host, provider, HA-shell, or playback behavior; those checks remain outside this authorization.
duration: not-measured
completed: 2026-10-27
status: complete
---

# Phase 25 Plan 07: Mock Library Acceptance Summary

**Deterministic mock acceptance now covers saved-library CRUD, provider shortcuts, exact-reference availability, keyboard/focus behavior, responsive backstops, and failure retention without live HA or playback.**

## Performance

- **Duration:** Not measured
- **Completed:** 2026-10-27
- **Tasks:** 3/3
- **Declared files changed:** 9, plus this summary
- **Commits:** 0 under the explicit no-stage/no-commit override

## Accomplishments

- Extended the in-memory `hass.callWS` harness with list/create/update/delete, provider shortcut idempotency/rename/removal, exact-reference browse status, revision conflicts, and injected failures before or after mutation.
- Added a dedicated `playlist-library.spec.ts` while keeping the legacy mock-catalog spec unchanged and runnable. Browser checks cover empty drafts, duplicate opaque IDs, ordering in both keyboard directions, confirmation/Escape focus, provider retry label preservation, exact availability IDs, stable drafts/records/dialogs on errors, and no playback or queue calls.
- Added local rendered assertions for the ten UI backstops and empty-library states at 375px, 768px, and 1440px. Three screenshots are present under the ignored `panel_ui/test-results/playlist-library/` directory.
- Long provider titles are explicitly unclamped with `overflow-wrap:anywhere`; the responsive Playwright assertions verify all metadata starts below the full title. Mock revision tests pin save-after-commit retry at revision 1, rename at 2, and delete at 3.
- Updated only the Phase 25 claims in root, integration, and bridge docs. Added module-local docs contract tests; neither test reads the root README.

## Verification

- `npm --prefix modules/integration/panel_ui test -- --run` - 68 passed across 2 files.
- `npm --prefix modules/integration/panel_ui run test:mock-panel` - 17 passed: 5 unchanged mock-catalog tests and 12 playlist-library/viewport tests.
- Complete Core playlist SIL: 42 passed on pinned Home Assistant Core 2026.10.3, no skips.
- `python -m pytest modules/integration/tests/test_phase25_docs.py -q` - 1 passed when rerun with `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`. The unmodified command first hit the Windows-only `fcntl` import from the auto-loaded Home Assistant SIL plugin.
- `Push-Location modules/bridge; python -m pytest tests/test_phase25_docs.py -q; $code = $LASTEXITCODE; Pop-Location; exit $code` - 1 passed with `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`.
- `npm --prefix modules/integration/panel_ui run build -- --outDir "$env:TEMP/bl-haos-phase25-final-build"` - TypeScript passed; Vite transformed 1,462 modules and emitted a 272.32 kB bundle (65.14 kB gzip) in the temporary directory.
- Focused Playwright check of mock-catalog and viewport/empty states - 11 passed.
- Editor diagnostics: no errors in the new Playwright spec/config or Python docs tests.

## Files Created/Modified

- `modules/integration/panel_ui/mock-harness.html` - Local deterministic library state, revisions, browse data, and failure controls.
- `modules/integration/panel_ui/e2e/playlist-library.spec.ts` - Dedicated CRUD, shortcut, availability, keyboard/focus, failure, empty, and responsive browser tests.
- `modules/integration/panel_ui/playwright.mock.config.ts` - Selects both mock-catalog and playlist-library specs.
- `modules/integration/README.md` - Local Phase 25 behavior and production boundaries.
- `modules/integration/tests/test_phase25_docs.py` - Integration documentation contract.
- `modules/bridge/README.md` and `modules/bridge/DOCS.md` - Local Phase 25 behavior and production boundaries.
- `modules/bridge/tests/test_phase25_docs.py` - Contract checks for both bridge documents.
- `README.md` - Local candidate and open production/release gates.

## Decisions Made

- Mock Playwright remains isolated to the local harness; external requests are blocked and asserted absent.
- The responsive screenshots are ignored test output, not release or production evidence.
- Build output was redirected to preserve the existing untracked `panel_static` tree.
- Updated assertions reject the previously truncated provider title layout and now verify mock library revision progression through create retry, rename, and removal.

## Deviations from Plan

No scope deviation. The docs-only pytest commands required `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` on Windows because the auto-loaded SIL plugin imports `fcntl`; both final documentation tests passed with plugin autoload disabled. The panel build used a temporary `--outDir` because the configured destination has `emptyOutDir: true` and overlaps the user's untracked baseline.

## Residual Risks

- All browser evidence is deterministic local mock evidence. No live HA/provider, HA-shell, assistive-technology, playback, queue, deployment, restart, or release verification was performed.
- Phase 24 production requirements remain pending; T-24-15 remains OPEN/HIGH and T-24-16 remains OPEN/MEDIUM. Release and deployment are not approved.
- Root STATE/ROADMAP and the unrelated dirty baseline files were not edited. Root, integration, and bridge indexes remain unstaged; no commit was created. Current HEADs: root `9ab8f2e`, integration `c9a5660`, bridge `97a0130`.

## Self-Check: PASSED

- Summary file created after all plan acceptance gates passed.
- Root HEAD is unchanged at `9ab8f2ead4f5fd96c3515e06f5a384a5fbcb045d`; no paths are staged in the root, integration, or bridge indexes.
- The three responsive screenshots exist in the ignored test-results directory.
- No task commit or STATE.md/ROADMAP.md update was made.

---
*Phase: 25-saved-playlist-library*
*Completed: 2026-10-27*
