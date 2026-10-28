---
phase: 38-headless-addon-ingress-ui-retirement
plan: 02
subsystem: compatibility
tags: [identity, semantic-versioning, repairs, diagnostics]
requires:
  - phase: 38-01
    provides: native-only bridge endpoints and identity surface
provides:
  - Additive authenticated product release metadata while protocol remains 1
  - Shared stable-version evaluator used during config flow, setup and reconnect
  - Persistent per-entry compatibility repairs, operation gate and safe diagnostics
affects: [38-03, 39]
tech-stack:
  added: []
  patterns: [AwesomeVersion semantic comparison, fixed compatibility result schema, stable HA issue identity]
key-files:
  created: [modules/integration/custom_components/bl_haos/compatibility.py, modules/integration/tests/unit/test_compatibility.py]
  modified: [modules/bridge/backend/bl_haos/api/routes.py, modules/integration/custom_components/bl_haos/client.py, modules/integration/custom_components/bl_haos/config_flow.py, modules/integration/custom_components/bl_haos/diagnostics.py, modules/integration/tests/test_ha_integration_sil.py]
key-decisions:
  - "Protocol and queue versions stay integers independent of add-on/integration product versions."
  - "Both product fields absent on protocol 1 is unknown_legacy with a warning; partial or invalid metadata is incompatible."
metrics:
  duration: "not captured (continued from prior execution context)"
  completed: 2026-10-28
  commits: 0
plan_head_before: a8289bfd01db3468ac5ad33a4203f774b409bc3b
plan_head_after: a8289bfd01db3468ac5ad33a4203f774b409bc3b
status: complete
actuals:
  tokens: 12932
  tasks: 3
  commits: 0
requirements-completed: [NUX-05]
---

# Phase 38 Plan 02: Compatibility and Repairs Summary

**The integration now evaluates authenticated product versions independently of native protocol 1, shows actionable Home Assistant repairs, blocks known-incompatible operation and clears the issue after recovery.**

## Accomplishments

- Bridge identity now adds `addon_version` from runtime `VERSION` and `min_integration_version` (`0.2.22`) while preserving bridge ID, protocol `version: 1`, credential fingerprint and conditional queue metadata.
- Added a shared compatibility evaluator using HA's `AwesomeVersion` with a strict stable `x.y.z` grammar; the numeric fallback is limited to the project's Windows unit harness where HA dependencies are absent.
- Integration version is read through Home Assistant's loaded integration metadata (with manifest fallback only for the HA-free unit harness). Minimum add-on supported is `0.2.70`.
- Manual/discovery config flows show a specific translated incompatibility error. Existing-entry setup and websocket reconnect create/update a stable, non-fixable issue; incompatible states block snapshot/stream setup and all client command/management entry points. Legacy protocol-1 peers with both product fields missing are warned but remain operational.
- Diagnostics expose only the whitelisted status/reason/protocol/product-version fields. Repairs persist through unload and clear on compatible recovery or config-entry removal.

## Verification

| Check | Result |
|---|---|
| Integration Windows-safe unit + package-layout suite | PASS — 115 tests |
| WSL compatibility/setup/recovery SIL selection | PASS — 3 selected tests |
| Full WSL fake-backend HA SIL suite | PASS — 98 tests, Python 3.14.4, Core-pinned venv |
| Bridge full suite including identity metadata assertions | PASS — 364 passed, 1 skipped |

## Compatibility Policy

- Compatible requires protocol 1, valid stable product metadata, integration at or above the bridge's declared minimum, and add-on at or above `0.2.70`.
- Both new product fields absent on protocol 1 means `unknown_legacy` (warning; supported behavior is not positively confirmed).
- Partial, malformed, prerelease/development metadata, unsupported protocol, too-old add-on or too-old integration is incompatible.
- Queue version does not affect product compatibility. Integration `0.2.21` cannot satisfy the new bridge's advertised `0.2.22` minimum; Phase 38-03 bumps the candidate manifest to `0.2.22`.

## Deviations from Plan

- A WSL invocation with plugin autoload disabled did not expose the HA SIL fixture plugin. Re-ran using the documented pinned WSL environment with normal plugin autoload; all 98 SIL tests passed. No package install was attempted.
- The first reconnect test draft accidentally used HA's real session; corrected it to use the fake bridge transport before rerunning. No live host was contacted.
- No commits, pushes, STATE.md updates, installs, publications or live actions were made, per user instruction and Phase 38 context.

## Deferred Rollout Limitation

- Legacy integrations predating this compatibility evaluator cannot enforce the minimum metadata announced by the new bridge. This is a rollout-order limitation, not an implementation stub; the integration-first staged migration is documented in Plan 03.

## Self-Check: PASSED

- Compatibility helper, integration tests, bridge identity assertions and translated flow/repair strings exist.
- The reported WSL SIL and Windows unit results completed successfully; no commit history was changed.
