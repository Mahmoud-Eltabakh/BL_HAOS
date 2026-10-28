---
phase: 29-pr-safe-root-bridge-integration-ci
verified: 2026-10-28T07:24:03Z
status: human_needed
score: 6/8 must-haves verified
covered_files:
  - .github/workflows/tests.yml
  - .planning/phases/29-pr-safe-root-bridge-integration-ci/29-01-PLAN.md
  - .planning/phases/29-pr-safe-root-bridge-integration-ci/29-01-SUMMARY.md
  - modules/integration/tests/test_package_layout.py
covered_digest: "v3:sha256:4d8975e06cbf7133beac099d4e7555de8b815d37f10dea68d6c181856239f9fb"
behavior_unverified: 0
overrides_applied: 0
decision_coverage:
  honored: 0
  total: 0
  not_honored: []
deferred:
  - truth: "Production security threshold and reviewed closure evidence for T-24-15/T-24-16 are established."
    addressed_in: "Phase 30"
    evidence: "Roadmap Phase 30 success criteria cover high-threshold enforcement and closure evidence; PRD-03 remains pending."
  - truth: "Authorized HA/provider browsing, playback, and safe denial/unavailable/session-expiry acceptance is complete."
    addressed_in: "Phase 31"
    evidence: "Roadmap Phase 31 success criteria require separate authorization and live host/provider/playback evidence; PRD-04 and PRD-05 remain pending."
  - truth: "The packaged panel passes actual HA-shell accessibility and responsive acceptance."
    addressed_in: "Phase 32"
    evidence: "Roadmap Phase 32 success criteria require authorized actual-shell checks at 375, 768, and 1440 pixels; PRD-06 remains pending."
  - truth: "Authorized reconnect hardware soak demonstrates bounded recovery, pairing retention, and stable playback."
    addressed_in: "Phase 33"
    evidence: "Roadmap Phase 33 success criteria require a separately authorized hardware soak; PRD-07 remains pending."
  - truth: "Release candidate evidence, rollback rehearsal, and explicit go/no-go preparation are complete."
    addressed_in: "Phase 34"
    evidence: "Roadmap Phase 34 success criteria cover candidate evidence and rollback; PRD-08 remains pending and this phase does not authorize publication."
human_verification:
  - test: "Run the ordinary hosted pull_request checks for the currently reviewed Phase 29 change after a PR/check run is authorized. Confirm all required jobs pass on their declared runtimes, especially integration-unit on Node 22 with package parity executed rather than skipped; record the check-run result and rerun Phase 29 verification."
    expected: "The hosted pull_request workflow completes successfully, including Node 22 setup, locked npm install with lifecycle scripts disabled, preflight, and passing package-layout parity; no publishing job or release artifact is invoked."
    why_human: "No authorized hosted pull_request run exists. Local Node 24 and static workflow assertions cannot establish hosted Node 22 execution or the actual PR gate result. Current state forbids commit/push; resume only when a PR/check run is separately authorized."
---

# Phase 29: PR-Safe Root, Bridge & Integration CI Verification Report

**Phase Goal:** Contributors can validate root, bridge, and integration changes through passing pull-request gates without publishing release artifacts.
**Verified:** 2026-10-28T07:24:03Z
**Status:** human_needed
**Re-verification:** No — initial verification

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | The root CI gate passes on its declared runtime and required checks. | UNCERTAIN | Local declared Python-runtime evidence passes, but the authorized hosted pull_request result is absent; the integration Node 22 path has not run on GitHub Actions. See Human Verification. |
| 2 | Bridge and integration CI gates pass on their declared runtimes and required checks. | UNCERTAIN | Bridge Python 3.12.10 and integration Python 3.12.10 / SIL Python 3.14.4 evidence passes. The Node 22 hosted PR path remains unexecuted, so the complete declared CI gate is not established. |
| 3 | Pull-request validation can run without publishing add-on images, packages, or release artifacts. | VERIFIED | `.github/workflows/tests.yml` uses ordinary `pull_request`, grants only `contents: read`, has five independent `ubuntu-latest` jobs, and contains no publisher, write permission, secret interpolation, artifact upload, cache, or cross-job output path. The static contract test passed. |
| 4 | The root workflow wires bridge/integration client gates to Python 3.12 and pinned Home Assistant SIL to Python 3.14. | VERIFIED | The workflow sets Python 3.12 for bridge and integration L1 and Python 3.14 for `integration-sil`; the recorded local bridge/integration/SIL suites passed on Python 3.12.10 / 3.14.4. |
| 5 | Integration package-layout validation provisions Node 22, installs the existing panel lock with lifecycle scripts disabled, and fails before pytest if required tools are missing. | VERIFIED | Workflow uses `actions/setup-node@v5` with Node 22, `npm ci --prefix panel_ui --ignore-scripts`, and Node/npm/Vite/TypeScript preflight before pytest. Static workflow assertions passed. |
| 6 | Panel parity builds into a unique pytest temporary directory and leaves the tracked `panel_static` bundle unchanged. | VERIFIED | Test uses `tmp_path / "panel-build"`, compares fresh output byte-for-byte, and checks packaged bytes are unchanged. The parity test ran in the focused 12-test suite and passed. |
| 7 | The root pull-request workflow is read-only and cannot reach an add-on image, package, or release-artifact publisher. | VERIFIED | Workflow contract test checks allowed actions, permissions, checkout credential non-persistence, publisher markers, and absence of secret interpolation; all 12 package-layout tests passed. |
| 8 | Local exact-runtime evidence is distinguished from the hosted pull_request result, which remains deferred. | VERIFIED | `29-VALIDATION.md` and `29-01-SUMMARY.md` state the local runtime results and explicitly say hosted Node 22 PR execution was not run and is not proven by Node 24. |

**Score:** 6/8 truths verified (2 hosted-runtime truths await human verification)

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `.github/workflows/tests.yml` | Root-owned, non-publishing pull-request gates with mandatory integration panel parity prerequisites | VERIFIED | Exists and is substantive; canonical artifact verifier passed. Static workflow contract test passed. |
| `modules/integration/tests/test_package_layout.py` | Static workflow contract and package parity safety assertions | VERIFIED | Exists and is substantive; canonical artifact verifier passed. Local focused suite passed 12/12 with parity active. |

**Artifacts:** 2/2 verified.

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `.github/workflows/tests.yml` | `modules/integration/tests/test_package_layout.py` | `integration-unit` provisions Node 22 and locked panel dependencies before package-layout pytest | WIRED | Canonical key-link verifier found the expected workflow pattern; test asserts setup/install/preflight/pytest ordering. |
| `modules/integration/tests/test_package_layout.py` | `modules/integration/custom_components/bl_haos/panel_static/bl-haos-media-panel.js` | Fresh Vite output in `tmp_path` compared byte-for-byte without writing the packaged bundle | WIRED | Canonical verifier found the pattern; the focused package-layout suite executed parity successfully. |

**Wiring:** 2/2 verified.

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|---------------|--------|--------------------|--------|
| Panel parity assertion | Fresh compiled panel bytes | Reviewed panel source through the locked TypeScript/Vite build into pytest `tmp_path` | Yes; exact bytes compared with the tracked packaged bundle | FLOWING |
| Root workflow contract assertion | Parsed workflow sections and job steps | Checked-in `.github/workflows/tests.yml` | Yes; assertions inspect actual triggers, permissions, jobs, actions, and step ordering | FLOWING |

### Behavioral Spot-Checks

| Behavior | Command / evidence | Result | Status |
|----------|--------------------|--------|--------|
| Workflow contract and isolated package parity | `py -3.12 -m pytest tests/test_package_layout.py -q` from `modules/integration` | 12 passed in 4.35s; parity did not skip | PASS |
| Bridge L1 | Recorded in `29-VALIDATION.md` / `29-01-SUMMARY.md` | Python 3.12.10; 357 passed, 1 skipped | PASS |
| Integration client/package L1 | Recorded in `29-VALIDATION.md` / `29-01-SUMMARY.md` | Python 3.12.10; 89 passed, package parity active | PASS |
| Home Assistant integration SIL | Recorded in `29-VALIDATION.md` / `29-01-SUMMARY.md` | WSL Python 3.14.4; 95 passed | PASS |
| Bridge frontend unit/build/E2E | Recorded in `29-VALIDATION.md` / `29-01-SUMMARY.md` | Node 24.19.0 / npm 11.17.0; 39 tests, build, and 4 E2E passed; diagnostic only, not Node 22 evidence | PASS (diagnostic) |
| Hosted Node 22 pull_request gate | No authorized check run | Not run; no result to evaluate | HUMAN VERIFICATION |

### Probe Execution

Not applicable. No phase-declared probe or conventional `scripts/**/tests/probe-*.sh` probe was found.

### Test Quality Audit

| Test File | Linked Req | Active | Skipped | Circular | Assertion Level | Verdict |
|-----------|------------|--------|---------|----------|-----------------|---------|
| `modules/integration/tests/test_package_layout.py` | PRD-02 | 12 | 0 in focused run | No | Value-level workflow contract, exact bundle-byte equality, and unchanged packaged-byte assertion | PASS |

**Disabled tests on requirements:** 0. **Circular patterns detected:** 0. **Insufficient assertions:** 0 identified. The test contains a defensive `pytest.skip` when local Node/Vite prerequisites are absent; this is not a disabled test. The hosted workflow installs Node 22 and runs a fail-closed preflight before pytest, and the contract test enforces that ordering.

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| PRD-02 | 29-01 | Root, bridge, and integration CI gates pass on declared runtimes; PR validation is non-publishing | NEEDS HUMAN / PENDING | Local Python gates and static non-publishing contract pass, but the hosted Node 22 pull_request check has not run. Do not mark complete until the hosted gate passes. |

No other Phase 29 requirement is orphaned. PRD-03 through PRD-08 belong to later phases and remain pending; no requirement status was changed by this verification.

### Decision Coverage

No trackable decisions in `29-CONTEXT.md`; canonical decision coverage result: 0/0, none unhonored.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| None | - | No unresolved debt markers, stubs, or disabled requirement tests found. The local parity skip guard is protected by the CI preflight. | - | No blocker identified. |

### Deferred Items

| Item | Addressed In | Evidence |
|------|--------------|----------|
| Production security threshold and T-24-15/T-24-16 closure evidence (PRD-03) | Phase 30 | Roadmap Phase 30; requirement remains pending. |
| Authorized HA/provider browsing, playback, and denial/unavailable/session-expiry acceptance (PRD-04/05) | Phase 31 | Roadmap Phase 31; live actions require separate authorization and both requirements remain pending. |
| Actual HA-shell accessibility and responsive acceptance (PRD-06) | Phase 32 | Roadmap Phase 32; requirement remains pending. |
| Authorized reconnect hardware soak (PRD-07) | Phase 33 | Roadmap Phase 33; requirement remains pending. |
| Release evidence, rollback rehearsal, and go/no-go preparation (PRD-08) | Phase 34 | Roadmap Phase 34; requirement remains pending and no publication is authorized. |

These later security, live-host, accessibility, hardware, and release phases are explicitly out of Phase 29 scope. Their requirements are not complete and no live, host, playback, provider/session, hardware, publishing, or deployment action occurred.

### Human Verification Required

#### Hosted pull_request check on Node 22

**Test:** Once a PR/check run is separately authorized, run the ordinary hosted `pull_request` workflow for the currently reviewed Phase 29 change. Confirm the required jobs pass on declared runtimes, especially that `integration-unit` installs the existing lock with lifecycle scripts disabled, completes the Node 22 preflight, and runs package parity without skipping. Record the check-run result and rerun Phase 29 verification. Do not invoke the nested publisher. Current state forbids commit/push; resume only after authorization for a PR/check run.

**Expected:** The hosted pull_request workflow passes its required checks, including Node 22 integration package parity, without publishing add-on images, packages, or release artifacts.

**Why human:** Local Node 24 and static workflow assertions cannot establish hosted Node 22 execution or the actual pull-request check result.

### Gaps Summary

No implementation gap was found in the workflow contract, toolchain wiring, parity isolation, or local declared Python-runtime evidence. The phase is not yet fully verified: PRD-02 requires a passing hosted pull_request result on the configured Node 22 path, which was not run because commit/push is not authorized. The status is therefore `human_needed`, not `passed`; PRD-02 remains pending until that gate is authorized and passes.

---

_Verified: 2026-10-28T07:24:03Z_  
_Verifier: the agent (gsd-verifier)_
