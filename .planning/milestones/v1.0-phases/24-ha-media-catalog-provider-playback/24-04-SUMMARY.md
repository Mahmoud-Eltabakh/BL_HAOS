---
phase: 24-ha-media-catalog-provider-playback
plan: "04"
subsystem: frontend
tags: [home-assistant, media-source, react, accessibility, playwright]
status: complete
completion_scope: local-plan-only-awaiting-parent-review
review_fix_status: implemented-awaiting-parent-rerun
completed: "2026-10-24"
duration: "End-to-end wall clock not instrumented; actual executable timings recorded below"
requires:
  - phase: "24-02"
    provides: "Approved injected-hass contract and clean reviewed session/thumbnail guards"
  - phase: "24-03"
    provides: "Clean reviewed opaque-reference native playback with one transport attempt"
provides:
  - "Hierarchical catalog states, capability-gated public-Core search and explicit one-target manual retry"
  - "Navigation-only secure top-frame ingress catalog anchor"
  - "Local generated-bundle viewport, pixel, keyboard and reduced-motion evidence"
affects: [24-05, 24-06]
requirements-covered-locally: [PL-03]
requirements-completed: []
tech-stack:
  added: []
  patterns: [injected-hass-only, same-request-manual-retry, generation-guarded-results, offline-browser-fixture]
key-files:
  created:
    - modules/bridge/web_ui/src/App.test.tsx
    - .planning/phases/24-ha-media-catalog-provider-playback/host-probe/24-04-local-browser.mjs
  modified:
    - modules/integration/panel_ui/src/media-panel.tsx
    - modules/integration/panel_ui/src/media-panel.test.tsx
    - modules/integration/custom_components/bl_haos/panel_static/bl-haos-media-panel.js
    - modules/bridge/web_ui/src/App.tsx
    - .planning/phases/24-ha-media-catalog-provider-playback/24-VALIDATION.md
key-decisions:
  - "Verify search against exact installed Core 2026.10.3 media_source/http.py before encoding any fields"
  - "Use native /bl-haos-media anchor with target _top and rel noopener noreferrer; no parent/auth scripting"
  - "Preserve all 28 prior panel regressions unchanged"
  - "Honor no commits/staging/branches, no STATE/ROADMAP changes, and no live/deployment actions"
  - "Release version/docs remain plan 24-06; preserve pre-existing bridge 0.2.68 work"
actuals:
  tokens: null
  tasks: 3
  commits: 0
actuals_note: "An isolated before-diff was not captured for the already-untracked panel package; no comparable chars/4 delta can be honestly reconstructed. Not a harness-token estimate."
commits: 0
commit_policy: "Explicit user prohibition; no task or metadata commits attempted"
heads_observed_after:
  root: 9ab8f2ead4f5fd96c3515e06f5a384a5fbcb045d
  integration: f428a2a4df69c29080ea1515c5b706cd1af9f8a2
  bridge: 97a0130916ad8203903c6cb0e539f69b0a7c99f5
bundle:
  filename: bl-haos-media-panel.js
  bytes: 232392
  gzip_bytes: 58224
  sha256: 48d12229891c0e145906bfefec4b609016c5908c790529f57f2c3b05a3cf90f7
coverage:
  - id: D1
    description: "Catalog states, hierarchy, target guards, bounded same-request manual retry and verified public search"
    requirement: PL-03
    verification:
      - kind: unit
        ref: "media-panel.test.tsx: 41 passed after review fixes; all original 40 cases, including the 28 prior guards, retained"
        status: pass
    human_judgment: false
  - id: D2
    description: "Secure navigation-only top-frame ingress CTA, with no attributable bridge API calls"
    requirement: PL-03
    verification:
      - kind: unit
        ref: "App.test.tsx: 2 passed; full bridge frontend 26 passed"
        status: pass
      - kind: automated_ui
        ref: "24-04-local-browser.mjs: actual built ingress in iframe, keyboard Enter reaches top-level route, zero additional API calls"
        status: pass
    human_judgment: false
  - id: D3
    description: "Local generated-module geometry, pixels, focus and reduced motion at 375/768/1440 x 900"
    verification:
      - kind: automated_ui
        ref: "24-04-local-browser.mjs: six viewport/motion combinations, all passed; screenshots inspected"
        status: pass
    human_judgment: false
  - id: D4
    description: "Authenticated HA shell, real provider, physical speaker, assistive technology and host contrast acceptance"
    verification: []
    human_judgment: true
    rationale: "Explicit plan 24-06 host backstop; local injected fixture is not live authentication/provider acceptance"
---

# Phase 24 Plan 04: Catalog Interaction and Ingress Navigation Summary

**HA-owned hierarchy and metadata, source-advertised public-Core search, explicit connected targeting and bounded manual retry, with a navigation-only ingress entry.**

## Scope and Tasks

- **24-04-01:** Added full empty copy for absent/empty children, stable hierarchy during loading/failure, ancestor navigation, source capability controls, unsupported-state copy, selected-item marking, explicit connected targets, and item/target-bound retry. No automatic playback or retry, provider resolution, playlist expansion, saved-playlist controls or queue state was added.
- **24-04-02:** Added icon-plus-label `Open Media Catalog` adjacent to native integration status. The native anchor navigates to `/bl-haos-media` with `target="_top"` and `rel="noopener noreferrer"`. No auth/window-parent script or catalog host was added to ingress. `api/client.ts` is unchanged.
- **24-04-03:** Added native semantic breadcrumbs/controls, Escape-to-parent and source-button focus return, a close-to-HA-home anchor, polite atomic loading/result status, two-line titles with full labels/tooltips, visible wrapped selected-speaker detail, 44px controls, bounded list scrolling and 150ms/reduced-motion styling. No dialog was introduced, so modal trapping/close restoration is not applicable.

The original structured thumbnail URL validation and HA connection/user/availability generation invalidation remain intact. New search results also pass through the browse generation guard. Ordinary same-session state updates do not reload the root. Play is disabled during loading/pending requests and when the explicit target becomes unavailable; no replacement target is chosen. Completion checks the current supplied speaker state. Service acceptance alone produces `Starting playback on {speaker}`; it does not claim audible output.

## Exact Core Search Contract

Read the installed **Core 2026.10.3** source in the existing WSL environment before production implementation:

- `homeassistant/components/media_source/http.py:25-28` registers browse, search and resolve handlers.
- Lines 35-39 define browse as `type: media_source/browse_media` with optional `media_content_id` only. No query fields were added to browse.
- Lines 56-79 define `media_source/search_media`, optional `media_content_id` defaulting to the empty string, required `search_query`, optional `media_filter_classes`, and the `SearchMediaQuery` handoff. Lines 81-82 return `result.as_dict()`.
- `media_player/browse_media.py:175-186` defines the search response as `{ result: [...] }`.

The panel sends only the verified `type`, original `media_content_id`, and `search_query` fields after explicit form submission, and only if `can_search` is true. It never calls the distinct entity-scoped `media_player/search_media` API. Search failure retains the stable list; manual `Retry search` repeats the captured original query even if the input has since changed. There is **no search contract blocker** in this Core version. Initial narrowed inspection omitted `http.py`; directory-wide source inspection corrected that provisional hypothesis before any search production code was written.

## TDD Evidence

Commands ran from `F:\Workspace\BL-HAOS`, using existing node_modules. No dependencies were installed.

| Stage | Exact Command | Observed Result |
|-------|---------------|-----------------|
| Panel intended assertion RED before production | `npm --prefix modules/integration/panel_ui test -- --run src/media-panel.test.tsx --reporter=dot` | **7 failed, 28 passed**, 7.35s; empty copy, retries, hierarchy/status and search missing |
| Ingress intended assertion RED before CTA | `npm --prefix modules/bridge/web_ui test -- --run src/App.test.tsx --reporter=dot` | **2 failed**, 15.25s; catalog anchor absent |
| Immediate panel check after incomplete patch application | Panel focused command, output filtered for failure/summary | **7 failed, 28 passed**, 7.34s; patch tool had applied only part of the edit |
| Immediate panel GREEN after complete state-machine edit | Same focused panel command, output filtered | **35 passed**, 1.54s |
| Immediate ingress GREEN | Same focused ingress command | **2 passed**, 917ms |
| Accessibility/style RED before final CSS | Same focused panel command, output filtered | **1 failed, 39 passed**, 1.61s; missing constrained catalog-body scrolling rule |
| Immediate accessibility/style GREEN | Same focused panel command, unfiltered | **40 passed**, 1.66s |
| Final CTA utility cleanup focused check | Same focused ingress command | **2 passed**, 762ms |

All 28 pre-existing panel assertions were preserved, not weakened. New fixtures initially reused one opaque ID for two list entries; unique test-only folder IDs removed the resulting duplicate-key warnings. App's new tests now await its normal initialization, avoiding an act warning. The tool rejected two unordered patch payloads without applying them; ordered patches succeeded. No production defect required three repair iterations.

## Original Gates (Historical)

| Gate | Exact Command | Result |
|------|---------------|--------|
| Full panel Vitest | `npm --prefix modules/integration/panel_ui test -- --reporter=dot` | **40 passed**, 2.52s |
| Final full bridge frontend Vitest | `npm --prefix modules/bridge/web_ui test -- --reporter=dot` | **26 passed**, six files, 1.04s |
| Typed fixed-name panel production build | `npm --prefix modules/integration/panel_ui run build` | `tsc && vite build` passed; Vite 2.13s; **232169 bytes**, gzip **58216** |
| Final typed ingress production build | `npm --prefix modules/bridge/web_ui run build` | `tsc && vite build` passed; Vite 1.44s |
| Final local actual-bundle browser | `node .planning/phases/24-ha-media-catalog-provider-playback/host-probe/24-04-local-browser.mjs` | **Six viewport/motion combinations and framed-ingress keyboard navigation passed** |

Original panel SHA256: `1023bbcc18e2107dd638957da358b42bbe8bb34e733224df108413db94ddc58e`.
Generated bundle was produced only by Vite, not edited by hand. Bridge generated dist files remain ignored build output.

## Browser Evidence and Limits

The reproducible fixture uses the existing bridge Playwright installation and Chromium. Every request is intercepted locally at `http://catalog.fixture.invalid`; it starts **no server**, reads **no token**, and contacts **no HA/provider**. The actual packaged panel bundle receives a synthetic injected `hass`; the actual built ingress app runs inside a synthetic frame. Browser contexts are closed in `finally`.

At **375, 768 and 1440 x 900**, for both normal and reduced motion:

- No horizontal overflow; native target selector stays within viewport; every rendered button/select/link/input is at least 44px high. Catalog body scrolls independently and header controls remain reachable.
- Long selected-speaker names are fully visible in wrapped detail below the native select; complete long item labels remain accessible while row titles clamp to two lines. Screenshots at all three widths were opened and visually inspected.
- Native selector-to-close Tab traversal, cyan visible focus and Escape-to-source focus return passed. Normal transition is **0.15s**; reduced motion is **0s**.
- HA-origin fixture image assets loaded with nonzero natural dimensions. Screenshot pixel checks found **174 / 166 / 154** sampled colors at the three widths, confirming nonblank rendering. The fixture image is synthetic, not provider artwork acceptance.
- Failed play submitted once; only manual retry submitted a second identical opaque item/type to the same entity. Search used the exact verified message. Unavailable speaker selection stayed selected with Play disabled. Zero page errors and off-origin requests were observed.
- Actual built ingress keyboard activation navigated the **top frame** to `/bl-haos-media`, with **zero additional API calls** attributed to the CTA. Normal initialization calls were allowed and measured separately.

Screenshots: `%TEMP%\bl-haos-plan24-04-visual\panel-{375,768,1440}-{no-preference,reduce}.png`.
The first fixture run failed because `selectOption()` does not focus the native control; explicit `focus()` corrected the harness before the successful rerun. Browser elapsed wall clock was not instrumented and is not invented.

The editor reported no panel/test TypeScript diagnostics. After CTA utility correction, it continued to return stale Tailwind messages quoting the **removed** `focus-visible:outline` and `min-h-[44px]` utilities against the updated line. Typed builds, focused/full tests, and generated-asset browser geometry pass; no diagnostic suppression was added.

## Deviations and Boundaries

- **User override:** No commits, staging, branches, STATE/ROADMAP/requirements updates, deployment, restart, live-host/token access or pairing. Work is intentionally uncommitted. No atomic-commit claim is made.
- **User override:** Full bridge patch version and docs release work stays in **24-06**. Existing **0.2.68** phase 27 work and all previous Python/docs changes were left untouched; no release is claimed.
- Added only the permitted minimal App test file plus a reproducible phase-local browser verification fixture. No new dependency, provider client or authentication surface.
- Python was untouched. The previously supplied **103 Core / 58 separate unit** baseline is historical and was **not rerun or re-claimed**. No broad unrelated assurance gates were added.
- Production has no placeholder data, TODO/FIXME, saved-playlist or queue stub introduced by this plan. Synthetic data exists only in the explicit local test fixture. No new threat surface outside the plan's HA metadata/service and ingress-navigation boundaries was introduced.
- Actual HA-shell framing, real provider capability/search behavior, expired sessions, physical audio, assistive technology and host contrast remain the explicit **24-06** backstop. Local fixtures do not establish live authentication acceptance.
- **Stop here for parent review before 24-05.** Neither later plan was executed, and PL-03/phase completion remains unmarked globally.

## Original Self-Check: PASSED

Read-only Node assertions found all eight recorded source/test/bundle/browser/summary/validation artifacts, recomputed the packaged SHA256 and matched it to this summary, and checked the panel for forbidden storage/parent-window/fetch/stub patterns. The ingress anchor's route, top-frame target and rel protections are also covered by the passing DOM and actual-frame browser checks. One quoting-invalid PowerShell/Node command did not execute and was discarded; the quoting-safe rerun passed.

Planning `git diff --check` passed; the existing validation file produced only its CRLF-normalization advisory. No commit verification or state advancement applies because both were explicitly prohibited. No browser or server remains running from this execution. Parent review, not later-plan execution, is the next step.

## 24-04 Review Fix Evidence - 2026-10-24

Status: implemented locally, **awaiting independent parent review rerun**. The
source review remains `issues_found`; no clean-review or live acceptance claim.

- **CR-01:** Separate playback error state from browse error/recovery. Selecting
  a target clears playback feedback/retry only. Root, child and captured-search
  failures retain their bounded alert and manual retry. Playing a retained item
  cannot erase browse recovery. Back retains its previous feedback-clearing
  behavior. No additional automatic browse/search/play attempt was introduced.
- **WR-01:** Breadcrumb buttons have `min-width:44px` alongside their existing
  wrapping/max-width rules. Unit assertions pin minimum width and height;
  Chromium measures actual width and height, not CSS strings alone.
- Read the actual components and existing reproductions first. Existing App
  already has `min-h-11` and `focus-visible:outline-solid`; scoped `get_errors`
  reports no errors for App, App tests, panel or panel tests. No App edit or
  diagnostic suppression was needed.

All commands ran in the **main checkout** at `F:\Workspace\BL-HAOS`, using existing
dependencies. No worktree, branch, staging or commit was created.

| Gate | Actual Result |
|------|---------------|
| Intended RED immediately before production fix: `npm --prefix modules/integration/panel_ui test -- --run src/media-panel.test.tsx --reporter=dot` | **4 failed, 37 passed**, 1.62s; root/search/child recovery after target selection and missing breadcrumb width |
| Immediate GREEN, same command | **41 passed**, 1.54s |
| Back compatibility follow-up, same command | **41 passed**, 1.71s |
| Full panel: `npm --prefix modules/integration/panel_ui test -- --reporter=dot` | **41 passed**, initially 1.60s; final-source repeat **41 passed**, 1.71s; original 40 cases retained, including all 28 earlier guards |
| Full bridge frontend: `npm --prefix modules/bridge/web_ui test -- --reporter=dot` | **26 passed**, six files, 1.07s |
| Panel: `npm --prefix modules/integration/panel_ui run build` | `tsc && vite build` passed; final Vite build 1.11s |
| Bridge: `npm --prefix modules/bridge/web_ui run build` | `tsc && vite build` passed; Vite 1.26s |
| Browser: `node .planning/phases/24-ha-media-catalog-provider-playback/host-probe/24-04-local-browser.mjs` | Passed twice, including after final rebuild: six viewport/motion combinations and framed-ingress keyboard navigation |

At **375/768/1440 x 900**, normal/reduced motion, the one-character `A`
breadcrumb after opening `I` measures **44 x 44px** in all six cases. Every
rendered navigation/target/close/play/search control passes both dimensions.
Root failure followed by target selection and a same-session state update
retains the original alert/retry with **one** browse call; manual retry makes
exactly **two**, with identical messages and zero service calls. Failed search
retains its original `evening` query despite edited input and target selection;
manual retry repeats that identical message. Playback still retries only the
same item/target, and unavailable selection remains selected with Play disabled.

Long-name wrapping, narrow layout, no horizontal overflow, loaded thumbnails,
scrolling, keyboard/focus, 0.15s/0s motion, zero page/off-origin errors and zero
CTA-attributable API calls passed. Nonblank screenshot samples: **168/164/155**
colors; normal-motion screenshots at all three widths were visually inspected.
The browser fixture starts no server and closes Chromium in `finally`.

Final generated bundle: **232392 bytes**, gzip **58224**, SHA256
`48d12229891c0e145906bfefec4b609016c5908c790529f57f2c3b05a3cf90f7`.
It was generated only by the typed build. Existing public-Core search fields and
safe source-inspection commands are unchanged; no Python/Core tests were rerun
for this JS-only fix. No install, live-host/token/deployment/restart action,
STATE/phase 27 edit, release version change or later-plan execution occurred.
Both defects passed the first production repair; one small Back compatibility
follow-up also passed immediately, within the three-loop limit. Human HA-shell,
provider, physical audio and accessibility backstops remain unchanged.