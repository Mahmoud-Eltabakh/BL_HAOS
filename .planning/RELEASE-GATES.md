# BL-HAOS Release Gate Contract

This is the blocking release-candidate contract for BL-HAOS. A release is
green only when the command for every required gate exits successfully and its
declared evidence is present, valid, redacted, and retained. A successful
command without its evidence is not a passing release.

## Release Path

Run these gates in order from the repository root unless a working directory
is shown. The first four gates are deterministic repository or container
checks. `DEEP-HAOS` and `LIVE-HARDWARE` are environment-qualified and remain
outstanding when their required environment is unavailable.

| Gate | Exact command and working directory | Prerequisites / duration | Required evidence | Blocking outcome | Owner |
|---|---|---|---|---|---|
| `PREFLIGHT` | `python -m pytest tests/integration/tests/test_release_contract.py -q` (repo root) | Python and pytest; fast | Test output | Test, import, or missing-file failure | Release engineer |
| `REGRESSION` | `python -m pytest tests/ -q` (repo root) | Root test dependencies; fast | JUnit or CI test result | Any nonzero exit or missing dependency | QA owner |
| `SIL-CONTRACT` | `python -m pytest tests/integration/tests/test_orchestration.py -q` (repo root) | Python and pytest; fast | Contract test result | Contract drift or missing input | Integration owner |
| `SIL-CONTAINER` | `docker compose -f tests/integration/docker-compose.yml build test-runner` then `docker compose -f tests/integration/docker-compose.yml run --rm test-runner` (repo root) | Docker, network, declared image dependencies; medium | `bridge-junit.xml`, `integration-junit.xml`, `sil-junit.xml`, `coverage.xml`, `coverage-html/` | Suite, merge, coverage, dependency, Docker, or report failure | CI owner |
| `DEPENDENCY-AUDIT` | `python3 -m pip install --disable-pip-version-check pip-audit==2.7.3`; `python3 -m pip_audit --strict --requirement backend/requirements.txt`; `npm --prefix web_ui ci --ignore-scripts`; `npm --prefix web_ui audit --audit-level=high`; `trivy fs --severity HIGH,CRITICAL --exit-code 1 modules/bridge` (working directory `modules/bridge`) | Python, npm, Trivy; medium | Pinned tool output and audit logs | Missing tool, high/critical finding, or permissive fallback | Security owner |
| `ARCH-BUILD` | `docker buildx`/Home Assistant Builder invocation for `aarch64`, `amd64`, and `armv7` (workflow) | Docker Buildx, registry auth, QEMU where required; slow | One successful image/build result per declared architecture | Any missing architecture or failed build/publish | Release engineer |
| `ARTIFACT-COMPAT` | Workflow manifest/matrix assertions and retained evidence checks | `config.yaml`, `build.yaml`, workflow, and reports available; fast | Architecture parity and all named reports | Mismatch, absent artifact, or unredacted evidence | Release engineer |
| `DEMO-OFFLINE` | `python -m pytest modules/bridge/tests/test_demo_mode.py -q` (repo root) | Root Python dependencies; fast | Test result covering deterministic offline demo scenarios | Demo failure or missing deterministic scenario | QA owner |
| `DEEP-HAOS` | `docker compose -f tests/integration/docker-compose.yml up --abort-on-container-exit --exit-code-from test-runner test-runner` (repo root) | Linux, Docker, `/dev/kvm`, HAOS image/config, network; slow | SIL reports plus redacted HAOS/Compose logs | KVM, boot, image, service, or network failure; unavailable is not pass | HAOS environment owner |
| `LIVE-HARDWARE` | `python test_live_pi.py` and/or `python test_full_pi_workflow.py` (repo root) | Provisioned HAOS, adapter, speaker, `websockets`, `HA_URL`, `HA_WS`, `HA_TOKEN`; manual/slow | Redacted operator evidence and live assertions | Failure or unavailable credentials/hardware; never a SIL substitute | Hardware owner |

The canonical SIL runner is
`tests/integration/scripts/run-sil-tests.sh`. It preflights dependencies,
runs the bridge suite before the Home Assistant integration suite, merges both
JUnit files, writes XML and HTML coverage, and returns the aggregate status.
There is one runner and no parallel SIL lane.

## Required SIL Evidence

The following paths are required under `tests/integration/reports/` after every
`SIL-CONTAINER` or `DEEP-HAOS` run:

- `bridge-junit.xml`
- `integration-junit.xml`
- `sil-junit.xml`
- `coverage.xml`
- `coverage-html/`

Reports must contain valid XML or HTML output from the current candidate. A
missing, empty, stale, or malformed report is a report-generation failure even
when the test process returned zero. Retained evidence must exclude access
tokens, raw WebSocket frames, private URLs, full Bluetooth addresses, PINs,
and other secrets or identifying credentials. Upload only redacted reports,
logs, and summaries; retain detailed local evidence only under the approved CI
retention period.

The runner treats missing test dependencies as a dependency failure. Missing JUnit or coverage output is a report-generation failure. These states are
never converted to an unqualified pass.

## Failure and Availability Semantics

| Condition | Classification | Release meaning |
|---|---|---|
| Test assertion, audit finding, build failure, or invalid policy | `failure` | Blocking; fix and rerun |
| Missing pytest, optional Home Assistant package, npm, pip-audit, Trivy, Docker, or report | `dependency-failure`, `infrastructure-failure`, or `report-generation-failure` | Non-passing; a skip or host-only result cannot satisfy the gate |
| Windows host cannot run Docker/KVM | `environment-unavailable` | Record the unavailable gate and run it on a capable Linux CI/environment; do not claim release pass |
| Missing HAOS credentials, adapter, speaker, or reachable hardware | `hardware-unavailable` | `LIVE-HARDWARE` remains outstanding; deterministic SIL is unaffected and is not replaced |
| Missing or unredacted evidence | `evidence-failure` | Blocking; redact and rerun |

## Compatibility and Support Policy

- **Stable:** versioned releases supported on HAOS 12 / Debian Bookworm base,
  Home Assistant Core 2024.x or later, and all declared architectures:
  `aarch64`, `amd64`, and `armv7`. Stable status requires all blocking gates
  and release evidence.
- **Preview:** prerelease builds may expose experimental behavior and are
  supported for reproducible reports only. Preview builds use the same pinned
  dependencies, architecture matrix, security thresholds, and redaction rules
  as stable; promotion requires the full stable gate path.
- **Compatibility:** the add-on manifest image template, `config.yaml`,
  `build.yaml`, builder matrix, and published image tags must agree. The
  native Home Assistant integration is the product boundary; its entity and
  transport contract must remain compatible with the add-on version. A
  breaking contract requires a documented version transition and migration
  evidence before promotion.
- **Upgrade:** preserve configuration keys and existing media-player entity
  behavior where possible. Any incompatible upgrade requires an explicit
  release note, rollback guidance, and a passing upgrade/rollback check.
- **Operational reference:** Sendspin may inform synchronization and operational
  checks, but Sendspin and Music Assistant are not BL-HAOS dependencies.

## Security and Dependency Exceptions

Report vulnerabilities privately to the repository maintainers with affected
version, reproduction or impact, and a proposed disclosure timeline. Do not
publish credentials, raw runtime frames, or unredacted live evidence in an
issue, artifact, or release note.

`pip-audit`, `npm audit --audit-level=high`, and Trivy fail closed on high and
critical findings. high and critical findings are always blocking. An exception is allowed only when a named security owner
records the affected dependency, severity, rationale, compensating control,
tracking issue, and expiry date in the release record. Expired or ownerless
exceptions fail the release. There is no default bypass, `continue-on-error`,
or `|| true` fallback for these checks.

## Requirement Traceability

| Requirement | Owning gates | Verification artifact |
|---|---|---|
| `REL-01` | `REGRESSION`, `SIL-CONTRACT`, `SIL-CONTAINER` | Regression result and five SIL reports |
| `REL-02` | `SIL-CONTRACT`, `SIL-CONTAINER`, `DEEP-HAOS` | Sequential runner result, merged JUnit, coverage |
| `REL-03` | `REGRESSION`, `DEMO-OFFLINE`, `LIVE-HARDWARE` | Regression matrix and redacted scenario evidence |
| `REL-04` | `DEPENDENCY-AUDIT`, `ARCH-BUILD`, `ARTIFACT-COMPAT` | Audit logs, three architecture builds, retained reports |
| `OPS-03` | `DEMO-OFFLINE` | Deterministic offline demo test result and scenario evidence |
