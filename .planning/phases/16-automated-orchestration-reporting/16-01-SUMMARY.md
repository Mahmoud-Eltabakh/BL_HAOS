---
phase: 16-automated-orchestration-reporting
plan: 01
subsystem: test-orchestration
status: complete
tags: [docker-compose, pytest, pytest-cov, junit, coverage, sil]
dependency_graph:
  requires: [Phase 14 bridge SIL suite, Phase 15 Home Assistant integration SIL suite]
  provides: [sequential SIL runner, unified JUnit and coverage reports, orchestration contract tests]
  affects: [tests/integration Docker runner]
tech_stack:
  added: [pytest-cov==2.12.1]
  patterns: [explicit dependency preflight, continue-after-suite-failure, standard-library JUnit merge]
key_files:
  created:
    - tests/integration/scripts/run-sil-tests.sh
    - tests/integration/tests/test_orchestration.py
  modified:
    - tests/integration/Dockerfile.test
    - tests/integration/docker-compose.yml
    - tests/integration/requirements-test.txt
decisions:
  - Invoke the bind-mounted POSIX runner through sh for Windows-host portability.
  - Pin pytest-cov to 2.12.1 because the verified Home Assistant SIL harness requires that version.
metrics:
  duration: approximately 30 minutes
  completed: 2026-09-23
  commits: 0
  plan_head_before: not recorded (user requested no commits)
actuals:
  tokens: 5600
  tasks: 3
  commits: 0
---

# Phase 16 Plan 01: Automated SIL orchestration and reporting

The compose test runner now executes the bridge and Home Assistant SIL suites sequentially, preserves suite failures, and writes host-visible unified JUnit and coverage evidence.

## Delivered

- Added `pytest-cov==2.12.1` to the shared test image requirements.
- Added `build-essential` to the test image for transitive native C-extension builds.
- Replaced the idle compose command with the report-mounted SIL runner.
- Added explicit preflight checks for pytest, coverage, pytest-cov, and the Home Assistant harness.
- Added bridge-before-integration pytest execution with separate JUnit files, aggregate exit status, and standard-library JUnit merging.
- Added terminal, XML, and HTML coverage generation for the bridge backend and bundled integration source roots.
- Added dependency-free static tests covering compose wiring, suite ordering, report outputs, failure propagation, and image requirements.

## Validation

- `python -m pytest tests/integration/tests/test_orchestration.py -q`: 3 passed.
- `git diff --check`: passed; only existing CRLF/LF warnings were reported.
- `docker compose -f tests/integration/docker-compose.yml config`: passed; Docker emitted the existing obsolete `version` warning.
- Docker image build/run was not completed within the available execution window. The initial build exposed a resolver conflict between the unpinned coverage dependency and the Home Assistant harness; the requirements now pin the harness-compatible `pytest-cov==2.12.1` and require a subsequent build/run confirmation.

## Deviations from Plan

### Auto-fixed Issues

**1. Rule 3 - Blocking dependency resolution**
- **Found during:** Task 1 container build.
- **Issue:** The unpinned `pytest-cov` requirement conflicted with the verified Home Assistant harness, which requires `pytest-cov==2.12.1`.
- **Fix:** Pinned the test-only coverage dependency to `2.12.1`.
- **Files modified:** `tests/integration/requirements-test.txt`

**2. Rule 3 - Windows bind-mount portability**
- **Found during:** Compose wiring review.
- **Issue:** A bind-mounted shell file may not retain executable mode bits on Windows hosts.
- **Fix:** Invoke the runner through `sh` while keeping the POSIX script and shebang.
- **Files modified:** `tests/integration/docker-compose.yml`, `tests/integration/tests/test_orchestration.py`

**3. Rule 3 - Blocking native dependency build**
- **Found during:** Task 1 container build.
- **Issue:** The shared image lacked compilers needed to build `lru-dict` and `ciso8601`.
- **Fix:** Added the standard `build-essential` package to the test-only image.
- **Files modified:** `tests/integration/Dockerfile.test`, `tests/integration/tests/test_orchestration.py`

## Known Stubs

None.

## Unrun Verification

The Docker build and container runner remain unconfirmed because the build exceeded the available execution window after adding native build tooling. The host interpreter is not authoritative for the Phase 15 suite because its optional Home Assistant harness is unavailable. No mounted report artifacts were produced.

## Self-Check: PASSED

- Summary file created at the planned path.
- Focused orchestration contract tests passed.
- Compose configuration parsed successfully.
- No commits or pushes were made.