---
phase: 24-ha-media-catalog-provider-playback
plan: "02"
subsystem: integration
tags: [home-assistant, react, vite, panel, lifecycle, sil]
status: complete
completion_scope: local-plan-only
completed: "2026-10-24"
duration: "Wall-clock duration not captured; executable gate timings recorded below"
requires:
  - phase: "24-01"
    provides: "Accepted Core 2026.10.3 public-host mechanism evidence"
provides:
  - "Fixed-name injected-hass browse-to-one-speaker custom-element tracer"
  - "Serialized shared entry ownership and real public HTTP 200/404/reload regression coverage"
  - "Exact-pinned reproducible panel package and bundled inline styles"
affects: [24-03, 24-04, 24-05, 24-06]
requirements-completed: []
requirements-covered-locally: [PL-01, PL-02, PL-03]
tech-stack:
  added: ["separate React/Vite panel package using existing repository versions"]
  patterns: ["injected-hass only", "stable inert Core route plus temporary served copy", "serialized config-entry owner set"]
key-files:
  created:
    - modules/integration/custom_components/bl_haos/panel_static/bl-haos-media-panel.js
    - modules/integration/panel_ui/.gitignore
    - modules/integration/panel_ui/package.json
    - modules/integration/panel_ui/package-lock.json
    - modules/integration/panel_ui/tsconfig.json
    - modules/integration/panel_ui/vite.config.ts
    - modules/integration/panel_ui/vitest.config.ts
    - modules/integration/panel_ui/src/media-panel.tsx
    - modules/integration/panel_ui/src/media-panel.test.tsx
  modified:
    - modules/integration/custom_components/bl_haos/__init__.py
    - modules/integration/custom_components/bl_haos/manifest.json
    - modules/integration/tests/test_panel_registration.py
    - modules/integration/tests/test_package_layout.py
    - modules/integration/tests/unit/conftest.py
    - modules/integration/README.md
    - .planning/phases/24-ha-media-catalog-provider-playback/24-VALIDATION.md
key-decisions:
  - "Honor the user's explicit approve-contract recorded by the parent; no new contract approval inferred"
  - "Use only public Core registration/removal APIs; retain the inert static route rather than claiming unregister"
  - "An uncertain static-registration failure blocks further attempts for that Core lifetime"
  - "Run real-Core SIL and HA-stub unit tests in separate Linux processes"
  - "No commits, staging, branches, deployment or restarts, as explicitly requested"
actuals:
  tokens: 95260
  tasks: 3
  commits: 0
actuals_scope: "381037 chars / 4 rounded up: owned integration tracked diff plus nine new integration files; excludes pre-existing requirements-sil and parent planning edits"
plan_head_before: f428a2a4df69c29080ea1515c5b706cd1af9f8a2
plan_head_after: f428a2a4df69c29080ea1515c5b706cd1af9f8a2
commits: 0
bundle:
  bytes: 225032
  gzip_bytes: 56407
  sha256: 2ad1bc409ea3e56b1f0495de64e5b40fc352ce454c2adc61e171189ffe0d4ff0
coverage:
  - id: D1
    description: "Public lifecycle serves the actual packaged module, disables it on final unload/failure and reuses the stable route on reload"
    requirement: PL-03
    verification:
      - kind: integration
        ref: "modules/integration/tests/test_panel_registration.py: 14 tests on Linux Core 2026.10.3"
        status: pass
    human_judgment: false
  - id: D2
    description: "Injected-hass tracer preserves opaque IDs/types and targets exactly one explicitly selected connected speaker"
    requirement: PL-02
    verification:
      - kind: unit
        ref: "modules/integration/panel_ui/src/media-panel.test.tsx: 6 passing Vitest tests"
        status: pass
      - kind: automated_ui
        ref: "Local built-module Chromium fixture at 375/768/1440 pixels; not live HA acceptance"
        status: pass
    human_judgment: false
  - id: D3
    description: "Production panel loads in authenticated HA and plays real provider media on a physical speaker"
    verification: []
    human_judgment: true
    rationale: "Intentionally deferred to plan 24-06; no live deployment, session access or restart authorized in this run"
---

# Phase 24 Plan 02: Local HA Media Panel Tracer Summary

**Injected-hass React custom element preserves opaque media references for one explicit speaker, with shared fail-closed public-Core asset ownership.**

## Scope and Tasks

- **24-02-01:** User's `approve-contract` was already recorded in STATE.md by the parent. The accepted plan 24-01 SUMMARY and target-host evidence were read, not rerun.
- **24-02-02:** Implemented and built the local tracer. Repeated build, actual public HTTP lifecycle and built-module injected-hass browser checks passed before declaring the tracer proven locally.
- **24-02-03:** Added lifecycle/package regressions before production edits and the typed injected-hass test suite before component creation. All final scoped executable gates passed.
- **Commits:** None. No staging, branch or git metadata writes were performed. Work remains uncommitted by explicit user instruction, not a claim of atomic task commits.
- **Inventory:** 15 integration files: nine created and six modified. This SUMMARY and the phase VALIDATION addendum bring the execution-owned inventory to 17 files. Pre-existing `requirements-sil.txt`, parent planning edits and all phase 27 changes were preserved.

## Contract and Lifecycle

The approved module URL is `/api/bl_haos/catalog/bl-haos-media-panel.js`, the element is `bl-haos-media-panel`, and packaged output is `modules/integration/custom_components/bl_haos/panel_static/bl-haos-media-panel.js`. Public panel registration uses sidebar path `/bl-haos-media` after client initialization. The manifest now declares the required `http` dependency.

One lock-protected owner set is shared across config entries. First setup copies the fixed packaged module into an integration-owned temporary location using executor-backed standard file APIs, registers one public static path and one public custom panel, then forwards platforms. Additional owners reuse them. Successful final-owner unload removes the panel using `frontend.async_remove_panel` and deletes the served copy; the module returns HTTP 404. Failed setup releases only that entry's ownership and closes its client; partial platform setup is unloaded. Actual cancellation waits for acquisition to settle before rollback, avoiding an executor/register cleanup race.

**Core limitation:** Core 2026.10.3 has no public static unregister API. The route and owned pathname remain in memory for the Core lifetime; normal reload recreates the file at the same path and reuses the inert route. This is NOT complete route unregistration and does not revoke already loaded browser code or caches. Long-lived static cache headers are disabled. If the public static registration call raises after an indeterminate partial mutation, the file is removed and subsequent setup fails closed with `ConfigEntryNotReady` for that Core lifetime rather than risking duplicate route registration. No private router mutation, private frontend import, process hook or automatic restart was added.

## Frontend Boundary and Package

The custom element accepts only the injected `hass` property. It browses via typed browse-only `callWS`, offers connected `media_player` states carrying the existing `bluetooth_address` plus nonempty `adapter` attributes, and starts with no selected target. It rechecks the current target before invoking `media_player.play_media` with exactly one `entity_id` and the unchanged opaque ID/type. It does not resolve media, import an ingress client, fetch provider/catalog endpoints, copy auth, use browser storage or discover a global/parent `hass`. Bounded errors do not reflect raw provider exceptions.

The presentation follows the existing Neumorphic UI-SPEC, native controls, lucide icons, 44px targets and reduced-motion styling. HA same-origin thumbnails are used when supplied; no stock artwork was introduced. Inline shadow-root CSS is included in the JS module, with no external CSS/chunk path. Full catalog states/search/ingress CTA, filtering and URL-log redaction remain in plans 03-05, not silently implemented here.

Before installation, public npm metadata verified all 13 direct identities, exact versions, tarball origins and integrity fields. Installed versions match the existing bridge package installation:

| Packages | Exact Versions |
|----------|----------------|
| react, react-dom | 18.2.0 |
| lucide-react | 0.344.0 |
| @types/react, @types/react-dom | 18.2.66, 18.2.22 |
| @vitejs/plugin-react, vite, typescript | 4.7.0, 7.3.7, 5.2.2 |
| vitest, jsdom | 5.0.4, 25.0.1 |
| @testing-library/react, jest-dom, user-event | 16.3.3, 6.9.1, 14.6.7 |

Only the new panel package was installed. Initial install added 168 packages in 29s; lockfile-only `npm ci` added the same 168 packages in 10s. Registry installs used `--ignore-scripts --no-audit --no-fund`. No provider/auth dependency or existing-package update was introduced. Context7's installed CLI verified Vite 7 library-mode output documentation. Clean-lockfile and subsequent identical builds produced SHA256 `2ad1bc409ea3e56b1f0495de64e5b40fc352ce454c2adc61e171189ffe0d4ff0`, 225032 bytes, gzip 56407 bytes.

## TDD Gate Compliance

Exact commands and intermediate outcomes are retained in `24-VALIDATION.md`.

| Stage | Command / Discriminating Check | Observed Result |
|-------|--------------------------------|-----------------|
| Lifecycle RED before production | Linux `pytest tests/test_panel_registration.py -q -p asyncio --asyncio-mode=auto -k owned_panel --tb=short --show-capture=no`, `BLHAOS_RUN_SIL=1` | **4 failed, 3 deselected, 1.24s**: missing HTTP 200/registration and missing failure/cancellation close |
| Initial lifecycle GREEN | Same command | **4 passed, 3 deselected, 1.07s** |
| Package RED before component | Windows `pytest -c modules/integration/pytest.ini modules/integration/tests/test_package_layout.py -q -k panel_build --tb=short` | **1 failed, 5 deselected, 0.11s**: missing component |
| Frontend scaffold RED | `npm --prefix modules/integration/panel_ui test -- --run` before component creation | **1 failed suite, zero collected tests, 626ms**: missing import; not assertion-level behavior evidence |
| First frontend GREEN | Same command after implementation | **5 passed, 1.00s** |
| Partial panel registration RED | Linux panel test `-k partial_public` | **1 failed, 11 deselected, 0.53s**: real registered panel survived failure |
| Partial static registration RED | Linux panel tests `-k 'partial_static or actual_cancellation'` | **1 failed, 1 passed, 12 deselected, 1.21s**: duplicate retry; cancellation already passed |
| Focused repair GREEN | Same partial-static/cancellation command | **2 passed, 12 deselected, 0.74s** |

The first fixture attempt had four setup errors because optional `hass_frontend` is not installed; it was not accepted as RED. Full frontend setup was unnecessary: actual public registration and actual HTTP remain exercised. The first production validation exposed HTTP-test startup ordering and repeated directory cleanup, which were repaired locally. TypeScript initially rejected generic mock typing and missing matcher augmentation; a typed browse-only surface and Vitest matcher import fixed it.

## Final Verification

Linux commands ran from `/mnt/f/Workspace/BL-HAOS/modules/integration` using `/home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python` (Core 2026.10.3, helper 0.13.374, Python 3.14.4, pytest 9.0.3).

| Gate | Exact Command / Scope | Final Result |
|------|-----------------------|--------------|
| Full real-Core integration/SIL/package | `BLHAOS_RUN_SIL=1 python -m pytest tests --ignore=tests/unit -q -p asyncio --asyncio-mode=auto --tb=short --show-capture=no` | **41 passed, zero skips, 7.10s** |
| Full isolated Linux units | `BLHAOS_RUN_SIL=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest tests/unit -q -p asyncio --asyncio-mode=auto --tb=short --show-capture=no` | **54 passed, zero skips, 1.84s** |
| Windows portable checks | `.venv/Scripts/python.exe -m pytest -c modules/integration/pytest.ini modules/integration/tests/test_package_layout.py modules/integration/tests/unit -q --tb=short` | **60 passed, 1.17s**, not HA proof |
| Frontend | `npm --prefix modules/integration/panel_ui test -- --run` | **6 passed, 1.15s** |
| Final typed build | `npm --prefix modules/integration/panel_ui run build` | Passed; Vite **1.07s**; identical fixed single-module hash |
| Built-module Chromium | Existing bridge Playwright; temporary loopback-only server, then closed | **375/768/1440 x 900 passed**, no overflow, 44px controls, explicit one-target opaque dispatch, reduced-motion transition 0s, zero page errors |
| Patch hygiene | Integration and validation `git diff --check` | Passed; root validation only reports its existing CRLF normalization warning |

The two Linux processes cover **95 tests total**, not a green monolithic run. The all-in-one attempt originally reported 24 failed/64 passed in 7.85s: missing new production HTTP/tracing requirements plus existing real-Core/stub import-order incompatibility. HTTP/tracing were fixed. Standalone units then exposed seven missing import stubs; the existing unit fixture now supplies fail-fast test-only HTTP/panel names. Those stubs never establish public lifecycle proof. Running the suites separately avoids cross-contamination without changing unrelated client logic.

Chromium screenshots at `%TEMP%/bl-haos-plan24-02-visual/panel-{375,768,1440}.png` were visually inspected. These are injected fixtures, not authenticated HA-host/provider or artwork acceptance. The fixture page has a plain body outside the mounted panel, so its white remainder is not a claim about HA shell framing. The editor still reports one relative-import diagnostic in the test file despite passing TypeScript and Vitest resolution; no compiler failure was suppressed.

## Deviations and Limits

- **Approved lifecycle adjustment:** No full static unregister exists. Public panel removal plus temporary-file removal, stable inert-route reuse and fail-closed uncertain-registration handling implement the user's explicit constraint.
- **Rule 1:** Fixed failure/cancellation rollback, idempotent file cleanup, partial public panel rollback and duplicate static-registration retries. Three production-file repair iterations were used; no further production repair loop was attempted.
- **Rule 2:** Declared the required HTTP dependency and applied the repository's call-tracing convention to new functions.
- **Rule 3:** Extended only the existing unit fixture's import stubs and isolated unit execution from real-Core SIL. Added the minimal separate panel package/configuration required by the plan.
- **User execution override:** No commits, staging, branches or parent-owned planning state updates. Zero commits is intentional and all work remains available locally.
- No new stub or placeholder blocks this tracer. Empty initial React state is lifecycle state, not mock production data. Source scanning found no TODO/FIXME/placeholder markers or prohibited browser-auth/resolution/network patterns in the component.
- No live HA access, deployment, restart, token extraction, radio reset, unpair, phase 27 change or later-plan execution occurred. No requirement or phase completion is claimed. Live production-panel/provider/physical-audio acceptance remains plan 24-06.

## Self-Check: PASSED

All 15 integration files and both planning artifacts exist. Bundle SHA256 matches
the recorded production artifact; direct dependency/devDependency pins match the
lockfile root. Integration HEAD remains
`f428a2a4df69c29080ea1515c5b706cd1af9f8a2`; no task commit is claimed. The recorded
Linux, frontend, build and browser results are the executed gates above, not a
claim of live acceptance or phase completion. Parent-owned state remains untouched.

## Review Remediation Addendum - 2026-10-24

Three of three BLOCKER findings in `24-02-REVIEW.md` have local fixes and passing
focused regressions; none were skipped. **Independent parent re-review remains
pending.** The review itself is unchanged and still says `issues_found`. Earlier
counts, package metadata and browser observations above are historical evidence;
the current executable results and bundle metadata are recorded here.

- **CR-01:** Root-relative HA thumbnails are parsed with the standard URL API
  against a fixed safe dummy origin. Off-origin, protocol-relative, backslash,
  literal control-character and normalized double-slash paths are rejected.
  Only the validated normalized path is rendered; no session authentication is
  read or copied. The existing legitimate HA image path is preserved.
- **CR-02:** Session identity uses injected HA connection identity, connection
  availability and user ID, not the changing `hass` object or user object.
  Session changes invalidate independent browse/play generations and clear
  navigation, target, busy state and feedback. Old success/error/finally handlers
  cannot mutate a replacement session. Same-session out-of-order browse results
  are discarded. Dispatch uses current injected methods/state, and completion
  rechecks current speaker connectivity. Errors remain fixed, bounded messages.
- **CR-03:** `_finish_operation` continues shielding and draining its task after
  repeated caller cancellation, then re-raises cancellation. Task-originated
  cancellation remains cancellation. Event-gated real-Core copy/removal and
  public registration tests verify the ownership lock stays held until work
  settles, final owners are empty, client cleanup occurs, HTTP returns 404 and
  reload returns 200 before a final unload returns 404. No route unregister or
  private Core API was introduced; existing multi-entry semantics are unchanged.

Regressions were added and immediately run before their production fixes. The
initial thumbnail run had **5 assertion failures**, the session run **6 assertion
failures**, and executor cancellation **2 assertion failures**. Each source fix
was immediately followed by the identical focused command and passed. A stricter
protocol-relative-policy regression then failed once and passed after the narrow
guard change. Exact commands and RED/GREEN counts are in the validation addendum.

Final gates ran in the **main checkout**, with no worktree, installation, staging,
commit, branch, deployment, live-host/session access or phase 27/global STATE edit:

| Gate | Current Result |
|------|----------------|
| Full panel Vitest | **28 passed**, 1.34s |
| Full real-Core SIL/package, Linux Core 2026.10.3 | **45 passed**, no skips, 8.35s |
| Separate isolated Linux unit process, plugin autoload disabled | **54 passed**, no skips, 1.91s |
| Expanded registration/executor cancellation check | **5 passed**, 13 deselected, 1.38s |
| `npm run build` including both existing Vite config files in TypeScript | Passed; repeated build byte-identical, Vite 1.07s |
| Editor diagnostics for all seven touched source/test/config files | No errors reported, including the former relative-import diagnostic |
| Integration `git diff --check` | Passed |

Current single output: `panel_static/bl-haos-media-panel.js`, **225873 bytes**,
gzip **56712 bytes**, SHA256
`3eb60c232558add8642101d97f4df3ce7f704040a251e91f692e0057c81a1d6e`.
Only the existing `tsconfig.json` include list was extended for `vite.config.ts`
and `vitest.config.ts`; no suppression or declaration workaround was added.

Warnings/limits: The one-off Node repeat-build wrapper emitted DEP0190 about
`shell:true` with child-process arguments (all arguments were fixed local build
paths). TypeScript, Vite, Vitest and pytest passed. The earlier multiline terminal
attempt returned incomplete output and was not accepted as determinism evidence;
the self-contained rerun reported `stable:true`. No fresh Chromium/viewport matrix,
authenticated HA/provider or physical-speaker acceptance is claimed. The two
Linux suites remain separate processes, not a claimed green monolithic run.

## WR-01 Late-Failure Remediation Addendum - 2026-10-24

The updated review's sole WARNING, WR-01, has a local fix. Independent re-review
is still required; `24-02-REVIEW.md` is unchanged with `status: issues_found`.
This addendum supersedes earlier current-gate counts, not their historical
observations, and does not approve plan 24-03 or advance phase/global state.

`_finish_operation` now shields a non-failing completion future rather than the
failure-bearing task. Its done callback only resolves completion; after that
signal settles, `task.result()` explicitly retrieves the original outcome.
Saved caller cancellation wins after draining, including repeated cancellation;
without caller cancellation, operation errors and operation-originated
cancellation still propagate. No loop-handler replacement or private asyncio
callback manipulation was used.

Focused regressions were edited and immediately run before production changed.
On the unchanged helper, **10 test bodies passed, 16 deselected, 6 teardown
errors, 2.97s, exit 1**: each one/two/three-cancel late failure escaped Core's
normal loop-error capture, both in the helper and after public registration.
The zero-cancel error-propagation control and successful-operation cases passed.
Immediately after the small production change, the identical command returned
**10 passed, 16 deselected, 2.28s, exit 0**, with no teardown errors.

The registration cases assert lock ownership and pending work before release,
then cancellation, closed client, zero owners, removed file/panel and HTTP 404.
Subsequent setup serves HTTP 200 at the same public URL without another static
registration; final unload restores zero owners and HTTP 404. Helper cases
assert the original child has settled and was not cancelled. Existing real
executor copy/removal regressions and operation-originated cancellation also pass.

All checks ran in the **main checkout** through the existing Ubuntu WSL
Python 3.14.4 environment, Core 2026.10.3, helper 0.13.374, pytest 9.0.3:

| Latest Gate | Observed Result |
|-------------|-----------------|
| Focused late-failure/actual-cancellation RED | **10 passed, 6 teardown errors**, 16 deselected, 2.97s; exit 1 |
| Same focused command immediately after production fix | **10 passed**, 16 deselected, 2.28s; exit 0 |
| Real-Core panel registration + package layout | **32 passed**, 5.23s; exit 0 |
| Full real-Core `tests --ignore=tests/unit` | **53 passed**, no skips or teardown errors, 9.13s; exit 0 |
| Separate `tests/unit`, plugin autoload disabled | **54 passed**, no skips, 1.79s; exit 0 |

The former 45-test Core suite now has eight additional cases: four helper
late-failure controls plus four added registration parameter combinations.
The two full Linux processes cover **107 tests**, not a monolithic test run.
Exact commands are recorded in the matching validation addendum.

Only the integration helper, existing panel test and these two evidence documents
were edited for WR-01. Frontend source, fixtures, configs and packaged assets were
unchanged, so no frontend build or browser gate was rerun. Prior frontend/hash
results remain historical, not freshly measured. No install, staging, commit,
branch/worktree, deployment, live-host/token access, STATE or phase 27 edit occurred.