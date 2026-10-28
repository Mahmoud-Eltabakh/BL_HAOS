---
phase: "27"
slug: bluetooth-reconnect-reliability
status: validated
nyquist_compliant: true
wave_0_complete: true
created: "2026-10-24"
completion_scope: local-implementation-and-tests-only
coverage_status: pass
hardware_soak: pending-authorized-deployment
---

# Phase 27 Validation Strategy

## Test Infrastructure

- Python 3.14.7, pytest 9.0.3, pytest-asyncio 1.4.0; existing infrastructure only.
- Interpreter: F:/Workspace/BL-HAOS/.venv/Scripts/python.exe.
- Config: modules/bridge/pytest.ini, including explicit asyncio plugin/auto mode.
- PowerShell setup: `$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'` before tests.
  Ordinary autoload fails before collection because the unrelated HA plugin imports
  fcntl on Windows; this is not acceptable RED evidence.
- Baseline: existing three Bluetooth files, 43 passed in 5.42s with isolated plugins.
- No new test files, installs, hardware, access tokens or live recovery actions.

## Commands

All pytest commands run from F:/Workspace/BL-HAOS/modules/bridge. Selecting a
pytest config does not change cwd; metadata tests read config.yaml relative to cwd.
Quick gate from the bridge directory:

```powershell
F:/Workspace/BL-HAOS/.venv/Scripts/python.exe -m pytest -c pytest.ini tests/test_bluetooth_device.py tests/test_bluetooth_manager.py tests/test_auto_reconnect.py tests/test_api.py tests/test_bridge_sil.py -q
```

Final metadata gate adds tests/test_addon_config.py to the quick gate.
Required full bridge gate, after focused tests:

```powershell
F:/Workspace/BL-HAOS/.venv/Scripts/python.exe -m pytest -c pytest.ini tests -q
```

Observed final focused gate: 110 passed, 1 warning in 9.55s. Observed complete
bridge gate: 253 passed, 1 skipped, 1 warning in 11.97s (254 collected), exit 0.
Existing Windows skip: tests/test_media_player.py:654, POSIX process groups are
required. Existing Starlette/httpx TestClient deprecation was the sole warning.
No unrelated test was modified, weakened or newly skipped.

## Sampling and RED-First Contract

Every behavior task first adds tests and immediately runs its selected regression
command before changing production. Task 1 uses `-k phase27_connection` across the
three Bluetooth files; task 2 uses `-k phase27_pacing` in test_auto_reconnect.py.
Each RED run must collect the new tests and exit 1 on expected behavioral assertions;
an import/collection crash or zero selected tests is an infrastructure failure.
Capture failing assertions, then rerun the exact same selection for GREEN before
widening to focused tests. New regressions use fake D-Bus calls, event barriers and
clock/jitter patches, not real 30s/300s waits. Drain every created worker.

After every substantive production edit, rerun the relevant selection before more
editing. After tasks 1-2 run their focused gates; task 3 runs the quick/metadata and
full bridge gates in that order. No commits are authorized; sampling is per edit/task,
not per commit. Record counts, failures, skips and timings in the execution summary.

## Per-Task Verification Map

| Task | Requirement | Threat Ref | Secure Behavior | Test Type | Command | Exists | Status |
|------|-------------|------------|-----------------|-----------|---------|--------|--------|
| 27-01-01 | PROD-04, PROD-05 | T-27-01, T-27-03, T-27-04 | Bounded real engine-to-manager-to-fake-BlueZ calls; shared ownership; cancellation; no busy fallback | Async unit/in-process integration | Plan task 1 selected and manager/device commands; named tests below | Yes | COVERED/PASS; prior independent final gate includes all 53 device/manager cases and real scheduler tracer |
| 27-01-02 | PROD-04, PROD-05 | T-27-01, T-27-02, T-27-03 | Persistent conservative deadlines, no automatic reset, half-open breaker history, stop/unregister cleanup | Deterministic scheduler and focused API/SIL | Plan task 2 selected then quick command; named tests below | Yes | COVERED/PASS; prior independent final gate includes all 38 reconnect cases and 27 review-fix cases across manager/reconnect |
| 27-01-03 | PROD-05 | T-27-02, T-27-04 | Accurate docs, version consistency, existing bridge contracts preserved | Metadata/focused then full suite | Plan task 3 commands; named metadata tests below | Yes | COVERED/PASS; final focused 137 passed (fixer); independent full 280 passed, 1 platform skip (prior verifier) |

## Observed Execution Evidence

All valid runs used explicit bridge cwd, the absolute interpreter above, isolated
plugins, `-c pytest.ini`, and `-q --tb=short` (`-ra` additionally on the full run).
Exact file selections, command flags and intermediate failures are recorded in
27-01-SUMMARY.md. No commits, installs, branch changes, state updates or deployment
were performed by the executor. Parent implementation re-review is now clean;
authorized HAOS soak remains pending. Earlier counts below are historical runs,
superseded for final local acceptance by the review-fix and independent gates.

| Gate | RED before behavior edit | GREEN immediately after behavior edit |
| --- | --- | --- |
| `phase27_connection` across the three Bluetooth files | 56 collected, 13 failed, 43 deselected, exit 1, 9.08s | 13 passed, 43 deselected, exit 0, 4.43s |
| `phase27_pacing` in test_auto_reconnect.py | 20 collected, 6 failed, 1 passed, 13 deselected, exit 1, 1.35s | 7 passed, 13 deselected, exit 0, 1.40s |

Task1 actual assertions: busy/generic errors did not raise, manager Connect count
was 3 instead of 1, deadline capture was [] instead of [30.0], contenders timed out
instead of reporting busy, and real scheduled tracer invoked a forbidden profile.
Task2 assertions: initial delay was 1 instead of 10, presence shortened 1500 to
1000, scheduled manager calls were 3 instead of 2, and stop left RECONNECTING.
These were planned behavioral failures, not import/plugin/collection errors.
The existing unregister cleanup case was already green and remains covered.

Additional compatibility results: manager/device initially 40 passed + 3 legacy
failures in 6.06s, then 43 passed in 6.81s; integrated five-file gate initially
95 passed + 7 legacy failures in 9.54s, then 103 passed in 9.61s. Those deliberate
contract updates replaced immediate refresh/reset, fast-track and history-reset
expectations, retaining explicit pairing/API/health assertions. A manual-first
real-manager contention test expanded pacing coverage to eight cases; all pass
in the final focused/full gates. No pending-task/unawaited-coroutine warnings.

Invalid attempts were rejected, not counted as RED: the first unbounded contention
test run was interrupted (8 failures, 310.74s), then bounded and rerun; a subsequent
wrong-cwd command collected no tests (0.00s) before the explicit-cwd correction.
Neither authorizes GREEN; only the completed RED runs above do.

## Wave 0 Requirements

Existing test infrastructure covers the slice. No separate scaffold/install wave.
New tests were added first and observed RED then GREEN by the executor for both
behavior tasks. No scaffold, new source/test file or dependency was introduced.

## Manual-Only Verification

Live HAOS/hardware soak is DEFERRED pending separate deployment authorization.
Eventually exercise power-off/on, return to range, busy BlueZ, extended failures,
half-open recovery, operator reset and stable playback with pairing retained.
Neither local SIL nor this planning run proves the live fault is fixed. Do not run
physical checks, reset/unpair, deploy or contact the previously shared host/token.

## Validation Sign-Off

- [x] Each task has executable automated verification and explicit failure signals.
- [x] Existing test paths and interpreter are grounded; focused baseline ran.
- [x] Regression RED must precede production edits; selected GREEN precedes widening.
- [x] New regressions observed RED then GREEN by executor.
- [x] Focused Bluetooth/API/SIL/metadata gate passes after implementation.
- [x] Complete bridge suite passes with environment/skips recorded.
- [x] Independent parent checker has reviewed the plan (PASS supplied by parent).
- [x] Independent parent implementation review/verification is complete locally.
- [ ] Future authorized hardware soak evidence exists (deferred, not a local gate).

Local Nyquist/test-first requirements are satisfied by observed execution, not
planning artifacts alone. Final independent local verification passed 9/9 truths;
future separately authorized hardware soak remains pending and is not a local
test claim. STATE.md, state.json, ROADMAP.md and paused phase24 remain untouched
by this bounded audit.

## Review-Fix Validation: CR-01 and WR-01

Observed 2026-10-24T08:56:31Z in the main checkout (no isolated worktree).
Historical evidence above is retained as originally reported, not re-created.
At the time of this follow-up, source re-review was pending. The subsequent
independent parent re-review is clean; historical execution evidence follows.
No hardware approval is implied by these local passes.

All commands ran from F:/Workspace/BL-HAOS/modules/bridge after setting
`$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'`, using the exact prefix:
`F:/Workspace/BL-HAOS/.venv/Scripts/python.exe -m pytest -c pytest.ini`.

| Sequence | Arguments after prefix | Actual result | Exit | Duration |
| --- | --- | --- | --- | --- |
| Test-first RED | tests/test_bluetooth_device.py tests/test_bluetooth_manager.py tests/test_auto_reconnect.py -q -k phase27_review --tb=short | 23 failed, 4 passed, 64 deselected (91 collected, 27 selected) | 1 | 1.23s |
| Immediate manager check | Identical regression arguments | 13 failed, 14 passed, 64 deselected; all 10 manager cases passed | 1 | 1.07s |
| Immediate reconnect check | Identical regression arguments | 27 passed, 64 deselected | 0 | 0.82s |
| Required focus6 | tests/test_bluetooth_device.py tests/test_bluetooth_manager.py tests/test_auto_reconnect.py tests/test_api.py tests/test_bridge_sil.py tests/test_addon_config.py -q --tb=short | 137 passed, 1 warning | 0 | 10.28s |
| Required full bridge | tests -q --tb=short -ra | 280 passed, 1 skipped, 1 warning (281 collected) | 0 | 12.36s |

The initial test edit was immediately followed by RED before source changes.
Each production file was edited once and immediately followed by that identical
regression command before further reading or patching. No repair loop or
invalid collection/environment result occurred in this follow-up.

CR-01 RED: both missing/detached GetAll races replaced the canonical record;
all eight awaited stop_scan/settle/Connect/trust removal/replacement cases
incorrectly changed the real engine profile to CONNECTED instead of BACKOFF.
GREEN verifies the busy loser cannot replace the winner, cached connected state
is canonical, withdrawn pre-Connect records cause zero Connect calls, late
withdrawal permits only the one in-flight Connect, retained bonds remain visible,
failure/step history increments once, retry deadlines are future, and ownership
is released. Event barriers and bounded waits are deterministic; all tasks drain.

WR-01 RED: initial 0.0 and 1e-320 at step 1024 explicitly failed on intermediate
OverflowError; eleven unsupported constructor cases failed to raise ValueError.
GREEN retains zero and tiny-positive semantics, matches math.ldexp's finite
scaled result at step 1024, handles step 1000000, and validates finite initial
>= 0, finite multiplier >= 1 and finite positive cap. Four already-supported
boundary cases remained green; the complete existing pacing suite also passes.

The only full-suite skip is the existing Windows POSIX-process-group case at
test_media_player.py:654. The sole warning is the existing Starlette/httpx
TestClient deprecation. No new skip, pending-task or unawaited-coroutine warning.
Editor diagnostics found no errors in the four changed Python files; bridge
git diff --check passed. No dependency install or unrelated test edit occurred.

All work remains uncommitted and unstaged. No branch/worktree, deployment, host
operation, reset/unpair, phase24 change or state update was performed. REVIEW.md
was unchanged by the fixer. Independent parent re-review is now clean; authorized
hardware soak remains pending. Per-finding details are in 27-REVIEW-FIX.md.

## Final Coverage Audit

Direct local audit on 2026-10-24 using the gsd-validate-phase skill/workflow,
State A (existing validation report). The specialized Nyquist auditor was
unavailable and supplied no assessment; this is a direct test/assertion audit,
not a delegated auditor verdict. No new source/test files or edits were needed.
The existing prior verifier gate observed 280 passed, 1 skipped, 1 warning in
11.98s; this metadata refresh does not claim a second full-suite execution.
Historical RED ordering is attributed to executor/fixer records, not replayed.

The configured verify:post hooks include active validate-phase (Nyquist) and
secure-phase steps. A fresh bounded check in this metadata-only audit ran from
the required bridge cwd with isolated plugins and the absolute interpreter:
`-m pytest -c pytest.ini tests/test_bluetooth_manager.py::test_phase27_review_concurrent_resolution_keeps_canonical_record -q --tb=short -p no:cacheprovider`.
Result: 2 collected, 2 passed in 0.76s, exit 0. This checks the real concurrent
resolution boundary, not a second full-suite run. Canonical verification.status
after this audit's first edit identified only SUMMARY and VALIDATION as changed;
no previously covered source/test artifact changed since the independent gate.

Test paths below are relative to modules/bridge/tests. All listed cases were
active and passed in that prior independent full gate; assertions were inspected
directly during this audit. No in-scope local coverage gap was found.

| Required behavior | Actual tests and decisive assertions | Coverage |
| --- | --- | --- |
| One Connect; busy never profiles or reports success | test_auto_reconnect.py::test_phase27_connection_scheduled_tick_has_one_bluez_attempt; test_bluetooth_device.py::test_phase27_connection_busy_never_activates_profile (5 variants), test_phase27_connection_generic_error_preserves_disconnected_state; exact Connect=1, ConnectProfile=0, disconnected and one scheduler failure | COVERED/PASS |
| Actual-adapter automatic/manual races | test_bluetooth_manager.py::test_phase27_connection_shared_actual_adapter_ownership (2 orderings); test_auto_reconnect.py::test_phase27_pacing_cleanup_releases_real_manager_lock (2 cleanup modes), test_phase27_pacing_manual_owner_defers_automatic_without_erasing_history; hci0 lock despite preferred hci1, same/other-speaker busy, independent adapter proceeds, history retained | COVERED/PASS |
| Concurrent ensure/cache withdrawal | test_bluetooth_manager.py::test_phase27_review_concurrent_resolution_keeps_canonical_record (missing/detached); test_phase27_review_withdrawn_record_never_succeeds (8 removal/replacement cases at stop_scan/settle/Connect/trust); canonical object identity, no early Connect, no false success, bonds retained, BACKOFF and failure increment once | COVERED/PASS |
| Cancellation and complete-operation timeout | test_auto_reconnect.py::test_phase27_pacing_cleanup_releases_real_manager_lock; test_bluetooth_manager.py::test_phase27_connection_complete_operation_timeout_releases_ownership (resolution/Connect); captured 30.0s deadline, real short timeout, released/reusable lock, no resurrected profile | COVERED/PASS |
| Conservative pacing; busy/presence; half-open | test_auto_reconnect.py::test_phase27_pacing_defaults_saturate_without_negative_jitter, test_phase27_pacing_scheduled_failures_never_reset_or_amplify, test_phase27_pacing_busy_and_presence_retain_history_and_later_deadlines, test_phase27_pacing_breaker_half_open_retains_history_until_success; exact delays/cap, retained counters/deadlines, eighth failure opens 300s, one half-open, failed reopen and success clear | COVERED/PASS |
| Numeric domain and overflow review fix | test_auto_reconnect.py::test_phase27_review_backoff_scaled_exponential_at_1024 (2), test_phase27_review_backoff_rejects_unsupported_domain (11), test_phase27_review_backoff_supported_boundaries (4); independent math.ldexp oracle, million-step saturation and invalid values rejected | COVERED/PASS |
| Pairing, reset, grace/settle/flap compatibility | test_bluetooth_manager.py::test_phase27_connection_one_failure_preserves_bond, test_already_connected_speaker_is_not_torn_down, test_operator_connect_still_resets_an_existing_link; test_auto_reconnect.py::test_stale_recovery_preserves_pairing_for_a_speaker_not_in_pairing_mode, test_reconnect_state_machine, test_scheduled_retry_waits_for_the_full_settle_window, test_repeated_flaps_earn_a_cooldown_instead_of_a_retry_loop | COVERED/PASS |
| API/SIL compatibility and busy response | All 26 test_api.py and 13 test_bridge_sil.py cases passed in prior independent gate; prior verifier additionally invoked real routes.connect_device with busy manager, asserting HTTP 409, reset_existing=True, one manager call and no publication. No permanent HTTP-409 test is claimed | COVERED/PASS with direct prior runtime probe |
| Version/docs | test_addon_config.py::test_runtime_version_is_sourced_from_the_shared_constant, test_repository_yaml_and_documentation, test_dependency_and_release_policy_is_explicit; prior direct YAML/import probe asserts 0.2.68 manifest/runtime/package equality. README/DOCS/current changelog manually checked against policy; prose accuracy is not claimed as wholly test-enforced | COVERED/PASS, automated metadata plus direct document inspection |

Requirements PROD-04 and PROD-05 are now explicitly recorded as locally verified
in finalized REQUIREMENTS.md and Phase 27 has 1/1 completed plans in ROADMAP.md.
All three tasks have executable checks with nonzero/empty-selection failures
defined in PLAN. T-27-01 through T-27-04 map to the behavior rows above;
T-27-SC is the documented no-dependency-change accepted risk, not a test claim.
The parent-authored 27-SECURITY.md records direct ASVS L1 closure (zero open
threats) and explicitly discloses that the security agent assessed nothing.

Only the preexisting Windows/POSIX process-group test is skipped; it does not
prove a Phase 27 requirement. No disabled phase test, circular generated oracle,
or existence-only assertion substitutes for the listed behavioral evidence.
Hardware power-loss/range/playback soak remains explicitly DEFERRED, not PASS.

## Validation Audit

| Metric | Count |
| --- | --- |
| Gaps found | 0 |
| Resolved | 0 |
| Escalated | 0 |

Final coverage status: PASS for the approved local boundary; nyquist_compliant:
true. The audit trail is updated via apply_patch as explicitly requested, rather
than permitting the workflow append-audit verb to write this report. No commit,
staging, source/test edit, deployment or planning-state advancement was performed.