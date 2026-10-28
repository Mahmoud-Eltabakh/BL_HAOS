---
phase: 24-ha-media-catalog-provider-playback
plan: "04"
reviewed: "2026-10-24"
depth: deep
files_reviewed: 4
files_reviewed_list:
  - modules/integration/panel_ui/src/media-panel.tsx
  - modules/integration/panel_ui/src/media-panel.test.tsx
  - modules/bridge/web_ui/src/App.tsx
  - modules/bridge/web_ui/src/App.test.tsx
findings:
  critical: 0
  warning: 0
  info: 0
  total: 0
status: clean
---

# Phase 24 Plan 04: Code Review Report

## Narrative Findings (AI reviewer)

No unresolved findings in this two-finding re-review. Both original repros
passed independent checks on 2026-10-24. `clean` applies to this bounded
re-review, not to new scope or live acceptance.

### CR-01: Original BLOCKER - Resolved

The original defect hid browse recovery when a target change cleared shared
error state. Current source separates `playError` from browse `error`; target
selection clears only playback feedback/retry and leaves `browseRetry` intact.

Independent offline Chromium loaded the actual packaged module. At each of
375/768/1440 x 900, with normal and reduced motion, initial root browse rejected.
Selecting Kitchen and injecting an ordinary same-session state update retained
the original bounded alert and visible `Retry media sources`, with exactly
**one browse call**. Manual retry made exactly **two identical root requests**,
restored the catalog, cleared the alert and preserved Kitchen selection.
There were **zero service calls** and no automatic browse recovery.

The same independent browser probe failed an advertised search for `original`,
edited the input to `edited` and changed the target. The alert/retry survived
without another request; manual retry repeated the captured `original` query
and exact message once. The existing panel tests independently passed root,
child and captured-search recovery after selection, plus playback retry
invalidation when changing targets. No production/test edits were made here.

### WR-01: Original WARNING - Resolved

The original one-character ancestor measured 43.34375 x 44px. Current source
adds `min-width:44px` to `.catalog-path button`, preserving its existing
wrapping/max-width rules.

The independent browser probe navigated from root `A` into source `I` using
the actual packaged module. The `A` breadcrumb measured **44 x 44px in all six
viewport/motion combinations**. All five rendered child-view controls
(Back, target selector, Close catalog, breadcrumb and Play) measured at least
44px in both dimensions. No horizontal overflow occurred. The panel test's
CSS assertion also passed; resolution is grounded in actual geometry, not
that string assertion alone.

## Scope And Preserved Contracts

Reviewed only the four explicitly requested source/test files against
24-04-PLAN, UI-SPEC, and 24-04-SUMMARY. STATE still describes 24-02; the explicit
24-04 review request controlled this read-only scope. The panel files are
untracked, so an isolated versioned 24-04 panel diff is unavailable. The prior
24-02/24-03 clean reviews were read to preserve their accepted fixes, not to
reopen unrelated backend work.

For this re-review, only the two original findings and their owning panel
source/tests were re-examined, plus the generated module for independent
browser reproduction. The original four-file list above is retained as the
review's original scope, not a claim of a fresh App review. The prior verified
Core search/session-guard/navigation conclusions below remain unchanged and
were not reopened.

No additional concrete defect was established in these requested paths:

- Failed playback captures one opaque item and target; manual retry rechecks
  the same current target and connectivity. Changing the target removes that
  playback retry, becoming unavailable disables it without substitution, and
  the synchronous `playing` guard prevents concurrent duplicate submissions.
- Browse/search generation checks reject superseded responses. Connection,
  user, and availability transitions invalidate both browse and play; ordinary
  same-session HA updates preserve selection and use current methods/state.
- Independently inspected installed **Core 2026.10.3** without network access:
  `media_source/http.py:56-82` registers `media_source/search_media`, optional
  `media_content_id`, required `search_query`, and returns `result.as_dict()`;
  `media_player/browse_media.py:175-186` serializes `{ result: [...] }`. The
  panel uses those public fields only when `can_search` is advertised; it
  does not invent a browse-query field or provider-specific endpoint.
- Service/browse exception text is not reflected. Existing structured
  same-origin thumbnail validation and no-referrer behavior remain intact.
- The ingress change is a native `/bl-haos-media` anchor with `_top` and
  `noopener noreferrer`, matching the integration's registered `PANEL_PATH`.
  It does not derive a route from Referer, inspect a parent session, or add
  catalog/service calls. App tests exclude normal diagnostics initialization
  when comparing activation-attributable API calls.
- Long item labels retain full text/accessible action names; selected speaker
  detail wraps visibly; semantic controls, Escape focus restoration, polite
  status, visible focus, and reduced-motion rules remain present. This does
  not replace the explicit HA-shell/assistive-technology backstop.

## Verification And Limits

Independent re-review command, using existing dependencies in the main checkout:

```text
npm --prefix modules/integration/panel_ui test -- --run src/media-panel.test.tsx --reporter=dot
Test Files: 1 passed; Tests: 41 passed; Duration: 1.57s
```

A separate inline Node/Playwright probe, not the executor's browser script,
loaded the existing generated module entirely from intercepted requests and
injected synthetic HA state. All six viewport/motion combinations passed the
root-recovery, captured-search and geometry assertions described above, with
**zero page errors, off-origin requests or service calls**. Contexts and
Chromium closed in `finally`; no fixture/screenshot files or server were used.

Actual bundle: **232392 bytes**, SHA256
`48d12229891c0e145906bfefec4b609016c5908c790529f57f2c3b05a3cf90f7`.
The hash independently matched the supplied fix summary. Source/test/bundle
and STATE hashes were unchanged across the independent browser check.

The fixer's **4 failed / 37 passed -> 41 passed**, bridge **26 passed**, typed
builds and broader six-viewport fixture remain supplied historical evidence.
This re-review independently observed the current 41-pass result and the two
original browser repros; it did not reverse the fix to rerun RED, rebuild
assets, rerun bridge gates or repeat ingress navigation. Original editor-only
Tailwind diagnostics were not re-evaluated; they were not product findings.

Real HA shell, screen reader, provider behavior, physical playback and host
contrast remain unverified plan 24-06 backstops. The prior Core search contract,
session guards, navigation and 24-03 single-POST transport conclusions remain
preserved; no new live or broad correctness claim is made.

Only this review artifact was updated. No source/test/STATE changes, installs,
staging, commits, branches, deployments, token access or live actions occurred.
