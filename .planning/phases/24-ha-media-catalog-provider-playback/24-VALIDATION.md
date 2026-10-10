---
phase: "24"
slug: "ha-media-catalog-provider-playback"
status: planned
nyquist_compliant: true
wave_0_complete: false
created: "2026-10-11"
---

# Phase 24 - Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest, pytest-asyncio, pytest-homeassistant-custom-component, Vitest, and Playwright |
| **Config file** | `modules/integration/pytest.ini`, `modules/bridge/pytest.ini`, `modules/bridge/web_ui/package.json` |
| **Quick run command** | `./scripts/run-tests.ps1 L1` |
| **Full suite command** | `./scripts/run-tests.ps1 all` (HA SIL is skipped on native Windows) |
| **Estimated runtime** | Not measured; establish focused-test latency during execution. |

---

## Sampling Rate

- **After every task commit:** Run the focused test for the touched surface; use `./scripts/run-tests.ps1 L1` for integration and bridge behavior.
- **After every plan wave:** Run `./scripts/run-tests.ps1 all` and the web UI build when panel assets change.
- **Before `$gsd-verify-work`:** Run the full suite and required Linux/WSL2 HA SIL checks.
- **Max feedback latency:** Measure focused tests during execution; keep individual test commands under 30 seconds where practical.

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 24-01-01 | 24-01 | 1 | PL-01, PL-02, PL-03 | T-24-01, T-24-02 | Core 2026.9.4 public panel/static APIs are exercised under Linux/WSL2, never accepted from a native-Windows skip. | HA SIL contract | `cd modules/integration && BLHAOS_RUN_SIL=1 python -m pytest tests/test_panel_registration.py tests/test_ha_integration_sil.py -q -p asyncio --asyncio-mode=auto` | Create focused contract test | Planned |
| 24-01-02 | 24-01 | 1 | PL-03 | T-24-02 | Target Core 2026.9.4 proves registration, serving, module load, injected authenticated calls, and denied/expired rejection before panel source work. | Blocking host checkpoint | Manual target-host probe; no local substitute is valid | Summary evidence created during execution | Planned |
| 24-02-01 | 24-02 | 2 | PL-03 | T-24-03, T-24-05 | Blocking decision locks the Core-verified module URL, custom-element name, package output, and lifecycle cleanup before packaging or consumption. | Blocking contract decision | Review Plan 24-01 host evidence and select `approve-contract` or `revise-contract`; no downstream implementation may run before approval | Plan 24-01 summary evidence | Planned |
| 24-02-02 | 24-02 | 2 | PL-01, PL-02, PL-03 | T-24-03, T-24-04, T-24-05 | Injected `hass` browses one root and launches one unchanged opaque reference on exactly one explicit entity. | Build + HA SIL tracer | `npm --prefix modules/integration/panel_ui run build && cd modules/integration && BLHAOS_RUN_SIL=1 python -m pytest tests/test_panel_registration.py -q -p asyncio --asyncio-mode=auto` | Source/build harness created by task | Planned |
| 24-02-03 | 24-02 | 2 | PL-03 | T-24-03, T-24-04, T-24-05 | Lifecycle, package output, browser persistence, bridge-request, and resolved-URL boundaries are pinned. | Vitest + package + HA SIL | `npm --prefix modules/integration/panel_ui test -- --run && cd modules/integration && python -m pytest tests/test_package_layout.py -q -p asyncio --asyncio-mode=auto && BLHAOS_RUN_SIL=1 python -m pytest tests/test_panel_registration.py -q -p asyncio --asyncio-mode=auto` | Created/extended by task | Planned |
| 24-03-01 | 24-03 | 3 | PL-01 | T-24-06 | Audio/playlist leaves retain hierarchy and HA metadata/capabilities without provider-name guesses. | HA SIL | `cd modules/integration && BLHAOS_RUN_SIL=1 python -m pytest tests/test_ha_integration_sil.py -q -p asyncio --asyncio-mode=auto -k "browse or playlist or audio"` | Extend existing SIL | Planned |
| 24-03-02 | 24-03 | 3 | PL-02 | T-24-07, T-24-08 | Original opaque ID resolves for one selected entity; denied/unavailable/unresolvable paths issue no fallback command. | HA SIL | `cd modules/integration && BLHAOS_RUN_SIL=1 python -m pytest tests/test_ha_integration_sil.py -q -p asyncio --asyncio-mode=auto -k "play_media or resolve or denied or unavailable"` | Extend existing SIL | Planned |
| 24-04-01 | 24-04 | 3 | PL-03 | T-24-09, T-24-10 | Catalog states preserve target/item selection and allow only user-activated same-request retry. | Vitest | `npm --prefix modules/integration/panel_ui test -- --run src/media-panel.test.tsx` | Extend tracer test | Planned |
| 24-04-02 | 24-04 | 3 | PL-03 | T-24-11 | Ingress CTA navigates to the HA panel and makes zero catalog/play requests through add-on APIs. | Vitest | `npm --prefix modules/bridge/web_ui test -- --run src/App.test.tsx` | Create App test | Planned |
| 24-04-03 | 24-04 | 3 | PL-03 | T-24-09, T-24-10 | Keyboard, focus, live-region, overflow, and reduced-motion contracts are automated before host layout review. | Vitest + build | `npm --prefix modules/integration/panel_ui test -- --run src/media-panel.test.tsx && npm --prefix modules/integration/panel_ui run build` | Extend tracer test | Planned |
| 24-05-01 | 24-05 | 4 | PL-02, PL-03 | T-24-12 | Integration log capture omits raw URL, host, path, query, credential, token, and password sentinels. | HA SIL caplog | `cd modules/integration && BLHAOS_RUN_SIL=1 python -m pytest tests/test_ha_integration_sil.py -q -p asyncio --asyncio-mode=auto -k "play_media and (log or redact)"` | Extend existing SIL | Planned |
| 24-05-02 | 24-05 | 4 | PL-03 | T-24-13 | Native route logs/errors omit all URL sentinels while authenticated execution still receives the URL. | Bridge pytest caplog | `cd modules/bridge && python -m pytest tests/test_api.py -q -p asyncio --asyncio-mode=auto -k "native and (play or log or redact)"` | Extend existing test | Planned |
| 24-05-03 | 24-05 | 4 | PL-03 | T-24-14 | Player logs/errors omit all URL sentinels while one validated subprocess argument remains. | Bridge pytest caplog | `cd modules/bridge && python -m pytest tests/test_media_player.py -q -p asyncio --asyncio-mode=auto -k "url or log or redact"` | Extend existing test | Planned |
| 24-06-01 | 24-06 | 5 | PL-01, PL-02, PL-03 | T-24-15, T-24-16 | Authenticated host scenarios cover provider metadata, one-target play, denied/expired failure, leakage checks, and 375/768/1440 screenshots. | Target-host Playwright + human backstop | `npm --prefix modules/integration/panel_ui exec playwright test -- --config e2e/playwright.config.ts` | Create host harness | Planned |
| 24-06-02 | 24-06 | 5 | PL-01, PL-02, PL-03 | T-24-16 | Content-sensitive assertions require the shipped HA-owned boundary/procedure and reject positive claims for stored credentials, bridge resolution, Phase 25/26 features, or retired Docker E2E acceptance. | Static documentation pytest | `python -m pytest modules/integration/tests/test_package_layout.py -q && cd modules/bridge && python -m pytest tests/test_addon_config.py tests/test_frontend_assets.py -q -p asyncio --asyncio-mode=auto` | Extend existing static test patterns | Planned |
| 24-06-03 | 24-06 | 5 | PL-03 | T-24-16 | User-visible ingress entry is versioned and changelog scope excludes bridge catalog/provider/queue ownership. | Bridge static pytest | `cd modules/bridge && python -m pytest tests/test_addon_config.py tests/test_frontend_assets.py -q -p asyncio --asyncio-mode=auto` | Existing tests | Planned |

---

## Wave 0 Requirements

- [ ] **24-01-01:** Upgrade/check the SIL Core and compatible test-helper pins at `2026.9.4`; execute under Linux/WSL2.
- [ ] **24-01-01 / 24-02-03:** Add public panel/static contract and lifecycle cleanup tests.
- [ ] **24-02-02 / 24-02-03:** Add the custom-element build/test harness with injected `hass` and forbidden-boundary assertions after the Task 24-02-01 contract decision.
- [ ] **24-05-01 / 24-05-02 / 24-05-03:** Add captured-log URL sentinel tests for all three required paths.
- [ ] **24-06-01 / 24-06-02:** Add and document repeatable HA 2026.9.4 authenticated, denied, expired-session, and viewport host validation.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Pre-source architecture gate | PL-03 | Registration/static serving and injected `hass` must be observed on the target Core before panel source changes. | Task 24-01-02: on Core/HAOS 2026.9.4 prove the six named public-host observations; reject any undocumented fallback. |
| Registered panel browses/plays through actual authenticated host | PL-03 | Integration routing, supplied `hass`, session expiry, and provider access require the supported HA frontend host. | Task 24-06-01: verify module load, current-session browse, one selected target with original media-source ID, and denied/expired fail-closed behavior. |
| Provider-specific audio/playlist metadata is accepted without flattening hierarchy | PL-01, PL-02 | Enabled provider metadata is not observable from native Windows or generic mocks. | Browse one configured audio provider and one provider playlist; verify hierarchy/capabilities, then unavailable and denied items. |
| Responsive/accessibility host acceptance | PL-03 | Layout, contrast, screen-reader integration, and HA-shell focus behavior are not established by jsdom. | Review 375px, 768px, and 1440px screenshots and manually verify target selector, long speaker name, 44px controls, keyboard/focus, labels/live region, contrast, and reduced motion. |

---

## Validation Sign-Off

- [x] All implementation tasks have `<automated>` verify; the pre-source host gate is explicitly manual and blocking.
- [x] Sampling continuity: no 3 consecutive tasks without automated verify.
- [x] Wave 0 requirements map to concrete generated task IDs.
- [x] No watch-mode flags.
- [ ] Focused-test latency measured and recorded
- [x] `nyquist_compliant: true` set after plan/task reconciliation.

**Approval:** planning contract reconciled; execution evidence pending
