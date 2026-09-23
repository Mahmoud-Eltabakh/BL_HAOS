# CI Gate Contract

This document defines the quality gates for BL-HAOS validation. It is the
invocation and evidence contract for current or future CI jobs; it does not add
a workflow. This repository currently has no root GitHub Actions test workflow.
The existing `modules/bridge/.github/workflows/builder.yaml`
publishes add-on images and is outside this test-gate scope.

## Gate Policy

| Gate ID | Command / boundary | Blocking policy | Required evidence |
|---|---|---|---|
| `REGRESSION` | `pytest tests/ -q` | Fast, blocking pull-request gate | Successful command exit and test output |
| `SIL-CONTRACT` | `pytest tests/integration/tests/test_orchestration.py -q` | Fast, blocking pull-request gate | Successful command exit and static contract test output |
| `SIL-CONTAINER` | `docker compose -f tests/integration/docker-compose.yml build test-runner` then `docker compose -f tests/integration/docker-compose.yml run --rm test-runner` | Required, blocking pull-request and release integration gate | Successful command exit plus `bridge-junit.xml`, `integration-junit.xml`, `sil-junit.xml`, `coverage.xml`, and `coverage-html/` |
| `DEEP-HAOS` | `docker compose -f tests/integration/docker-compose.yml up --abort-on-container-exit --exit-code-from test-runner test-runner` | Linux/KVM-capable release or scheduled gate; not a local Windows prerequisite | Successful command exit, SIL reports, and retained HAOS/Compose logs |
| `LIVE-HARDWARE` | `python test_live_pi.py` or `python test_full_pi_workflow.py` with provisioned environment | Manual release evidence only; never silently substitutes for deterministic CI | Redacted operator evidence and successful live checks |

## Passing Means Passing

A gate passes only when its command exits successfully **and** every artifact
required by the gate exists. A green-looking partial log is not evidence of a
passing gate.

For `SIL-CONTAINER`, the runner must preflight `pytest`, `pytest-cov`, and
`pytest-homeassistant-custom-component`, run the bridge suite before the
integration suite, merge their JUnit output, and generate XML and HTML
coverage. A suite failure, merge failure, coverage failure, missing report, or
aggregate nonzero runner status is blocking. The runner's `sil-junit.xml`,
`coverage.xml`, and `coverage-html/` are required even when a CI system also
uploads the two per-suite JUnit files.

## Non-Passing Environment Outcomes

These outcomes must remain visible and actionable; they are never converted to
an unqualified pass. The phrase missing test dependencies identifies a
dependency failure, not a successful skip:

- Missing test dependencies or executables: **dependency failure**. The job
  owner installs or repairs the declared environment.
- Docker unavailable, image build failure, KVM unavailable, HAOS boot failure,
  or service/network failure: **infrastructure failure**. The owning CI or
  environment maintainer repairs the runner; a host-only test pass does not
  waive `SIL-CONTAINER`.
- Missing JUnit or coverage output after a command exits: **report-generation
  failure**. The gate is non-passing until the artifact contract is met.
- Missing live credentials, Raspberry Pi, adapter, speaker, or reachable HAOS:
  **environment/hardware unavailable**. Manual evidence remains outstanding;
  it is not a deterministic SIL result.

## Ownership and Boundaries

The repository regression and `SIL-CONTRACT` gates cover code and contract
drift without Docker, HAOS, Bluetooth hardware, credentials, or optional Home
Assistant packages. `SIL-CONTAINER` is the authoritative deterministic SIL
gate and uses the existing Phase 16 image and Compose stack (D-01).

The policy preserves sequential execution and aggregate failure propagation
(D-02), explicit dependency preflight (D-03), required report artifacts
(D-04), and the prohibition on production, SIL assertion, provisioning, mock,
or live-workflow changes in this plan (D-05). Together with `SIL-03`, these
rules define the expected CI behavior without introducing a second runner or a
new GitHub Actions workflow.

See [SMOKE-MATRIX.md](SMOKE-MATRIX.md) for the complete lane matrix and exact
operator commands.