# Phase 16 Research

## Existing Orchestration

- `tests/integration/docker-compose.yml` already defines `haos` and `test-runner`, mounts the repository at `/workspace`, and currently keeps `test-runner` alive with `tail -f /dev/null`.
- `tests/integration/Dockerfile.test` is based on `mcr.microsoft.com/playwright/python:v1.42.0-jammy`, installs `openssh-client`, `curl`, and `jq`, then installs `tests/integration/requirements-test.txt` and Chromium.
- `tests/integration/requirements-test.txt` already contains `pytest`, `pytest-asyncio`, `pytest-playwright`, `requests`, and the Phase 15 `pytest-homeassistant-custom-component` dependency.
- `pytest.ini` discovers `modules/bridge/tests` and `modules/integration/tests` from the repository root and sets `modules/bridge` on `PYTHONPATH`.

## Suite Boundaries

- Phase 14 provides `modules/bridge/tests/test_bridge_sil.py`, an in-process FastAPI/WebSocket suite that needs no HAOS VM, D-Bus socket, Bluetooth hardware, or live network.
- Phase 15 provides `modules/integration/tests/test_ha_integration_sil.py` and checked-in JSON fixtures, but its runtime collection requires `pytest-homeassistant-custom-component`.
- Phase 15 validation was blocked in the active local Python 3.14 environment because that optional harness was unavailable; the container requirements are the intended shared execution environment.

## Selected Implementation

- Add `pytest-cov` to the existing requirements file; this is a verified PyPI test-only package needed to append coverage data across the two pytest processes.
- Add a shell runner under `tests/integration/scripts` that checks required imports/tools, erases prior coverage data, runs the bridge suite and HA suite separately, preserves both exit statuses, merges their JUnit XML with Python standard-library XML handling, and emits `coverage report`, `coverage xml`, and `coverage html` artifacts.
- Update compose to invoke the runner on container start and mount a stable host `reports` directory. Keep the repository bind mount so source and tests remain authoritative.
- Use explicit source roots (`modules/bridge/backend` and `modules/integration/custom_components/bl_haos`) and per-suite JUnit files so unrelated deep/Playwright tests do not enter the Phase 16 report.

## Package Legitimacy Audit

| Package | Registry URL | Use | Status |
|---|---|---|---|
| `pytest-homeassistant-custom-component` | https://pypi.org/project/pytest-homeassistant-custom-component/ | Home Assistant custom-component SIL harness | VERIFIED; existing Phase 15 dependency |
| `pytest-cov` | https://pypi.org/project/pytest-cov/ | Pytest coverage collection and report generation | VERIFIED; new test-only dependency |

No production dependency or unverified package is required. The plan must not silently skip the HA suite when the harness is absent.

## Risks To Cover

- An idle compose command can make a green container appear healthy without running tests.
- A shell `set -e` path can prevent the second suite or report generation from running after the first failure, hiding useful evidence.
- Reusing one JUnit output path can overwrite the first suite's result; each suite needs its own file before standard-library merging.
- Coverage must be erased at run start and accumulated intentionally, otherwise stale `.coverage` data can inflate results.
- The host Python environment may still lack optional dependencies; container validation is authoritative and local failure messaging must remain explicit.