"""Static contract tests for the local and CI SIL test runner."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
INTEGRATION = ROOT / "tests" / "integration"
COMPOSE = INTEGRATION / "docker-compose.yml"
DOCKERFILE = INTEGRATION / "Dockerfile.test"
REQUIREMENTS = INTEGRATION / "requirements-test.txt"
RUNNER = INTEGRATION / "scripts" / "run-sil-tests.sh"
SMOKE_MATRIX = INTEGRATION / "SMOKE-MATRIX.md"
CI_GATES = INTEGRATION / "CI-GATES.md"
README = ROOT / "README.md"


def test_compose_starts_runner_and_exposes_reports():
    compose = COMPOSE.read_text()

    assert 'command: ["sh", "/workspace/tests/integration/scripts/run-sil-tests.sh"]' in compose
    assert "- ./reports:/reports" in compose
    assert "- ../../:/workspace" in compose
    assert "- ./config_usb:/config_usb" in compose


def test_runner_contract_preserves_order_preflight_and_failure_visibility():
    runner = RUNNER.read_text()
    bridge = "modules/bridge/tests/test_bridge_sil.py"
    integration = "modules/integration/tests/test_ha_integration_sil.py"

    assert runner.index(bridge) < runner.index(integration)
    assert "pytest, pytest_cov, pytest_homeassistant_custom_component" in runner
    assert "command -v pytest" in runner
    assert "command -v coverage" in runner
    assert "coverage erase" in runner
    assert "--cov-append" in runner
    assert "modules/bridge/backend" in runner
    assert "modules/integration/custom_components/bl_haos" in runner
    assert "bridge-junit.xml" in runner
    assert "integration-junit.xml" in runner
    assert "sil-junit.xml" in runner
    assert "coverage.xml" in runner
    assert "coverage-html" in runner
    assert "|| true" not in runner
    assert "exit \"$status\"" in runner
    assert "bridge_status" in runner
    assert "integration_status" in runner


def test_image_installs_shared_requirements_with_verified_reporting_tools():
    dockerfile = DOCKERFILE.read_text()
    requirements = REQUIREMENTS.read_text().splitlines()

    assert "build-essential" in dockerfile
    assert "COPY requirements-test.txt ." in dockerfile
    assert "RUN pip install -r requirements-test.txt" in dockerfile
    assert any(line.startswith("pytest-homeassistant-custom-component") for line in requirements)
    assert any(line.startswith("pytest-cov") for line in requirements)


def test_smoke_matrix_covers_canonical_commands_and_reports():
    matrix = SMOKE_MATRIX.read_text()

    required_commands = [
        "pytest tests/ -q",
        "pytest tests/integration/tests/test_orchestration.py -q",
        "docker compose -f tests/integration/docker-compose.yml build test-runner",
        "docker compose -f tests/integration/docker-compose.yml run --rm test-runner",
        "docker compose -f tests/integration/docker-compose.yml up --abort-on-container-exit --exit-code-from test-runner test-runner",
        "python test_live_pi.py",
        "python test_full_pi_workflow.py",
    ]
    required_reports = [
        "bridge-junit.xml",
        "integration-junit.xml",
        "sil-junit.xml",
        "coverage.xml",
        "coverage-html",
    ]

    for expected in required_commands + required_reports:
        assert expected in matrix
    for decision in ("D-01", "D-02", "D-03", "D-04", "D-05", "SIL-03"):
        assert decision in matrix
    assert "HA_URL" in matrix
    assert "HA_WS" in matrix
    assert "HA_TOKEN" in matrix
    assert "not a deterministic CI substitute" in matrix


def test_ci_gate_policy_and_readme_remain_discoverable_and_artifact_aware():
    gates = CI_GATES.read_text()
    readme = README.read_text()

    for gate in ("SIL-CONTRACT", "SIL-CONTAINER", "DEEP-HAOS", "LIVE-HARDWARE"):
        assert gate in gates
    for report in ("bridge-junit.xml", "integration-junit.xml", "sil-junit.xml", "coverage.xml", "coverage-html"):
        assert report in gates
    assert "command exits successfully" in gates
    assert "no root GitHub Actions test workflow" in gates
    assert "missing test dependencies" in gates
    assert "infrastructure failure" in gates
    assert "not a deterministic SIL result" in gates
    for decision in ("D-01", "D-02", "D-03", "D-04", "D-05", "SIL-03"):
        assert decision in gates

    assert "tests/integration/SMOKE-MATRIX.md" in readme
    assert "tests/integration/CI-GATES.md" in readme