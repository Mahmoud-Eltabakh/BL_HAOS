"""Validate redacted, machine-readable BL-HAOS release evidence."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


REQUIRED_GATES = {
    "REGRESSION",
    "SIL-CONTRACT",
    "SIL-CONTAINER",
    "DEPENDENCY-AUDIT",
    "ARCH-BUILD",
    "ARTIFACT-COMPAT",
    "DEMO-OFFLINE",
    "DEEP-HAOS",
    "LIVE-HARDWARE",
    "HAOS-PREFLIGHT",
    "UPGRADE-ROLLBACK",
}
REQUIRED_REPORTS = {
    "bridge-junit.xml",
    "integration-junit.xml",
    "sil-junit.xml",
    "coverage.xml",
    "coverage-html",
}
REDACTION_PATTERNS = (
    re.compile(r"(?i)bearer\s+[A-Za-z0-9._~+/=-]{12,}"),
    re.compile(r"\beyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
    re.compile(r"(?i)(?:ha_token|access_token|password|secret|api[_-]?key)\s*[:=]\s*[^\s,}\]]+"),
    re.compile(r"(?i)(?:https?|wss?)://(?:localhost|127\.0\.0\.1|0\.0\.0\.0|10\.(?:\d{1,3}\.){2}\d{1,3}|192\.168\.(?:\d{1,3}\.)\d{1,3}|172\.(?:1[6-9]|2\d|3[0-1])\.(?:\d{1,3}\.)\d{1,3}|\[::1\])(?::\d+)?(?:/[^\s\"']*)?"),
    re.compile(r"\b(?:[0-9a-f]{2}:){5}[0-9a-f]{2}\b", re.IGNORECASE),
    re.compile(r'"type"\s*:\s*"(?:auth|result|event)"\s*,\s*"(?:access_token|event|result)"', re.IGNORECASE),
)


class EvidenceError(ValueError):
    pass


def _read_manifest(evidence_dir: Path) -> dict[str, Any]:
    manifest_path = evidence_dir / "evidence.json"
    if not manifest_path.is_file():
        raise EvidenceError("missing evidence.json manifest")
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise EvidenceError(f"invalid evidence.json: {error}") from error
    if not isinstance(data, dict):
        raise EvidenceError("evidence.json must contain an object")
    return data


def _require_string(data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise EvidenceError(f"missing {key}")
    return value


def _check_freshness(manifest: dict[str, Any], max_age: timedelta = timedelta(days=7)) -> None:
    timestamp = _require_string(manifest, "generated_at")
    try:
        generated = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError as error:
        raise EvidenceError("generated_at must be an ISO-8601 timestamp") from error
    if generated.tzinfo is None:
        raise EvidenceError("generated_at must include a timezone")
    now = datetime.now(timezone.utc)
    if generated > now + timedelta(minutes=5):
        raise EvidenceError("evidence timestamp is in the future")
    if now - generated > max_age:
        raise EvidenceError("evidence is stale")


def _scan_redaction(value: Any, location: str = "manifest") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            _scan_redaction(key, f"{location}.{key}")
            _scan_redaction(child, f"{location}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _scan_redaction(child, f"{location}[{index}]")
    elif isinstance(value, str):
        for pattern in REDACTION_PATTERNS:
            if pattern.search(value):
                raise EvidenceError(f"unredacted sensitive material at {location}")


def _check_reports(evidence_dir: Path, manifest: dict[str, Any]) -> None:
    reports = manifest.get("required_reports")
    if not isinstance(reports, list) or set(reports) != REQUIRED_REPORTS:
        raise EvidenceError("required_reports must name the complete report set")
    for relative in reports:
        path = evidence_dir / relative
        if not path.exists() or (path.is_file() and path.stat().st_size == 0):
            raise EvidenceError(f"missing or empty report: {relative}")
        if path.is_dir() and not any(path.iterdir()):
            raise EvidenceError(f"empty report directory: {relative}")
        if path.is_file():
            try:
                text = path.read_text(encoding="utf-8", errors="strict")
            except OSError as error:
                raise EvidenceError(f"cannot read report {relative}: {error}") from error
            _scan_redaction(text, relative)


def validate(evidence_dir: Path) -> dict[str, Any]:
    manifest = _read_manifest(evidence_dir)
    _check_freshness(manifest)
    candidate = manifest.get("candidate")
    if not isinstance(candidate, dict):
        raise EvidenceError("missing candidate identity")
    for key in ("version", "architecture", "build_identity"):
        _require_string(candidate, key)
    if candidate["architecture"] not in {"aarch64", "amd64", "armv7"}:
        raise EvidenceError("candidate architecture is unsupported")

    gates = manifest.get("gates")
    if not isinstance(gates, dict) or set(gates) != REQUIRED_GATES:
        missing = sorted(REQUIRED_GATES - set(gates or {}))
        raise EvidenceError(f"gate set is incomplete; missing: {', '.join(missing)}")
    blockers = manifest.get("blockers")
    if not isinstance(blockers, list):
        raise EvidenceError("blockers must be a list")
    for name, gate in gates.items():
        if not isinstance(gate, dict) or gate.get("status") not in {"pass", "blocked", "fail"}:
            raise EvidenceError(f"invalid status for gate {name}")
        if gate["status"] != "pass":
            if not any(isinstance(item, dict) and item.get("gate") == name and item.get("owner") and item.get("rerun_command") for item in blockers):
                raise EvidenceError(f"non-passing gate {name} has no owner and rerun command")
        if not isinstance(gate.get("exit_status"), int):
            raise EvidenceError(f"missing command exit_status for gate {name}")
        _require_string(gate, "timestamp")

    _check_reports(evidence_dir, manifest)
    _scan_redaction(manifest)
    decision = manifest.get("decision")
    if decision not in {"GO", "HOLD", "NO-GO"}:
        raise EvidenceError("decision must be GO, HOLD, or NO-GO")
    if decision == "GO" and (blockers or any(gate["status"] != "pass" for gate in gates.values())):
        raise EvidenceError("GO is invalid while blockers or non-passing gates remain")
    return {"decision": decision, "candidate": candidate, "gates": sorted(gates), "blockers": len(blockers)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate redacted BL-HAOS release evidence")
    parser.add_argument("--evidence-dir", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        result = validate(args.evidence_dir)
    except EvidenceError as error:
        print(f"RELEASE EVIDENCE INVALID: {error}", file=sys.stderr)
        return 1
    print(json.dumps({"valid": True, **result}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())