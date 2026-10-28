---
phase: 28-package-panel-bundle-parity
verified: 2026-10-28T05:51:45Z
status: passed
score: 4/4 must-haves verified
covered_files:
  - .planning/phases/28-package-panel-bundle-parity/28-01-PLAN.md
  - .planning/phases/28-package-panel-bundle-parity/28-01-SUMMARY.md
  - modules/integration/custom_components/bl_haos/panel_static/bl-haos-media-panel.js
  - modules/integration/tests/test_package_layout.py
  - modules/integration/tests/test_panel_registration.py
covered_digest: "v3:sha256:fd05f37965d300b1d6ed3e81bbf6ef9e52c425ea55996d9559f3de8400af2922"
behavior_unverified: 0
overrides_applied: 0
deferred:
  - truth: "CI must provision the selected Node/npm runtime and panel dependencies so parity cannot be skipped there."
    addressed_in: "Phase 29"
    evidence: "Phase 29 covers declared integration CI runtimes; Phase 28 PLAN assigns CI runtime selection to Phase 29, and the parity test skips only when required tools/dependencies are absent."
  - truth: "Actual HAOS/provider/session and audible playback acceptance has not been established by local SIL."
    addressed_in: "Phase 31"
    evidence: "Phase 31 success criteria require separately authorized host, provider, denial/unavailable/session, and speaker playback acceptance."
  - truth: "Actual Home Assistant shell accessibility and responsive acceptance has not been established by local SIL."
    addressed_in: "Phase 32"
    evidence: "Phase 32 success criteria require actual-shell evidence at 375, 768, and 1440 pixels plus accessibility checks."
---

# Phase 28: Package Panel Bundle Parity Verification Report

**Phase Goal:** Home Assistant serves the reviewed panel source as a generated bundle containing the saved-playlist launch and queue controls.
**Verified:** 2026-10-28T05:51:45Z
**Status:** passed for local package and SIL scope only

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | The tracked integration bundle is generated from the reviewed panel source and matches a fresh isolated Vite build byte-for-byte. | VERIFIED | Reviewed source/test diff is the change recorded by the clean standard-depth review; full panel Vitest passed 73/73; package-layout parity test built to `tmp_path` and passed exact `filecmp` comparison. Current bundle is 279,980 bytes. |
| 2 | Package checks confirm saved-playlist launch and queue-summary markers are present in the generated bundle. | VERIFIED | `test_panel_build_source_and_stable_bundle_contract` checks `Play playlist` and `Playback queue`; all 11 package-layout tests passed. |
| 3 | Home Assistant's integration route serves the queue-capable packaged module and preserves unload/reload and ownership lifecycle. | VERIFIED | WSL SIL served HTTP 200 responses with the custom-element, launch, and queue markers; final unload returned 404, reload returned 200, and shared-entry ownership behavior passed. Panel-registration SIL: 26/26. |
| 4 | A reproducible local check detects source-to-bundle drift without overwriting the package artifact. | VERIFIED | The parity test invokes the existing npm/Vite build with a unique temporary `--outDir`, requires exactly the expected JS file, and compares bytes. A separate fresh temporary build differed from the pre-refresh `HEAD` bundle (279,980 vs 269,836 bytes), confirming stale-artifact detection; the current tracked bundle passes. |

**Score:** 4/4 truths verified (0 present, behavior-unverified)

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `modules/integration/tests/test_package_layout.py` | Isolated build parity, one-file output, package markers, and source safety guards | VERIFIED | Substantive assertions use `tmp_path`, the existing build script, exact output-set checking, byte comparison, queue markers, and retained source exclusions. All 11 tests passed. |
| `modules/integration/custom_components/bl_haos/panel_static/bl-haos-media-panel.js` | Generated bundle from reviewed panel source | VERIFIED | Exists and is substantive; freshly generated output is byte-identical to the tracked artifact and includes both required UI markers. |
| `modules/integration/tests/test_panel_registration.py` | SIL coverage for served markers and lifecycle | VERIFIED | HTTP response assertions cover element name, `Play playlist`, and `Playback queue`; existing unload, reload, failure cleanup, and ownership cases remain. All 26 SIL tests passed. |

**Artifacts:** 3/3 verified

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `modules/integration/panel_ui/src/media-panel.tsx` | `panel_static/bl-haos-media-panel.js` | Existing TypeScript/Vite build with temporary `--outDir`, followed by byte comparison | WIRED | `test_panel_bundle_matches_fresh_build` invokes `npm run build`, checks the one-file output set, and compares the fresh bytes with the tracked bundle. |
| `panel_static/bl-haos-media-panel.js` | Home Assistant static module URL and SIL assertions | `_PanelOwners._copy_bundle` and `StaticPathConfig` serve the package asset at `/api/bl_haos/catalog/bl-haos-media-panel.js` | WIRED | SIL reads the actual response body from the registered URL and exercises unload/reload and shared ownership. |

**Wiring:** 2/2 verified

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|--------------|--------|--------------------|--------|
| Generated panel bundle | Compiled `MediaPanel` module | `media-panel.tsx` through the configured Vite library build | Yes; fresh build output is compared byte-for-byte with the shipped module | FLOWING |
| Served module response | Static JS response body | Integration copies `PANEL_BUNDLE` to its served path and registers the static route | Yes; SIL response contains the package module and queue markers | FLOWING |

This verifies package bytes and route delivery, not actual browser rendering or live Home Assistant/provider/audio behavior.

### Threat Mitigations

| Threat | Required mitigation | Evidence | Status |
|--------|---------------------|----------|--------|
| T-28-01 Tampering | Review source changes first; isolate the fresh build, verify the expected output set, compare exact bytes, then refresh only as a distinct package update. | `28-REVIEW.md` records review of source, tests, and generated bundle with 0 Critical/Warning findings. The close-after-discard source regression passed; isolated parity passed. Fresh output differs from pre-refresh `HEAD`, demonstrating the old bundle would fail parity. | VERIFIED |
| T-28-02 Information disclosure | Preserve source guards against browser credential storage, provider resolution, direct network access, and authorization material; parity binds the package to that guarded source. | Package test retains assertions for `localStorage`, `sessionStorage`, `resolve_media`, `apiClient`, `fetch`, `Authorization`, and `Bearer ` exclusions. Exact parity and served-marker checks passed. | VERIFIED |
| T-28-03 Denial of service / destructive output cleanup | Use unique temporary output for parity; constrain the output set and confirm `panel_static` contains only the intended bundle before any intentional refresh. | Parity output uses pytest `tmp_path` and contains exactly the expected JS file; package-layout test confirms the package directory contains only that bundle. Verification did not run the normal package build or modify the bundle. | VERIFIED |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| Reviewed close-after-discard navigation transition | `npm --prefix modules/integration/panel_ui test -- -t "navigates through the Close link only after confirming discard"` | 1 passed | PASS |
| Panel source behavior suite | `npm --prefix modules/integration/panel_ui test` | 73 passed across 2 files | PASS |
| Package layout, markers, and fresh-build parity | `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 .venv/Scripts/python.exe -m pytest modules/integration/tests/test_package_layout.py -q` | 11 passed; parity did not skip | PASS |
| Home Assistant static route and lifecycle in WSL SIL | `BLHAOS_RUN_SIL=1 ... pytest tests/test_panel_registration.py -q` | 26 passed | PASS |
| Stale pre-refresh baseline comparison | Fresh Vite build to OS temp directory compared with `git show HEAD:<bundle>` | 279,980 fresh bytes vs 269,836 pre-refresh bytes | PASS; stale baseline detected |

Local build runtime observed during verification: Node `v24.19.0`, npm `11.17.0`. These are environment observations, not CI support pins.

### Probe Execution

Not applicable. The plan declares no phase probe, and this is a local package/SIL verification rather than a migration or CLI phase.

### Test Quality Audit

| Test File | Linked Requirement | Active | Skipped | Circular | Assertion Level | Verdict |
|-----------|-------------------|--------|---------|----------|-----------------|---------|
| Panel Vitest suite | PRD-01 | 73 | 0 in full run | No | Behavioral workflow assertions | PASS |
| `modules/integration/tests/test_package_layout.py` | PRD-01 | 11 | 0 in this run | No | Exact byte equality, output-set, marker, and source-safety values | PASS |
| `modules/integration/tests/test_panel_registration.py` | PRD-01 | 26 in WSL SIL | 0 in this run | No | Response values and multi-step lifecycle behavior | PASS |

No disabled test was the sole evidence for PRD-01. The parity check is intentionally conditional when Node/npm or panel build dependencies are absent; that guard did not trigger locally and Phase 29 owns CI provisioning. The registration module's platform guard was bypassed by running the supported WSL SIL command. No circular expected-value generation was found.

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| PRD-01 | 28-01 | Package serves a generated bundle from reviewed source and checks saved-playlist launch and queue UI | SATISFIED for this phase's local scope | Exact local build parity, package marker checks, and WSL SIL route/lifecycle passed. This report does not establish CI, live host, provider, playback, or actual HA-shell acceptance. |

No v1.0 PL requirement or v1.1 requirement other than PRD-01 is marked complete. `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`, and `.planning/STATE.md` were not updated by this verification.

### Decision Coverage

No trackable decisions in `28-CONTEXT.md`; the non-blocking decision-coverage gate returned `total: 0`, `honored: 0`, and no unhonored decisions.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| None | - | No unresolved debt markers, stubs, or disabled requirement tests found in the phase artifacts. | - | No impact |

### Deferred Items and Preserved Gates

These are outside Phase 28's local acceptance and remain open; they do not block this local package-parity result:

| Item | Addressed in | Boundary |
|------|--------------|----------|
| Select/provision Node/npm and panel dependencies so integration CI must run parity rather than skip it | Phase 29 | Local Node `v24.19.0` and npm `11.17.0` are observations only, not CI pins. |
| Authorized HAOS/provider/session cases and audible playback acceptance | Phase 31 | WSL SIL is not a live Home Assistant host, provider, session-expiry, or audio test. No such action was performed. |
| Actual HA-shell keyboard, focus, labeling, announcements, contrast, reduced-motion, and responsive acceptance | Phase 32 | Static bundle markers and SIL do not establish visual or accessibility behavior in the actual shell. |
| Production security closure, reconnect hardware soak, and release evidence/go-no-go | Phases 30, 33, and 34 | Their requirements and gates remain unchanged and pending. |

### Human Verification Required

None for Phase 28's local package and SIL acceptance. Actual HA-shell and audible production acceptance are explicitly deferred to Phases 31-32 and must not be inferred from these results.

### Gaps Summary

**No gaps found within Phase 28's local scope.** The reviewed source, generated package artifact, fresh isolated build, package assertions, and Home Assistant SIL route lifecycle agree. This is not a production acceptance or release-readiness verdict. CI runtime provisioning and all later security, live-host, accessibility, hardware, and release gates remain in force.

---

_Verified: 2026-10-28T05:51:45Z_  
_Verifier: the agent (gsd-verifier)_
