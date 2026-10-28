---
phase: 29-pr-safe-root-bridge-integration-ci
plan: 01
subsystem: ci
tags: [github-actions, pytest, npm, vite, security]
requires:
  - phase: 28
    provides: Package parity test and generated panel bundle used by integration CI.
provides:
  - Root integration CI provisions Node 22 and installs the existing panel lock with lifecycle scripts disabled before pytest.
  - CI preflight requires Node, npm, Vite, and TypeScript so panel parity cannot silently skip in the hosted job.
  - Static workflow contract checks enforce read-only PR permissions, isolated jobs, checkout credential non-persistence, and no publisher path.
affects: [phase-30-security, phase-34-release]
tech-stack:
  added: []
  patterns:
    - Fail-closed CI preflight before test collection.
    - Root-owned, non-publishing validation kept separate from nested module publishers.
key-files:
  created: []
  modified:
    - .github/workflows/tests.yml
    - modules/integration/tests/test_package_layout.py
key-decisions:
  - "Use Node 22 via the existing setup-node action and keep Python 3.12 L1 / Python 3.14 SIL runtimes unchanged."
  - "Disable persisted checkout credentials in all five root jobs and do not grant publication permissions."
  - "Retain all nine screened package versions; install the existing lock with lifecycle scripts disabled and make no manifest or lockfile change."
  - "Do not infer causes for protected historical L1 failures or substitute local Node 24 for hosted Node 22 evidence."
patterns-established:
  - "CI preflights required parity tools before pytest so a defensive local skip cannot produce a green hosted gate."
  - "Static workflow contract tests constrain event, permissions, jobs, actions, secrets, publisher paths, and step ordering."
requirements-completed: []
coverage:
  - id: D1
    description: Root CI provisions and verifies the panel parity toolchain with a non-publishing workflow contract.
    requirement: PRD-02
    verification:
      - kind: unit
        ref: modules/integration/tests/test_package_layout.py::test_root_ci_requires_panel_parity_without_publication
        status: pass
      - kind: unit
        ref: modules/integration/tests/test_package_layout.py::test_panel_bundle_matches_fresh_build
        status: pass
      - kind: integration
        ref: Python 3.12 integration client/package suite; 89 passed
        status: pass
    human_judgment: true
    rationale: A hosted pull_request run on Node 22 cannot be observed without an authorized commit/push; local Node 24 and static workflow assertions do not prove hosted execution.
completed: 2026-10-28
status: complete
---

# Phase 29: PR-Safe Root, Bridge & Integration CI Summary

**Root pull-request CI now provisions the locked panel build toolchain and enforces a read-only, non-publishing contract; hosted Node 22 execution remains unverified.**

## Accomplishments

- Added Node 22 setup, `npm ci --prefix panel_ui --ignore-scripts`, and a fail-closed Node/npm/Vite/TypeScript preflight to the existing root `integration-unit` job.
- Added static workflow assertions for the trigger/permission/job/action allowlists, independent runners, no shared cache/artifact wiring, no persisted checkout credentials, no publisher/secret path, and setup/install/preflight/pytest ordering.
- Ran the declared Python 3.12 bridge and integration L1 gates, Python 3.14.4 Home Assistant SIL, and available bridge frontend unit/build/E2E checks.
- Reviewed the nine existing package-legitimacy flags. Their locked versions matched the registry, sources were canonical, adoption was high, and no relevant direct install scripts were identified. Versions and lockfiles remain unchanged.
- Standard-depth code review completed with 0 Critical and 0 Warning findings.

## Verification

- Bridge L1: Python 3.12.10, 357 passed, 1 skipped, 1 non-fatal deprecation warning.
- Integration L1: Python 3.12.10, 89 passed; package parity ran without skipping. `voluptuous` was exposed from a temporary target using the CI-declared test dependency, without changing project dependency files.
- Integration SIL: Python 3.14.4, 95 passed.
- Bridge frontend: Node 24.19.0 / npm 11.17.0; 39 Vitest passed, production build passed, 4 Playwright E2E passed. One non-fatal Windows connection-reset message occurred during E2E.
- Root workflow static contract: passed as part of the 12-test package-layout suite.
- Hosted pull-request result on the configured Node 22 runner: not run. Changes remain uncommitted because project state forbids commit/push; do not treat local Node 24 results as Node 22 evidence.

## Files Created/Modified

- `.github/workflows/tests.yml` - Node 22 panel setup/install/preflight and non-publishing root CI.
- `modules/integration/tests/test_package_layout.py` - Static workflow contract, checkout-token controls, and isolated bundle-parity invariants.
- `.planning/phases/29-pr-safe-root-bridge-integration-ci/29-CONTEXT.md` - Infrastructure constraints and CI conventions.
- `.planning/phases/29-pr-safe-root-bridge-integration-ci/29-RESEARCH.md` - Workflow ownership, package review, runtimes, and research dispositions.
- `.planning/phases/29-pr-safe-root-bridge-integration-ci/29-PATTERNS.md` - Existing workflow and test analogs.
- `.planning/phases/29-pr-safe-root-bridge-integration-ci/29-VALIDATION.md` - Local gate evidence and deferred hosted PR check.
- `.planning/phases/29-pr-safe-root-bridge-integration-ci/29-REVIEW.md` - Clean standard-depth source review.

## Lock Review

The nine heuristic `SUS: too-new` packages remain at their existing locked/registry versions: `lucide-react` 0.344.0, `react` 18.2.0, `react-dom` 18.2.0, `@playwright/test` 1.63.0, `@testing-library/user-event` 14.6.7, `@vitejs/plugin-react` 4.7.0, `jsdom` 25.0.1, `vite` 7.3.7, and `vitest` 5.0.4. No package or lockfile changes were made.

## Issues and Deferred Verification

- Historical protected CI failures remain unexplained; the public annotations exposed only exit codes, and no new hosted run was authorized.
- A hosted `pull_request` check on Node 22 is still required before PRD-02 can be marked complete. This summary records local and static evidence only.
- No publisher workflow, package/image upload, commit, push, deployment, host change, Core restart, playback, provider/session manipulation, or hardware test was performed.

---
*Phase: 29-pr-safe-root-bridge-integration-ci*
*Completed local plan execution: 2026-10-28*