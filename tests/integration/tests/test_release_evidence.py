import importlib.util
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[3]
VALIDATOR_PATH = ROOT / "tests" / "integration" / "scripts" / "validate-release-evidence.py"
SPEC = importlib.util.spec_from_file_location("release_evidence_validator", VALIDATOR_PATH)
validator = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(validator)


def _fixture(tmp_path: Path, **overrides):
    reports = ["bridge-junit.xml", "integration-junit.xml", "sil-junit.xml", "coverage.xml", "coverage-html"]
    for report in reports:
        path = tmp_path / report
        if report == "coverage-html":
            path.mkdir()
            (path / "index.html").write_text("<html>coverage</html>", encoding="utf-8")
        else:
            path.write_text("<?xml version=\"1.0\"?><testsuites></testsuites>", encoding="utf-8")
    now = datetime.now(timezone.utc).isoformat()
    gates = {
        name: {"status": "pass", "exit_status": 0, "timestamp": now, "command": f"command-for-{name}"}
        for name in validator.REQUIRED_GATES
    }
    manifest = {
        "schema_version": 1,
        "generated_at": now,
        "candidate": {"version": "0.2.23", "architecture": "amd64", "build_identity": "local-release-candidate"},
        "required_reports": reports,
        "gates": gates,
        "blockers": [],
        "decision": "GO",
    }
    manifest.update(overrides)
    (tmp_path / "evidence.json").write_text(json.dumps(manifest), encoding="utf-8")
    return tmp_path


def test_complete_redacted_fixture_validates():
    from tempfile import TemporaryDirectory

    with TemporaryDirectory() as directory:
        result = validator.validate(_fixture(Path(directory)))
    assert result["decision"] == "GO"
    assert set(result["gates"]) == validator.REQUIRED_GATES


@pytest.mark.parametrize("missing", ["bridge-junit.xml", "coverage.xml", "coverage-html"])
def test_missing_required_evidence_is_rejected(tmp_path, missing):
    evidence = _fixture(tmp_path)
    path = evidence / missing
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()
    with pytest.raises(validator.EvidenceError, match="missing|empty"):
        validator.validate(evidence)


def test_failed_gate_requires_explicit_blocker(tmp_path):
    evidence = _fixture(tmp_path)
    manifest = json.loads((evidence / "evidence.json").read_text())
    manifest["gates"]["DEEP-HAOS"]["status"] = "blocked"
    manifest["gates"]["DEEP-HAOS"]["exit_status"] = 1
    manifest["decision"] = "HOLD"
    (evidence / "evidence.json").write_text(json.dumps(manifest))
    with pytest.raises(validator.EvidenceError, match="owner and rerun"):
        validator.validate(evidence)


def test_unredacted_tokens_urls_frames_and_device_material_are_rejected(tmp_path):
    for index, secret in enumerate((
        "Bearer abcdefghijklmnop",
        "https://192.168.1.21:8123",
        "eyJabcdefghijklmnopqrstuv.abcdefghijklmnop.abcdefghijklmnop",
        "aa:bb:cc:11:22:33",
        '"type":"auth","access_token":"secret"',
    )):
        evidence_path = tmp_path / f"secret-{index}"
        evidence_path.mkdir()
        evidence = _fixture(evidence_path)
        manifest = json.loads((evidence / "evidence.json").read_text())
        manifest["operator_note"] = secret
        (evidence / "evidence.json").write_text(json.dumps(manifest))
        with pytest.raises(validator.EvidenceError, match="unredacted"):
            validator.validate(evidence)


def test_query_ha_documentation_is_guarded_and_secret_free():
    source = (ROOT / "query_ha.py").read_text()
    assert "preflight" in source
    assert "--apply" in source
    assert "os.environ.get(\"HA_TOKEN\"" in source
    assert "https://192.168" not in source


def test_runbook_orders_preflight_lifecycle_and_rollback():
    runbook = (ROOT / "tests" / "integration" / "RELEASE-RUNBOOK.md").read_text()
    ordered = [
        "python query_ha.py preflight",
        "python query_ha.py addon-stop --apply",
        "python query_ha.py addon-start --apply",
        "python query_ha.py native-setup --apply",
        "python query_ha.py play-media --apply",
        "post-rollback",
    ]
    positions = [runbook.index(marker) for marker in ordered]
    assert positions == sorted(positions)
    for marker in ("known-good", "backup", "candidate version", "native config", "bounded", "operator audible"):
        assert marker in runbook
    for architecture in ("aarch64", "amd64", "armv7"):
        assert architecture in runbook or architecture in (ROOT / "tests" / "integration" / "RELEASE-GATES.md").read_text()


def test_readout_cannot_claim_go_with_environment_blockers():
    readout = (ROOT / "tests" / "integration" / "GO-LIVE-READOUT.md").read_text()
    assert "Decision: HOLD" in readout
    assert "must be changed to `GO` only" in readout
    assert "Windows-local" in readout
    assert "Upgrade and rollback" in readout