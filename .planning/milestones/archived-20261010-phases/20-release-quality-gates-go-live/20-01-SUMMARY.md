---
phase: 20-release-quality-gates-go-live
plan: 01
subsystem: release-quality
tags: [release-gates, regression, ci, security, compatibility, sil]
dependency_graph:
  requires: [Phase 16 SIL runner, Phase 17 runtime tests, Phase 18 security gates, Phase 19 diagnostics contracts]
  provides: [release checklist, regression matrix, CI release evidence gate, support policy]
  affects: [modules/bridge builder workflow, release operations]
tech_stack:
  added: []
  patterns: [artifact-aware gates, fail-closed audits, sequential SIL evidence]
key_files:
  created:
    - tests/integration/RELEASE-GATES.md
    - tests/integration/REGRESSION-MATRIX.md
    - tests/integration/tests/test_release_contract.py
    - .planning/phases/20-release-quality-gates-go-live/20-01-SUMMARY.md
  modified:
    - modules/bridge/.github/workflows/builder.yaml
    - modules/bridge/README.md
decisions:
  - Keep the existing sequential bridge-before-integration SIL runner as the only SIL runner.
  - Make the release evidence job a prerequisite of architecture-specific image publishing.
  - Treat missing dependencies, reports, Docker/KVM, credentials, and hardware as explicit non-passing states.
  - Keep Sendspin and Music Assistant as operational references only, not runtime dependencies.
metrics:
  duration: not recorded
  completed_date: 2026-09-23
  tasks: 3
  commits: 0
  plan_head_before: not committed by request
actuals:
  tokens: 7766
  tasks: 3
  commits: 0
status: complete
---

# Phase 20 Plan 01: Release Quality Gates and Go-Live Summary

Enforceable BL-HAOS release checklist, regression matrix, compatibility/security policy, and CI evidence gate for stable and preview releases.

## Accomplishments

- Added `RELEASE-GATES.md` with exact commands, working directories, prerequisites, duration classes, owners, blocking outcomes, required SIL artifacts, redaction/retention rules, support policy, security disclosure, dependency exceptions, and REL-01 through REL-04 / OPS-03 traceability.
- Added `REGRESSION-MATRIX.md` covering startup, connect, disconnect, reconnect exhaustion/recovery, playback failure, native authentication success/failure, degraded dependencies, recovery actions, deterministic demo scenarios, architecture parity, compatibility, and secret-safe evidence.
- Added static contract tests that detect missing commands, reports, policies, architecture declarations, audit thresholds, workflow ordering, and permissive fallbacks.
- Extended the bridge builder workflow with a blocking release-gates job that runs the canonical SIL build/run, requires all five report artifacts, asserts `config.yaml`/`build.yaml`/workflow architecture parity, uploads retained evidence, and gates the multi-architecture publish job.
- Linked the new policy documents from the bridge README without changing runtime code or adding dependencies.

## Verification

- `python -m pytest tests/integration/tests/test_release_contract.py tests/integration/tests/test_orchestration.py -q` -> **11 passed**.
- `docker compose -f tests/integration/docker-compose.yml build test-runner` -> **passed**.
- `docker compose -f tests/integration/docker-compose.yml run --rm test-runner` -> **passed**; `bridge-junit.xml`, `integration-junit.xml`, `sil-junit.xml`, `coverage.xml`, and `coverage-html/` were present.
- `git diff --check` -> **passed**.
- `python -m pytest tests/ -q` -> **blocked during collection** because `playwright` is unavailable for `tests/integration/test_addon_e2e.py`; this is an environment/dependency blocker outside the plan files.
- Docker was available and running; WSL2 exposed `/dev/kvm`. Multi-architecture publishing was not run locally because it is the GitHub Actions release workflow and requires registry credentials.

## Deviations from Plan

None. The requested release policy, tests, workflow enforcement, and README discoverability were implemented without runtime production changes. No commit was created; the parent workflow owns commit/push.

## Blockers

- Full repository verification remains blocked by the missing `playwright` Python package during test collection in `tests/integration/test_addon_e2e.py`.
- Multi-architecture builder publishing requires the GitHub Actions runner and registry authentication; the workflow now enforces all three declared architectures.

## Self-Check: PASSED

Created files exist, the focused verification passed, the canonical SIL evidence set was generated successfully, and no commit was made.
