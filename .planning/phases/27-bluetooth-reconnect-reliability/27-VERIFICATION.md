---
phase: 27-bluetooth-reconnect-reliability
verified: "2026-10-28T02:16:13Z"
status: human_needed
score: 9/9 local must-haves verified
completion_scope: local-implementation-and-tests-only
refresh_scope: phase25-26-docs-test-sync-only
prior_verification:
  status: passed
  score: 9/9
  verified: "2026-10-24T17:12:18.438Z"
  refresh_reason: phase26-shared-files-and-integration-surfaces
nyquist_compliant: true
validation_status: validated
security_status: verified
security_assessment: parent-direct-asvs-l1-specialized-agent-unavailable
covered_files:
  - .planning/phases/26-sequential-playback-queue-controls/26-05-SUMMARY.md
  - .planning/phases/26-sequential-playback-queue-controls/26-VALIDATION.md
  - .planning/phases/27-bluetooth-reconnect-reliability/27-01-PLAN.md
  - .planning/phases/27-bluetooth-reconnect-reliability/27-01-SUMMARY.md
  - .planning/phases/27-bluetooth-reconnect-reliability/27-CONTEXT.md
  - .planning/phases/27-bluetooth-reconnect-reliability/27-RESEARCH.md
  - .planning/phases/27-bluetooth-reconnect-reliability/27-REVIEW-FIX.md
  - .planning/phases/27-bluetooth-reconnect-reliability/27-REVIEW.md
  - .planning/phases/27-bluetooth-reconnect-reliability/27-SECURITY.md
  - .planning/phases/27-bluetooth-reconnect-reliability/27-VALIDATION.md
  - modules/bridge/CHANGELOG.md
  - modules/bridge/DOCS.md
  - modules/bridge/README.md
  - modules/bridge/backend/bl_haos/api/routes.py
  - modules/bridge/backend/bl_haos/bluetooth/device.py
  - modules/bridge/backend/bl_haos/bluetooth/manager.py
  - modules/bridge/backend/bl_haos/bluetooth/reconnect.py
  - modules/bridge/backend/bl_haos/constants.py
  - modules/bridge/backend/bl_haos/ha/player.py
  - modules/bridge/backend/bl_haos/health.py
  - modules/bridge/backend/bl_haos/main.py
  - modules/bridge/config.yaml
  - modules/bridge/pytest.ini
  - modules/bridge/tests/test_addon_config.py
  - modules/bridge/tests/test_api.py
  - modules/bridge/tests/test_auto_reconnect.py
  - modules/bridge/tests/test_bluetooth_device.py
  - modules/bridge/tests/test_bluetooth_manager.py
  - modules/bridge/tests/test_bridge_sil.py
  - modules/bridge/tests/test_health.py
  - modules/bridge/tests/test_media_player.py
  - modules/bridge/tests/test_native_transport.py
  - modules/bridge/tests/test_phase25_docs.py
  - modules/bridge/tests/test_phase26_docs.py
  - modules/bridge/web_ui/src/api/client.test.ts
  - modules/bridge/web_ui/src/api/client.ts
  - modules/bridge/web_ui/src/components/SpeakerCard.test.tsx
  - modules/bridge/web_ui/src/components/SpeakerCard.tsx
  - modules/bridge/web_ui/src/constants.ts
  - modules/bridge/web_ui/src/hooks/useBluetoothEvents.test.tsx
  - modules/bridge/web_ui/src/hooks/useBluetoothEvents.ts
  - modules/integration/README.md
  - modules/integration/custom_components/bl_haos/client.py
  - modules/integration/custom_components/bl_haos/const.py
  - modules/integration/custom_components/bl_haos/media_player.py
  - modules/integration/custom_components/bl_haos/playlist_library.py
  - modules/integration/panel_ui/e2e/playlist-library.spec.ts
  - modules/integration/panel_ui/mock-harness.html
  - modules/integration/panel_ui/src/media-panel.test.tsx
  - modules/integration/panel_ui/src/media-panel.tsx
  - modules/integration/tests/test_ha_integration_sil.py
  - modules/integration/tests/test_phase25_docs.py
  - modules/integration/tests/test_phase26_docs.py
  - modules/integration/tests/test_playlist_library_sil.py
covered_digest: "v3:sha256:b994a22c1ede8521bb43ad28fcede6ab3215c4329ae948a3ef3fae3e5ff02113"
behavior_unverified: 0
overrides_applied: 0
hardware_soak: pending-authorized-deployment
hardware_proven: false
current_prepared_bridge_version: "0.2.69"
historical_phase27_version: "0.2.68"
this_refresh_full_suite_runs: 0
this_refresh_named_checks:
  bridge_docs_contracts:
    command: "F:/Workspace/BL-HAOS/.venv/Scripts/python.exe -m pytest -c pytest.ini tests/test_phase25_docs.py tests/test_phase26_docs.py -q --tb=short -p no:cacheprovider"
    cwd: modules/bridge
    collected: 2
    passed: 2
    skipped: 0
    duration_seconds: 0.02
    exit_code: 0
  integration_docs_contracts:
    command: "F:/Workspace/BL-HAOS/.venv/Scripts/python.exe -m pytest -c pytest.ini tests/test_phase25_docs.py tests/test_phase26_docs.py -q --tb=short -p no:cacheprovider"
    cwd: modules/integration
    collected: 2
    passed: 2
    skipped: 0
    duration_seconds: 0.01
    exit_code: 0
this_refresh_reconnect_suite_runs: 0
this_refresh_phase26_ui_tests: not-run
reconnect_implementation_tests_changed_in_final_adjustment: false
phase26_recorded_evidence:
  bridge_queue_player_api_native: 33 passed
  pinned_core_2026_10_3_integration_queue_sil: 11 passed
  panel_queue_and_touched_vitest: "4 and 46 passed"
  ingress_queue_and_touched_vitest: "12 and 28 passed"
  mock_playwright_queue: 3 passed
  docs_contracts: 2 passed
  panel_and_ingress_build_typechecks: passed
  rerun_in_this_refresh: false
security_threshold:
  value: critical
  scope: local-only
  restore_to: high
  required_before: "any live verification, release, or deployment work"
human_verification:
  - test: "Authorized HAOS and physical-speaker reconnect soak"
    expected: "After separate deployment authorization, observe bounded retries, retained pairing, busy pacing, half-open recovery, explicit operator reset, and stable playback through power loss/return and repeated failures."
    why_human: "Fake BlueZ and SIL cannot establish real daemon ordering, radio stability, or audible playback; no deployment or hardware action is authorized in this refresh."
decision_coverage:
  honored: 0
  total: 0
  not_honored: []
  skipped: true
  reason: no trackable decisions
retained_pre_phase26_full_bridge_gate:
  evidence_scope: historical-phase24-independent-final-gate-predates-phase26-shared-changes
  source_report: .planning/phases/24-ha-media-catalog-provider-playback/24-VALIDATION.md
  source_section: Final Independent Local Coverage Audit - G3
  observed_before: "2026-10-24T17:01:39.046Z"
  command: "& ./scripts/run-tests.ps1 -Layer L1"
  cwd: F:/Workspace/BL-HAOS
  bridge_cwd: F:/Workspace/BL-HAOS/modules/bridge
  bridge_interpreter: F:/Workspace/BL-HAOS/.venv/Scripts/python.exe
  bridge_plugin_autoload: disabled
  independent_full_runs: 1
  exit_code: 0
  collected: 324
  passed: 323
  skipped: 1
  warnings: 1
  duration_seconds: 13.24
prior_phase27_refresh_checks:
  bluetooth_three_files:
    collected: 91
    passed: 91
    skipped: 0
    warnings: 0
    duration_seconds: 9.81
    exit_code: 0
  version_metadata:
    collected: 2
    passed: 2
    duration_seconds: 0.08
    exit_code: 0
  api_reconnect_false:
    collected: 53
    selected: 3
    passed: 3
    deselected: 50
    warnings: 1
    duration_seconds: 1.12
    exit_code: 0
must_haves:
  truths:
    - One scheduled reconnect invokes the manager once and Device1.Connect at most once; only AlreadyConnected can additionally activate one A2DP profile.
    - Busy BlueZ responses issue no ConnectProfile and propagate BluetoothOperationInProgress without false connection success.
    - Automatic and operator connect_device requests share actual-adapter ownership, fail fast on contention, and release ownership after exceptions, timeout and cancellation.
    - An entire manager connect operation is bounded to 30 seconds; automatic attempts never disconnect an existing link and explicit operator reset remains supported.
    - Failure pacing uses 10s initial delay, multiplier 2, 120s final cap, non-negative 15% jitter and a 300s breaker after eight failures; busy, presence and failed recovery never shorten pacing or clear failure history.
    - Breaker expiry permits one half-open attempt with retained history; failure reopens the breaker and confirmed connection success clears failure pacing.
    - Existing 5s dropout grace, 15s successful-link settle and six-flaps-in-120s suppression with 60s cooldown remain effective.
    - Focused regression tests are observed red before each behavior edit, then focused Bluetooth/API/SIL and the complete bridge suite pass.
    - Operator documentation describes conservative retries and preserved pairing; historical Phase 27 release 0.2.68 remains in changelog history and current manifest/runtime/package versions consistently equal the superseding prepared release 0.2.69.
---

# Phase 27: Bluetooth Reconnect Reliability Verification Report

**Phase Goal:** Prevent reconnect storms by removing nested connection retries, sharing connection ownership across automatic and operator requests, and preserving conservative backoff through failure and recovery.
**Verified:** 2026-10-28T02:16:13Z
**Status:** human_needed. Local implementation/test criteria pass; the authorized hardware soak remains outstanding.
**Scope:** `local-implementation-and-tests-only`. No hardware soak, live/production verification, release, or deployment is claimed.
**Score:** 9/9 Phase 27 local must-haves verified; 0 behavior-unverified local truths. The plan's future hardware human-check remains pending.

## Final Docs/Test Sync — 2026-10-28

The final adjustment changed shared bridge `DOCS.md` and `tests/test_phase25_docs.py`; Phase 27 reconnect implementation and tests did not change. Fresh checks were limited to the four Phase 25/26 documentation contracts: bridge **2/2 passed** and integration **2/2 passed**. No reconnect suite or Phase 26 UI tests were run in this final refresh. Earlier reconnect/API evidence remains prior local evidence, not a new suite result.

## Phase 26 Shared-Surface Refresh — 2026-10-28 (Prior)

This section preserves the source/wiring audit from the preceding shared-surface refresh. Phase 26 changed bridge player/API/lifecycle/docs and integration/UI surfaces, which were re-read against Phase 27's reconnect contract. The final docs/test sync above is the current report authority.

### Observable Truths

| # | Truth | Status | Current evidence |
|---|---|---|---|
| 1 | One scheduled reconnect invokes the manager once and Device1.Connect at most once; only AlreadyConnected may additionally activate one A2DP profile. | VERIFIED | Current `_attempt_reconnect` has one manager await; current manager has one `dev.connect()` in the bounded operation. Phase 27's prior local Bluetooth gate recorded 91/91 passing across device, manager, and reconnect files; the real fake-BlueZ scheduler tracer asserts one Connect and zero profile calls. |
| 2 | Busy BlueZ responses issue no ConnectProfile and propagate `BluetoothOperationInProgress` without false connection success. | VERIFIED | Current device code classifies busy before the AlreadyConnected profile branch and sets Connected only after success. The prior 91-case Bluetooth gate includes the busy spellings and disconnected-state assertions. Phase 26 queue-command failure remains a separate HTTP 409 path with no reconnect; failed-play recovery still uses its explicit reset contract. |
| 3 | Automatic and operator connects share actual-adapter ownership and release it after exception, timeout, and cancellation. | VERIFIED | Current manager selects the resolved device's adapter and uses its manager-owned lock through the operation. Prior phase27 tests cover both contention orderings, other-adapter independence, cancellation/timeout reuse, and real-lock cleanup. Phase 26 did not change this manager boundary. |
| 4 | The complete manager operation is bounded to 30 seconds; automatic attempts do not disconnect existing links and explicit operator reset remains supported. | VERIFIED | Current `asyncio.timeout(30.0)` encloses resolution through trust update. The scheduler calls `connect_device` without reset; REST Connect and failed-play recovery explicitly pass `reset_existing=True`. Phase 26 queue routes dispatch queue operations directly and its tests assert queue-start failure does not enter reconnect/retry. |
| 5 | Backoff uses 10-second initial delay, multiplier 2, 120-second cap, non-negative 15% jitter, and a 300-second breaker after eight failures; busy, presence, and failed recovery preserve pacing/history. | VERIFIED | Current constants and scheduler match those bounds; prior phase27 deterministic tests cover exact delays, saturation, busy/presence deadlines, half-open history, and overflow boundaries. |
| 6 | Breaker expiry allows one half-open attempt with retained history; failure reopens it and confirmed success clears pacing. | VERIFIED | Current tick checks the breaker deadline before scheduling and the inflight map suppresses duplicate workers. Prior named half-open regression asserts retained history, reopening on failure, and reset after success. |
| 7 | Five-second dropout grace, 15-second successful-link settle, and six-flaps-in-120-seconds/60-second cooldown remain effective. | VERIFIED | Current constants preserve these values; prior phase27 state-machine, settle, and flap tests exercise the transitions. Phase 26 playback generation invalidation is separate and does not own reconnect deadlines. |
| 8 | Focused deterministic tests cover reconnect behavior and the changed API/native queue consumers without overstating suite coverage. | VERIFIED | Phase 27 prior local evidence includes 91/91 Bluetooth cases and its six-file focus gate/full-bridge evidence. Phase 26 records 33 bridge queue/player/API/native-selector passes and 11 pinned integration queue SIL passes. These Phase 26 checks are not a fresh full reconnect suite. |
| 9 | Current operator docs describe conservative retries/pairing preservation, and soak remains pending authorization. | VERIFIED | Current bridge README/DOCS and changelog retain the reconnect policy, undeployed 0.2.69 identity, pairing preservation, and pending authorized soak. Phase 26 bridge/integration documentation contracts each passed in its recorded gate; those docs describe queue semantics and keep local/mock versus production acceptance distinct. |

**Local score:** 9/9; behavior_unverified=0; overrides_applied=0. PROD-04 and PROD-05 remain locally satisfied. No playlist requirement is claimed complete here.

### Phase 26 Shared-Surface Audit

| Changed surface | Effect on Phase 27 contract | Evidence/provenance |
|---|---|---|
| Bridge `api/routes.py` | Explicit Connect and failed-play recovery still request one manager reset under shared ownership; busy remains HTTP 409. Queue commands use a separate non-retryable branch and do not call the reconnect manager. | Current source trace; Phase 26 bridge selector evidence; prior Phase 27 API boundary evidence. |
| Bridge `main.py` and `ha/player.py` | Lifecycle still starts/stops the reconnect engine; speaker-loss queue invalidation and generation-fenced process completion affect playback state, not Bluetooth connection ownership. | Current source trace; Phase 26 bridge player/API/native selector evidence. |
| Bridge docs and integration docs/client/entity/library | Reconnect policy remains intact; Phase 26 adds queue-specific single-attempt semantics and retains HA-owned resolution/capability boundaries. | Current bridge DOCS and integration README read; Phase 26 docs contracts and recorded SIL/UI tests. |
| Integration and UI | Queue controls use versioned bridge commands; queue start/next/previous are not auto-retried. No new reconnect or reset path was found in the changed client/entity paths. | Current integration client/entity trace; Phase 26 recorded pinned SIL, panel/ingress tests, and temporary-output builds. |

Phase 26 recorded: bridge queue/player/API/native selector **33 passed**; pinned Core 2026.10.3 integration queue SIL **11 passed**; panel queue/full touched tests **4/46 passed**; ingress queue/full touched tests **12/28 passed**; mock Playwright queue suite **3 passed**; bridge and integration docs contracts **1 passed each**; both UI temporary-output builds/typechecks passed. These are Phase 26 recorded results, not tests rerun by this report refresh and not a full reconnect-suite result.

### Retained Phase 27 Local Evidence

The latest prior Phase 27 evidence recorded a three-file Bluetooth gate of **91 passed**, two version metadata cases passed, and three selected changed-API cases passed. The earlier independent full bridge evidence recorded **323 passed, 1 existing POSIX-only skip, and 1 warning**. Those historical local runs were not repeated as a full reconnect or bridge suite in this refresh. This report will separately identify any narrow named checks run during refresh; no Phase 26 count is substituted for them.

Historical red-first results, review-fix regressions, and the full command/timing ledger remain in `27-01-SUMMARY.md` and `27-VALIDATION.md`. The clean scoped review and its boundary remain in `27-REVIEW.md`; the local threat disposition and security-agent limitation remain in `27-SECURITY.md`.

### Named Reconnect/API Checks — Prior Refresh

These selected reconnect/API checks were run before the final docs-only sync. They remain prior local evidence and were not rerun here because reconnect implementation and tests did not change.

Run from `modules/bridge` with `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` and the bridge-local `pytest.ini`:

```powershell
F:/Workspace/BL-HAOS/.venv/Scripts/python.exe -m pytest -c pytest.ini tests/test_auto_reconnect.py::test_phase27_connection_scheduled_tick_has_one_bluez_attempt tests/test_auto_reconnect.py::test_phase27_pacing_breaker_half_open_retains_history_until_success tests/test_bluetooth_manager.py::test_phase27_connection_shared_actual_adapter_ownership tests/test_bluetooth_manager.py::test_operator_connect_still_resets_an_existing_link tests/test_bluetooth_device.py::test_phase27_connection_busy_never_activates_profile tests/test_api.py::test_native_play_media_redact_logs_and_errors tests/test_api.py::test_native_queue_start_does_not_reconnect_or_retry_sink_failure tests/test_phase26_docs.py::test_phase26_queue_usage_docs_match_the_bridge_contract -q --tb=short -p no:cacheprovider
```

**Result:** 36 passed, 0 skipped, 1 existing Starlette/httpx TestClient deprecation warning, 5.32 seconds; exit 0. This named spot-check covers scheduler call count, breaker state, manager ownership/operator reset, busy classification, explicit failed-play recovery, queue no-reconnect behavior, and the bridge Phase 26 docs contract. It is not a full reconnect or bridge suite.

### Required Artifacts and Key Links

Canonical artifact query: exit 0, **4/4** passed (`manager.py`, `reconnect.py`, `test_auto_reconnect.py`, and `DOCS.md`); all exist and are substantive. The canonical key-link query returns **0/4 automatic matches** because the plan's `from` values are symbols, not repository-relative file paths. Manual source and behavioral-test trace verifies all four declared runtime links:

| From | To | Status | Evidence |
|---|---|---|---|
| `AutoReconnectEngine._attempt_reconnect` | `BluetoothManager.connect_device` | WIRED | One awaited manager call; no reset flag; the scheduled fake-BlueZ tracer asserts one Connect. |
| `BluetoothManager.connect_device` | `BluetoothDevice.connect` | WIRED | One awaited connect inside the manager timeout and actual-adapter lock; contention and cleanup tests pass. |
| `BluetoothDevice.connect` | `BluetoothOperationInProgress` | WIRED | Busy classification precedes profile fallback; five busy spellings assert no profile call and no connected success. |
| `AutoReconnectEngine._on_device_event` | `SpeakerReconnectProfile.next_retry_time` | WIRED | Presence does not advance the pending deadline; the retained-deadline behavior test passes. |

### Requirements Coverage

| Requirement | Status | Evidence |
|---|---|---|
| PROD-04 | Satisfied locally | Bounded manager operation, shared adapter ownership, and release after failure/timeout/cancellation are covered by prior Phase 27 behavior tests and the current named manager checks. |
| PROD-05 | Satisfied locally | Conservative backoff, breaker history, no automatic reset/retry amplification, and pairing preservation are covered by the prior Phase 27 regressions and current named scheduler/device checks. |

No additional Phase 27 requirement is mapped to this phase outside PROD-04/05. Phase 26's PL-07 through PL-10 remain production-pending and are not claimed here.

### Test Quality, Anti-Patterns, and Probes

The current 36 selected cases all ran and passed; no selected case was skipped. Phase 27's prior local audit inspected value-level call-count, deadline, history, identity, and cleanup assertions; Phase 26's verifier records no disabled queue tests or circular expected-value generation. No unreferenced `TBD`, `FIXME`, `XXX`, `TODO`, `HACK`, or implementation placeholder was found in the inspected Phase 27 Bluetooth source, regression tests, or current DOCS. The three `PLACEHOLDER` matches in `constants.py` are explicit redaction markers (`[omitted]`, `[redacted]`, `[url redacted]`), not unfinished code. No Phase 27 probe is declared or required; no server or service was started.

Decision coverage query: **skipped, 0/0**, because `27-CONTEXT.md` has no trackable decision IDs. Its descriptive decisions were traced to the local truths; the gate is non-blocking.

### Requirements and Residuals

| Requirement | Local status | Production/live status |
|---|---|---|
| PROD-04 | Satisfied locally: bounded manager operation and shared adapter ownership. | Hardware soak pending separate authorization. |
| PROD-05 | Satisfied locally: conservative pacing, retained pairing, and no nested automatic reset/retry. | Hardware soak pending separate authorization. |

The hardware reconnect soak remains pending authorized deployment. Release and deployment remain blocked; the prepared bridge 0.2.69 is undeployed. `.planning/config.json` currently sets `workflow.security_block_on` to `critical` for local progression only; restore it to `high` before any live verification, release, or deployment work. The Phase 26 generated `panel_static` bundle remains unchanged and needs its separately authorized packaging step before HA serves the updated panel source.

### Human Verification Required

**Authorized HAOS and physical-speaker reconnect soak**

**Test:** After separate deployment authorization, exercise speaker power loss/return, BlueZ busy responses, repeated failures and half-open recovery, then explicit operator reset and playback stability.
**Expected:** Scheduled attempts remain bounded and paced, the breaker retains history, pairing survives, operator reset remains explicit, and playback is stable.
**Why human:** Fake BlueZ/SIL cannot establish daemon ordering, radio stability, physical pairing retention, or audible playback. No live Home Assistant/Bluetooth, deployment, restart, or physical playback is authorized or performed by this refresh.

### Refresh Boundary

No live HA/Bluetooth access, deployment, restart, physical playback, staging, or commit occurred. Only this verification report is in scope. The four fresh checks cover documentation contracts only; no reconnect suite or Phase 26 UI tests ran in this final refresh. `this_refresh_full_suite_runs` and `this_refresh_reconnect_suite_runs` are zero.

## Prior Refresh Scope and Authority — 2026-10-24 (Superseded)

The following section is retained as a historical report snapshot. Its Phase 24 refresh evidence and timestamps are not the current Phase 26 shared-surface refresh.

  This section and the frontmatter are the current canonical assessment. The
  older report body below is preserved as a dated historical record, not current
  version, suite-count, phase-routing or deployment guidance.

  Read Phase 27 CONTEXT, PLAN, SUMMARY, clean REVIEW, SECURITY and prior
  VERIFICATION, the current ROADMAP/REQUIREMENTS/STATE scope, actual Bluetooth
  source and assertion-level tests, all nine moved covered files, and Phase 24's
  canonical VERIFICATION plus its latest independent VALIDATION gate evidence.
  SUMMARY claims alone were not accepted as behavior proof.

  The initial canonical query returned stale with exactly these moved files:
  27-SECURITY.md; bridge CHANGELOG.md, DOCS.md, README.md, api/routes.py,
  constants.py, config.yaml, test_addon_config.py and test_api.py. Core device,
  manager and reconnect source and their three test files were not moved in the
  prior fingerprint. Their current control flow and passing behavioral assertions
  were nevertheless checked directly.

  Current authority supersedes old phase-routing prose: Phase 24 plans 02-05 have
  local implementation and plan 06 has preparation only; Phase 24 remains
  human_needed pending real-host acceptance. The earlier Phase 27 statement that
  playlist work was paused is historical, not an instruction to undo Phase 24.
  Only this Phase 27 report is edited. No production/test, PLAN/SUMMARY/SECURITY,
  Phase 24 artifact, global STATE or other planning-state edit is authorized.

  ## Goal Achievement

  ### Observable Truths

  All paths below are bridge-relative. VERIFIED denotes local source/wiring plus
  appropriate behavioral evidence, not physical BlueZ, deployment or playback proof.

  | # | Truth | Status | Current evidence |
  | --- | --- | --- | --- |
  | 1 | One scheduled request calls the manager once and Device1.Connect at most once; only AlreadyConnected may activate one A2DP profile. | VERIFIED | `_attempt_reconnect` awaits manager once; manager awaits `dev.connect` once. Fresh real engine/manager/device tracer asserts one fake BlueZ Connect, zero profile calls and one failure; AlreadyConnected compatibility remains green. |
  | 2 | Busy never starts profile fallback or falsely reports connection success. | VERIFIED | Device classifies busy before AlreadyConnected and sets Connected only after success. Five busy spellings, generic error and manager busy assertions pass in the fresh 91-case gate. Existing explicit Connect HTTP 409 handling remains wired. |
  | 3 | Automatic/operator requests share actual-adapter ownership and release it after failure, timeout and cancellation. | VERIFIED | Manager-owned `_connection_locks`, fail-fast contention and async lock scope remain intact. Both caller orderings, other-adapter independence, 30s timeout capture, canonical resolution, withdrawal barriers and real-lock cleanup pass. |
  | 4 | Entire manager connection is bounded to 30s; automatic reconnect never resets a live link; operator reset remains explicit. | VERIFIED | Timeout begins before ensure_device; disconnect requires `dev.connected and reset_existing`. Scheduler supplies no reset flag. Existing connected no-op/operator-reset tests pass. Changed failed-play route still calls manager once with reset_existing=True; fresh API failure slice asserts exact call and HTTP 409. |
  | 5 | Conservative 10/20/40/80/120s pacing, non-negative 15% jitter and eight-failure/300s breaker retain failure history and later deadlines. | VERIFIED | Constants and scheduler match; exact delay, supported-domain, huge-step, busy/presence and manual-owner tests pass. No automatic reset recovery or scheduler-owned adapter lock remains. |
  | 6 | Breaker expiry permits one half-open attempt retaining history; failure reopens it and confirmed success clears pacing. | VERIFIED | `_tick` checks breaker deadline and inflight ownership; fresh half-open test asserts eight failures, no early attempt, ninth failure/reopen and later success resetting counters/deadlines. |
  | 7 | Grace, settle, flap suppression and identity-safe cancellation remain effective. | VERIFIED | Existing 5s grace, 15s settle, six-flaps/120s and 60s cooldown regressions pass. Stop/unregister cleanup tests use real manager locks; replacement-profile identity is preserved and old completion cannot resurrect it. |
  | 8 | Historical red-first provenance is retained and current Bluetooth/API/bridge regression evidence is green. | VERIFIED | Historical RED/GREEN is attributed to SUMMARY/VALIDATION and prior review, not reconstructed. Fresh Bluetooth 91/91 and changed API 3/3 pass. Latest independent Phase 24 G3 records full bridge 323 pass/1 POSIX skip; no full-suite rerun here. |
  | 9 | Retry/pairing docs remain accurate and release evolution preserves Phase 27 history with consistent current metadata. | VERIFIED | DOCS stability section/README retain conservative policy and deferred soak. Changelog keeps 0.2.68 reconnect fixes beneath undeployed 0.2.69. Two fresh tests assert parsed manifest == runtime == package version and exact current 0.2.69/changelog agreement. |

  **Score:** 9/9 local truths; behavior_unverified=0; overrides_applied=0.
  Roadmap criteria 1-4 map to truths 1-8; criterion 5 maps to truth 9 and the
  explicitly pending hardware boundary. All five criteria remain satisfied within
  that approved boundary. PROD-04 and PROD-05 remain locally satisfied, with
  hardware soak pending; both are claimed by PLAN, with no orphaned Phase 27 ID.
  No later-phase deferral is used to conceal an implementation gap.

  ### Release Evolution, Not a Version Regression

  PLAN/SUMMARY correctly describe the historical Phase 27 patch 0.2.68. They are
  not rewritten. The approved current request explicitly recognizes the later
  Phase 24 integrated prepared release 0.2.69; current config/constants/package
  must agree at 0.2.69 rather than be rewound to satisfy the old literal version.
  This is the current release contract, not an invented override or a production
  edit. Both changelog sections remain, and the top release expressly retains the
  0.2.68 reconnect fixes. Neither release is claimed deployed or hardware-proven.

  ### Shared-File Audit

  | Changed covered surface | Evidence and impact on Phase 27 |
  | --- | --- |
  | 27-SECURITY.md | Current direct-parent local L1 report remains verified, five scoped threats closed, zero open; accepted no-dependency-change risk and unavailable specialized-agent limitation are explicit. No new independent security certification is claimed. |
  | CHANGELOG/DOCS/README | 0.2.69 adds HA-owned catalog guidance and truthful undeployed acceptance limits; reconnect history/policy and pending soak remain intact. Historical aggressive/reset descriptions in older changelog entries are not current promises. |
  | constants.py/config.yaml | Current release is 0.2.69. Phase 27 retry defaults and grace/settle/flap constants remain intact; fresh behavior/version assertions pass. |
  | api/routes.py | Actual diff changes bounded URL-free playback logs/errors and exception display. Explicit Connect busy mapping and reset intent persist. Existing failed-play execution retry loop is not a new manager/BlueZ connection loop: its single connect is outside that loop. Scheduler never enters this route. |
  | test_addon_config.py/test_api.py | Adds content-sensitive release/doc and URL/error assertions without disabling Bluetooth coverage. Fresh version and reconnect-false branches pass; latest independent G3 includes the expanded API suite. |

  ### Required Artifacts and Key Links

  Canonical `verify.artifacts` from repository root: exit 0, **4/4** passed.
  Manager, reconnect engine and its test artifact remain substantive and wired;
  DOCS agrees with the real control flow. The first invocation from bridge cwd
  resolved repository-relative paths incorrectly and is rejected as harness
  evidence, not classified as missing implementation.

  Canonical `verify.key-links`: exit 1, **0/4 automatic matches** because every
  PLAN `from` is a symbol rather than a relative file path, the same documented
  declaration limitation as before. PLAN is preserved; no automatic wiring pass
  is claimed. Manual implementation tracing and fresh behavioral assertions
  establish **4/4 runtime links**:

  | From | To | Runtime evidence | Status |
  | --- | --- | --- | --- |
  | Scheduler `_attempt_reconnect` | Manager `connect_device` | One await, no reset flag; real tracer and exact-call pacing tests | WIRED |
  | Manager `connect_device` | Device `connect` | One await under actual-adapter lock and whole-operation timeout | WIRED |
  | Device `connect` | BluetoothOperationInProgress | Busy classification precedes profile fallback; five actual device cases | WIRED |
  | Device event handler | Profile retry deadline | Presence never accelerates retained deadline; exact-value event tests | WIRED |

  ### Data-Flow Trace

  | Value | Source and flow | Status |
  | --- | --- | --- |
  | Inventory/connection state | BlueZ properties -> canonical BluetoothDevice -> manager.get_devices -> REST/native records; replacement/withdrawal assertions reject stale success | FLOWING locally; hardware source uncontacted |
  | Retry state/history/deadline | Real manager results/events -> registered profile -> guarded scheduling and identity-safe inflight cleanup | FLOWING; behavior exercised |
  | Health outcome | Classified manager/engine observations -> registry snapshot/native health output | FLOWING; existing fresh reconnect health assertions and retained full-gate health evidence |
  | Version | constants.VERSION -> package.__version__, compared to parsed add-on manifest and current changelog | FLOWING; fresh exact 0.2.69 assertions |

  ### Fresh Behavioral Checks

  All three commands ran from `F:/Workspace/BL-HAOS/modules/bridge`, Windows
  Python 3.14.7, pytest 9.0.3, using the absolute interpreter
  `F:/Workspace/BL-HAOS/.venv/Scripts/python.exe`. Environment:
  `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`, `PYTHONDONTWRITEBYTECODE=1`; module-local
  pytest.ini loads asyncio 1.4.0. Cache writes were disabled. Arguments after
  the interpreter are recorded verbatim:

  | Check | Arguments | Observed result |
  | --- | --- | --- |
  | Three-file Bluetooth regression | `-m pytest -c pytest.ini tests/test_bluetooth_device.py tests/test_bluetooth_manager.py tests/test_auto_reconnect.py -q --tb=short -p no:cacheprovider` | 91 collected/passed: device 11, manager 42, reconnect 38; zero skips/warnings; 9.81s; exit 0 |
  | Manifest/runtime/current release | `-m pytest -c pytest.ini tests/test_addon_config.py::test_runtime_version_is_sourced_from_the_shared_constant tests/test_addon_config.py::test_phase24_release_metadata_is_synchronized -q --tb=short -p no:cacheprovider` | 2 collected/passed; 0.08s; exit 0 |
  | Changed API reconnect-false boundary | `-m pytest -c pytest.ini tests/test_api.py -k 'redact_logs_and_errors and connect_false' -q --tb=short -p no:cacheprovider` | 53 collected, 3 selected/passed, 50 deselected; 1.12s; exit 0; one existing Starlette/httpx deprecation warning |

  **Fresh total:** 96 passing cases across disjoint selections, no skips; not a
  fresh full bridge gate. The 50 API deselections are selection, not skipped tests.
  No pending-task or unawaited-coroutine warning was emitted.

  ### Retained Full-Gate Evidence and Provenance

  Phase 24 canonical VERIFICATION (verified 2026-10-24T17:01:39.046Z) and
  VALIDATION's Final Independent Local Coverage Audit/G3 record the independently
  executed root `& ./scripts/run-tests.ps1 -Layer L1`: full Windows bridge
  **323 passed, 1 existing POSIX process-group skip, 1 Starlette warning in
  13.24s**, with bridge cwd and plugin isolation correct. That supersedes the
  older 280-pass full-gate count for the current integrated checkout. It includes
  all Phase 27 regressions and the changed shared API/config tests. It was read
  and retained, not executed again or claimed personally observed by this
  refresh. The only newly executed pytest checks are the three rows above.

  ### Decision Coverage

  Owner result: "No trackable decisions in CONTEXT.md." Skipped, 0/0, not an
  automated prose-decision pass. A cwd-invalid initial attempt was rejected and
  rerun from root. Manual decision trace: Retry Ownership -> truths 1/2/4;
  Shared Connection Ownership -> truths 3/4/7; Backoff and Recovery -> truths
  5/6/7; bounded scope/preserved bonds/docs -> truths 4/8/9 and this audit boundary.

  ### Test Quality and Anti-Patterns

  Fresh Bluetooth file counts are 11/42/38 with zero disabled cases. Assertions
  test values, exact calls, exceptions, event-barrier ownership, deadlines,
  history and replacement identity, not mere existence. The real tracer and
  real-manager cancellation tests complement manager-mocked pacing inputs;
  mocked I/O is not credited as hardware proof. Backoff boundary expected values
  use independent math.ldexp, not the production helper. No circular generated
  oracle, new skipped Phase 27 test, unresolved unreferenced TBD/FIXME/XXX marker,
  automatic stale-reset recovery, nested manager/device retry or scheduler-owned
  adapter lock was established. Existing state defaults/redaction placeholders
  are not production data stubs. No reproducible local blocker was found.

  ### Probe Execution

  No phase-declared probe script or new probe acceptance contract. Not applicable;
  no server/service, host probe or physical Bluetooth operation was started.

  ### Advisory (New Scope, Unevidenced)

  None. The symbolic key-link helper limitation remains a declared metadata
  caveat, not evidence of an unwired runtime path or grounds to rewrite PLAN.

  ## Human Verification and Deferred Hardware Boundary

  No unresolved human item inside the approved LOCAL scope. Hardware soak is
  explicitly pending under roadmap criterion 5 and CONTEXT/PLAN's deferred
  human-check; it is not silently counted as proven behavior. No prohibition
  override, deployment approval or accepted physical outcome is invented.

  Physical power-loss/return, busy BlueZ, sustained failure/half-open pacing,
  pairing retention, explicit reset and playback stability require separately
  authorized HAOS deployment/soak of the then-approved release. Current prepared
  0.2.69 remains undeployed. Process-local history and cooperative asyncio
  cancellation remain limitations. Fake boundaries cannot prove actual daemon
  reply/signal ordering or radio stability; the live physical fault is NOT
  declared fixed. Phase 24 remains human_needed pending its real-host checks.

  ## Refresh Outcome

  No local gaps or regressions found. Current fingerprint fields above are copied
  verbatim from `query verification.fingerprint`, preserving the same 26 covered
  paths and excluding this report itself. Only 27-VERIFICATION.md is changed in
  this refresh; no source/tests, historical PLAN/SUMMARY/SECURITY, Phase 24 or
  global state is modified. No deployment/live host, install, staging, commit,
  branch, pairing or phase-completion action occurred. Canonical status must be
  self-checked after writing; the intended owner result is passed, not stale.

  ---

  # Historical Verification Record: 2026-10-24T09:09:23Z

  The remainder is preserved verbatim from the previous report body. Its version
  0.2.68, 280-pass gate, phase-24 pause and prior edit-scope statements describe
  that earlier run only; the canonical frontmatter and current audit above
  supersede them. They are not new results or current deployment instructions.

**Phase Goal:** Prevent reconnect storms by removing nested connection retries, sharing connection ownership across automatic and operator requests, and preserving conservative backoff through failure and recovery.
**Verified:** 2026-10-24T09:09:23Z
**Status:** passed
**Re-verification:** Yes; bounded metadata refresh of the prior passed verdict at 2026-10-24T09:01:59Z. No source/test changes since that independent gate; no full-suite rerun in this refresh.

## Metadata Refresh Evidence

Re-read finalized 27-01-SUMMARY.md (status complete, parent_review clean,
local-only completion), 27-SECURITY.md, ROADMAP.md and REQUIREMENTS.md. The
historical review-fix subsection of SUMMARY still preserves its original
pending-review handoff wording; the final structured status and clean independent
REVIEW supersede that historical point-in-time statement.

Canonical verification.status after the validation audit identified only
27-01-SUMMARY.md and 27-VALIDATION.md as moved files; none of the previously
covered implementation/test artifacts changed. The existing independent
280-pass/1-skip gate below therefore remains applicable, not newly executed.
Direct assertion inspection confirms the requested local coverage, and two
bounded named checks were executed in this refresh with isolated plugins:

| Fresh check | Command arguments after the absolute Python interpreter | Result |
| --- | --- | --- |
| Canonical concurrent ensure/cache resolution | `-m pytest -c pytest.ini tests/test_bluetooth_manager.py::test_phase27_review_concurrent_resolution_keeps_canonical_record -q --tb=short -p no:cacheprovider` | 2 collected, 2 passed in 0.76s; exit 0 |
| Manifest/runtime/package version contract | `-m pytest -c pytest.ini tests/test_addon_config.py::test_runtime_version_is_sourced_from_the_shared_constant -q --tb=short -p no:cacheprovider` | 1 collected, 1 passed in 0.04s; exit 0 |

Both ran from F:/Workspace/BL-HAOS/modules/bridge using
F:/Workspace/BL-HAOS/.venv/Scripts/python.exe and
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1. No full-suite, deployment or hardware result
is inferred from these three fresh passing cases. The fingerprint fields above
are copied verbatim from query verification.fingerprint after the final
validation edit; SECURITY is now explicitly covered. Root planning documents
were read for authority, not edited or added as inert fingerprint evidence.

## Acceptance Boundary

This verdict covers the approved local implementation/test boundary, not deployment or radio reliability. ROADMAP criterion 5 explicitly requires real-host soak to remain pending until deployment authorization. CONTEXT defers live deployment, adapter recovery/reset, physical receiver checks and soak; PLAN task 3 accepts green local gates plus truthful pending hardware documentation. Its future human-check is therefore recorded below as deferred validation, not an unresolved local acceptance item. No override was invented or applied.

STATE's phase-27-only authorization was checked. Playlist phases 24-26 remain paused. No deployment, host operation, reset/unpair, access-token use, install, staging, commit or branch operation was performed by this verifier. Only 27-VALIDATION.md and this report were edited via apply_patch in this refresh. Existing root ROADMAP/STATE/state.json/PROJECT/REQUIREMENTS and bridge worktree changes were left intact; phase.complete was not called again and historic next-phase routing was not followed.

## Goal Achievement

### Roadmap Success Criteria

All five criteria are retained. The nine detailed truths below merge the plan's additional guarantees without narrowing the roadmap contract.

| # | Roadmap criterion | Status | Evidence |
|---|---|---|---|
| 1 | One scheduled reconnect performs one bounded connection attempt; busy or failed BlueZ calls cannot trigger immediate nested retries or destructive stale-link recovery. | VERIFIED | Truths 1, 2, 4; real engine/manager/device tracer, busy variants, single-failure and next-request stale resolution tests pass. |
| 2 | Manual and automatic connection requests share adapter ownership, including cleanup after cancellation and failure; pairing is preserved. | VERIFIED | Truth 3; both ownership orderings, different-adapter independence, timeout/cancellation, bond retention and canonical-cache race assertions pass. |
| 3 | Repeated failures use longer exponential backoff and a meaningful circuit-breaker cooldown; recovery, presence events, and busy responses cannot erase accumulated backoff. | VERIFIED | Truths 5, 6; exact defaults/delays, retained deadlines/counters, eighth-failure breaker and failed/successful half-open transitions pass. |
| 4 | Deterministic module-local tests verify call counts, concurrent requests, cancellation, backoff, and breaker behavior, with existing Bluetooth and API regressions passing. | VERIFIED | Truths 7, 8; independently observed 280 passing bridge tests, including all 137 tests in the six-file focused slice. |
| 5 | Release notes and operator documentation describe the change, with real-host soak validation explicitly pending until deployment is authorized. | VERIFIED | Truth 9; current README/DOCS/changelog match code and explicitly defer hardware validation; parsed manifest/runtime/package version equals 0.2.68. |

### Observable Truths

Paths in this section are relative to modules/bridge. Every behavior-dependent verdict uses passing runtime assertions, not symbol presence alone.

| # | Truth | Status | Actual source and behavioral evidence |
|---|---|---|---|
| 1 | One scheduled reconnect invokes the manager once and Device1.Connect at most once; only AlreadyConnected can additionally activate one A2DP profile. | VERIFIED | reconnect.py `_attempt_reconnect` has one `await self.manager.connect_device(addr)`; manager.py `connect_device` has one `await dev.connect()` without a retry loop. `test_phase27_connection_scheduled_tick_has_one_bluez_attempt` uses real engine/manager/device and fake BlueZ, asserts one Connect, zero profile calls, one failure and retained cache. Device's AlreadyConnected test asserts exactly one A2DP UUID. All pass. |
| 2 | Busy BlueZ responses issue no ConnectProfile and propagate BluetoothOperationInProgress without false connection success. | VERIFIED | device.py normalizes busy before the AlreadyConnected branch and sets Connected only after success. Five busy strings and generic error tests assert exceptions, one Connect, zero profiles and false Connected. Manager busy tests assert no stale failure observation. Independent real-route in-memory probe observes HTTP 409, one explicit-reset manager call and zero success-publication calls. |
| 3 | Automatic and operator requests share actual-adapter ownership, fail fast on contention, and release it after exceptions, timeout and cancellation. | VERIFIED | manager.py initializes `_connection_locks` once; `connect_device` selects the resolved device's validated adapter, checks contention without an intervening await and uses `async with lock`. Ownership tests cover both caller orderings and another adapter; cleanup tests use real manager locks blocked in fake BlueZ. Named cleanup test independently passes both stop/unregister cases. Two named concurrent-resolution cases independently pass; eight withdrawal/replacement cases in the full gate retain backoff/bonds and reject false success. |
| 4 | The entire manager operation is bounded to 30 seconds; automatic attempts never disconnect an existing link and explicit operator reset remains supported. | VERIFIED | `asyncio.timeout(30.0)` encloses ensure_device through trust/final identity check. Two deadline tests capture 30.0 and use a shorter real timeout to test blocked resolution/connection cleanup. Connected automatic request returns without reset; disconnect is guarded by `dev.connected and reset_existing`. Operator reset test records one disconnect and successful connection; routes.py passes reset_existing=True only on explicit Connect/existing failed-play recovery paths. |
| 5 | Pacing is 10s initial, multiplier 2, final cap 120s, non-negative 15% jitter, eight failures/300s breaker; busy, presence and failed recovery preserve pacing/history. | VERIFIED | constants.py defaults match. `_calculate_backoff_delay`, `_defer_busy_connection` and failure handling preserve floors/deadlines. Default tests assert 10/20/40/80/120/120 at zero jitter and final cap at 15%; scheduled failures count one call and no reset per attempt. Busy/presence retain a later deadline and counters; manual-first real lock contention preserves history. Review tests validate zero/tiny values at step 1024, million-step saturation, eleven invalid domains and four supported boundaries. All pass. |
| 6 | Breaker expiry admits one half-open attempt with retained history; failed probe reopens it and confirmed success clears pacing. | VERIFIED | `_tick` checks circuit deadline before scheduling; `_inflight` suppresses duplicates and expiry does not clear counters. Failure advances once/reopens 300s; success clears failures, step and deadlines. `test_phase27_pacing_breaker_half_open_retains_history_until_success` independently passes as one named test (0.13s), including repeated ticks and ninth-failure retained history. Full gate also passes health exhaustion and successful recovery clearing old failure. |
| 7 | Existing 5s grace, 15s settle and six-flaps-in-120s suppression with 60s cooldown remain effective. | VERIFIED | constants.py keeps 5/15/6/120/60. `_on_device_event`, `_arm_backoff`, `_record_flap` and `_tick` enforce grace, cooldown and settle. `test_reconnect_state_machine`, `test_scheduled_retry_waits_for_the_full_settle_window` and `test_repeated_flaps_earn_a_cooldown_instead_of_a_retry_loop` pass in the independent full gate. |
| 8 | Focused regressions have recorded pre-edit RED evidence, and current focused Bluetooth/API/SIL plus complete bridge tests pass. | VERIFIED | Historical process evidence is explicitly attributed to the executor/fixer records, not personally re-observed: SUMMARY/VALIDATION report connection 13 failed -> 13 passed; pacing 6 failed/1 passed -> 7 passed; review-fix 23 failed/4 passed -> 13 failed/14 passed -> 27 passed. REVIEW independently reports 27 review cases and focus137 passing after fixes. This verifier directly observed all 137 focused-slice cases passing within the single 280-pass full gate; it did not independently replay historical edit ordering or rerun a separate focus137 command. |
| 9 | Operator docs describe conservative retries and preserved pairing; manifest/runtime version is 0.2.68. | VERIFIED | README current feature, DOCS stability section and top CHANGELOG entry match delays, busy handling, half-open history, shared ownership, explicit reset and preserved bonds. All state hardware soak is pending. YAML parse/import probe confirms manifest version == constants.VERSION == package.__version__ == 0.2.68; metadata test passes. Historical changelog retry descriptions are not current promises. |

**Score:** 9/9 truths verified; 0 present-but-behavior-unverified local truths; 0 overrides. Roadmap coverage: 5/5.

### Required Artifacts

Canonical `query verify.artifacts` returned exit 0, all_passed=true, passed=4, total=4. Manual checks below additionally establish wiring and substantive behavior.

| Artifact | Expected | Status | Evidence beyond existence |
|---|---|---|---|
| modules/bridge/backend/bl_haos/bluetooth/manager.py | Shared ownership and bounded single connect | VERIFIED | API and engine use the same method; timeout, canonical record checks and actual-adapter lock surround the connection; real-path tests pass. |
| modules/bridge/backend/bl_haos/bluetooth/reconnect.py | Scheduler-only retry ownership and retained pacing | VERIFIED | main.py constructs/registers/starts engine and stops it at shutdown; manager events drive its listener; deterministic deadline/worker tests pass. |
| modules/bridge/tests/test_auto_reconnect.py | Real scheduler/manager/device regression using fake BlueZ | VERIFIED | Included by module-local pytest configuration and full gate: 38 passing cases, including real tracer, real-lock cancellation and retained pacing. |
| modules/bridge/DOCS.md | Correct retry/reset policy and pending soak notice | VERIFIED | Stability section describes actual code constants/control flow and explicitly distinguishes local tests from live-fault proof. |

**Artifacts:** 4/4 declared artifacts exist, are substantive and are wired. Supporting device/constants, three regression files and release metadata were also inspected.

### Key Link Verification

The canonical key-link query returned exit 1, 0/4 automatic matches: all four PLAN `from` entries are symbol names, whereas the helper requires repository-relative file paths. This is a declaration-format limitation, not proof that runtime links are absent. No PLAN edit was authorized. Each link was resolved manually to its owning source and exercised by passing tests:

| From | To | Via | Status | Evidence |
|---|---|---|---|---|
| AutoReconnectEngine._attempt_reconnect | BluetoothManager.connect_device | One call, no automatic reset | WIRED | reconnect.py awaits manager once without reset flag; real scheduled tracer and scheduled-failure call-count tests pass. |
| BluetoothManager.connect_device | BluetoothDevice.connect | Shared lock and bounded call | WIRED | manager.py awaits dev.connect once inside timeout/lock; generic/stale failure, concurrency and timeout tests pass. |
| BluetoothDevice.connect | BluetoothOperationInProgress | Busy before profile fallback | WIRED | device.py raises existing exception before AlreadyConnected branch; five busy variants and generic-error test pass. |
| AutoReconnectEngine._on_device_event | SpeakerReconnectProfile.next_retry_time | Presence retains deadline | WIRED | Disconnected/RSSI branch does not pull retry time forward; scheduled failure and presence/busy retained-deadline tests pass. |

**Wiring:** 4/4 manually verified; automatic helper cannot evaluate symbol-form declarations. No NOT_WIRED implementation link found.

### Data-Flow Trace (Level 4)

| Artifact/value | Actual source | Path to output/state | Status |
|---|---|---|---|
| Device inventory connected/paired/detached | BlueZ properties and manager signal handlers | BluetoothDevice properties -> to_info -> manager.get_devices -> REST/native event consumers | FLOWING; canonical resolution and eight withdrawal barriers assert no stale cached success. Real hardware source is not contacted in this run. |
| Reconnect state, counts and retry deadline | Manager success/busy/error/cancellation and device events | Registered profile -> `_attempt_reconnect`/`_on_device_event` -> `_tick` scheduling guards | FLOWING; exact deadlines, half-open history and identity-safe cancellation tested. |
| Speaker health/failure | Manager classification and reconnect result | HealthRegistry.observe_speaker -> bounded snapshot/API health | FLOWING; stale classification once, busy not misclassified, exhaustion unavailable, confirmed CONNECTED clears old failure. |
| Version | Parsed manifest and imported shared constant | constants.VERSION -> package.__version__; manifest consumed by add-on | FLOWING; exact 0.2.68 agreement independently asserted. |

No hardcoded empty production output or disconnected dynamic-data artifact was established. No-bus simulation is an explicit existing local-test path, not evidence of physical BlueZ behavior.

## Prior Independent Executable Evidence

The runs in this section were observed by the prior verifier before
2026-10-24T09:01:59Z and are retained unchanged as evidence for the untouched
source/tests. They are not runs performed during this metadata refresh; fresh
checks are listed separately above. independent_full_runs remains 1.

All pytest commands below used PowerShell, cwd F:/Workspace/BL-HAOS/modules/bridge, PYTEST_DISABLE_PLUGIN_AUTOLOAD=1, and the absolute interpreter F:/Workspace/BL-HAOS/.venv/Scripts/python.exe. The module config explicitly loads asyncio; no installs or plugin changes occurred.

```powershell
Set-Location F:/Workspace/BL-HAOS/modules/bridge
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
& F:/Workspace/BL-HAOS/.venv/Scripts/python.exe -m pytest -c pytest.ini tests -q --tb=short -ra
```

| Check | Arguments/result | Status |
|---|---|---|
| Required full bridge gate; run exactly once | 281 collected; 280 passed, 1 skipped, 1 warning in 11.98s; exit 0 | PASS |
| Focused-slice coverage inside that full gate | device 11 + manager 42 + reconnect 38 + API 26 + SIL 13 + metadata 7 = 137 passed | PASS; not a separate focused invocation |
| Named half-open test | `tests/test_auto_reconnect.py::test_phase27_pacing_breaker_half_open_retains_history_until_success -q --tb=short`; 1 passed in 0.13s; exit 0 | PASS |
| Named real-manager cancellation test | `tests/test_auto_reconnect.py::test_phase27_pacing_cleanup_releases_real_manager_lock -q --tb=short`; 2 passed in 1.38s; exit 0 | PASS |
| Named canonical cache resolution test | `tests/test_bluetooth_manager.py::test_phase27_review_concurrent_resolution_keeps_canonical_record -q --tb=short`; 2 passed in 0.76s; exit 0 | PASS |
| Direct API busy and version probe | Python stdin invokes real routes.connect_device with an AsyncMock manager raising BluetoothOperationInProgress; asserts HTTP 409, normalized address/reset_existing=True, manager once, publish never. Parses YAML and imports package/runtime versions, asserting all equal 0.2.68. Both PASS lines observed; exit 0 | PASS |

**Skip:** tests/test_media_player.py:654, `POSIX process groups are required` on Windows. That process-group behavior is not proven here; no new skip was added.
**Warning:** fastapi/testclient.py imports Starlette TestClient's deprecated httpx integration; the requested run reports one StarletteDeprecationWarning. No pending-task or unawaited-coroutine warning was emitted.

### Probe Execution

No phase-declared executable probe script or probe/PASS-marker acceptance contract exists. Step 7c script execution is not applicable to this Bluetooth phase. The independent in-memory API/version probe above supplements, rather than substitutes for, the required full bridge gate. No server or service was started.

## Requirements Coverage

| Requirement | Source plan | Description/authority | Status | Evidence |
|---|---|---|---|---|
| PROD-04 | 27-01 | Final REQUIREMENTS: one bounded connection attempt shares adapter ownership across automatic/operator requests, releasing it on failure, timeout and cancellation; hardware soak pending | SATISFIED for Phase 27 local scope | Per-address inflight identity plus actual-adapter manager locks; both request orderings, cancellation and canonical-cache races pass. |
| PROD-05 | 27-01 | Final REQUIREMENTS: recovery preserves pairing and conservative failure pacing without nested retries or automatic link resets; hardware soak pending | SATISFIED for Phase 27 local scope | Single bounded attempt, stale detach/next-request resolution, pairing retained, no auto reset, retained pacing and truthful docs pass. |

Final REQUIREMENTS.md explicitly defines PROD-04 and PROD-05 under Scoped Bluetooth Reliability Follow-Up and maps both to Phase 27 as locally verified with hardware soak pending. Both are claimed by PLAN; no orphaned Phase 27 requirement exists. All PL-01 through PL-11 remain pending and belong to paused playlist phases. Final ROADMAP records Phase 27 as locally complete with 1/1 completed plans, clean independent review, the prior 280-pass gate and deferred hardware soak. No later phase exists to absorb an implementation gap; no gap was silently deferred to playlist work. These root documents and their statuses were preserved, not rewritten.

### Validation and Security Gates

The configured verify:post hooks include active validate-phase and secure-phase
steps. The gsd-validate-phase skill and complete workflow were loaded for a
direct State A audit. 27-VALIDATION.md now has status validated,
nyquist_compliant true and coverage_status pass. All three tasks map to actual
active behavioral tests or the explicitly identified prior in-memory API probe
and direct documentation inspection. Coverage includes the real cross-layer
single Connect/busy path, both actual-adapter caller orderings, concurrent
ensure/cache withdrawal, cancellation/timeout, conservative pacing, retained
busy/presence/half-open history, pairing/reset, API compatibility and version/docs.
Zero local gaps were found; no source/test file was created or changed. The
specialized Nyquist auditor was unavailable and provided no assessment; no
delegated success is claimed.

27-SECURITY.md records the parent's direct ASVS L1 assessment, status verified,
five closed register entries and threats_open 0. T-27-01 through T-27-04 map to
the inspected call-count/ownership, no-reset/bond, cancellation/timeout and
busy/stale-success tests. T-27-SC is the plan's documented accepted risk because
no dependency change/install was introduced. The report explicitly states that
the specialized security agent had no filesystem tools and assessed no threats;
this is direct parent closure, not an independent specialized-agent audit or
a broader ASVS certification. Both reports preserve the pending authorized
hardware soak boundary.

### Decision Coverage

No trackable decisions in CONTEXT.md.

That is the canonical checker's skip message (0/0), not a claim that its heuristic verified every prose bullet. Manual decision trace:

| Context group | Shipped evidence | Assessment |
|---|---|---|
| Retry Ownership | One scheduler manager call; manager/device have no connect retry loop; busy does not activate profile; no automatic remove/reset | Honored in source and passing tracer/busy/bond tests |
| Shared Connection Ownership | Manager actual-adapter locks, existing exception/API, timeout/finally cleanup, canonical-record guards | Honored in ownership/cancellation/cache tests and direct HTTP 409 probe |
| Backoff and Recovery | 10/2/120/15%, eight/300, retained busy/presence history, half-open, grace/settle/flap guards | Honored in deterministic runtime assertions |
| Agent Discretion | Existing files/helpers, 11-file bridge diff, matching 0.2.68 docs, no dependency change, autonomous local verification only | Honored in inspected scope; historical executor actions remain attributed, not personally reconstructed |

### Test Quality Audit

| Test file | Linked requirement | Active cases in independent full gate | Skipped | Circular | Assertion strength | Verdict |
|---|---|---|---|---|---|---|
| modules/bridge/tests/test_bluetooth_device.py | PROD-04/05 | 11 | 0 | None found | Exceptions, exact call count, profile UUID, connected/bond values | PASS |
| modules/bridge/tests/test_bluetooth_manager.py | PROD-04/05 | 42 | 0 | None found | Event barriers, canonical object identity, retained bonds, fail-fast contention, timeout and lock cleanup | PASS |
| modules/bridge/tests/test_auto_reconnect.py | PROD-04/05 | 38 | 0 | None found | Real path tracer, exact deadlines/counters, scheduler transitions, half-open and real-lock cancellation | PASS |
| modules/bridge/tests/test_api.py | Existing API compatibility | 26 | 0 | None established | HTTP/value/error contracts; passing baseline does not alone prove Connect busy | PASS; busy supplemented by real-route probe |
| modules/bridge/tests/test_bridge_sil.py | API/data-flow compatibility | 13 | 0 | None established | REST/WS state and failed-play recovery outputs/arguments | PASS |
| modules/bridge/tests/test_addon_config.py | Version/docs metadata | 7 | 0 | None found | Parsed manifest/runtime equality; exact 0.2.68 additionally checked directly | PASS |

All 27 review-fix parameterized cases are present and active: ten manager cases and seventeen backoff-domain/boundary cases. Independent full execution covers them. Tests use input fixtures, events, clock/jitter patches and independent expected values; no generated expected-output fixtures were found in changed tests. The tiny-value numeric oracle uses math.ldexp, not the production backoff helper. Some unit cases mock the manager and cannot by themselves establish cross-layer behavior; the real tracer, cache barriers and real-lock cleanup supply that missing boundary evidence. No requirement relies solely on a disabled test or existence/type assertion.

### Anti-Patterns and Disconfirmation

| File/area | Finding | Classification | Impact |
|---|---|---|---|
| Changed production/tests/docs | No unreferenced TBD/FIXME/XXX, new skipped phase test, circular fixture writer or automatic `_recover_stale_device` path found | No blocker | Scan ran over all 11 changed bridge files |
| modules/bridge/backend/bl_haos/constants.py:159 | OMITTED_PLACEHOLDER and existing redaction constants at 250/252 match PLACEHOLDER text | Benign | Real redaction values, not incomplete behavior |
| PLAN key_links | Symbol endpoints are not file paths required by the helper | Metadata caveat | Canonical auto-check is unevaluated for these declarations; all four runtime links independently traced/tested |
| SUMMARY/fix handoff text | Historical pending-review/issues_found wording remains in point-in-time follow-up evidence | Historical metadata caveat | Final SUMMARY says complete/parent_review clean; independent REVIEW is clean. VALIDATION is now finalized by direct coverage audit; historical claims are not treated as new execution evidence |

Adversarial checks targeted (1) busy/profile fallback reporting false success, (2) cache replacement/withdrawal across awaits, and (3) cancellation/breaker history leaking or resetting. Real source and passing runtime assertions disconfirm these local failure hypotheses. Residual untested path: physical BlueZ profile reply/signal ordering and cooperative daemon cancellation cannot be inferred from fake boundaries. Existing AlreadyConnected compatibility test checks the UUID but does not independently exercise every busy/error variant returned by ConnectProfile; source handles that branch, but no exhaustive branch-coverage claim is made. No new reproducible in-scope defect was established.

## Human Verification Required

None for the approved local acceptance boundary. There are no unresolved local behavior-unverified truths or judgment-tier prohibitions. The future hardware check below was explicitly deferred by CONTEXT, PLAN and ROADMAP criterion 5; it is not silently counted as passing hardware evidence.

### Advisory (New Scope, Unevidenced)

None. This bounded metadata refresh found no new reproducible local defect or
source/test regression and did not reopen the clean implementation review.

## Deferred Hardware Validation

**Not performed; hardware_proven=false.** No assertion is made that the observed live Bluetooth fault is fixed. Fake BlueZ/SIL validates local control flow only; it does not prove physical radio stability, actual daemon reply/signal ordering, playback quality or real-time cancellation responsiveness. Retry history remains process-local, and the 30-second timeout relies on cooperative asyncio cancellation.

**Requested future action:** Obtain separate authorization to deploy 0.2.68 to HAOS, then soak an already paired/trusted speaker through power loss/return, out-of-range/return, busy BlueZ and prolonged failures. Capture timestamped attempt counts/delays, eighth-failure 300-second cooldown, single half-open failure/reopen and successful recovery, preserved bonds, explicit operator reset and stable playback. Do not reset/unpair merely to complete this check. No invented soak duration or hardware outcome is asserted.

## Gaps Summary

No blocking local implementation or coverage gap was found. All five roadmap criteria and nine detailed plan truths remain supported within the authorized local boundary, with the historical TDD provenance caveat explicitly retained. Required full gate independently passed once before this refresh; only the two named checks (three passing cases) were newly run. Declared artifacts remain 4/4 verified, and runtime links remain 4/4 manually verified despite the helper's endpoint-format limitation. Final Nyquist coverage is PASS/compliant; security is parent-direct L1 verified with specialized agents explicitly unavailable. Real-host soak remains pending separate deployment authorization, not proven and not required for this local-scope verdict. Parent owns final status projection only; this report does not advance planning state or authorize release/deployment.

---

_Verifier: gsd-verifier_