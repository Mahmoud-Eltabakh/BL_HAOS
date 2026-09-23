---
phase: 19-diagnostics-supportability-observability
plan: 02
subsystem: recovery-demo-supportability
tags: [recovery, diagnostics, demo-mode, fastapi, react, tdd]
dependency_graph:
  requires: [phase-19-plan-01-diagnostics, phase-18-auth-validation-redaction]
  provides: [bounded-recovery-contract, deterministic-demo-runtime, guided-recovery-ui]
  affects: [bridge-api, ingress-ui, health-timestamps, operator-documentation]
tech_stack:
  added: []
  patterns: [allowlisted-manager-actions, environment-gated-dependency-injection, fixed-clock-demo-fixtures]
key-files:
  created:
    - modules/bridge/backend/bl_haos/recovery.py
    - modules/bridge/backend/bl_haos/demo.py
    - modules/bridge/web_ui/src/components/DiagnosticsPanel.tsx
    - modules/bridge/web_ui/src/components/RecoveryPanel.tsx
    - modules/bridge/tests/test_recovery.py
    - modules/bridge/tests/test_demo_mode.py
  modified:
    - modules/bridge/backend/bl_haos/api/routes.py
    - modules/bridge/backend/bl_haos/main.py
    - modules/bridge/backend/bl_haos/config.py
    - modules/bridge/backend/bl_haos/health.py
    - modules/bridge/web_ui/src/api/client.ts
    - modules/bridge/web_ui/src/App.tsx
    - modules/bridge/tests/test_api.py
    - modules/bridge/tests/test_frontend_assets.py
    - modules/bridge/DOCS.md
  preserved:
    - unrelated parent-worktree planning, integration, temporary, and nested-repository changes
decisions:
  - Recovery actions are fixed operation ids routed directly to existing manager APIs; arbitrary commands and targets are rejected.
  - Recovery requests reuse native bridge authentication and normalized Bluetooth/component validation.
  - Demo mode is selected by environment, defaults off, and is injected before live dependency initialization.
  - HealthRegistry accepts an injected clock so deterministic demo diagnostics include stable timestamps.
metrics:
  duration: under 1 hour
  completed_date: 2026-09-23
  status: complete
  commits: 0
  plan_head_before: not committed by executor
actuals:
  tokens: 25269
  tasks: 2
  commits: 0
---

# Phase 19 Plan 02: Guided recovery and deterministic demo summary

Implemented authenticated, allowlisted guided recovery actions and a deterministic offline runtime that exercises the production diagnostics and UI contracts without host Bluetooth, audio, Snapcast, or Home Assistant initialization.

## Completed Tasks

1. Added failure-class guidance for pairing, sink, reconnect, native-integration, D-Bus, and stale-object failures, with generic escalation for unknown classes. Recovery action results include stable action ids, normalized targets, correlation ids, bounded outcomes, and refreshed diagnostics.
2. Added deterministic demo scenarios for healthy, pairing failure, sink missing, reconnect exhausted, native integration unavailable, and restart/degraded lifecycle states. Demo selection is environment-gated and production-safe by default.
3. Added diagnostics and guided recovery panels with loading, unavailable, failure, success, support-export, and demo states, plus shared TypeScript API contracts.
4. Added TDD coverage for action safety, authentication, concurrency conflict handling, demo route injection, byte-stable scenario exports, and frontend assets. Documented operator recovery and demo configuration in `modules/bridge/DOCS.md`.

## Verification

- `Set-Location modules/bridge; python -m pytest tests/test_recovery.py tests/test_demo_mode.py tests/test_api.py tests/test_frontend_assets.py -q` -> 26 passed, 4 warnings.
- `Set-Location modules/bridge; npm --prefix web_ui run build` -> passed (`tsc && vite build`).
- `Set-Location modules/bridge; python -m pytest tests/ -q` -> 100 passed, 4 warnings.
- Repeated serialized `DemoRuntime` exports for all six scenarios -> all stable byte-for-byte.
- `git diff --check` -> passed; only CRLF warnings.
- Focused file diagnostics -> no errors reported.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Determinism] Added an injectable health clock.**
- **Found during:** Task 2 demo stability validation.
- **Issue:** Pydantic health observations used wall-clock defaults, making repeated demo exports differ.
- **Fix:** HealthRegistry now stamps component, speaker, failure, and snapshot timestamps through its injected clock; DemoRuntime uses a fixed clock.
- **Files modified:** `modules/bridge/backend/bl_haos/health.py`

**2. [Rule 1 - Build compatibility] Adjusted frontend APIs to the installed TypeScript/lucide versions.**
- **Found during:** Task 1 frontend build.
- **Issue:** `CircleAlert` was unavailable and `String.replaceAll` exceeded the configured ES2020 library.
- **Fix:** Used the installed `AlertCircle` export and an ES2020-compatible regex replacement.
- **Files modified:** `modules/bridge/web_ui/src/components/RecoveryPanel.tsx`

## Known Stubs

None introduced by this plan.

## Threat Flags

None beyond the registered plan surfaces. Recovery preserves native auth, strict action/target validation, bounded timeout and concurrency behavior, and redacted diagnostics contracts. Demo mode defaults off and is injected before live services.

## Self-Check: PASSED

- Summary file exists at `.planning/phases/19-diagnostics-supportability-observability/19-02-SUMMARY.md`.
- Focused recovery/demo/API/frontend tests passed.
- Full bridge suite passed: 100 tests.
- UI build passed.
- No commits were made; parent workflow owns commit/push.
