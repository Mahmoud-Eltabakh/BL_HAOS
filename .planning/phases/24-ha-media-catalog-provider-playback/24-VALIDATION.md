---
phase: "24"
slug: "ha-media-catalog-provider-playback"
status: validated
validation_scope: user-approved-local-mock-progression
nyquist_compliant: true
local_coverage_complete: true
wave_0_complete: true
hardware_deferred: true
human_verification_pending: true
production_acceptance_pending: true
audited: "2026-10-24"
created: "2026-10-11"
---

# Phase 24 - Validation Strategy

> Final local coverage audit. Required host/provider/hardware acceptance remains
> pending; validated does not mean Phase 24, Plan 06 or PL-01/02/03 is complete.
> The current map below supersedes historical pending/review/count statements in
> the preserved chronological execution evidence.

## User-Approved Full Mock Autonomous Progression

On 2026-10-24 the user explicitly selected mock-only local progression. The five
`mock-catalog.spec.ts` browser cases and three retained viewport captures are
the Phase 24 Plan 06 local acceptance artifact for sequencing phases 25/26.
The actual test uses a headless mock hass/entity/media-source implementation;
it is not a live Core session, configured provider, real authorization check or
physical playback test. A fresh run passed 5/5 cases in 5.4 seconds.

Scope effect: local phase progression may continue under the user's mock-only
decision. This is not release/production acceptance and does not complete
PL-01/PL-02/PL-03 for a deployed system. Keep live provider, actual expired
session, deployed-panel, real audio and HA-shell/accessibility evidence deferred
post-milestone. Keep T-24-15 OPEN/HIGH; the user explicitly chose to keep that
host security threat open while proceeding with local mock work, not accept or
close the risk. No publication, installation, Core restart, session mutation or
playback is authorized by this scope override.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest, pytest-asyncio, pytest-homeassistant-custom-component, Vitest, and Playwright |
| **Config file** | `modules/integration/pytest.ini`, `modules/bridge/pytest.ini`, `modules/bridge/web_ui/package.json` |
| **Quick run command** | `./scripts/run-tests.ps1 L1` |
| **Full suite command** | `./scripts/run-tests.ps1 all` (HA SIL is skipped on native Windows) |
| **Measured final runtime** | Full non-unit Core 23.49s; isolated WSL units 1.36s; Windows bridge 13.24s. |
| **Active Core contract** | Approved Core 2026.10.3 / helper 0.13.374 / aiohttp 3.14.5 / pytest 9.0.3. Earlier disposable mechanism probe accepted and removed; final production host gate still pending. |

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
| 24-01-01 | 24-01 | 1 | PL-01, PL-02, PL-03 | T-24-01, T-24-02 | Core 2026.10.3 public panel/static APIs are exercised under Linux/WSL2, never accepted from a native-Windows skip. | HA SIL contract | Final gate G1 below | test_panel_registration.py | COVERED: G1, 127 non-unit passes |
| 24-01-02 | 24-01 | 1 | PL-03 | T-24-02 | Target Core 2026.10.3 proves the public mechanism; denied/invalid access was observed, not actual expiry. | Blocking host checkpoint | Previously authorized disposable silent probe, not rerun | 24-01-SUMMARY and accepted validation evidence | ACCEPTED: one restart used, probe removed; not production acceptance |
| 24-02-01 | 24-02 | 2 | PL-03 | T-24-03, T-24-05 | Fixed module URL, element, package output and inert-route lifecycle contract. | Blocking contract decision | Existing explicit approve-contract | Approval recorded in STATE and user scope | ACCEPTED: local implementation only |
| 24-02-02 | 24-02 | 2 | PL-01, PL-02, PL-03 | T-24-03, T-24-04, T-24-05 | Injected hass, opaque one-target dispatch and public lifecycle. | Build + SIL + Vitest | G1, G4, G5 | media-panel.tsx, test_panel_registration.py | COVERED locally; host backstop pending |
| 24-02-03 | 24-02 | 2 | PL-03 | T-24-03, T-24-04, T-24-05 | Lifecycle, packaged output and forbidden browser boundaries. | Vitest + package + SIL | G1, G4 | media-panel.test.tsx, lifecycle/package tests | COVERED locally, including cancellation/late failure |
| 24-03-01 | 24-03 | 3 | PL-01 | T-24-06 | Provider-neutral audio/playlist filtering preserves metadata and hierarchy. | HA SIL | G1 | native_audio_browse tests | COVERED locally; real provider pending |
| 24-03-02 | 24-03 | 3 | PL-02 | T-24-07, T-24-08 | One-target resolution, bounded failures and one transport submission. | HA SIL + isolated units | G1, G2 | native_play_media tests, test_client_commands.py | COVERED locally; physical playback pending |
| 24-04-01 | 24-04 | 3 | PL-03 | T-24-09, T-24-10 | Hierarchy, search, bounded errors and same-request manual retry. | Vitest | G4 | media-panel.test.tsx | COVERED locally |
| 24-04-02 | 24-04 | 3 | PL-03 | T-24-11 | Navigation-only top-frame ingress CTA. | Vitest | G3 | App.test.tsx | COVERED locally |
| 24-04-03 | 24-04 | 3 | PL-03 | T-24-09, T-24-10 | Semantic focus/live-region and CSS motion/overflow contracts. | Vitest + builds | G4, G5, G6 | media-panel.test.tsx | COVERED locally; actual HA geometry/AT manual-only |
| 24-05-01 | 24-05 | 4 | PL-02, PL-03 | T-24-12 | Real entity/client/listener logs and displayed errors omit sentinels. | HA SIL caplog | G1 | play_media/native_websocket redact tests | COVERED locally |
| 24-05-02 | 24-05 | 4 | PL-03 | T-24-13 | Authenticated route preserves internal URL and omits log/error sentinels. | Bridge pytest caplog | G3 | test_api.py | COVERED locally |
| 24-05-03 | 24-05 | 4 | PL-03 | T-24-14 | Validated exact URL argv, bounded parser/stderr/background errors. | Bridge pytest caplog | G3 | test_media_player.py | COVERED locally; existing unrelated POSIX skip retained |
| 24-06-01 local scope | 24-06 | 5 | PL-01, PL-02, PL-03 | T-24-15, T-24-16 | Mock-HA browse hierarchy, opaque playlist dispatch, one mock target, 44px controls, responsive captures and keyboard navigation. | Mock Playwright + human screenshot review | `npm --prefix modules/integration/panel_ui run test:mock-panel` | mock-harness.html, mock-catalog.spec.ts, three ignored screenshots | COVERED for user-approved local progression; not live proof |
| 24-06-01 production backstop | 24-06 | post-milestone | PL-01, PL-02, PL-03 | T-24-15, T-24-16 | Real provider/session, physical audio, HA shell/accessibility and leakage acceptance. | Authorized target-host Playwright + human | `npm run test:host` only after all inputs/authorization | Separate catalog.spec.ts host harness | DEFERRED; release blocker |
| 24-06-02 | 24-06 | 5 | PL-01, PL-02, PL-03 | T-24-16 | Content-sensitive docs and explicit undeployed/excluded claims. | Static pytest | G1, G3 | test_package_layout.py, test_addon_config.py | COVERED locally |
| 24-06-03 | 24-06 | 5 | PL-03 | T-24-16 | Bridge 0.2.69 constants/config/top changelog; local integration candidate 0.2.20 differs from live 0.2.19. | Static pytest + structured manifest check | G1, G3, package-layout candidate assertion | Existing static tests | COVERED locally; candidates unpublished |

---

## Wave 0 Requirements

- [x] **24-01-01:** Pin Core `2026.10.3` and helper `0.13.374`; Linux/WSL2 gate passed 24 tests on 2026-10-24. This does not approve Task 24-01-02.
- [x] **24-01-01 / 24-02-03:** Public API and real HTTP lifecycle/cancellation tests exist and pass.
- [x] **24-02-02 / 24-02-03:** Approved injected-hass build/test infrastructure exists and passes.
- [x] **24-05-01 / 24-05-02 / 24-05-03:** All three captured-log sentinel paths exist and pass.
- [x] **24-06-01 / 24-06-02:** Host harness and documented procedure exist; preparation only, host execution remains mandatory and pending.

---

## Manual-Only Verifications

The user-approved **Full Mock Autonomous Progression** permits Phase 25/26
local mock development after 24-06-01 local checks pass. It does not waive or
claim the post-milestone production acceptance rows. PL-01/02/03 remain pending
for live provider/audio behavior; T-24-15 remains OPEN/HIGH and release stays
blocked.

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Pre-source architecture gate (accepted, not rerun) | PL-03 | Previously observed on the approved target with a disposable silent probe. | User accepted the recorded mechanism evidence; one restart used and probe removed. Actual expiry was not part of that acceptance. |
| Registered panel browses/plays through actual authenticated host | PL-03 | Integration routing, supplied `hass`, session expiry, and provider access require the supported HA frontend host. | Task 24-06-01: verify module load, current-session browse, one selected target with original media-source ID, and denied/expired fail-closed behavior. |
| Provider-specific audio/playlist metadata is accepted without flattening hierarchy | PL-01, PL-02 | Enabled provider metadata is not observable from native Windows or generic mocks. | Browse one configured audio provider and one provider playlist; verify hierarchy/capabilities, then unavailable and denied items. |
| Responsive/accessibility host acceptance | PL-03 | Layout, contrast, screen-reader integration, and HA-shell focus behavior are not established by jsdom. | Review 375px, 768px, and 1440px screenshots and manually verify target selector, long speaker name, 44px controls, keyboard/focus, labels/live region, contrast, and reduced motion. |

---

## Validation Sign-Off

- [x] All implementation tasks have `<automated>` verify; the pre-source host gate is explicitly manual and blocking.
- [x] Sampling continuity: no 3 consecutive tasks without automated verify.
- [x] Wave 0 requirements map to concrete generated task IDs.
- [x] No watch-mode flags.
- [x] Focused two-file Linux SIL latency measured and recorded: 4.06s; broader acceptance remains pending.
- [x] Final map reconciles all 16 tasks: 13 automated local contracts covered, two prior explicit human decisions accepted, one mandatory host task partial.
- [ ] Full Nyquist acceptance: actual provider/session/hardware/layout evidence pending; `nyquist_compliant: false` prevents a fake full pass.

**Approval:** Earlier mechanism probe and fixed production contract accepted for local work. Final production deployment, real play and host acceptance are not authorized or complete. No Plan 06 SUMMARY or global completion update is permitted.

## Autonomous Resume Evidence - 2026-10-24

- Task 24-01-01 prerequisite confirmed in the existing Ubuntu WSL virtual environment: Linux, Home Assistant 2026.9.4, pytest-homeassistant-custom-component 0.13.367. No installs or dependency changes were made.
- Executed from modules/integration using /home/mse/.venvs/bl-haos-sil-2026.9.4/bin/python and BLHAOS_RUN_SIL=1:

```text
python -m pytest tests/test_panel_registration.py tests/test_ha_integration_sil.py -q -p asyncio --asyncio-mode=auto
24 passed in 5.86s
```

- Task 24-01-02 remains BLOCKED. Read-only inspection through the shared Home Assistant browser reports Core 2026.10.3, not the plan's exact 2026.9.4 target. The current session is connected and exposes public hass.callWS/callService functions, but their presence alone does not prove the six required host observations.
- No disposable integration probe was installed; no panel source was created; no browse/play service, denied/expired-session manipulation, deployment, restart, downgrade or token handling occurred.
- The user was unavailable at the version-contract decision. Generic autonomous delegation was not treated as approval to replace the exact-version gate. Resume after explicit rebaseline approval or a matching target host; preserve the no-fallback architecture.
- No plan summary, phase completion, requirement completion or milestone lifecycle acceptance is claimed by this partial evidence. Phases 25-26 were not started; phase 27 remains locally verified and undeployed.

## Approved 2026.10.3 Rebaseline Addendum - 2026-10-24

The user explicitly approved replacing the active Core 2026.9.4 contract with 2026.10.3. The preceding resume evidence is historical and unchanged; its former version-decision blocker is superseded, not its pending public-host observations.

- Parent RED evidence: after setting `TARGET_CORE_VERSION = "2026.10.3"`, the old `/home/mse/.venvs/bl-haos-sil-2026.9.4/bin/python` run of `tests/test_panel_registration.py -k sil_runtime_matches_target_core_release` failed as intended (`2026.9.4 != 2026.10.3`, 1 failed, 2 deselected). This was supplied by the parent, not rerun here.
- Created only `/home/mse/.venvs/bl-haos-sil-2026.10.3` with `/usr/bin/python3.14 -m venv`; Ubuntu WSL Python is 3.14.4. Older environments were not overwritten.
- Public PyPI JSON confirmed helper `0.13.374` requires Python `>=3.14`, Core `==2026.10.3`, and pytest `==9.0.3`; Core requires Python `>=3.14.2` and aiohttp `==3.14.5`. Artifact URLs use `files.pythonhosted.org`. Exact source references are in the research addendum.
- Initial resolver dry-run preserving aiohttp `3.14.3` failed with `ResolutionImpossible`: Core requires `3.14.5`. Only that additional pin changed; pytest `9.0.3` was preserved. The corrected dry-run and install succeeded using the public index, and `pip check` reported `No broken requirements found.`

Commands run in Ubuntu WSL from `/mnt/f/Workspace/BL-HAOS/modules/integration`:

```sh
/home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pip --isolated install --dry-run --index-url https://pypi.org/simple -r requirements-sil.txt
/home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pip --isolated install --index-url https://pypi.org/simple -r requirements-sil.txt
BLHAOS_RUN_SIL=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests/test_panel_registration.py tests/test_ha_integration_sil.py -q -p asyncio --asyncio-mode=auto
/home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pip check
```

Measured gate: Linux, Python 3.14.4, pytest 9.0.3, helper 0.13.374, **24 collected, 24 passed in 4.06s, no skips** (3 panel/static tests and 21 integration SIL tests). No local test-contract or production API repair was needed. These tests exercise public registration calls, not live module serving, browser injection, or session denial.

Phase 24 remains PAUSED at Task 24-01-02 (`blocking-human`). The parent must obtain evidence on Core/HAOS 2026.10.3 for static serving, public panel registration, custom-element loading, authenticated `hass.callWS` browse, `hass.callService` play-media access, and denied/expired rejection. SIL success and version approval do not approve these observations. No live host was accessed or changed in this rebaseline; no probe installation, deployment, restart, token handling, panel source/build harness, summary, plan/requirement completion, or commit/staging/branch operation occurred. Phase 27 and Bluetooth work were untouched.

## Authorized Live Contract Probe - 2026-10-24

This run supersedes the earlier missing-live-evidence blocker, not the required human acceptance. The user approved the temporary probe and one Core restart if needed. No Bluetooth fix or production media panel was deployed.

### Preparation

- Disposable source is retained under host-probe/custom_components/bl_haos_phase24_probe with its local test in host-probe/test_probe.py. This is test-only evidence, not the Phase 24 production panel.
- Local real-Core 2026.10.3 test: 1 passed in 1.15s. It exercised config flow, public panel registration, silent service dispatch, duplicate rejection and unload; static registration was mocked locally and verified live below. JavaScript checks also exercised explicit invocation, sanitization, target selection and denied calls.
- Uploaded only the five integration files to a previously absent /config/custom_components/bl_haos_phase24_probe directory. No configuration YAML or existing integration was edited.
- Initial config flow returned Invalid handler before Core discovery. ha core check passed, then exactly one authorized ha core restart succeeded. No second restart was requested or performed.

### Observations

| Observation | Live evidence | Result |
|-------------|---------------|--------|
| Exact target | Live injected hass and SSH report Core 2026.10.3 on HTTP port 80 | Pass |
| Static serving | Public async_register_static_paths module /bl_haos_phase24_probe/probe.js returned HTTP 200 with the expected custom-element definition | Pass |
| Public panel registration | panel_custom.async_register_panel exposed bl-haos-phase24-probe in the HA panel map and its route loaded | Pass |
| Custom element and injected hass | Actual bl-haos-phase24-probe element loaded and reported injected=true, version=2026.10.3 | Pass |
| Authenticated browse | The element called its injected hass.callWS with media_source/browse_media and received an object; no provider payload or resolved URL was returned to diagnostic output | Pass |
| Authenticated play-media service | Injected hass.callService targeted only media_player.bl_haos_phase24_probe_sink; service=true, recorded=true, call_count=1, media_type=music | Pass |
| Denied access | Separate credentials-omitted REST /api/config returned 401; an independent WebSocket using an invalid non-secret sentinel received auth_invalid | Pass |

The sink implements only a counter and sanitized media type; it never resolves a reference, launches playback or addresses the real speaker. This establishes public service dispatch, not physical audio playback. No real access token was copied or persisted. The active user session stayed connected and the sink count remained one after denied requests. Actual session expiration was not forced; denied/invalid-session rejection was the observed branch of the plan's denied-or-expired check.

### Cleanup and Limitations

- Removed the probe config entry through the authenticated public config-entry API. Server-side config_entries/get and states confirmed no probe entries or entities; the panel map confirmed no probe panel.
- A browser wait timed out during unload navigation and the frontend logged a transient removed-panel error. Authoritative server checks afterward confirmed cleanup. No repeated delete or restart was used.
- Removed only the integration directory created for this run, including generated cache files. The module URL then returned HTTP 404 with cache bypassed; currentSessionConnected=true, panelAbsent=true and probeEntityAbsent=true.
- Home Assistant retains the unloaded static route object in memory until a normal future restart, but the underlying file is gone and the route returns 404. No follow-up restart was performed.
- Returned the shared browser to the original BL-HAOS add-on route. Existing integration files, Bluetooth pairing and version 0.2.68 changes were not deployed or modified on the host.
- These observations prove the public registration/injection mechanism using disposable identifiers. The final production URL, custom-element name, package output and lifecycle remain the separate Task 24-02-01 decision; no approval for that contract is inferred here.
- User accepted Task 24-01-02 evidence on 2026-10-24. Plan 24-01 summary records that acceptance. This does not complete phase 24, PL-01/PL-02/PL-03, final physical playback acceptance, or the separate production panel contract decision.

## Plan 24-02 Local Tracer Evidence - 2026-10-24

This addendum supersedes earlier statements that Task 24-02-01 is pending.
The user explicitly supplied `approve-contract`; the parent recorded it in
STATE.md before this execution. Only plan 24-02 was executed. Plans 03-06,
phase/requirement completion, deployment and further restarts remain out of scope.

### Approved Contract and Ownership

- URL: `/api/bl_haos/catalog/bl-haos-media-panel.js`.
- Element: `bl-haos-media-panel`; sidebar path: `/bl-haos-media`.
- Packaged artifact: `modules/integration/custom_components/bl_haos/panel_static/bl-haos-media-panel.js`.
- The integration serializes per-entry ownership with an asyncio lock and owner set.
  Its public static route points to one integration-owned temporary served copy,
  not the packaged source. Final unload/failure deletes that copy and removes the
  panel with `frontend.async_remove_panel`. Actual HTTP 200/404/reload is tested.
- Core 2026.10.3 has no public static unregister. The inert route and its stable
  owned pathname remain in memory; later setup recreates the file and reuses the
  route without private router mutation. An uncertain static-registration error
  blocks retries for that Core lifetime, leaving HTTP 404; no restart was executed.
- Failed second-owner setup cannot remove the first owner's panel or module.
  Tests cover refused unload, initialization `ConfigEntryNotReady`, partial public
  registration, platform failure/cancellation, and actual cancellation while
  registration is in flight.

### RED and GREEN Evidence

All Linux commands below ran from `/mnt/f/Workspace/BL-HAOS/modules/integration`
with `/home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python`, Core 2026.10.3,
helper 0.13.374, Python 3.14.4 and pytest 9.0.3.

1. Initial fixture attempt: 4 setup errors, 3 deselected, 1.17s, because full
	frontend setup requires optional `hass_frontend`. This is NOT behavior RED.
	Removed unnecessary full frontend setup; public panel registration stays real.
2. Required lifecycle RED, before production changes:
	`BLHAOS_RUN_SIL=1 python -m pytest tests/test_panel_registration.py -q -p asyncio --asyncio-mode=auto -k owned_panel --tb=short --show-capture=no`:
	**4 failed, 3 deselected, 1.24s** (404 instead of 200, missing registration,
	and unclosed client after platform failure/cancellation).
3. Initial implementation exposed test-server startup ordering and repeated
	directory cleanup. Deferred HTTP client startup until registration and made
	removal idempotent. Same focused command: **4 passed, 3 deselected, 1.07s**.
4. Windows static package RED:
	`.venv/Scripts/python.exe -m pytest -c modules/integration/pytest.ini modules/integration/tests/test_package_layout.py -q -k panel_build --tb=short`:
	**1 failed, 5 deselected, 0.11s**, missing component source.
5. Frontend pre-implementation run:
	`npm --prefix modules/integration/panel_ui test -- --run`:
	**1 failed suite, 0 collected tests, 626ms**, missing component import.
	This is scaffold/import evidence, not an assertion-level behavior RED.
	First implemented run: **5 passed, 1.00s**.
6. TypeScript build initially rejected generic mock typing and matcher augmentation.
	Narrowed typed `callWS` to the browse-only response contract and loaded Vitest
	matcher types. The subsequent TypeScript/Vite build passed in **1.07s**.
7. Partial-public-registration RED:
	`BLHAOS_RUN_SIL=1 python -m pytest tests/test_panel_registration.py -q -p asyncio --asyncio-mode=auto -k partial_public --tb=short --show-capture=no`:
	**1 failed, 11 deselected, 0.53s**, real panel remained after registration raised.
	Ownership-safe rollback repair plus declared HTTP dependency and required tracing:
	**39 passed, 6.74s** across panel, existing SIL and package tests.
8. Partial-static-registration/cancellation check:
	`BLHAOS_RUN_SIL=1 python -m pytest tests/test_panel_registration.py -q -p asyncio --asyncio-mode=auto -k 'partial_static or actual_cancellation' --tb=short --show-capture=no`:
	**1 failed, 1 passed, 12 deselected, 1.21s**; retry attempted duplicate public
	route registration. Fail-closed lifetime guard: **2 passed, 12 deselected, 0.74s**.

### Final Gates

| Gate | Exact Command / Scope | Result |
|------|-----------------------|--------|
| Linux real-Core suite | `BLHAOS_RUN_SIL=1 python -m pytest tests --ignore=tests/unit -q -p asyncio --asyncio-mode=auto --tb=short --show-capture=no` | **41 passed, zero skipped, 7.10s**: 21 existing SIL, 14 panel/public HTTP, 6 package |
| Linux isolated unit suite | `BLHAOS_RUN_SIL=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest tests/unit -q -p asyncio --asyncio-mode=auto --tb=short --show-capture=no` | **54 passed, zero skipped, 1.84s** |
| Windows portable package/unit checks | `.venv/Scripts/python.exe -m pytest -c modules/integration/pytest.ini modules/integration/tests/test_package_layout.py modules/integration/tests/unit -q --tb=short` | **60 passed, 1.17s**; not HA runtime proof |
| Panel Vitest | `npm --prefix modules/integration/panel_ui test -- --run` | **6 passed, 1.15s**; explicit target, opaque ID/type, injected custom element, unavailable target, bounded service error and denied browse, no fetch/storage |
| Reproducible install | `npm --prefix modules/integration/panel_ui ci --registry=https://registry.npmjs.org --ignore-scripts --no-audit --no-fund` | **168 packages, 10s**; initial verified install was 29s |
| TypeScript + Vite | `npm --prefix modules/integration/panel_ui run build` | Fixed single JS module; no external CSS/chunk required |
| Chromium built-module fixture | Existing bridge Playwright package; temporary loopback-only server; 375/768/1440 x 900; server closed after run | All three passed: no horizontal overflow, 44px controls, opaque ID/one-target dispatch, reduced-motion transition 0s, zero page errors |
| Patch hygiene | `git -C modules/integration diff --check` | Passed |

The all-in-one Linux `pytest tests` attempt initially reported **24 failed,
64 passed, 7.85s**: production setup lacked declared HTTP/tracing, and unit tests
imported real Core client helpers before their stubs. The former was repaired;
the latter is avoided by running the real-Core suite and standalone unit suite
in separate processes. Standalone unit collection then exposed seven missing
panel/HTTP import-stub errors; existing `tests/unit/conftest.py` now supplies
fail-fast test-only names. Real-Core panel tests do not use these stubs.
The final two Linux processes cover **95 tests total**, not a claimed green
single-process run. No skip is counted as HA proof.

### Package Provenance and Limits

Public `https://registry.npmjs.org/<encoded-name>/<exact-version>` metadata
confirmed all 13 direct package identities, exact versions, registry tarballs
and integrity fields before installation. Existing bridge-installed versions
were reused: React/react-dom 18.2.0, lucide-react 0.344.0, @types/react 18.2.66,
@types/react-dom 18.2.22, @vitejs/plugin-react 4.7.0, TypeScript 5.2.2,
Vite 7.3.7, Vitest 5.0.4, jsdom 25.0.1, @testing-library/react 16.3.3,
@testing-library/jest-dom 6.9.1, @testing-library/user-event 14.6.7.
Only the new panel package was installed; no existing dependency manifest or
lockfile was updated. No provider/auth package was added. Context7's installed
CLI verified Vite 7 `build.lib`, ES output and `fileName` contracts against
`https://v7.vite.dev/config/build-options`.

The bundle includes its Neumorphic CSS string in the custom-element shadow root.
Generated output is not a source declaration. The panel accepts only injected
`hass`, uses browse-only `callWS` and one-target `callService`, preserves opaque
references/types, and never resolves media, copies tokens or invokes a provider,
bridge catalog, browser fetch or persistence path. Safe same-origin HA thumbnails
are rendered when supplied; the Chromium fixture used icon fallbacks, not live
provider artwork. Temporary screenshots were inspected outside the repository:
`%TEMP%/bl-haos-plan24-02-visual/panel-{375,768,1440}.png`.

No live HA session, provider, physical speaker, deployment, extra restart,
radio operation, token access, branch, staging or commit was used. Parent-owned
STATE/ROADMAP/REQUIREMENTS and all phase 27 source/evidence were untouched.
Live authenticated production-panel/provider/physical-audio acceptance remains
in plan 24-06; full catalog states/search/entry actions and filtering/redaction
remain in the explicitly deferred plans. This addendum is not phase completion.

Final metadata: bundle **225032 bytes**, gzip **56407 bytes**, SHA256
`2ad1bc409ea3e56b1f0495de64e5b40fc352ce454c2adc61e171189ffe0d4ff0`.
The final typed rebuild passed in **1.07s** and preserved that hash. Owned module
inventory: **15 files** (nine created, six modified), plus this addendum and
24-02-SUMMARY.md. Measured owned integration diff/new-file content is **381037
characters**, or **95260 estimate-scale tokens** rounded up; generated bundle and
lockfile are included, pre-existing requirements-sil and parent planning edits
are excluded. Total wall-clock duration was not captured. One editor-only test
relative-import diagnostic remains despite passing compiler and Vitest module
resolution; it is not hidden as a passing editor diagnostic gate.

## Plan 24-02 BLOCKER Remediation Evidence - 2026-10-24

This addendum records the direct, user-authorized local fixes for CR-01, CR-02
and CR-03 in `24-02-REVIEW.md`: **3 implemented, 0 skipped; independent parent
re-review pending**. It does not change the review's `issues_found` verdict or
advance global STATE, a requirement or a phase. Earlier evidence above remains
historical, including its bundle hash, installs and browser observations.

All gates ran against the **main checkout**, not an isolated worktree. No install,
commit, staging, branch, deployment, live host, session credential access,
Bluetooth/phase 27 change or global planning-state edit occurred in this fix run.
Only lifecycle source/tests, panel source/tests, its existing TypeScript include
list, generated stable module and these two phase evidence files were edited.

### Intended RED Then Immediate GREEN

Frontend commands used the installed local package; each test-only edit was
immediately executed. Each production edit was immediately followed by the same
focused command, before further patching or exploration.

| Finding / Command | Before Production Fix | Immediately After Fix |
|-------------------|-----------------------|-----------------------|
| CR-01: `npm --prefix F:/Workspace/BL-HAOS/modules/integration/panel_ui test -- --run -t 'thumbnail'` | **5 failed, 4 passed, 6 skipped**, 1.05s; exact slash/backslash-host payload plus literal TAB/LF/CR/NUL rendered as images | **9 passed, 6 skipped**, 0.84s |
| CR-02: focused session regex command below | **6 failed, 3 passed, 14 skipped**, 2.255s test time; old catalog survived connection/user replacement and stale play completion survived loss/replacement/disconnection | **9 passed, 14 skipped**, 0.932s total |
| CR-03: Linux command below, `-k 'repeated_cancellation or operation_originated'` | **2 failed, 1 passed, 14 deselected**, 0.95s; repeated cancellation cancelled Core's real executor waits for both copy and removal | **3 passed, 14 deselected**, 0.93s |
| CR-01 path-only refinement: same thumbnail command after adding protocol-relative dummy-host and normalization variants | **1 failed, 11 passed, 14 skipped**, 0.878s; `//ha.invalid/...` was normalized instead of rejected | **12 passed, 14 skipped**, 0.854s |

Exact CR-02 and CR-03 RED/GREEN commands from Windows:

```powershell
npm --prefix F:/Workspace/BL-HAOS/modules/integration/panel_ui test -- --run -t 'session|normal hass|out of order'
wsl --cd /mnt/f/Workspace/BL-HAOS/modules/integration env BLHAOS_RUN_SIL=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests/test_panel_registration.py -q -p asyncio --asyncio-mode=auto -k 'repeated_cancellation or operation_originated' --tb=short --show-capture=no
```

The executor regressions use thread/asyncio event barriers, not sleep-based race
timing, and call Core's actual executor API. They first exercise HTTP 200 and
inert-route HTTP 404, then cancel setup twice while a real copy is blocked (or
cancel unload twice during real removal). They verify the executor wait is not
cancelled, the shared lock is still held, and the caller is still pending before
opening the gate. After all work settles, owners are empty, the served file and
panel are absent, the client is closed and real HTTP is 404. Reload serves 200;
final unload returns 404 again. Public registration is also gated and tested with
one and two cancellations. Task-originated cancellation is tested independently.
Existing failed-second-owner, concurrent-owner, refused-unload, platform rollback
and native integration tests continue to pass without changing their contracts.

Frontend additions also cover late errors after loss/reconnection on the same
connection, rejection of old play errors while a replacement play is pending,
current speaker connectivity at completion, current injected service methods,
unchanged connection/user-ID updates without root reload, and same-session browse
responses arriving out of order. These supplemental checks passed on first run;
they are not misreported as additional observed RED failures.

### Final Commands and Results

```powershell
npm --prefix F:/Workspace/BL-HAOS/modules/integration/panel_ui test -- --run
npm --prefix F:/Workspace/BL-HAOS/modules/integration/panel_ui run build
wsl --cd /mnt/f/Workspace/BL-HAOS/modules/integration env BLHAOS_RUN_SIL=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests --ignore=tests/unit -q -p asyncio --asyncio-mode=auto --tb=short --show-capture=no
wsl --cd /mnt/f/Workspace/BL-HAOS/modules/integration env BLHAOS_RUN_SIL=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests/unit -q -p asyncio --asyncio-mode=auto --tb=short --show-capture=no
wsl --cd /mnt/f/Workspace/BL-HAOS/modules/integration env BLHAOS_RUN_SIL=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests/test_panel_registration.py -q -p asyncio --asyncio-mode=auto -k 'cancellation or operation_originated' --tb=short --show-capture=no
git -C F:/Workspace/BL-HAOS/modules/integration diff --check
```

| Gate | Actual Result |
|------|---------------|
| Full Vitest | **28 passed**, 1.34s |
| Full Linux real-Core SIL/package | **45 passed**, no skips, 8.35s: 21 native SIL, 18 panel/public HTTP, 6 package |
| Separate Linux stub units with autoload disabled | **54 passed**, no skips, 1.91s |
| Expanded cancellation slice | **5 passed**, 13 deselected, 1.38s |
| First typed production build after tsconfig include change | Passed, Vite 1.16s |
| Self-contained repeated npm build plus byte comparison | Passed, Vite 1.07s; `stable:true`; exactly one fixed-name JS output |
| Editor diagnostics: lifecycle source/test, panel source/test, tsconfig and both existing Vite configs | No errors reported; previous test-import phantom no longer reported |
| Integration patch hygiene | Passed |

The two Linux gates are separate processes (99 tests total), not monolithic
pytest acceptance. Full Vitest has 22 additional cases versus the reviewed six;
real-Core panel tests have four additional cases versus the reviewed fourteen.

Current artifact: `panel_static/bl-haos-media-panel.js`, **225873 bytes**, gzip
**56712 bytes**, SHA256
`3eb60c232558add8642101d97f4df3ce7f704040a251e91f692e0057c81a1d6e`.
The repeat-build check read bytes before and after invoking the same npm build
and compared them directly, then reported SHA256 and directory inventory. The
earlier multiline terminal attempt returned incomplete output and is excluded
from this proof. The self-contained Node child-process wrapper emitted DEP0190
for `shell:true` argument handling; arguments were fixed local paths/commands.
There were no compiler/test failures or suppressed diagnostics in the final gates.
Phase-evidence `git diff --check` also passed, with the existing CRLF-to-LF
normalization warning for this validation document; integration diff was clean.
No dependency or lockfile changes, ts-ignore, declaration shim or private Core
route mutation were used. No fresh Chromium/viewport matrix, live session/provider
or physical-speaker playback is claimed; independent re-review remains required.

## Plan 24-02 WR-01 Remediation Evidence - 2026-10-24

The updated review retained one WARNING: Python 3.14.4 reports a late operation
failure through a cancelled shield even when `_finish_operation` drains the
operation and re-raises caller cancellation. This local remediation does not
change `24-02-REVIEW.md` or its `issues_found` verdict. Independent re-review
and parent approval remain required; previous results above remain history.

### Observed RED and Immediate GREEN

Before changing production, extended the existing public-registration test to
cover successful and late-failing registration with one/two/three caller
cancellations. Added helper late-failure controls with zero/one/two/three
cancellations. These use event barriers and the normal Core fixture exception
capture, not a replacement loop handler. The helper test verifies the original
operation has settled; the zero-cancel control requires the original RuntimeError
to propagate. Existing operation-originated cancellation remains covered.

The immediate pre-fix run returned **10 passed, 16 deselected, 6 teardown errors
in 2.97s, exit 1**. All bodies passed, but each cancelled late failure produced
a RuntimeError at Core teardown: three helper cases and three public-registration
cases. This is teardown-error RED, not an assertion failure or environment error.

The small production fix shields only a successfully resolved completion signal,
waits through repeated cancellation, then retrieves `task.result()` explicitly.
It preserves caller cancellation after draining and propagates operation failures
or operation-originated cancellation when the caller was not cancelled. No
private callback mutation, task cancellation or global error-handler suppression
was added. The **very next action** reran the identical focused command:
**10 passed, 16 deselected in 2.28s, exit 0**, no teardown errors.

### Exact Commands and Latest Gates

All commands ran from the **main checkout** in Ubuntu WSL, not a worktree, using
the existing Python 3.14.4 / Core 2026.10.3 / helper 0.13.374 / pytest 9.0.3
environment. The full Core and stub-unit gates are separate Python processes.
Bytecode and pytest cache writes were disabled; unit plugin autoload was disabled.

```powershell
wsl.exe -d Ubuntu --cd /mnt/f/Workspace/BL-HAOS/modules/integration -- env BLHAOS_RUN_SIL=1 PYTHONDONTWRITEBYTECODE=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests/test_panel_registration.py -q -p asyncio --asyncio-mode=auto -p no:cacheprovider -k 'late_failure_after_cancellation or actual_cancellation' --tb=short --show-capture=no
wsl.exe -d Ubuntu --cd /mnt/f/Workspace/BL-HAOS/modules/integration -- env BLHAOS_RUN_SIL=1 PYTHONDONTWRITEBYTECODE=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests/test_panel_registration.py tests/test_package_layout.py -q -p asyncio --asyncio-mode=auto -p no:cacheprovider --tb=short
wsl.exe -d Ubuntu --cd /mnt/f/Workspace/BL-HAOS/modules/integration -- env BLHAOS_RUN_SIL=1 PYTHONDONTWRITEBYTECODE=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests --ignore=tests/unit -q -p asyncio --asyncio-mode=auto -p no:cacheprovider --tb=short --show-capture=no
wsl.exe -d Ubuntu --cd /mnt/f/Workspace/BL-HAOS/modules/integration -- env BLHAOS_RUN_SIL=1 PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests/unit -q -p asyncio --asyncio-mode=auto -p no:cacheprovider --tb=short --show-capture=no
```

| Latest Gate | Actual Result |
|-------------|---------------|
| Focused RED, before production change | **10 passed, 6 teardown errors**, 16 deselected, 2.97s; exit 1 |
| Identical focused GREEN, immediately after production change | **10 passed**, 16 deselected, 2.28s; exit 0 |
| Real-Core panel/package slice | **32 passed**, 5.23s; exit 0 |
| Full real-Core SIL/package | **53 passed**, no skips or teardown errors, 9.13s; exit 0 |
| Separate stub-unit process | **54 passed**, no skips, 1.79s; exit 0 |

Full Core comprises 21 native SIL, 26 panel/public HTTP and six package tests.
The former 45 cases remain covered; eight additional parameterized cases account
for the increase to 53. The two full processes total **107 passing tests**, not
single-process acceptance. The panel slice includes active real executor
copy/removal with repeated cancellation and operation-originated cancellation.
Late registration failure cases verify lock ownership until settled, client close,
zero owners, absent file/panel, HTTP 404, then reload HTTP 200 at the same URL with
no duplicate static registration, followed by final unload/zero owners/HTTP 404.

Scope is only WR-01: helper, existing panel test, summary and this validation
addendum. No frontend source/config/fixture or generated asset changed; no build
or browser gate was needed or rerun. Earlier frontend and bundle observations
are historical. No installation, staging, commit, branch/worktree, deployment,
live-host/token access, STATE/phase 27 change or later-plan execution occurred.

## Plan 24-03 Native Browse and Opaque Playback - 2026-10-24

Executed only plan 24-03 after the user accepted plan 24-01 and approved the panel
contract and locally clean plan 24-02 review. This addendum does not change earlier
historical gate results or declare the phase/requirements complete. No STATE,
ROADMAP or REQUIREMENTS updates, installs, staging, commits, branches, live-host
calls, tokens, deployment, restarts or pairing operations were authorized or made.

### Exact Runtime and Command Contract

All runs below used Ubuntu WSL, cwd
`/mnt/f/Workspace/BL-HAOS/modules/integration`, interpreter
`/home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python`, BLHAOS_RUN_SIL=1.
Runtime inspection confirmed Core **2026.10.3**; pytest output confirmed Python
**3.14.4**, pytest **9.0.3**, helper **0.13.374**. Core BrowseMedia, media enums,
resolver, PlayMedia and Unauthorized source were inspected in that environment.
Core's filter covers immediate children only, requiring the small recursive
wrapper to filter returned nested trees without altering provider metadata.

The exact browse RED and immediate GREEN command was:

```powershell
wsl -e bash -lc "cd /mnt/f/Workspace/BL-HAOS/modules/integration && BLHAOS_RUN_SIL=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests/test_ha_integration_sil.py -q -p asyncio --asyncio-mode=auto -k native_audio_browse --tb=short --show-capture=no"
```

The exact playback RED/immediate GREEN and resolution-validity RED/immediate
GREEN command was identical across those four accepted runs:

```powershell
wsl -e bash -lc "cd /mnt/f/Workspace/BL-HAOS/modules/integration && BLHAOS_RUN_SIL=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests/test_ha_integration_sil.py -q -p asyncio --asyncio-mode=auto -k native_play_media --tb=short --show-capture=no"
```

| Run | Actual Outcome | Evidence |
|-----|----------------|----------|
| Browse RED before production | **2 failed**, 21 deselected, **1.16s**, exit 1 | Both explicit speaker cases retained video/image/unknown playable leaves; expected supported six leaves, observed nine |
| Same check immediately after browse edit | **2 passed**, 21 deselected, **0.98s**, exit 0 | Metadata/hierarchy/source nonmutation assertions passed |
| First task browse selection | **2 passed**, 21 deselected, **0.84s**, exit 0 | Plan selection before playback cases were added |
| Initial playback attempt | **10 failed, 8 passed**, 23 deselected, **4.16s**, exit 1 | Five failures were test construction: Unauthorized(detail) incorrectly treated the string as Core Context; not accepted as full intended RED |
| Corrected playback RED, still before production | **10 failed, 8 passed**, 23 deselected, **5.56s**, exit 1 | Denied/unresolvable message assertions, raw expired/unavailable/timeout errors, malformed-resolution exceptions, missing target rejection and URL-bearing submission error |
| Same check immediately after playback edit | **18 passed**, 23 deselected, **6.49s**, exit 0 | Bounded fixed messages, exact original reference/self.entity_id, one successful command, no failure fallback |
| Intermediate playback selection | **19 passed**, 22 deselected, **5.04s**, exit 0 | Includes existing transport-unavailable regression |
| Intermediate isolated units | **54 passed**, **2.05s**, exit 0 | Separate process, no unit changes |
| Intermediate full real Core/package | **73 passed**, **15.92s**, exit 0 | Before supplementary resolution/metadata cases |
| Resolution-validity RED before hardening | **4 failed, 22 passed**, 23 deselected, **8.18s**, exit 1 | Opaque/non-URL/missing-host/file results wrongly submitted commands; target-loss/missing-entity/cancellation controls already passed |
| Same check immediately after hardening | **26 passed**, 23 deselected, **8.45s**, exit 0 | Parser-based validation prevents invalid source output from reaching command submission |
| Added positive/direct-leaf compatibility | **15 passed**, 49 deselected, **2.13s**, exit 0 | Documented audio metadata, unsupported direct leaves, actual Core relative-media URL processing |
| README/package compatibility | **6 passed**, **0.42s**, exit 0 | Immediate check after concise README paragraph |

The compatibility command used the same native SIL invocation with
`-k 'documented_metadata or direct_leaf or relative_resolution'`. The package
check used `tests/test_package_layout.py` without `-k`. Initial constructor-source
inspection via inspect.signature encountered Core's deferred annotation NameError;
inspect.getsource verified the real signature and the test was repaired once.
No production file edit failed its immediately following focused check. No
per-defect three-repair limit was exceeded.

### Final Exact Commands and Gates

```powershell
wsl -e bash -lc "cd /mnt/f/Workspace/BL-HAOS/modules/integration && BLHAOS_RUN_SIL=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests/test_ha_integration_sil.py -q -p asyncio --asyncio-mode=auto -k 'browse or playlist or audio' --tb=short --show-capture=no"
wsl -e bash -lc "cd /mnt/f/Workspace/BL-HAOS/modules/integration && BLHAOS_RUN_SIL=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests/test_ha_integration_sil.py -q -p asyncio --asyncio-mode=auto -k 'play_media or resolve or denied or unavailable' --tb=short --show-capture=no"
wsl -e bash -lc "cd /mnt/f/Workspace/BL-HAOS/modules/integration && BLHAOS_RUN_SIL=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests/test_ha_integration_sil.py -q -p asyncio --asyncio-mode=auto --tb=short --show-capture=no"
wsl -e bash -lc "cd /mnt/f/Workspace/BL-HAOS/modules/integration && BLHAOS_RUN_SIL=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests --ignore=tests/unit -q -p asyncio --asyncio-mode=auto --tb=short --show-capture=no"
wsl -e bash -lc "cd /mnt/f/Workspace/BL-HAOS/modules/integration && BLHAOS_RUN_SIL=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests/unit -q -p asyncio --asyncio-mode=auto --tb=short --show-capture=no"
```

| Final Gate | Actual Result |
|------------|---------------|
| Task 24-03-01 browse/audio/playlist | **24 passed**, 40 deselected, **3.75s** |
| Task 24-03-02 playback/failures | **28 passed**, 36 deselected, **7.39s** |
| Full native SIL file | **64 passed**, **13.38s** |
| Full real-Core SIL/lifecycle/package | **96 passed**, **20.30s**, zero skips/teardown errors |
| Separate isolated unit process | **54 passed**, **2.26s**, zero skips |
| Editor diagnostics, touched Python files | No errors |
| Integration git diff --check | Passed |

The two full processes cover **150 tests**, not a single-process run; overlapping
focused/full-native results are not counted again. The real-Core run consists of
64 native SIL, 26 public lifecycle and six package cases. This plan adds **43**
native SIL cases over the prior 21; no existing unit expectation changed.

### Scope, Deviations and Remaining Host Work

Only media_player.py, the existing native SIL file and a concise integration
README paragraph changed in the module. This addendum and 24-03-SUMMARY.md are
the only planning edits. The source policy copies returned BrowseMedia objects,
preserves every non-child field including not_shown/search capabilities, retains
unknown/empty expandable nodes and never fetches playlist tracks. Provider names,
IDs, extensions and URLs are not browse-support signals.

Original opaque IDs resolve once through Core for self.entity_id. Only valid
resolution plus a still-available selected speaker allows the existing command.
Tests cover both speakers, item/playlist references, all truthy enqueue modes,
denied/expired/unavailable/unresolvable/timeouts, malformed results, target loss,
missing entity ID, cancellation, and fixed submission-failure output without
retry/skip/fallback/target substitution. Relative URL compatibility uses Core's
actual helper. Provider behavior itself is fixture-backed, not a live provider.

Correctness additions under plan task 02 include parser-based source-result
validation and pre/post-resolution target guards. All work remains deliberately
uncommitted; the measured source/test diff plus this run's README paragraph is
**6249 chars/4 tokens**, excluding prior README changes and evidence prose.
No new endpoint, credential persistence or schema trust boundary was added.
Stub scanning found no TODO/FIXME/placeholder marker in the touched code.

Existing URL-bearing operational logs remain **plan 24-05** work, not a claim of
complete URL redaction now. Fixed user-visible errors are bounded and suppress
displayed exception chaining. Real configured provider hierarchy/playlists,
session denial/expiration, production-panel behavior and physical audible playback
still require separately authorized **plan 24-06** host acceptance. No whole-phase
completion, live fault resolution or physical playback is claimed.

## Plan 24-03 CR-01 Transport Remediation - 2026-10-24

This addendum supersedes the prior 96 Core / 54 unit counts and the claim that
above-client mocks established transport-level no-retry behavior. CR-01 in
24-03-REVIEW.md is implemented locally; independent re-review remains pending.
The review itself is unchanged and still `issues_found`.

### Scope and Contract

The user explicitly authorized client.py as the nearest root-cause contract
boundary. BLHAOSClient.async_command retains its public signature and payload;
operation == "play_media" selects one attempt, while every other command keeps
COMMAND_ATTEMPTS. Reads, lifecycle/filter changes, panel assets, phase 27 and
global STATE are untouched by this remediation. The method's old claim that
restarting playback was safe to retry was corrected.

Four cases were added to the existing client unit file below the retry loop.
Fake HTTP records the POST and marks it applied before response-context entry
raises: disconnect then hypothetical success, persistent disconnect, TimeoutError
and generic ClientError. No client command/send method is mocked. The old unit
expectation intentionally changes from retrying play_media to retrying pause;
it verifies two attempts and one sleep. No shared import stubs/fixtures changed.

The existing Core failure test replaces its async_command mock with fake HTTP
I/O around the real entity/client/send path. Its eight parameterized cases cover
the same four failures for each speaker. Assertions require exactly one original
opaque-reference resolution, one selected target/payload, one applied POST, zero
retry sleeps and the exact bounded HomeAssistantError. Its displayed message
contains no resolved URL or credential details; context is suppressed and cause
is None. A failed acknowledgement is not proof playback was unapplied.

### Immediate RED and GREEN

The first regression edit was immediately executed before production changes:
**2 failed, 2 passed, 15 deselected in 0.54s, exit 1**. The disconnect/success case
failed DID NOT RAISE because a second POST succeeded. Persistent disconnect
failed with two recorded POSTs. Timeout/generic-error controls already passed.
This is intended behavioral RED, not a fixture/environment failure.

After the one-attempt production edit, the very next action ran the identical
command: **4 passed, 15 deselected in 0.38s, exit 0**. One production change,
zero repair loops; the maximum three-repair limit was not reached.

### Exact Commands and Latest Counts

All gates ran against the **main checkout**, not a worktree, in Ubuntu WSL using
the existing Python 3.14.4 / Core 2026.10.3 / helper 0.13.374 / pytest 9.0.3
environment. No installations occurred. Real Core and stub units ran in separate
Python processes; unit plugin autoload was disabled. The first command below was
used unchanged for both RED and immediate GREEN.

```powershell
wsl --cd /mnt/f/Workspace/BL-HAOS/modules/integration -e env PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -B -m pytest -c pytest.ini tests/unit/test_client_commands.py -q -k play_media_does_not_repeat_ambiguous_http_submission
wsl --cd /mnt/f/Workspace/BL-HAOS/modules/integration -e env BLHAOS_RUN_SIL=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -B -m pytest -c pytest.ini tests/test_ha_integration_sil.py -q -p asyncio --asyncio-mode=auto -k command_failure_is_bounded_without_retry --tb=short --show-capture=no
wsl --cd /mnt/f/Workspace/BL-HAOS/modules/integration -e env PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -B -m pytest -c pytest.ini tests/unit/test_client_commands.py -q --tb=short
wsl --cd /mnt/f/Workspace/BL-HAOS/modules/integration -e env BLHAOS_RUN_SIL=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -B -m pytest -c pytest.ini tests --ignore=tests/unit -q -p asyncio --asyncio-mode=auto --tb=short --show-capture=no
wsl --cd /mnt/f/Workspace/BL-HAOS/modules/integration -e env BLHAOS_RUN_SIL=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -B -m pytest -c pytest.ini tests/unit -q -p asyncio --asyncio-mode=auto --tb=short --show-capture=no
```

| Latest Gate | Actual Result |
|-------------|---------------|
| Identical focused RED | **2 failed, 2 passed**, 15 deselected, 0.54s |
| Immediate identical focused GREEN | **4 passed**, 15 deselected, 0.38s |
| Real-Core transport slice | **8 passed**, 63 deselected, 2.35s |
| Existing client unit file | **19 passed**, 1.06s |
| Full Core non-unit suite | **103 passed**, 18.29s, no skips/teardown errors |
| Separate full stub-unit suite | **58 passed**, 1.29s, no skips |
| Editor diagnostics, client and both touched test files | No errors |

Full total is **161 passed across two processes**. The Core baseline 96 grows
by seven because one mocked case becomes eight HTTP cases: 71 native SIL,
26 lifecycle, six package. Units grow from 54 to 58 with four new cases.
Focused runs overlap the full gates and are not counted again.

Only client.py, the two existing test files, 24-03-SUMMARY.md and this validation
addendum were edited for CR-01. No new test files, dependencies, installs,
staging, commits, branches, worktrees, live-host/credential access, deployment,
STATE updates or phase 27 changes occurred. Existing operational URL logging
remains plan 24-05 work; real-provider/physical-audio acceptance remains plan
24-06. No independent clean-review verdict or whole-phase completion is claimed.

## Plan 24-04 Local Catalog and Ingress Evidence - 2026-10-24

Only plan 24-04 was executed after reading the clean 24-02 and 24-03 reviews and
the approved contract. No commits/staging/branches, STATE/ROADMAP changes,
Python changes, installs, deployment/restart, live access or phase 27 edits.
Release version/docs remain 24-06; the existing 0.2.68 work is preserved.

### Source-Verified Search Contract

Confirmed installed Core **2026.10.3** using the existing WSL interpreter.
Read exact `homeassistant/components/media_source/http.py`: setup registers
`websocket_search_media` (line 28); the public schema (56-62) is
`media_source/search_media`, optional `media_content_id` defaulting to `""`,
required `search_query`, optional `media_filter_classes`. The handler returns
`SearchMedia.as_dict()`, whose public shape is `{result: [...]}` in
`media_player/browse_media.py:175-186`. No query field was added to the separate
browse schema, and no entity-scoped search command was substituted. Search is
rendered only with `can_search`, and runs only on explicit form submission.

Exact source inspection command:

```powershell
wsl --cd /mnt/f/Workspace/BL-HAOS sh -c 'sed -n "1,110p" /home/mse/.venvs/bl-haos-sil-2026.10.3/lib/python3.14/site-packages/homeassistant/components/media_source/http.py'
```

### Intended RED, Immediate GREEN and Final Gates

Commands ran from `F:\Workspace\BL-HAOS`, with existing node_modules:

```powershell
npm --prefix modules/integration/panel_ui test -- --run src/media-panel.test.tsx --reporter=dot
npm --prefix modules/bridge/web_ui test -- --run src/App.test.tsx --reporter=dot
npm --prefix modules/integration/panel_ui test -- --reporter=dot
npm --prefix modules/bridge/web_ui test -- --reporter=dot
npm --prefix modules/integration/panel_ui run build
npm --prefix modules/bridge/web_ui run build
node .planning/phases/24-ha-media-catalog-provider-playback/host-probe/24-04-local-browser.mjs
Get-FileHash modules/integration/custom_components/bl_haos/panel_static/bl-haos-media-panel.js -Algorithm SHA256
```

| Gate | Actual Result |
|------|---------------|
| Initial panel assertion RED, before production | **7 failed, 28 passed**, 7.35s |
| Initial ingress assertion RED, before CTA | **2 failed**, 15.25s |
| Immediate panel check after partial patch application | **7 failed, 28 passed**, 7.34s; completed the same edit |
| Immediate panel state-machine GREEN | **35 passed**, 1.54s |
| Immediate ingress GREEN | **2 passed**, 917ms |
| Accessibility/style RED before CSS completion | **1 failed, 39 passed**, 1.61s; missing catalog-body overflow rule |
| Immediate accessibility/style GREEN | **40 passed**, 1.66s |
| Final full panel suite | **40 passed**, 2.52s; original 28 assertions unchanged |
| Final full bridge frontend suite | **26 passed**, six files, 1.04s |
| Typed panel production build | Passed, Vite 2.13s, fixed filename, 232169 bytes / 58216 gzip |
| Final typed ingress production build | Passed, Vite 1.44s |
| Final generated-bundle Chromium fixture | All six viewport/motion cases and actual framed-ingress keyboard navigation passed |

Panel SHA256:
`1023bbcc18e2107dd638957da358b42bbe8bb34e733224df108413db94ddc58e`.
No generated source was manually edited. The earlier 103 Core / 58 separate
unit baseline was not rerun because Python was untouched.

### Browser Scope and Remaining Host Backstop

The phase-local Playwright script uses the **actual generated panel and ingress
bundles**, intercepts all requests locally, injects a synthetic `hass`, and
closes browser contexts in `finally`. No server was started or left running.
The first browser attempt exposed a fixture assumption: `selectOption()` does
not focus the control. An explicit focus before Tab fixed the harness; the
subsequent full runs passed. Browser wall-clock duration was not instrumented.

At 375/768/1440 x 900, in normal/reduced-motion modes, measured no horizontal
overflow, selector within viewport, independently scrollable body, zero controls
under 44px, visible keyboard focus, 0.15s/0s transitions and loaded same-origin
fixture thumbnails. Nonblank screenshot pixel samples contained 174/166/154
colors respectively. Screenshots for all three widths were actually opened and
inspected, including reduced motion. Long speaker names wrap visibly below the
native select, and full long item names remain accessible with two-line rows.

Browser checks also prove explicit identical item/target retry only, exact
public search message, target-unavailable Play disabling without substitution,
Escape/focus return, and zero off-origin/page errors. Actual built ingress inside
a frame navigated the **top frame** to `/bl-haos-media` by keyboard, with **zero
extra API calls** beyond normal initialization. Screenshots are under
`%TEMP%\bl-haos-plan24-04-visual`; the fixture is reproducible from the command above.

No live HA/provider/authentication, physical-audio, screen-reader or host contrast
acceptance is claimed. These remain 24-06 host backstops. Parent review is required
before 24-05. See 24-04-SUMMARY.md for task inventory, diagnostics limitations and
exact execution deviations; no global completion state was advanced.

## Plan 24-04 Review Fix Validation - 2026-10-24

This addendum supersedes the original 24-04 bundle identity and local test
counts above. It does **not** replace independent parent review: the existing
review remains `issues_found` until the parent reruns it. No clean-review claim.

Actual component reads confirmed CR-01's shared-error clearing and WR-01's
missing breadcrumb width. Tests were extended before the production fix, with
no existing case removed. Commands ran in the **main checkout**, not an isolated
worktree, from `F:\Workspace\BL-HAOS`, using existing dependencies.

| Gate | Exact Command / Actual Result |
|------|-------------------------------|
| Intended RED before production | `npm --prefix modules/integration/panel_ui test -- --run src/media-panel.test.tsx --reporter=dot`: **4 failed, 37 passed**, 1.62s; root/search/child target-selection recovery plus breadcrumb width |
| Immediate GREEN after split-error/min-width fix | Same command: **41 passed**, 1.54s |
| Back feedback compatibility follow-up | Same command: **41 passed**, 1.71s |
| Full panel suite | `npm --prefix modules/integration/panel_ui test -- --reporter=dot`: **41 passed**, initially 1.60s; final-source repeat **41 passed**, 1.71s |
| Full bridge frontend suite | `npm --prefix modules/bridge/web_ui test -- --reporter=dot`: **26 passed**, six files, 1.07s |
| Typed panel build | `npm --prefix modules/integration/panel_ui run build`: passed; final Vite 1.11s |
| Typed bridge build | `npm --prefix modules/bridge/web_ui run build`: passed; Vite 1.26s |
| Browser syntax | `node --check .planning/phases/24-ha-media-catalog-provider-playback/host-probe/24-04-local-browser.mjs`: passed |
| Actual generated frontend browser checks | `node .planning/phases/24-ha-media-catalog-provider-playback/host-probe/24-04-local-browser.mjs`: passed twice, including final bundle; all six viewport/motion cases and framed-ingress navigation |

Preserved all original **40** panel tests, including the **28** prior security
and session guards. Added one root-failure regression and strengthened existing
search/child-retry, playback-error clearing, and two-dimensional style assertions.
Playback retry still checks the same opaque item, same selected connected target,
and synchronous pending guard; unavailable selection is not substituted. The
verified Core public search schema and quoted safe inspection commands above
are unchanged. No Python/Core rerun was needed or claimed for JS-only changes.

At **375/768/1440 x 900**, both motion modes:

- Root failure, target selection and same-session update preserve the bounded
	alert and Retry media sources with **1** browse call. Only manual retry makes
	call **2**, identical to the first, and no service call. No extra auto-browse.
- Short `A` breadcrumb after opening `I`: **44px width AND 44px height** in all
	six cases. Navigation, target, close, play and search controls all meet both
	dimensions; long-name/narrow-layout checks remain alongside this case.
- Captured search query `evening` survives changed input and target selection;
	retry is manual and repeats the identical message. Same-item/target play retry,
	unavailable selection, keyboard/Escape/focus, scrolling, thumbnails, no
	overflow and reduced motion pass. Zero page errors/off-origin requests and
	zero CTA-attributable API calls. Pixel samples: **168/164/155** colors.

Normal-motion screenshots at all three widths were opened and inspected. Fixture
screenshots remain under `%TEMP%\bl-haos-plan24-04-visual`. No server was started;
Chromium closes in `finally`. This is offline synthetic evidence, not HA/provider,
authentication, physical audio or screen-reader acceptance.

Final typed-build panel bundle: **232392 bytes**, gzip **58224**, SHA256
`48d12229891c0e145906bfefec4b609016c5908c790529f57f2c3b05a3cf90f7`.
No generated bundle was hand-edited. Actual App source already uses `min-h-11`
and `focus-visible:outline-solid`; scoped `get_errors` reports no errors in the
four reviewed source/test files, so no App edit or suppression was made.

Deviations: explicit user no-commit/no-branch policy overrides fixer automation;
no worktree, staging, commit, install, live host, token, deployment, restart,
STATE/phase 27 edit or version/docs release change. Both defects passed the first
production repair; the small Back feedback compatibility follow-up passed its
immediate check. No defect/file exceeded three repair loops. Existing summary
and validation carry the fix evidence; parent review rerun is still required.

## Plan 24-05 URL Log Privacy Evidence - 2026-10-24

Only 24-05 was executed. Three implementations pass their focused tests, but
full acceptance is **blocked** by an existing package-contract assertion. This
does not amend the clean prior reviews, advance STATE or requirements, execute
24-06, or claim release/deployment acceptance. Earlier evidence remains historical.

### Owning Boundaries and Preserved Behavior

Integration logging no longer prints the resolved URL or command kwargs. Real
client HTTP warning detail and playback command failure text are bounded. Native
route logging omits payload.url; playback/reconnect failures use controlled
messages with suppressed displayed causes instead of arbitrary URL fragments.
Unexpected play_media exceptions become bounded HTTP 409. Player execute, spawn
failure, child stderr, drain traceback, task exception, and URL-derived fallback
title logging omit sensitive values. Raw stderr is drained but not logged.
These are local owning-path extensions, not a global redaction abstraction;
existing value-free call_trace wrappers are unchanged and exercised at DEBUG.

The exact accepted query-credential URL reaches the real integration client
POST, the native route's execute boundary, and ffmpeg as one argument after -i.
Userinfo rejection is separately tested rather than weakening existing policy.
SSRF/protocol validation, fixed whitelist, bearer/trust checks, reconnect
classification/attempts/reset behavior, timeline title/duration and process
lifecycle remain covered. No child process or external URL is real in these tests.

New cases total **25**: five Core entity/client/resolver/HTTP cases, ten route
cases, and ten player cases. Captures assert full URL and distinct host, path,
query-key/value, user, password and token sentinels absent, including formatted
integration/player errors, raw/fragmented failures, stderr and background paths.
Bridge capture enables both bl_haos and backend.bl_haos so decorated boundaries
are included. No existing test was removed, skipped, or weakened.

### Commands and Immediate RED/GREEN

Core uses Ubuntu WSL cwd /mnt/f/Workspace/BL-HAOS/modules/integration and
/home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python: Python 3.14.4, pytest 9.0.3,
Core 2026.10.3 and helper 0.13.374. Unit stubs run in a separate process with
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1. Bridge uses Windows Python 3.14.7/pytest 9.0.3
at F:/Workspace/BL-HAOS/.venv/Scripts/python.exe, cwd modules/bridge,
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 and -c pytest.ini. No installs occurred.

```powershell
wsl -d Ubuntu --cd /mnt/f/Workspace/BL-HAOS/modules/integration env BLHAOS_RUN_SIL=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests/test_ha_integration_sil.py -q -p asyncio --asyncio-mode=auto -k "play_media and (log or redact)"
& { Set-Location F:/Workspace/BL-HAOS/modules/bridge; $env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'; & F:/Workspace/BL-HAOS/.venv/Scripts/python.exe -m pytest -c pytest.ini tests/test_api.py -q -p asyncio --asyncio-mode=auto -k 'native and (play or log or redact)' --tb=short --show-capture=no }
& { Set-Location F:/Workspace/BL-HAOS/modules/bridge; $env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'; & F:/Workspace/BL-HAOS/.venv/Scripts/python.exe -m pytest -c pytest.ini tests/test_media_player.py -q -p asyncio --asyncio-mode=auto -k 'url or log or redact' --tb=short --show-capture=no }
```

The integration GREEN added only --tb=short --show-capture=no for output size;
the test command/selection/interpreter are identical. Player RED used --tb=line
instead of --tb=short, with identical tests. All production patches were followed
immediately by the corresponding selection, before other reading or edits.

| Selection | Actual RED | Immediate GREEN |
|-----------|------------|-----------------|
| Integration | 4 failed, 1 passed, 71 deselected, 1.95s | 5 passed, 71 deselected, 1.92s |
| Native route, corrected capture | 7 failed, 7 passed, 22 deselected, 1 warning, 0.94s | 14 passed, 22 deselected, 1 warning, 1.07s |
| Player | 9 failed, 8 passed, 52 deselected, 0.33s | 17 passed, 52 deselected, 0.43s |
| Player metadata fallback title | 1 failed, 17 passed, 52 deselected, 0.33s | 18 passed, 52 deselected, 0.26s |

Initial route capture had 7 failed/7 passed in 0.95s because only the explicit
logger namespace was enabled. Correcting the harness before any production edit
exposed intended sentinel RED; the initial trace assertion failure is not counted
as behavioral RED. A multiline terminal invocation returned no pytest output;
it was rerun in one PowerShell block before production editing. No defect/file
exceeded three repair loops.

### Full Gates and Blocker

```powershell
wsl -d Ubuntu --cd /mnt/f/Workspace/BL-HAOS/modules/integration env BLHAOS_RUN_SIL=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest --ignore=tests/unit -q --tb=short --show-capture=no
wsl -d Ubuntu --cd /mnt/f/Workspace/BL-HAOS/modules/integration env BLHAOS_RUN_SIL=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests/unit -q -p asyncio --asyncio-mode=auto --tb=short --show-capture=no
& { Set-Location F:/Workspace/BL-HAOS/modules/bridge; $env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'; & F:/Workspace/BL-HAOS/.venv/Scripts/python.exe -m pytest -c pytest.ini -q --tb=short --show-capture=no }
& { Set-Location F:/Workspace/BL-HAOS; & ./scripts/run-tests.ps1 -Layer L1 }
```

| Final Gate | Actual Result |
|------------|---------------|
| Full real-Core non-unit | **107 passed, 1 failed**, 24.12s, zero skips; 108 = prior 103 + five cases |
| Full isolated WSL units | **58 passed**, 1.84s, zero skips; baseline unchanged |
| Full Windows bridge, after final player edit | **300 passed, 1 existing POSIX skip, 1 warning**, 12.64s; prior 280 + twenty new passing cases |
| Actual valid L1 runner | **Failed**: bridge **300 passed/1 skip/1 warning**, 13.11s; integration unit/package **63 passed/1 failed**, 1.16s; frontend stage not reached |

Before the extra metadata regression: full bridge 299 passed/1 skip/1 warning,
14.38s; initial L1 bridge 299 passed/1 skip/1 warning, 12.88s, then integration
63 passed/1 failed, 0.78s. Both bridge-containing gates were rerun after the last
production edit. Core/units were unaffected by that bridge-only log change.
Overlapping focused/full/runner results are not counted as additional cases.

Both failed gates hit the unchanged test_panel_build_source_and_stable_bundle_contract
at modules/integration/tests/test_package_layout.py:70: its forbidden string parent.
matches the ordinary breadcrumb variable parent.media_content_id in the existing
panel source. Neither file changed in 24-05; no unrelated fix or skip was made.
This is a test-contract failure, not missing infrastructure: the exact runtimes
and runner launched successfully. L1 supports the requested -Layer L1; no flag
substitution was needed. It stops before npm/frontend, so that stage is unrun.
The only pytest warning is the existing StarletteDeprecationWarning about httpx
TestClient. No dependency change/install was attempted to silence it.

User-facing logging guidance was updated in integration README and bridge DOCS
without a version/changelog/release claim. No STATE/ROADMAP/REQUIREMENTS, phase 27,
Bluetooth source, earlier review/summary, frontend/package check, or generated
asset was edited. No new dependencies, installs, staging/commits/branches, live
host/token access, deployment or restart occurred. 24-05-SUMMARY.md records
implementation plus blocked acceptance, not whole-phase completion.

Final evidence self-check passed: parsed summary YAML/status/tasks/zero commits,
verified every listed file exists and all recorded RED/GREEN/full-gate metrics
agree between the two artifacts, and checked both documentation additions.
Editor diagnostics found no errors in all seven touched Python files; both
module git diff --check commands passed. This does not convert the blocked
Core/package or L1 gate into a pass.

## Plan 24-05 Review Remediation - 2026-10-24

This latest addendum supersedes the preceding 24-05 package/L1 blocker and privacy
completeness claims, preserving the original evidence. The three blockers and
one warning in 24-05-REVIEW.md are fixed locally; that review remains
`issues_found` pending independent re-review. No 24-06 execution or phase/host
acceptance is implied. The parent's breadcrumb `ancestor` rename and rebuild
are preserved; all six strict package checks pass unchanged under real Core.

### Owning Source and New Evidence

1. CR-01: media_player.async_play_media and command_native_speaker logged
	validator-accepted labels containing host/path or standalone tokens. Only the
	logged type is mapped through exact known keys to constant audio/playlist/other
	values. Real Core entity/client HTTP and authenticated native HTTP tests prove
	sent URL/type and accepted model values are unchanged.
2. CR-02: BLHAOSClient._async_listen logged whole native events. A finite fake
	WebSocket now feeds a real MediaPlayerBridge fallback timeline plus embedded
	URL/token title/artist into the real decorated listener. Cached values remain
	exact and listener logs omit every sentinel. Additional intended RED justified
	the adjacent native-command operation allowlist and fixed malformed-event
	diagnostic: both leaked raw labels/parser text in the same client. Actual
	submitted operations, retry policy, authentication and unrelated command error
	behavior are unchanged; no framework middleware or global suppression exists.
3. CR-03: player.play_url reflected parser str(error) and displayed nested causes.
	It now chooses fixed policy text from exact known reasons, with safe fallback,
	and raises from None. Real malformed bracketed-host/nonnumeric-port cases
	assert bounded formatted chains, individual sentinel absence and no sink or
	process effects. Existing positive tests still assert exact URL once after -i,
	fixed protocol whitelist and no shell; URL rejection policy is not altered.
4. WR-01: The real authenticated HTTP route and decorated route are both exercised
	with reconnect=False and nested input-bearing playback causes. Its bounded 409
	now raises from None. One initial execute, reset_existing=True and no retry
	after false remain pinned. No reconnect timing/classification change was made.

### Runtime and Per-Finding RED/GREEN

Every command ran in the **main checkout**, not a worktree. Core: existing Ubuntu
WSL /home/mse/.venvs/bl-haos-sil-2026.10.3, Python 3.14.4, Core 2026.10.3,
helper 0.13.374, pytest 9.0.3. Native Windows bridge: existing .venv,
Python 3.14.7, pytest 9.0.3, cwd modules/bridge and plugin autoload disabled.
Stub units ran separately, never in the real-Core non-unit process. No installs.

| Finding | Intended RED Immediately Before Production | Next Action After Production Edit |
|---------|--------------------------------------------|-----------------------------------|
| CR-01 Core label selector | **2 failed**, 84 deselected, 1.31s | full real-client privacy selector **15 passed**, 71 deselected, 4.82s |
| CR-01 native HTTP label selector | **2 failed**, 48 deselected, 1.01s | full route privacy selector **21 passed**, 29 deselected, 1.24s |
| CR-02 listener/command/parser | **4 failed, 1 passed**, 86 deselected, 0.97s | identical selector **5 passed**, 86 deselected, 0.70s |
| CR-03 parser boundary | **2 failed, 3 passed**, 67 deselected, 0.32s | rejection + existing execution selector **12 passed**, 60 deselected, 0.26s |
| WR-01 reconnect-false boundary | **3 failed**, 50 deselected, 1.05s | identical selector **3 passed**, 50 deselected, 0.71s |

Initial CR-02 listener/command RED before the parser case: 3 failed, 1 passed,
86 deselected, 1.34s. Every RED was an actual sentinel disclosure. Each production
fix passed its first immediate check, with zero production repair loops. No
defect/file exceeded three repairs. Tier-1 source rereads confirmed fixes and
surrounding structure; runtime tests and editor diagnostics supply executable
syntax/behavior evidence.

Exact Core focused command prefix (cwd is set by --cd):

```powershell
wsl.exe -d Ubuntu --cd /mnt/f/Workspace/BL-HAOS/modules/integration env BLHAOS_RUN_SIL=1 PYTHONDONTWRITEBYTECODE=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests/test_ha_integration_sil.py -q -p asyncio --asyncio-mode=auto -p no:cacheprovider -k '<selector>' --tb=short --show-capture=no
```

Selectors: CR-01 RED `redact_real_client_logs and label and None`, GREEN
`redact_real_client_logs`; CR-02 both `native_websocket_redact or native_command_redact`.
Windows focused prefix, run from modules/bridge with
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1:

```powershell
& F:/Workspace/BL-HAOS/.venv/Scripts/python.exe -B -m pytest -c pytest.ini <test-file> -q -p asyncio --asyncio-mode=auto -p no:cacheprovider -k '<selector>' --tb=short --show-capture=no
```

CR-01 uses tests/test_api.py: RED `redact_logs_and_errors and label and None`,
GREEN `redact_logs_and_errors`. CR-03 uses tests/test_media_player.py: RED
`url_redact_rejection`, GREEN `url_redact_rejection or url_redact_real_execution`.
WR-01 uses tests/test_api.py with `connect_false` for both runs.

### Latest Full Gates and Actual Runner Contract

Inspected scripts/run-tests.ps1 before execution: -Layer accepts L1, which runs
full bridge pytest, separate Windows integration units/package, then bridge
frontend Vitest. It does not run real Core, so the explicit WSL gate is separate.
No runner flag, package check or test expectation was weakened.

```powershell
wsl.exe -d Ubuntu --cd /mnt/f/Workspace/BL-HAOS/modules/integration env BLHAOS_RUN_SIL=1 PYTHONDONTWRITEBYTECODE=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests --ignore=tests/unit -q -p asyncio --asyncio-mode=auto -p no:cacheprovider --tb=short --show-capture=no
wsl.exe -d Ubuntu --cd /mnt/f/Workspace/BL-HAOS/modules/integration env BLHAOS_RUN_SIL=1 PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests/unit -q -p asyncio --asyncio-mode=auto -p no:cacheprovider --tb=short --show-capture=no
Set-Location F:/Workspace/BL-HAOS/modules/bridge; $env:PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'; & F:/Workspace/BL-HAOS/.venv/Scripts/python.exe -B -m pytest -c pytest.ini tests -q -p asyncio --asyncio-mode=auto -p no:cacheprovider --tb=short --show-capture=no
Set-Location F:/Workspace/BL-HAOS; & ./scripts/run-tests.ps1 -Layer L1
```

| Gate | Latest Actual Result |
|------|----------------------|
| Complete real-Core non-unit suite | **123 passed**, 28.13s, zero skips; 91 native SIL, 26 lifecycle, 6 strict package |
| Complete isolated WSL units | **58 passed**, 1.27s, zero skips |
| Complete Windows bridge | **319 passed, 1 existing POSIX skip, 1 warning**, 12.61s |
| Actual root -Layer L1 | **Passed**: bridge 319 passed/1 skip/1 warning, 12.48s; integration units/package 64 passed, 0.67s; frontend 26 passed across six files, 1.22s |
| Seven changed Python files: editor diagnostics | No errors |
| Both module git diff --check | Passed |

The original 108 Core cases grow by 15; 301 bridge cases grow by 19 to 320
collected. Overlapping focused/full/L1 gates are not summed. The sole warning
remains the existing Starlette httpx TestClient deprecation. There are no new
environment blockers; no installs or warning suppression were attempted.

Only seven existing Python files and these two existing evidence artifacts were
edited. No STATE, phase 27/Bluetooth, panel source/bundle/package checks, review
status, dependencies/version/release docs, branches/worktrees, staging or commits
were changed. No live host/provider, credentials, physical playback, deployment
or restart was used. Independent re-review is the next gate, not 24-06 execution.

## Plan 24-06 Authorized Local Portions - 2026-10-24

**Status: blocked at mandatory Task 24-06-01 host precondition.** The user's
explicit local-only authorization permits harness preparation and Tasks 02/03,
not live acceptance or completion. Read the full 24-06 plan/UI-SPEC, all five
predecessor summaries and available clean reviews (02-05); their older pending
review statements remain historical. No 24-06 complete SUMMARY is created.
Parent-owned STATE/ROADMAP/REQUIREMENTS/state.json are not edited by this run.

### Local Changes and Safety Boundary

- Separate real-host config/specs use Core exactly 2026.10.3 and the actual
	`bl-haos-media-panel` open shadow root, not the bridge demo harness or mocks.
	The suite can dispatch **one real play** only after explicit environment
	consent, to the exact configured connected entity and opaque playlist.
- Pure prerequisite tests require explicit host/target/provider/playlist,
	playback consent and a separate authorized naturally expiring fixture.
	Browser-state paths must be absolute, canonical, external to the workspace
	and every Git checkout, and distinct by pathname and filesystem identity.
	Validation uses path/stat metadata only, never auth-file contents.
- No provider-name guessing or raw URL resolution. Public provider root and
	bounded hierarchy discovery are intentional constraints, not verified facts
	about a real provider. No playlist expansion into tracks is implemented.
- Traces, HAR, videos, auto failure screenshots, retries, debug payload output
	and raw diagnostic reporting are disabled. A value-free reporter prints only
	status. Only explicit guarded panel screenshots at 375/768/1440 may be taken
	in ignored panel_ui/test-results/ha-catalog. No host screenshot was produced.
- Independent unauthenticated denial is separate from actual expiry. The
	expiring fixture must first authenticate, then return an explicit auth error
	while disconnected; timeout/disconnect/invalid sentinels cannot pass as
	expiry. No token/session manipulation is performed. Whether the actual HA
	frontend exposes that auth-rejection code is unverified: without observable
	rejection this scenario fails, and actual expiry remains pending.
- Five user docs now distinguish local implementation from deployment,
	HA-owned auth/resolution, one-speaker opaque playback and Phase 25/26
	exclusions. Existing native direct-URL support is not a panel fallback.
	Two existing static-test files enforce positive fragments, forbidden positive
	claims, negated exclusions, exact release consistency and harness contracts.
- Bridge constants.VERSION/config.yaml/top changelog agree at **0.2.69**.
	Existing 0.2.68 reconnect source and notes are preserved; the integrated
	release remains undeployed. Integration manifest stays **0.2.19**.

### RED and Immediate GREEN

| Focused Check | Observed RED | Immediate/Final GREEN |
|---|---|---|
| Integration docs before prose | 1 failed, 2 passed, 6 deselected, 0.10s; missing Open Media Catalog | 9 passed, 0.03s after docs |
| Bridge docs/release before prose/version | 2 failed, 2 passed, 7 deselected, 0.12s; missing catalog and 0.2.69 | 16 config/asset tests passed, 0.43s |
| Pure validator before module | Missing-module scaffold failure, not assertion-level behavior RED | First implementation: 17 passed/1 test-double failure; corrected equal-path mock: 18 passed |
| Exact negated Docker exclusion | 1 failed/3 passed in each module | Integration 10 passed, 0.04s; bridge config/assets 16 passed, 0.43s |
| External-file safety edges | 3 failed/18 passed, 73.65ms; dot-dot child, other Git checkout, hardlink alias | Same command 21 passed, zero skipped, 77.79ms |
| Host TypeScript | 7 missing Node typing errors | Node-only loader/reporter in .mjs; typed config/spec pass, no extra typing dependency |

One initial multi-file docs patch was rejected without changes; verified exact
context then succeeded. The obsolete reporter .ts deletion did not take effect
through the file tool; only that newly created obsolete file was removed and
the typecheck rerun. No finding exceeded three repair attempts. No unrelated
source cleanup, test weakening, warning suppression or skipped test was added.

Public registry metadata verified @playwright/test **1.63.0**, matching the
existing bridge-installed version, before adding the exact panel dev pin.
`npm --prefix modules/integration/panel_ui install --ignore-scripts --no-audit
--no-fund --registry=https://registry.npmjs.org` added only three packages:
@playwright/test, playwright, playwright-core. Other direct pins remain
unchanged; direct lock metadata matches. No bridge dependency upgrade occurred.
Context7 CLI read official Playwright v1.63.0 trace/video/open-shadow-DOM docs.

### Latest Actual Gates

Commands were run from repository root unless the command sets its own cwd:

```powershell
wsl.exe -d Ubuntu --cd /mnt/f/Workspace/BL-HAOS/modules/integration env BLHAOS_RUN_SIL=1 PYTHONDONTWRITEBYTECODE=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests --ignore=tests/unit -q -p asyncio --asyncio-mode=auto -p no:cacheprovider --tb=short --show-capture=no
wsl.exe -d Ubuntu --cd /mnt/f/Workspace/BL-HAOS/modules/integration env PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests/unit -q -p asyncio --asyncio-mode=auto -p no:cacheprovider --tb=short --show-capture=no
Set-Location F:/Workspace/BL-HAOS/modules/bridge; $env:PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'; & F:/Workspace/BL-HAOS/.venv/Scripts/python.exe -B -m pytest -c pytest.ini tests -q -p asyncio --asyncio-mode=auto -p no:cacheprovider --tb=short --show-capture=no
Set-Location F:/Workspace/BL-HAOS
npm --prefix modules/integration/panel_ui run test:host-config
npm --prefix modules/integration/panel_ui run typecheck:host
npm --prefix modules/integration/panel_ui test -- --reporter=dot
npm --prefix modules/bridge/web_ui test -- --reporter=dot
npm --prefix modules/integration/panel_ui run build
npm --prefix modules/bridge/web_ui run build
./scripts/run-tests.ps1 -Layer L1
```

| Gate | Latest Measured Result |
|---|---|
| Version/docs/static gate before full suites | Integration 10 passed; bridge config/assets 16 passed |
| Full WSL real Core 2026.10.3 | **127 passed**, 23.24s, no skips: 123 baseline + 4 new package/docs checks |
| Separate WSL stub units | **58 passed**, 1.27s, no skips |
| Full Windows bridge, correct cwd/autoload isolation | **323 passed, 1 existing POSIX skip, 1 warning**, 12.55s: 319 baseline + 4 new docs/release checks |
| Panel Vitest | **41 passed**, 2.04s |
| Bridge frontend Vitest | **26 passed**, six files, 1.06s |
| Typed panel build | Passed; Vite 1.16s |
| Typed bridge build | Passed; Vite 1.49s |
| Actual root L1 runner | Passed: bridge 323/1 skip/1 warning, 12.54s; integration 68 passed, 0.69s; frontend 26 passed, 1.23s |
| Pure host-config checks after safety refinement | **21 passed**, zero skipped, 77.79ms; not host acceptance |
| Dedicated host typecheck after final reporter cleanup | Passed |
| Missing-env actual Playwright invocation | **Expected exit 1**, exact `Host prerequisites: BLHAOS_HA_URL is required`; zero host scenarios executed, not a host pass |
| Scoped editor diagnostics | No errors in both Python tests, bridge constants, host config/spec |
| Root scoped and both module diff --check | Passed; root CRLF-to-LF advisories only |

The missing-env command spawned the actual panel-installed Playwright CLI in
a child environment with every BLHAOS_HA_* key and DEBUG/PWDEBUG removed. It
confirmed the fixed missing-URL error without printing raw output or reading
any auth state. The first shell wrapper's boolean was simplified by the tool;
the corrected conditional wrapper independently confirmed the exact error.
Counts from overlapping runs are not summed. The existing warning is Starlette's
httpx TestClient deprecation. No new product warning was introduced.

Generated panel output after the requested build: **232397 bytes**, SHA256
`7ddaaad48e28683d0bdf2767b247ec1091acc1f481efb9f4a570d259df76cec6`.
No panel source was changed in this run; this is local generated output, not
an authenticated HA screenshot or physical-playback observation.

### Blocking Host Evidence and Authorization

The production panel is not deployed, the last known speaker was disconnected,
and no provider metadata/references or external disposable session files were
provided. Required next inputs: separately authorized deployment/host access,
Core 2026.10.3 origin, explicit connected BL-HAOS target, original public
provider and playable-playlist references, external disposable auth fixture,
explicit real-play consent and a separately authorized naturally expiring
fixture/expiry-observation consent. Do not obtain these from the shared session.

Actual HA/provider hierarchy and public-provider layout, denied/unavailable/
unresolvable flows, actual expiry, long-name shell layout, viewport screenshots,
keyboard/focus/contrast/screen-reader backstop and physical playback remain
**unverified**. Root-only provider discovery and auth-error observability may
need a source-grounded harness adjustment after authorized host evidence; no
fallback or fake success is permitted. No live host, shared browser, provider,
speaker, token, deployment, restart, pairing or radio operation was accessed.
The earlier temporary probe used exactly its one permitted Core restart and
was removed/accepted. That authorization cannot be reused. No commits, staging,
branches, parent-state updates, phase 27 source edits or Phase 25/26 execution
occurred. Continue from 24-06-CHECKPOINT.md; mandatory host acceptance blocks
24-06 completion and PL-01/PL-02/PL-03 sign-off.

## Plan 24-06 Review WR-01/WR-02 Remediation - 2026-10-24

Scope: only 24-06-REVIEW WR-01/WR-02, plus IN-01 and IN-03. IN-02 is
unchanged because the plain-HTTP LAN origin is legitimate and needs approval
to restrict. No live host, deployment, shared session, storage contents,
installs, STATE or commits were involved.

- **WR-01:** safe-reporter.mjs maps exact static spec titles to fixed ids
  `catalog-dispatch`, `unauthenticated-denial` and `attested-expiry`. Any
  other title prints `unlisted`, and any unknown status prints `unknown`. It
  never prints the provider, a URL, an error or auth state. A pure test binds
  the spec titles to the allowlist. Provider-layout and dispatch failures
  still share `catalog-dispatch`.
- **WR-02:** the old predicate needed a string auth code while disconnected,
  which a live HA cannot produce. Pure `classifyExpiryEvidence` now decides.
  `expired` requires all three:
  - an attested fixture;
  - HA auth rejection: the exact `/auth/authorize` login path, `/auth/token`
    400/401, or `/api/` 401;
  - no accepted call: no 2xx, no accepted probe and no live connection.

  Numeric loss alone gives `disconnected`. A 403, or `unauthorized` on a live
  connection, gives `denied`, even when attested. The same rejection without
  attestation also gives `denied`. Missing `hass` off the login path stays
  `pending`. The spec records only origin-local pathname and status. New
  required `BLHAOS_HA_EXPIRY_ATTESTATION` hard-fails when missing. It means
  the separate owner already expired the fixture, which is used read-only.
  Nothing is forced or revoked.
- **IN-01:** a real `os.tmpdir()` test covers a directory junction into the
  workspace, a hard-link alias and a fixture in another Git checkout. It
  writes `{}` placeholders only. It assumes the temp directory is not inside a
  Git checkout.
- **IN-03:** `test_hacs_component_layout_and_manifest` asserts manifest
  `0.2.19`.

| Check | Result |
|---|---|
| RED: `node --test e2e/host-env.test.mjs` before implementation | 1 file-level fail: missing `expiry-evidence.mjs`/`SCENARIO_IDS`. Scaffold RED, not assertion-level |
| GREEN: same command | **32 passed**, 0 failed, 0 skipped. That is 21 earlier tests, 1 new missing-key test and 10 new tests |
| `npm run typecheck:host` | Exit 0 |
| Missing-env real Playwright CLI, all BLHAOS_HA_*/DEBUG/PWDEBUG removed | **Expected exit 1**, fixed missing-URL precondition, 0 scenario lines. Not a host pass |
| `pytest tests/test_package_layout.py` (integration) | 10 passed |
| Bridge `tests/test_addon_config.py tests/test_frontend_assets.py` after TESTING.md update | 16 passed |

Files touched:

- e2e/safe-reporter.mjs
- e2e/host-env.mjs
- e2e/host-env.test.mjs
- e2e/catalog.spec.ts
- new e2e/expiry-evidence.mjs
- modules/integration/tests/test_package_layout.py
- TESTING.md
- 24-06-CHECKPOINT.md
- this file

One accidental empty scratch file created during this run was deleted
immediately. Each finding took one repair loop.

**Limitations:**

- Real HA behaviour is unverified for both expiry paths: the login redirect
  and the `/auth/token` rejection.
- Observing these on a real host proves rejection of an attested fixture.
  Natural expiry rests on the owner's attestation. A never-valid fixture
  would look the same.
- Provider layout, viewport screenshots and physical audio remain
  **unverified**.
- The run is blocked on separately authorized host acceptance. No 24-06
  SUMMARY was created.

## Final Independent Local Coverage Audit - 2026-10-24

This is the current authoritative local audit, superseding older pending-review
and suite-count statements above. All six PLANs, five SUMMARYs, four clean
02-05 reviews, 06 checkpoint/review, CONTEXT, UI-SPEC, actual source, tests,
docs and release metadata were read. No 06 SUMMARY exists or was created.
The parent-supplied final assertion-level RED (32 pass / 1 fail) is historical;
this verifier did not revert source to reconstruct it.

### Independently Executed Final Gates

| Gate | Command from root unless stated | Result |
| --- | --- | --- |
| G1 Core | `wsl.exe -d Ubuntu --cd /mnt/f/Workspace/BL-HAOS/modules/integration env BLHAOS_RUN_SIL=1 PYTHONDONTWRITEBYTECODE=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -B -m pytest tests --ignore=tests/unit -q -p asyncio --asyncio-mode=auto -p no:cacheprovider --tb=short --show-capture=no` | 127 passed, zero skips, 23.49s: 91 native SIL, 26 lifecycle, 10 package/docs |
| G2 isolated WSL units | Same cwd/interpreter; `env BLHAOS_RUN_SIL=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 ... -B -m pytest tests/unit -q -p asyncio --asyncio-mode=auto -p no:cacheprovider --tb=short --show-capture=no` | 58 passed, zero skips, 1.36s; separate process |
| G3 actual root runner | `& ./scripts/run-tests.ps1 -Layer L1` | PASS: bridge 323 passed / 1 POSIX skip / 1 existing Starlette warning, 13.24s; portable integration 68 passed, 0.71s; bridge Vitest 26 passed, 1.14s |
| G4 panel Vitest | `npm --prefix modules/integration/panel_ui test -- --reporter=dot` | 41 passed, 1.62s |
| G5 typed panel build | `npm --prefix modules/integration/panel_ui run build` | PASS, Vite 1.19s |
| G6 typed ingress build | `npm --prefix modules/bridge/web_ui run build` | PASS, Vite 1.29s |
| G7 pure harness | `node --test modules/integration/panel_ui/e2e/host-env.test.mjs` | 33 passed, zero skipped, 88.9952ms |
| G8 harness types | `npm --prefix modules/integration/panel_ui run typecheck:host` | PASS; configuration not evaluated |
| WR-02 independent control matrix | In-memory Node import of classifyExpiryEvidence, no environment loader | 12 assertions pass: live 401/403/token rejection without probe code is denied; successful calls win; numeric disconnect is not expiry; attestation distinguishes denied/expired classification |

Each full surface ran once. Root L1 supplies the requested full Windows bridge
gate in modules/bridge with plugin autoload disabled and the existing root
.venv Python 3.14.7; no redundant standalone Windows bridge or Vitest run.
Its portable integration overlap with the explicitly requested WSL gates is
not summed as unique coverage. Core uses Python 3.14.4 / pytest 9.0.3 /
helper 0.13.374, not HA stubs. Full gates are explicitly user-required final
gates, not repeated single-truth spot-checks.

The generated panel remains 232397 bytes with SHA256
7ddaaad48e28683d0bdf2767b247ec1091acc1f481efb9f4a570d259df76cec6.
Structured package/lock-root comparison passes. Bridge constants/config/top
changelog agree at 0.2.69; integration manifest is 0.2.19. Both remain undeployed.

### Coverage and Evidence Quality

All 16 task rows above are reconciled: 13 local automated contracts COVERED,
two prior explicit human gates ACCEPTED, one mandatory host task PARTIAL.
PL-01/02/03 each have green behavior-focused local tests, but full requirements
remain NEEDS HUMAN, not satisfied. No Phase 24 requirement is orphaned.
No new tests were needed or authorized; implementation/test files were not edited.
Wave 0 infrastructure is complete, not final host validation.

Core lifecycle tests use actual HTTP and event-gated executor/registration
cancellation; transport tests keep the entity/client loop real and fake only
I/O. URL tests assert both exact internal handoff and component-by-component
absence from logs/displayed chains. Panel tests assert state transitions and
exact calls, not just existence. CSS strings prove declared rules only, not
actual HA layout or assistive-technology behavior. The existing POSIX skip
does not replace any Phase 24 requirement test. Temporary `{}` files in the
pure path test are filesystem inputs, not circular generated expected output.

The current 24-06 review is clean for the bounded WR-02 resolution, retaining
the plain-HTTP informational risk. Actual expiry is not cryptographic proof:
only separate owner attestation plus observed HA rejection can support the
declared host result. No current/shared session is read or modified.

### Manual-Only and Nyquist Disposition

Still required: authorized deployment, Core 2026.10.3 origin, one connected
BL-HAOS entity, configured audio-provider and playable-playlist opaque refs,
external disposable authenticated fixture, explicit real-play consent, and a
different externally stored owner-attested expired disposable fixture with
read-only observation consent. Do not supply secrets through chat.

Actual provider/physical audio, denied/unavailable/unresolvable/expired access,
full host leakage review, 375/768/1440 screenshots, long-name/selector geometry,
keyboard/focus/AT/contrast/reduced-motion acceptance remain unverified. The
three prepared host scenarios do not automate every manual failure/backstop.
Native browser fixtures and prior accepted mechanism evidence are not final
HA proof. No host test, env-file inspection, install/network, deployment,
restart, playback or expiry manipulation ran in this audit.

Nyquist local mapping is complete; full compliance is false while the required
manual-only task is pending. Hardware is explicitly deferred, not passed.
No commits/staging/branches, STATE/ROADMAP/REQUIREMENTS/state.json updates,
Phase 27 evidence edits, phase completion or requirement completion.

## Validation Audit

| Metric | Result |
| --- | --- |
| Tasks audited | 16 |
| Automated local task contracts covered | 13 |
| Previously accepted explicit human gates | 2 |
| Mandatory host task partial / escalated | 1 |
| Concrete unresolved local defects | 0 |
| Full Nyquist compliant | false; host/hardware/manual acceptance pending |
