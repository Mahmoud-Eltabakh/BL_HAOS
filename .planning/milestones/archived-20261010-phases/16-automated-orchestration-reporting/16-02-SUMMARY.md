---
phase: 16-automated-orchestration-reporting
plan: 02
subsystem: validation-contract
status: complete
tags: [smoke-matrix, ci-gates, sil, documentation, static-contract-tests]
dependency_graph:
  requires: [16-01 sequential SIL runner and reporting]
  provides: [canonical smoke matrix, CI gate contract, README testing entry point, documentation drift tests]
  affects: [local validation, future CI invocation, release evidence]
tech_stack:
  added: []
  patterns: [artifact-aware gates, environment-qualified validation lanes, text-only contract tests]
key_files:
  created:
    - tests/integration/SMOKE-MATRIX.md
    - tests/integration/CI-GATES.md
    - .planning/phases/16-automated-orchestration-reporting/16-02-SUMMARY.md
  modified:
    - README.md
    - tests/integration/tests/test_orchestration.py
decisions:
  - Treat the existing Docker Compose SIL runner as the authoritative deterministic CI evidence path.
  - Require successful exit plus per-suite JUnit, merged JUnit, XML coverage, and HTML coverage artifacts for SIL-CONTAINER.
  - Keep deep HAOS and live Raspberry Pi/Bluetooth validation environment-qualified and never substitute them for deterministic SIL.
metrics:
  duration: approximately 45 minutes
  completed: 2026-09-23
  commits: 0
  plan_head_before: not recorded (user requested no commits)
actuals:
  tokens: 8200
  tasks: 3
  commits: 0
---

# Phase 16 Plan 02: Canonical smoke matrix and CI gate contract

The project now has one documented validation matrix, an artifact-aware CI gate policy, and static tests that prevent documentation from drifting away from the Phase 16 runner.

## Delivered

- Added `tests/integration/SMOKE-MATRIX.md` covering repository regression, static orchestration, container SIL build/run, deep HAOS/KVM orchestration, and live Raspberry Pi/Bluetooth validation.
- Documented exact commands, prerequisites, duration classes, report paths, audience/blocking policy, and distinctions between test, dependency, infrastructure, report, and hardware-unavailable outcomes.
- Added `tests/integration/CI-GATES.md` with stable `REGRESSION`, `SIL-CONTRACT`, `SIL-CONTAINER`, `DEEP-HAOS`, and `LIVE-HARDWARE` gate identifiers.
- Made successful exit plus required JUnit and coverage reports a condition of passing the deterministic SIL gate.
- Documented that there is no root GitHub Actions test workflow and that the existing bridge image-publisher workflow is outside this test-gate contract.
- Linked both canonical documents from the root README Testing & Verification section.
- Extended the dependency-free orchestration contract tests to assert commands, reports, gate identifiers, environment boundaries, decision references, and README discoverability.

## Validation

- `python -m pytest tests/integration/tests/test_orchestration.py -q`: **5 passed**.
- `git diff --check`: **passed**; only CRLF-to-LF normalization warnings were reported.
- `python -m pytest tests/ -q`: **blocked during collection** because the active interpreter lacks `playwright`, required by `tests/integration/test_addon_e2e.py`; no repository tests ran.
- `pytest tests/integration/tests/test_orchestration.py -q`: **blocked before collection** by an incompatible pytest wrapper (`ImportError: cannot import name '_console_main' from '_pytest.config'`). The module invocation is the validated equivalent.
- `docker compose -f tests/integration/docker-compose.yml build test-runner`: **not confirmed**; the build remained active beyond the 120-second execution window. The container run was not started by the validation wrapper, and no report artifacts were produced.
- Live Raspberry Pi/Bluetooth validation: **not run**; this environment does not provide the required provisioned HAOS host, credentials, adapter, or speaker.

## Deviations from Plan

None in implementation scope. Validation limitations were recorded honestly because the environment lacks the optional host dependency and the Docker build did not complete within the available execution window.

## Known Stubs

None in the implementation files. The unrun Docker SIL verification is an environment limitation, not a stub.

## Unrun Verification

The authoritative Docker build/run and deep HAOS lane remain unconfirmed. The build process was still active at inspection time; it was not killed. Per the matrix and CI policy, this is a non-passing/unavailable validation outcome until rerun to completion and the required reports are checked.

## Self-Check: PASSED

- Summary file created at the planned path.
- Focused static contract suite passed with 5 tests.
- README and both canonical policy documents contain the required links and contracts.
- No commits or pushes were made.
