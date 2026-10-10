---
phase: 20-release-quality-gates-go-live
plan: 02
subsystem: release-quality
tags: [haos, release-evidence, upgrade-rollback, go-live]
dependency_graph:
  requires: [20-01 release gates, deterministic SIL reports, provisioned HAOS for deep/live lanes]
  provides: [release runbook, evidence validator, retained redacted evidence, HOLD go-live readout]
  affects: [release operations, CI/release evidence]
tech_stack:
  added: []
  patterns: [fail-closed evidence validation, explicit environment blockers, guarded query_ha lifecycle]
key_files:
  created:
    - tests/integration/RELEASE-RUNBOOK.md
    - tests/integration/GO-LIVE-READOUT.md
    - tests/integration/scripts/validate-release-evidence.py
    - tests/integration/tests/test_release_evidence.py
    - tests/integration/reports/release/evidence.json
    - 20-02-SUMMARY.md
  modified: []
decisions:
  - Keep GO impossible while any gate is failed, blocked, stale, contradictory, or unredacted.
  - Treat missing playwright, pip_audit, Trivy, HAOS credentials, provisioning image, hardware, and CI registry as explicit blockers.
  - Do not launch an unprovisioned HAOS VM or perform live mutations without the guarded preflight and --apply path.
metrics:
  duration: not recorded
  completed_date: 2026-09-23
  tasks: 3
  commits: 0
  plan_head_before: not committed by request
actuals:
  tokens: 15000
  tasks: 3
  commits: 0
status: complete
---

# Phase 20 Plan 02: Final HAOS Validation, Upgrade/Rollback, and Go-Live Summary

Release tooling and evidence were completed. The current candidate is **HOLD**,
not GO: deterministic SIL and demo gates pass, but the Windows-local
environment cannot prove all mandatory HAOS, hardware, dependency, regression,
and architecture gates.

## Accomplishments

- Added a reproducible runbook ordering read-only HAOS preflight, guarded
  lifecycle mutations, native setup/playback checks, upgrade capture, bounded
  rollback, post-rollback native verification, and redacted evidence retention.
- Added a machine-checking validator requiring candidate version, architecture,
  build identity, timestamps, exit statuses, complete report paths, redaction,
  blocker ownership, rerun commands, and a truthful GO/HOLD/NO-GO decision.
- Retained fresh bridge, integration, merged SIL, XML coverage, and HTML
  coverage evidence under `tests/integration/reports/release/`.
- Added focused tests for complete evidence, missing reports, failed/unclassified
  gates, token/private URL/raw-frame/device redaction, guarded query_ha usage,
  runbook ordering, and HOLD readout semantics.

## Verification

| Check | Result |
|---|---|
| `python -m pytest tests/integration/tests/test_release_evidence.py tests/integration/tests/test_orchestration.py -q` | 14 passed |
| `python -m pytest tests/integration/tests/test_release_contract.py -q` | 6 passed |
| `python -m pytest modules/bridge/tests/test_demo_mode.py -q` | 4 passed, 1 warning |
| Canonical Docker SIL build/run | Passed; bridge 6, integration 5; all five reports present |
| `python tests/integration/scripts/validate-release-evidence.py --evidence-dir tests/integration/reports/release` | Valid; HOLD; 7 blockers |
| `python -m py_compile query_ha.py tests/integration/scripts/validate-release-evidence.py` | Passed |
| `git diff --check` | Passed; pre-existing line-ending warning only |
| `python -m pytest tests/ -q` | Blocked at collection: `playwright` unavailable |
| `python query_ha.py preflight` | Correctly blocked: `HA_URL`/`HA_TOKEN` absent |
| `npm --prefix modules/bridge/web_ui audit --audit-level=high` | Passed; 0 vulnerabilities |
| `python -m pip_audit ...` / Trivy | Blocked; tools unavailable |

## Environment-Qualified Blockers

1. `REGRESSION`: install the declared `playwright` dependency and rerun the
   full repository suite.
2. `DEPENDENCY-AUDIT`: run pinned `pip-audit` and Trivy on the security runner;
   npm audit passed locally.
3. `ARCH-BUILD`: dispatch the Home Assistant Builder for `aarch64`, `amd64`,
   and `armv7` with registry credentials.
4. `DEEP-HAOS`: `/dev/kvm` is present through WSL, but
   `tests/integration/config_usb` has no provisioning image.
5. `LIVE-HARDWARE`: no process credentials, approved adapter, speaker, or
   media item were available.
6. `HAOS-PREFLIGHT`: no `HA_URL`, `HA_WS`, or `HA_TOKEN` was supplied.
7. `UPGRADE-ROLLBACK`: no authenticated HAOS host or known-good Supervisor
   rollback target was available.

These are recorded in `evidence.json` with an owner and exact rerun command.
No live mutation, upgrade, rollback, or unsupported readiness claim was made.

## Deviations from Plan

None. The unavailable HAOS, Linux/KVM provisioning, live hardware, dependency,
and registry environments were handled as explicit blockers as required.

## Self-Check: PASSED

The summary, runbook, readout, validator, focused tests, evidence manifest, and
retained deterministic reports exist. The validator returns success for the
manifest and correctly reports `HOLD` with seven blockers. No commit was made;
the parent workflow owns commit/push.