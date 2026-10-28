---
phase: 38-headless-addon-ingress-ui-retirement
plan: 01
subsystem: bridge
tags: [headless, ingress-retirement, native-api, ci]
requires:
  - phase: 37
    provides: authenticated native pairing, speaker and settings endpoints
provides:
  - Backend-only add-on packaging with a fixed migration notice and no legacy management routes
  - Retained authenticated native API, watchdog, health, discovery and operational websockets
  - Root/module CI and runners retargeted to the Home Assistant-native panel
affects: [38-02, 38-03, 39]
tech-stack:
  added: []
  patterns: [fixed root migration notice, native route retirement assertions]
key-files:
  created: [modules/bridge/tests/test_headless_addon.py]
  modified: [modules/bridge/config.yaml, modules/bridge/Dockerfile, modules/bridge/backend/bl_haos/main.py, modules/bridge/backend/bl_haos/api/routes.py, .github/workflows/tests.yml, scripts/run-tests.ps1, scripts/run-tests.sh, TESTING.md]
key-decisions:
  - "Accepted local headless retirement with integration-first migration; live release remains gated for Phase 39."
  - "Retained /ws as operational transport; only ingress-specific HTTP management routes and UI assets were removed."
metrics:
  duration: "not captured (continued from prior execution context)"
  completed: 2026-10-28
  commits: 0
plan_head_before: a8289bfd01db3468ac5ad33a4203f774b409bc3b
plan_head_after: a8289bfd01db3468ac5ad33a4203f774b409bc3b
status: complete
actuals:
  tokens: 85448
  tasks: 4
  commits: 0
requirements-completed: [NUX-04]
---

# Phase 38 Plan 01: Headless Add-on and Ingress UI Retirement Summary

**The bridge is now a backend-only service: the legacy ingress management app and its unauthenticated management routes are removed while authenticated native controls and operational health remain.**

## Accomplishments

- Removed the tracked `modules/bridge/web_ui/` tree, its Node/Vite Docker build stage and static asset copy, static directory discovery, and all ingress/panel manifest keys.
- Added a constant, read-only `GET /` migration notice using the shared minimum integration release. It contains no host-derived content, assets, controls, redirects or API fallback.
- Removed legacy adapter, scan, device, ingress queue and settings HTTP handlers. Kept `/api/health`, diagnostics/incidents, authenticated `/api/native/*`, `/ws/native`, and the deprecated operational `/ws` publisher.
- Ported bridge API/SIL behavior assertions to authenticated native routes; added explicit retirement, auth and notice checks.
- Removed bridge frontend builder/install/audit steps and retargeted root CI, local runners, package-layout checks and `TESTING.md` to the distinct HA-native panel. No real-HA browser tests were substituted.

## Verification

| Check | Result |
|---|---|
| `py -3.12 -m pytest tests -q` from `modules/bridge` | PASS — 364 passed, 1 skipped; one Starlette/httpx deprecation warning |
| `npm --prefix modules/integration/panel_ui test` | PASS — 76 tests |
| `npm --prefix modules/integration/panel_ui run build` | PASS — TypeScript and Vite build |
| Integration `tests/test_package_layout.py` | PASS — 12 tests including fresh-build byte parity |
| CI YAML, PowerShell/Bash runner syntax, `git diff --check` | PASS |

## Staged Retirement Decision

The user directed execution using the plan's recommended staged approach. Local headless removal is accepted; migration order remains integration 0.2.22 first, verify native controls against the existing bridge, then bridge 0.2.71 only under Phase 39 authorization. Old Supervisor ingress links/bookmarks may stop resolving; the root notice cannot make removed ingress reachable. No host, install, restart, publication, Bluetooth operation, playback or live acceptance occurred.

## Deviations from Plan

- Replaced the retired visual/theme and frontend-presence tests with headless packaging and notice guards, rather than dropping the coverage.
- Updated `TESTING.md` in this plan to remove the deleted demo harness instructions and clarify the native mock panel boundary.
- No commits, pushes, STATE.md updates, or live/release actions were made, per user instruction and Phase 38 context.

## Deferred / Risks

- Ingress users who have not migrated lose the old management surface; the no-ingress candidate must remain locally uninstalled until the separate Phase 39 release gate.
- Legacy unauthenticated route behavior is intentionally unavailable; native integration controls require the configured bearer credential.

## Self-Check: PASSED

- Headless source/test files and CI/runner files exist; the bridge UI tree is absent.
- Verification results above were run from their documented module roots; no commits were made.
