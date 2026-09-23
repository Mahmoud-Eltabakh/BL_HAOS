---
phase: 19-diagnostics-supportability-observability
plan: 01
subsystem: diagnostics-observability
tags: [diagnostics, telemetry, support-bundle, redaction, websocket, home-assistant]
dependency_graph:
  requires: [phase-17-canonical-health, phase-18-redaction]
  provides: [bounded-diagnostics-projection, correlated-telemetry-envelope, redacted-support-bundle]
  affects: [bridge-api, lifecycle-events, native-ha-diagnostics]
tech_stack:
  added: []
  patterns: [single-health-registry-projection, bounded-deque-history, deterministic-redacted-serialization]
key-files:
  created:
    - modules/bridge/backend/bl_haos/diagnostics.py
    - modules/bridge/tests/test_diagnostics.py
  modified:
    - modules/bridge/backend/bl_haos/api/routes.py
    - modules/bridge/backend/bl_haos/main.py
    - modules/bridge/tests/test_api.py
    - modules/bridge/tests/test_ws.py
    - modules/integration/custom_components/bl_haos/diagnostics.py
    - modules/integration/tests/test_ha_integration_sil.py
  preserved:
    - modules/bridge/backend/bl_haos/health.py
    - modules/bridge/backend/bl_haos/api/ws.py
    - unrelated pre-existing nested-repository changes
key-decisions:
  - Diagnostics reads HealthRegistry snapshots and does not create a second health truth.
  - Support exports use fixed event, collection, age, detail, and serialized-byte limits with omission of unsafe fields.
  - Existing health and WebSocket framing remain compatible; new lifecycle telemetry is delivered as a versioned telemetry event.
metrics:
  duration: under 1 hour
  completed_date: 2026-09-23
  status: complete
  commits: 0
  plan_head_before: not committed by executor
actuals:
  tokens: 10500
  tasks: 3
  commits: 0
---

# Phase 19 Plan 01: Canonical diagnostics and support telemetry summary

Implemented the canonical bounded diagnostics projection, correlated lifecycle telemetry envelope, and redacted support-bundle export on top of the Phase 17 HealthRegistry. No commits were made per the parent-agent instruction.

## Completed Tasks

1. Added `DiagnosticsService` with versioned aggregate/component/speaker/lifecycle diagnostics, bounded recent failures, fixed event history, correlation IDs, failure classification, transition reason, recovery outcome, recursive redaction, deterministic serialization, and support-bundle byte limits.
2. Added `/api/diagnostics` and `/api/support/bundle` with stable JSON and attachment contracts; wired lifecycle health observations into versioned WebSocket telemetry while preserving existing health and native event compatibility.
3. Extended Home Assistant config-entry diagnostics with safe contract/schema/version metadata and added bridge plus integration SIL regression coverage.

## Verification

- `Set-Location modules/bridge; python -m pytest tests/test_diagnostics.py tests/test_api.py tests/test_health.py -q` -> 22 passed, 4 warnings.
- `Set-Location modules/bridge; python -m pytest tests/test_diagnostics.py tests/test_ws.py tests/test_health.py tests/test_bridge_sil.py -q` -> 20 passed, 1 warning.
- `Set-Location modules/bridge; python -m pytest tests/ -q` -> 90 passed, 4 warnings.
- `Set-Location modules/bridge; git diff --check` -> passed.
- `Set-Location modules/integration; git diff --check` -> passed.
- Focused diagnostics module errors -> none reported.

## Blockers

The integration SIL suite could not collect in this environment because `pytest_homeassistant_custom_component` is not installed:

`Set-Location modules/integration; python -m pytest tests/test_ha_integration_sil.py -q` -> collection error, `ModuleNotFoundError: No module named 'pytest_homeassistant_custom_component'`.

The plan's literal `Set-Location ../../integration` command was also invalid for this workspace; the integration project is under `modules/integration`, and that corrected command was used for the blocker report. No package was installed.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Determinism/size bug] Made diagnostics timestamps use the injected service clock and strengthened the final support-bundle size fallback.**
- **Found during:** Task 1 focused RED/GREEN validation.
- **Issue:** Repeated support exports differed because timestamps used wall-clock values, and oversized bundles needed a minimal fallback after clearing events.
- **Fix:** Use the service clock for projection timestamps and progressively omit events, failures, speaker/adapter collections, then retain only the minimal diagnostics contract.
- **Files modified:** `modules/bridge/backend/bl_haos/diagnostics.py`
- **Verification:** Focused diagnostics tests and full bridge suite passed.

## Known Stubs

None introduced by this plan.

## Threat Flags

None beyond the plan's registered diagnostics-to-client trust boundary; the implementation applies recursive redaction and fixed bounds before retention or export.

## Self-Check: PASSED

- Summary file exists at `.planning/phases/19-diagnostics-supportability-observability/19-01-SUMMARY.md`.
- Focused diagnostics and telemetry tests passed.
- Full bridge suite passed: 90 tests.
- No task or metadata commits were made; parent workflow owns commit/push.
