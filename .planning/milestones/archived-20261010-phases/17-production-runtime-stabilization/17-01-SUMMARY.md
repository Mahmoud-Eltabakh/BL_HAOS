---
phase: 17-production-runtime-stabilization
plan: 01
subsystem: runtime-health
tags: [health, bluetooth, pipewire, snapcast, websocket, reconnect]
dependency_graph:
  requires: [phase-16-orchestration]
  provides: [versioned-health-snapshot, bounded-failure-taxonomy, speaker-state-observations, reconnect-worker-ownership]
  affects: [api, websocket-events, bluetooth-reconnect, playback, multiroom, lifecycle]
tech_stack:
  added: []
  patterns: [pydantic-health-contract, injectable-observations, normalized-address-ownership]
key_files:
  created:
    - modules/bridge/backend/bl_haos/health.py
    - modules/bridge/tests/test_health.py
  modified:
    - modules/bridge/backend/bl_haos/api/routes.py
    - modules/bridge/backend/bl_haos/api/ws.py
    - modules/bridge/backend/bl_haos/main.py
    - modules/bridge/backend/bl_haos/bluetooth/reconnect.py
    - modules/bridge/backend/bl_haos/ha/player.py
    - modules/bridge/backend/bl_haos/multiroom/manager.py
    - modules/bridge/tests/test_api.py
    - modules/bridge/tests/test_bridge_sil.py
decisions:
  - Required dependency unavailability outranks startup lifecycle state in aggregate health.
  - Snapcast is optional for aggregate Bluetooth control and reports isolated degradation.
  - Reconnect ownership is keyed by normalized speaker address and workers are cancelled during shutdown.
metrics:
  duration: not measured
  completed_date: 2026-09-23
  status: complete
  commits: 0
  plan_head_before: not committed by executor
actuals:
  tokens: 12000
  tasks: 3
  commits: 0
---

# Phase 17 Plan 01: Lifecycle, health-state, event, and runtime-contract model Summary

Implemented a canonical, versioned runtime health contract and wired it through the bridge API, WebSocket event bus, lifecycle, Bluetooth reconnect engine, PipeWire playback boundary, and Snapcast boundary. The executor intentionally made no commits per the parent-agent instruction; the working tree retains the changes for parent review and commit.

## Completed Tasks

1. Added bounded Pydantic health and failure models with deterministic aggregate precedence, normalized speaker identities, lifecycle state, redaction, and versioned serialization.
2. Added API/WebSocket publication and lifecycle observations, plus deterministic speaker transitions, stale-object/reconnect classifications, and one in-flight reconnect worker per normalized address.
3. Added PipeWire probe/sink classifications, injectable Snapcast readiness observations, and SIL coverage for health, API compatibility, transitions, redaction, and worker ownership.

## Verification

- Focused Task 1: `python -m pytest modules/bridge/tests/test_health.py modules/bridge/tests/test_api.py modules/bridge/tests/test_bridge_sil.py -q` -> 16 passed.
- Focused Task 2: `python -m pytest modules/bridge/tests/test_health.py modules/bridge/tests/test_bluetooth_manager.py modules/bridge/tests/test_auto_reconnect.py -q` -> 12 passed.
- Full bridge suite from module root: `Set-Location modules/bridge; python -m pytest tests/ -q` -> 65 passed.
- `git diff --check` -> no whitespace errors.

## Blockers and Environment Notes

The literal plan command `python -m pytest modules/bridge/tests/ -q` was also run from the workspace root and produced 18 path-based failures because those tests resolve add-on fixtures relative to the current directory. The corrected module-root invocation passed all 65 tests. Four pre-existing warnings remain, including the existing unawaited WebSocket broadcast warning.

No package installation, repository commit, branch operation, or destructive cleanup was performed. Existing user changes in the root repository and bridge submodule were preserved.

## Self-Check: PASSED

- Summary file exists at `.planning/phases/17-production-runtime-stabilization/17-01-SUMMARY.md`.
- Focused tests passed: 16 and 12.
- Full bridge suite passed: 65.
- State and roadmap progress were updated without staging or committing.
