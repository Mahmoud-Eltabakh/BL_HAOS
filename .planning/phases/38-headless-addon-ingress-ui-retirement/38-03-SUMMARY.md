---
phase: 38-headless-addon-ingress-ui-retirement
plan: 03
subsystem: migration
tags: [headless, compatibility, migration, release-candidate]
requires:
  - phase: 38-01
    provides: retired bridge UI and legacy management routes
  - phase: 38-02
    provides: product-version compatibility evaluation and Home Assistant repairs
provides:
  - Synchronized local candidate versions bridge 0.2.71 and integration 0.2.22 with native protocol 1
  - Integration-first upgrade, compatibility matrix, repair, data preservation, and rollback guidance
  - Documentation/version drift guards and final local regression evidence
affects: [39, NUX-04, NUX-05]
actuals:
  tokens: 12230
  tasks: 2
  commits: 0
tech-stack:
  added: []
  patterns: [manifest/runtime version parity, migration documentation drift tests]
key-files:
  created:
    - modules/bridge/tests/test_phase38_docs.py
    - modules/integration/tests/test_phase38_docs.py
  modified:
    - modules/bridge/config.yaml
    - modules/bridge/backend/bl_haos/constants.py
    - modules/bridge/DOCS.md
    - modules/bridge/README.md
    - modules/bridge/CHANGELOG.md
    - modules/bridge/tests/test_addon_config.py
    - modules/integration/custom_components/bl_haos/manifest.json
    - modules/integration/README.md
    - modules/integration/tests/test_package_layout.py
    - modules/integration/tests/unit/test_compatibility.py
    - README.md
    - TESTING.md
    - .planning/ROADMAP.md
    - .planning/REQUIREMENTS.md
key-decisions:
  - "Bridge 0.2.71 and integration 0.2.22 are local candidate metadata only; protocol remains integer 1."
  - "The staged integration-first migration is documented; Phase 39 authority gates remain unchanged."
  - "Preserve speakers, aliases, pairings, credentials, and settings; do not treat in-memory queues as restart-persistent."
requirements-completed: [NUX-04, NUX-05]
metrics:
  duration: "not captured (execution resumed from prior context)"
  completed: 2026-10-28
  commits: 0
plan_head_before: a8289bfd01db3468ac5ad33a4203f774b409bc3b
plan_head_after: a8289bfd01db3468ac5ad33a4203f774b409bc3b
status: complete
---

# Phase 38 Plan 03: Candidate Versions and Headless Migration Summary

**The 0.2.71/0.2.22 local candidate pair now has an integration-first migration contract, explicit compatibility/repair guidance, and executable documentation/version drift checks.**

## Accomplishments

- Bumped bridge manifest/runtime to **0.2.71** and integration manifest to **0.2.22**. Native protocol remains integer **1**; queue and other wire versions were not bumped.
- Added prominent bridge and integration migration guidance: retired add-on Ingress application and legacy management routes; retained native media/Speakers panels; internal health/watchdog/discovery on port 8099 without host-port mapping; retained operational `/ws` is not a UI.
- Documented matrix: candidate pair 0.2.71/0.2.22 is compatible; integration requires add-on 0.2.70 or newer; add-on 0.2.69 and integration 0.2.21 are known too old for this pair; both product fields absent on protocol 1 yield `unknown_legacy` warning; malformed/partial/prerelease metadata and unsupported protocol are incompatible. Older integrations cannot enforce newer bridge requirements.
- Added backup-first, integration-first migration and coordinated rollback steps; explained Repairs, preserved speaker/config data, ephemeral queue limits, and possible loss of old Ingress links. Root migration notice cannot recreate Supervisor access. Phase 39 remains required for installation, publication, deployment, live acceptance, and go/no-go.
- Updated bridge/integration/root README and TESTING instructions; preserved historical Phase 24/25/26 local-only and acceptance caveats. No generated panel bundle was manually edited or changed by the build.
- Added Phase 38 bridge and integration docs/version tests, and corrected the 38-01/38-02 summary actuals and deferred-rollout classification.

## Verification

| Check | Result |
|---|---|
| `cd modules/bridge; py -3.12 -m pytest tests -q` | PASS — **366 passed, 1 skipped**, one existing Starlette/httpx deprecation warning |
| Integration Windows unit/package/docs suite | PASS — **120 passed**, including package-layout and fresh-build parity |
| Integration Phase 38 / compatibility / package targeted rerun | PASS — **24 passed** |
| Pinned WSL fake-backend HA SIL (`tests`, excluding `tests/unit` and `tests/test_package_layout.py`) | PASS — **179 passed**; includes config-flow, repair, reconnect, recovery and Phase 38 docs/SIL coverage |
| Panel Vitest | PASS — **76 tests** |
| Panel TypeScript/Vite build | PASS |
| Fresh packaged-panel parity check | PASS — **1 passed**; packaged bundle unchanged |
| Bridge targeted version/docs/native transport checks | PASS — **23 passed** |
| YAML/JSON and PowerShell/Bash runner syntax | PASS |
| Root, bridge, integration `git diff --check` | PASS; Git reported only existing line-ending normalization warnings |
| Live HAOS/browser/playback, Bluetooth, publishing/deployment | NOT RUN — not authorized and outside Phase 38 local scope |

## Deviations from Plan

### Auto-adjustments

1. Root README and TESTING.md were included in the docs cleanup after the audit found stale positive Ingress setup and test-harness directions. Current documentation now distinguishes the retired add-on UI from the retained native HA panel.
2. The first WSL SIL invocation included `test_package_layout.py`; its fresh-build check selected Windows `npm.cmd` through WSL PATH and failed with `Exec format error`. Re-ran the HA-dependent SIL suite with a WSL-native PATH and excluded that non-SIL packaging test. Packaging/layout and fresh panel parity passed separately on Windows, so no evidence gate remains unrun. No package install or host access occurred.
3. The user explicitly prohibited commits, pushes, and history changes. All task changes and summaries remain uncommitted; root HEAD is unchanged. The earlier plan summaries now record zero commits and measured diff-derived actuals. Durations from the prior execution context were not recoverable and are marked as not captured instead of guessed.
4. The user directed the recommended staged migration approach instead of pausing at the ingress one-way-door checkpoint. The rollback, update order, and reachability limitation are documented; no installation or release action occurred.

## Deferred Risks and Authority Boundary

- Candidate metadata does not imply published, installed, or deployed artifacts. A legacy integration without the new evaluator cannot enforce a newer bridge's minimum integration requirement until the integration-first update is made.
- `unknown_legacy` is a warning, not proof of compatibility; mismatched versions are blocked by the updated integration.
- Existing Ingress links may stop resolving. The constant root notice cannot restore Supervisor ingress reachability; a grace release would require separate approval.
- Phase 39 must independently authorize and perform any live HAOS acceptance, deployment, publication, security/go-no-go, or release decision. Phase 30's pause is unchanged.

## Self-Check: PASSED

- Candidate manifests/runtime, new tests, required docs, roadmap/requirements updates, and all three Phase 38 summaries exist.
- Local verification results are listed above; no live-host action or commit was performed.
- `.planning/STATE.md` was intentionally left unchanged per the Phase 38 authority boundary and user instruction.
