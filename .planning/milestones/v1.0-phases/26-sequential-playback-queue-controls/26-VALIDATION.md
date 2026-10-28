---
phase: "26"
slug: "sequential-playback-queue-controls"
status: draft
nyquist_compliant: false
wave_0_complete: false
created: "2026-10-27"
---

# Phase 26 — Validation Strategy

> Local/mock-only execution is authorized. Production/live HA acceptance is not authorized; PL-01/02/03 remain pending, T-24-15 OPEN/HIGH and T-24-16 OPEN/MEDIUM remain open, and release/deployment remain blocked.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 9.0.3 / pytest-asyncio 1.4.0; Home Assistant Core 2026.10.3 SIL; Vitest 5.0.4; Playwright 1.63.0 |
| **Config files** | `modules/bridge/pytest.ini`, `modules/integration/pytest.ini`, `modules/integration/panel_ui/vitest.config.ts`, `modules/integration/panel_ui/playwright.mock.config.ts` |
| **Quick bridge command** | `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest tests/test_media_player.py -q` from `modules/bridge` |
| **Quick integration command** | `wsl.exe -d Ubuntu --cd /mnt/f/Workspace/BL-HAOS/modules/integration env BLHAOS_RUN_SIL=1 PYTHONDONTWRITEBYTECODE=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests/test_ha_integration_sil.py -q -p asyncio --asyncio-mode=auto -k "queue or playlist or play_media"` |
| **Quick panel command** | `npm --prefix modules/integration/panel_ui test -- --run` |
| **Mock browser command** | `npm --prefix modules/integration/panel_ui run test:mock-panel` |
| **Panel build** | `npm --prefix modules/integration/panel_ui run build -- --outDir "$env:TEMP/bl-haos-phase26-build"` |
| **Full local suite** | Bridge playback/API/native tests; pinned WSL integration SIL; panel Vitest/build; dedicated local mock Playwright |

SIL runs only in the documented Ubuntu WSL environment (Python 3.14.4, Core 2026.10.3, helper 0.13.374, aiohttp 3.14.5, pytest 9.0.3). Native Windows skips are not SIL passes. No host/provider credentials, live service, deployment, restart, or physical audio are required or authorized.

---

## Sampling Rate

- **After every task:** run the narrowest bridge unit, Core SIL, or Vitest assertion for the changed boundary.
- **After every plan wave:** run bridge playback/API tests, the relevant pinned Core SIL selectors, and complete panel Vitest/build.
- **Before phase verification:** run all bridge queue/native/API tests, full pinned integration SIL and units, full panel Vitest/build, and the complete local mock Playwright suite.
- **Max feedback latency:** target under 30 seconds for unit/component slices; use the narrowest relevant selector for slower SIL/Playwright checks.

---

## Per-Requirement Verification Map

| Requirement | Behavior | Test Type | Automated Command | Existing Home |
|-------------|----------|-----------|-------------------|---------------|
| PL-07 | Queue preserves custom-reference order and advances only on accepted natural process success; provider shortcuts are atomic HA-resolved items. | bridge unit + HA SIL | Focused `test_media_player.py` queue selectors; pinned `test_ha_integration_sil.py` queue-start selectors. | Existing bridge/media-player and integration SIL files; add queue tests. |
| PL-08 | Ingress, native HA, and HA Library controls display/control the same queue snapshot and modes. | bridge/API + integration SIL + Vitest + mock Playwright | `test_media_player.py`, `test_api.py`, `test_native_transport.py`; full panel Vitest and `test:mock-panel`. | Existing module-local bridge/integration/panel tests; add assertions and local queue harness. |
| PL-09 | Stop, replacement, disconnect, shutdown, and stale process completion invalidate queue generations without advancing. | bridge unit + HA SIL + mock browser | `test_media_player.py -k "queue or watcher or stop"`; focused SIL queue/disconnect selector; mock Playwright replacement flow. | Existing process tests; add deterministic fake-process races. |
| PL-10 | Resolution/process failures are visible and retain the current item; no automatic retry or skip. | bridge unit + HA SIL + panel test | Focused resolver/queue failure selectors and panel Vitest. | Existing resolver failure tests and queue test homes; extend. |

---

## Wave 0 Requirements

- [ ] `modules/bridge/tests/test_media_player.py` — deterministic queue lifecycle/fake-process contract tests.
- [ ] `modules/bridge/tests/test_api.py` and `test_native_transport.py` — versioned command, capability, retry, and URL-free snapshot tests.
- [ ] `modules/integration/tests/test_ha_integration_sil.py` — resolve-all-before-replace, exact target, native feature gating, multi-reference errors.
- [ ] `modules/integration/panel_ui/src/media-panel.test.tsx` or `playlist-library.test.tsx` — authenticated saved-playlist launch and session/failure states.
- [ ] `modules/bridge/web_ui` module-local tests or existing UI test home — ingress snapshot/control mapping; no new test framework.
- [ ] Deterministic queue API/event model in the existing local mock harness and dedicated mock spec.

No framework or package installation is planned.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Real Home Assistant/provider resolution and audible multi-item playback | PL-07/PL-10 | Local SIL/mock evidence cannot establish provider authorization, speaker audio, or host process timing; separately release-gated. | Post-milestone, only after explicit user authorization, use a configured disposable HA host and one explicitly selected connected speaker. |
| Actual HA-shell and assistive-technology queue controls | PL-08 | Mock browser geometry and DOM assertions do not prove live HA shell or AT behavior. | Post-milestone live acceptance after deployment approval; not part of this phase's local pass. |

---

## Validation Sign-Off

- [ ] Every plan task maps to an automated command or explicit Wave 0 test dependency.
- [ ] No three consecutive tasks lack automated verification.
- [ ] Bridge process completion, HA resolution, and cross-client state boundaries each have tests.
- [ ] No live host/provider/playback action is present in local commands.
- [ ] `nyquist_compliant: true` set after validation audit.

**Approval:** pending
