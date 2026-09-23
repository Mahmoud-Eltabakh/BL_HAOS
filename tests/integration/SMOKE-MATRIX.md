# BL-HAOS Smoke Matrix

This is the canonical validation matrix for BL-HAOS. The Phase 16 container SIL
lane is the deterministic CI evidence path; deep HAOS and live Bluetooth lanes
are environment-qualified checks and must not be treated as substitutes for it.

The matrix preserves the Phase 16 decisions D-01 through D-05 and satisfies
SIL-03: the bridge SIL suite runs before the Home Assistant integration SIL
suite, both results contribute to one aggregate exit status, and the runner
publishes per-suite, merged JUnit, and coverage evidence.

## Lane Summary

| Lane | Exact command | Scope and prerequisites | Duration | Evidence | Audience / blocking | Status semantics |
|---|---|---|---|---|---|---|
| Repository regression | `pytest tests/ -q` | Root Python environment and test dependencies. No Docker, HAOS, Bluetooth hardware, or live credentials. | Fast | Pytest terminal output | Pull request blocking | A nonzero exit is a test failure. Missing imports or executables are a non-passing dependency failure. |
| Orchestration contract | `pytest tests/integration/tests/test_orchestration.py -q` | Root Python environment only. The test reads compose, Dockerfile, requirements, runner, and documentation; it does not import optional HA packages or launch services. | Fast | Pytest terminal output | Pull request blocking | A nonzero exit is a contract/test failure. Missing files are a non-passing repository/configuration failure. |
| Container SIL build | `docker compose -f tests/integration/docker-compose.yml build test-runner` | Docker Engine/Desktop and network access for the declared base image and package installation. No HAOS VM, KVM, Bluetooth hardware, or live credentials. | Medium | Build log; subsequent mounted reports | Pull request blocking as part of SIL-CONTAINER | A failed build is an infrastructure/dependency failure and is non-passing. A host-only pass does not replace this check. |
| Container SIL run | `docker compose -f tests/integration/docker-compose.yml run --rm test-runner` | Successful image build and Docker Compose. The runner preflights `pytest`, `pytest-cov`, and `pytest-homeassistant-custom-component`. | Medium | `/reports/bridge-junit.xml`, `/reports/integration-junit.xml`, `/reports/sil-junit.xml`, `/reports/coverage.xml`, `/reports/coverage-html/` | Pull request and release blocking as the authoritative SIL lane | The command must exit zero and every required report must exist. Suite, merge, coverage, missing-dependency, or report-generation failures are non-passing. Bridge runs before integration and failures cannot be masked. |
| Deep HAOS orchestration | `docker compose -f tests/integration/docker-compose.yml up --abort-on-container-exit --exit-code-from test-runner test-runner` | Linux host with Docker, `/dev/kvm`, sufficient RAM/disk/network, the HAOS image boot path, and the provisioned `tests/integration/config_usb/config.img`. | Slow | The same `/reports/` SIL and coverage artifacts, plus compose/HAOS logs | Release or scheduled gate; not a Windows/local PR requirement | KVM, image, boot, config, service, or network failures are infrastructure failures and non-passing. HAOS unavailability is not a SIL pass. |
| Live Raspberry Pi / Bluetooth | `python test_live_pi.py` or `python test_full_pi_workflow.py` | Provisioned HAOS, running add-on and integration, Bluetooth adapter/speaker, Python `websockets`, and environment variables `HA_URL`, `HA_WS`, and `HA_TOKEN`. Use a token through the environment only; do not commit it. | Slow / manual | Operator output and separately retained redacted evidence | Manual release evidence; not a deterministic CI substitute | A failed assertion/request is a live test failure. Missing credentials, host, packages, or hardware is hardware/environment unavailable and non-passing until explicitly rerun in a capable environment. |

## Authoritative SIL Sequence

Run the build and run as two commands from the repository root:

```text
docker compose -f tests/integration/docker-compose.yml build test-runner
docker compose -f tests/integration/docker-compose.yml run --rm test-runner
```

The existing `tests/integration/scripts/run-sil-tests.sh` is the only SIL
runner. It runs `modules/bridge/tests/test_bridge_sil.py` first and then
`modules/integration/tests/test_ha_integration_sil.py`, merges the two JUnit
files, writes XML and HTML coverage, and propagates any nonzero suite,
merge, or coverage status. Do not add a second command that runs the suites in
parallel or treats missing reports as success.

A container run is successful only when its command exits zero and all of these
mounted artifacts exist:

- `tests/integration/reports/bridge-junit.xml`
- `tests/integration/reports/integration-junit.xml`
- `tests/integration/reports/sil-junit.xml`
- `tests/integration/reports/coverage.xml`
- `tests/integration/reports/coverage-html/`

## Live Verification Variables

Provide live values in the process environment before invoking a root script:

```powershell
$env:HA_URL = "http://<haos-host>:8123"
$env:HA_WS = "ws://<haos-host>:8123/api/websocket"
$env:HA_TOKEN = "<long-lived-token>"
python test_live_pi.py
```

The live lane is intentionally separate from SIL. Credentials, raw WebSocket
frames, media URLs, and full device addresses must not be committed in reports
or tickets (D-05).

## Decision References

- **D-01:** Reuse the existing integration image and Compose stack.
- **D-02:** Preserve sequential suites and aggregate failure status.
- **D-03:** Missing optional dependencies are explicit, visible failures.
- **D-04:** Per-suite JUnit, merged JUnit, and coverage are gate evidence.
- **D-05:** Do not change production, SIL assertions, HAOS provisioning, mocks,
  or live-host workflows for this documentation contract.
- **SIL-03:** Both suites execute sequentially and produce one unified report.