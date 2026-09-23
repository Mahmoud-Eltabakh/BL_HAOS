# Phase 16 Context

## Scope

Wire the Phase 14 bridge SIL suite and Phase 15 Home Assistant integration SIL suite into the existing `tests/integration` Docker test runner. The runner must execute both suites in a deterministic local/CI container, expose machine-readable test and coverage artifacts on the host, and preserve failure visibility when optional test dependencies are unavailable.

## Decisions

- **D-01:** Reuse the existing `tests/integration/Dockerfile.test` and `tests/integration/docker-compose.yml`; do not introduce a second runner image or orchestration stack.
- **D-02:** Execute `modules/bridge/tests/test_bridge_sil.py` and `modules/integration/tests/test_ha_integration_sil.py` as separate sequential pytest invocations. Run the second suite even when the first fails, then return a nonzero aggregate status.
- **D-03:** Add only the verified test-only coverage dependency needed for unified reporting, and perform an explicit dependency preflight. Missing `pytest-homeassistant-custom-component`, `pytest-cov`, or other required packages must fail the runner clearly rather than being skipped or converted into a pass.
- **D-04:** Accumulate coverage across both invocations for bridge backend and bundled integration source roots, then write reports to a compose-mounted host directory. Preserve per-suite JUnit evidence and produce one merged JUnit report without requiring a third-party report merger.
- **D-05:** Keep Phase 16 focused on orchestration and reporting. Do not alter bridge or Home Assistant production behavior, SIL assertions, HAOS provisioning, Bluetooth mocks, or live-host workflows.

## Verification Boundary

The canonical executable check runs inside the `test-runner` image with `docker compose run --rm test-runner` or `docker compose up --abort-on-container-exit --exit-code-from test-runner test-runner`. Local execution outside the image may remain blocked when the active Python environment lacks the optional dependencies recorded by Phase 15; that condition must be reported as an environment failure, not worked around with unverified packages.

## Expected Outputs

- Host-visible per-suite logs and JUnit XML.
- A merged SIL JUnit XML report.
- Terminal coverage summary plus XML and HTML coverage reports covering both source roots.