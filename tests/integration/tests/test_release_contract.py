"""Static release-gate contract tests."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
INTEGRATION = ROOT / "tests" / "integration"
GATES = INTEGRATION / "RELEASE-GATES.md"
MATRIX = INTEGRATION / "REGRESSION-MATRIX.md"
WORKFLOW = ROOT / "modules" / "bridge" / ".github" / "workflows" / "builder.yaml"
CONFIG = ROOT / "modules" / "bridge" / "config.yaml"
BUILD = ROOT / "modules" / "bridge" / "build.yaml"
README = ROOT / "modules" / "bridge" / "README.md"


def test_release_path_has_exact_commands_and_blocking_evidence():
    gates = GATES.read_text()
    matrix = MATRIX.read_text()

    for gate in (
        "PREFLIGHT", "REGRESSION", "SIL-CONTRACT", "SIL-CONTAINER",
        "DEPENDENCY-AUDIT", "ARCH-BUILD", "ARTIFACT-COMPAT", "DEMO-OFFLINE",
        "DEEP-HAOS", "LIVE-HARDWARE",
    ):
        assert gate in gates
    for command in (
        "python -m pytest tests/ -q",
        "python -m pytest tests/integration/tests/test_orchestration.py -q",
        "docker compose -f tests/integration/docker-compose.yml build test-runner",
        "docker compose -f tests/integration/docker-compose.yml run --rm test-runner",
        "docker compose -f tests/integration/docker-compose.yml up --abort-on-container-exit --exit-code-from test-runner test-runner",
        "python test_live_pi.py", "python test_full_pi_workflow.py",
        "python -m pytest modules/bridge/tests/test_demo_mode.py -q",
    ):
        assert command in gates or command in matrix
    for report in ("bridge-junit.xml", "integration-junit.xml", "sil-junit.xml", "coverage.xml", "coverage-html/"):
        assert report in gates and report in matrix


def test_matrix_covers_runtime_auth_degraded_recovery_and_demo_paths():
    matrix = MATRIX.read_text()
    for scenario in (
        "REL-01-START", "REL-01-CONNECT", "REL-01-DISCONNECT",
        "REL-01-RECONNECT", "REL-01-PLAYBACK", "REL-01-AUTH-OK",
        "REL-01-AUTH-FAIL", "REL-01-DEGRADED", "REL-01-RECOVERY",
        "OPS-03-SCAN", "OPS-03-PAIR", "OPS-03-PLAY", "OPS-03-FAIL",
        "OPS-03-OFFLINE",
    ):
        assert scenario in matrix
    assert "same command / `DEMO-OFFLINE`" in matrix
    assert "unavailable is not pass" in matrix


def test_policy_defines_support_compatibility_security_and_traceability():
    gates = GATES.read_text()
    matrix = MATRIX.read_text()
    readme = README.read_text(encoding="utf-8")

    for text in (gates, matrix):
        for requirement in ("REL-01", "REL-02", "REL-03", "REL-04", "OPS-03"):
            assert requirement in text
        for policy_term in (
            "Stable", "Preview", "Home Assistant Core 2024.x", "aarch64",
            "amd64", "armv7", "security owner", "expiry date", "redacted",
            "high and critical",
        ):
            assert policy_term in text
    assert "tests/integration/RELEASE-GATES.md" in readme
    assert "tests/integration/REGRESSION-MATRIX.md" in readme
    assert "Sendspin" in gates and "Music Assistant" in gates


def test_missing_dependencies_and_reports_cannot_be_skipped():
    gates = GATES.read_text()
    workflow = WORKFLOW.read_text()
    for phrase in (
        "missing test dependencies", "Missing JUnit or coverage output",
        "never converted to an unqualified pass", "There is no default bypass",
        "continue-on-error",
    ):
        assert phrase in gates
    assert "pip-audit==2.7.3" in workflow
    assert "npm --prefix web_ui audit --audit-level=high" in workflow
    assert "severity: HIGH,CRITICAL" in workflow
    assert 'exit-code: "1"' in workflow


def test_architecture_matrix_matches_addon_manifests():
    workflow = WORKFLOW.read_text()
    config = CONFIG.read_text()
    build = BUILD.read_text()
    for architecture in ("aarch64", "amd64", "armv7"):
        assert architecture in workflow
        assert architecture in config
        assert architecture in build
    assert "config.yaml" in workflow
    assert "build.yaml" in workflow


def test_workflow_keeps_audits_before_build_and_has_retained_evidence():
    workflow = WORKFLOW.read_text()
    assert workflow.index("Audit Python and frontend dependencies") < workflow.index(
        "Build and Publish Add-on with Home Assistant Builder"
    )
    assert workflow.index("Scan repository dependency inputs") < workflow.index(
        "Build and Publish Add-on with Home Assistant Builder"
    )
    for artifact in ("bridge-junit.xml", "integration-junit.xml", "sil-junit.xml", "coverage.xml", "coverage-html"):
        assert artifact in workflow
    assert "continue-on-error" not in workflow
    assert "|| true" not in workflow