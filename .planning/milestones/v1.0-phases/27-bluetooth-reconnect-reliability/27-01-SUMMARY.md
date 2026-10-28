---
phase: 27-bluetooth-reconnect-reliability
plan: "01"
subsystem: bluetooth
tags: [asyncio, bluez, reconnect, reliability, tdd]
requires: []
provides:
  - Single bounded connect with shared actual-adapter ownership
  - Scheduler-only retries with conservative persistent failure pacing
  - Version 0.2.68 operator guidance and local validation evidence
affects: [bluetooth, reconnect, authorized-haos-soak]
tech-stack:
  added: []
  patterns: [manager-owned adapter locks, single-attempt connection, retained half-open history]
key-files:
  created:
    - .planning/phases/27-bluetooth-reconnect-reliability/27-01-SUMMARY.md
  modified:
    - modules/bridge/backend/bl_haos/bluetooth/device.py
    - modules/bridge/backend/bl_haos/bluetooth/manager.py
    - modules/bridge/backend/bl_haos/bluetooth/reconnect.py
    - modules/bridge/backend/bl_haos/constants.py
    - modules/bridge/tests/test_bluetooth_device.py
    - modules/bridge/tests/test_bluetooth_manager.py
    - modules/bridge/tests/test_auto_reconnect.py
    - modules/bridge/README.md
    - modules/bridge/DOCS.md
    - modules/bridge/CHANGELOG.md
    - modules/bridge/config.yaml
    - .planning/phases/27-bluetooth-reconnect-reliability/27-VALIDATION.md
key-decisions:
  - "One 30-second manager operation, actual-adapter locks, no inner retry or automatic reset"
  - "10-second initial delay, multiplier 2, final 120-second cap, non-negative 15% jitter"
  - "Eight failures open a 300-second breaker; half-open failures retain history and reopen it"
  - "No commits, state advancement, deployment or live operations; parent owns final verification"
requirements-completed: [PROD-04, PROD-05]
actuals:
  tokens: 16718
  tasks: 3
  commits: 0
commits: 0
commit_policy: prohibited-by-user
plan_head_before: null
plan_head_after: 97a0130916ad8203903c6cb0e539f69b0a7c99f5
root_head_at_handoff: 9ab8f2ead4f5fd96c3515e06f5a384a5fbcb045d
coverage:
  - id: D1
    description: Bounded single connection and shared actual-adapter ownership
    requirement: PROD-04
    verification:
      - kind: integration
        ref: "modules/bridge/tests/test_auto_reconnect.py#test_phase27_connection_scheduled_tick_has_one_bluez_attempt"
        status: pass
      - kind: unit
        ref: "modules/bridge/tests/test_bluetooth_manager.py#phase27_connection"
        status: pass
    human_judgment: false
  - id: D2
    description: Conservative scheduler pacing, retained breaker history and real-lock cleanup
    requirement: PROD-05
    verification:
      - kind: unit
        ref: "modules/bridge/tests/test_auto_reconnect.py#phase27_pacing"
        status: pass
    human_judgment: false
  - id: D3
    description: Version 0.2.68 metadata and current operator retry/reset documentation
    requirement: PROD-05
    verification:
      - kind: unit
        ref: "modules/bridge/tests/test_addon_config.py"
        status: pass
    human_judgment: false
duration: 12m 20s
completed: "2026-10-24"
status: complete
completion_scope: local-implementation-and-tests-only
parent_review: clean
hardware_soak: pending-authorized-deployment
---

# Phase 27 Plan 01: Bluetooth Reconnect Reliability Summary

**One bounded scheduler-to-BlueZ attempt, shared actual-adapter ownership, and retained 10-120 second retry pacing with a 300-second circuit breaker.**

## Performance and Scope

- Execution started: 2026-10-24T08:34:28Z; implementation/gates completed: 2026-10-24T08:46:48Z.
- Three tasks implemented; 11 existing bridge files changed, no new source/test files or dependencies.
- Realized bridge diff measured with PowerShell string length: 66,872 characters / 4, rounded up = 16,718 estimated tokens. This excludes phase-local evidence artifacts.
- Everything remains uncommitted. No branch, staging, commit, deployment, token use, adapter reset, pairing removal, or live host operation was performed.
- STATE.md, state.json, phase24 and ROADMAP.md were not modified by this executor. Their existing parent changes were present at entry and left alone.
- Parent independent plan-checker PASS was supplied in the execution request; this executor did not rerun or claim independent review.

## Accomplishments

1. **Connection path:** BluetoothDevice classifies busy case-insensitively before profile handling. Only AlreadyConnected may activate A2DP once; generic errors propagate without claiming Connected. BluetoothManager performs one connect under a 30-second timeout covering resolution, scan stop/settle, optional explicit reset and trust update. Locks are keyed by the resolved device's actual adapter and survive cache/transport refreshes. Contenders fail fast, and cancellation/timeout/exceptions release ownership. Generic failure preserves valid cache; classified stale-object failure detaches the record without deleting its bond and resolves on a later request.
2. **Scheduler:** Removed separate engine adapter locks and reset-based recovery. One manager call per scheduled attempt; delays are 10, 20, 40, 80, 120 seconds at zero jitter, with saturation before exponentiation and only non-negative jitter within the final cap. Busy preserves counters and defers at least the current delay or 15 seconds, whichever is longer. Presence cannot accelerate a retry. Existing deadlines, flap cooldowns and breaker deadlines remain lower bounds. Eight failures open the breaker for 300 seconds; expiry admits one half-open attempt without clearing history. Failure reopens it; confirmed success clears it. Stop/unregister cancellation drains workers, releases real manager ownership and cannot resurrect a replaced profile.
3. **Operator guidance:** Manifest, runtime VERSION and changelog identify 0.2.68. README/DOCS describe the conservative policy, preserved pairing, explicit Connect/failed-play reset under shared ownership, and pending authorized hardware soak. Existing 5-second grace, 15-second settle, six-flaps-in-120-seconds/60-second suppression, API 409, operator reset and SIL contracts pass.

## Changed Files

- backend/bl_haos/bluetooth/device.py: busy classification and AlreadyConnected-only profile activation.
- backend/bl_haos/bluetooth/manager.py: shared adapter locks, complete-operation timeout, single attempt, retained stale records.
- backend/bl_haos/bluetooth/reconnect.py: scheduler-only retry ownership, retained pacing/breaker history and cancellation cleanup.
- backend/bl_haos/constants.py: conservative timing defaults and VERSION 0.2.68.
- tests/test_bluetooth_device.py, tests/test_bluetooth_manager.py, tests/test_auto_reconnect.py: new regressions and deliberate legacy contract updates.
- README.md, DOCS.md, CHANGELOG.md, config.yaml: current retry/reset guidance and release metadata.
- Phase-local 27-VALIDATION.md and this summary: observed evidence and handoff limitations.

Bridge-relative paths above are under modules/bridge. No API, playlist, integration, frontend or unrelated test file changed.

## Test Commands and Results

Every valid run used PowerShell with this explicit setup (the terminal may reset cwd between calls):

```powershell
Set-Location F:/Workspace/BL-HAOS/modules/bridge
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
```

Every row uses the absolute workspace virtual-environment Python interpreter with
the arguments -m pytest -c pytest.ini.
All rows used `-q --tb=short`; the full suite additionally used `-ra`.

| Run | Arguments after prefix | Actual result | Exit | Pytest duration |
| --- | --- | --- | --- | --- |
| Task1 RED | tests/test_bluetooth_device.py tests/test_bluetooth_manager.py tests/test_auto_reconnect.py -q -k phase27_connection --tb=short | 13 failed, 43 deselected (56 collected) | 1 | 9.08s |
| Task1 GREEN | Same selection and flags | 13 passed, 43 deselected | 0 | 4.43s |
| Task1 compatibility, before legacy updates | tests/test_bluetooth_device.py tests/test_bluetooth_manager.py -q --tb=short | 3 failed, 40 passed | 1 | 6.06s |
| Task1 compatibility, after legacy updates | Same two files and flags | 43 passed | 0 | 6.81s |
| Task2 RED | tests/test_auto_reconnect.py -q -k phase27_pacing --tb=short | 6 failed, 1 passed, 13 deselected (20 collected) | 1 | 1.35s |
| Task2 GREEN | Same selection and flags | 7 passed, 13 deselected | 0 | 1.40s |
| Task2 integrated, before legacy updates | tests/test_bluetooth_device.py tests/test_bluetooth_manager.py tests/test_auto_reconnect.py tests/test_api.py tests/test_bridge_sil.py -q --tb=short | 7 failed, 95 passed, 1 warning | 1 | 9.54s |
| Task2 integrated, after legacy updates and manual-first ownership test | Same five files and flags | 103 passed, 1 warning | 0 | 9.61s |
| Final focused + metadata | tests/test_bluetooth_device.py tests/test_bluetooth_manager.py tests/test_auto_reconnect.py tests/test_api.py tests/test_bridge_sil.py tests/test_addon_config.py -q --tb=short | 110 passed, 1 warning | 0 | 9.55s |
| Complete bridge | tests -q --tb=short -ra | 253 passed, 1 skipped, 1 warning (254 collected) | 0 | 11.97s |

The final scheduler file contains eight phase27_pacing cases: seven in the initial RED/GREEN selection plus the manual-first ownership case added with the explicit legacy contract updates. All eight passed in both final integrated gates and the full suite. No pending-task or unawaited-coroutine warning appeared.

### Actual RED Assertions and Semantic Assessment

- Task1 busy parameterizations (InProgress, In Progress, br-connection-busy, operation-already-in-progress, uppercase spaced variant): `DID NOT RAISE BluetoothOperationInProgress` because the old profile fallback silently succeeded.
- Task1 generic device error: `DID NOT RAISE RuntimeError`; old code claimed success after a generic failed Connect.
- Task1 manager generic/stale failures: `assert 3 == 1` Connect calls. Both failure forms demonstrated nested retries before any production change.
- Task1 whole-operation timeout cases: `assert [] == [30.0]`; no manager timeout existed for blocked resolution or connection. Outer test deadlines prevent hangs and do not constitute a passing manager deadline.
- Task1 ownership in both request orderings: competing request reached the blocked operation and hit the test's 0.6-second deadline instead of fail-fast busy. Events/finally drained all tasks in the completed RED run.
- Task1 real engine/manager/device tracer: `Expected mock to not have been awaited. Awaited 1 times` for ConnectProfile after generic Connect failure. The manager/device were real; only BlueZ was fake.
- Task2 defaults: `assert 1.0 == 10.0`; initial scheduling: `assert 1001.0 == 1010.0`.
- Task2 presence: `assert 1000.0 == 1500.0`; RSSI pulled a retained deadline forward.
- Task2 breaker/call ownership: `assert 3 == 2` manager calls on the second scheduled failure because automatic recovery issued an extra call.
- Task2 stop cleanup: profile stayed `reconnecting` instead of `backoff`. Unregister/replacement cleanup already passed, retained as a compatibility test.
- Both valid RED runs collected the intended new tests and exited 1 for the planned behavior, not import/collection/plugin faults. GREEN immediately followed each behavior edit before widening scope. No machine RED-classifier verdict is claimed.

### Invalid/Interrupted Attempts (Not RED Proof)

- First task1 test run lacked a contention-test watchdog. It was interrupted after eight intended failures, 43 deselected, 310.74s; production remained untouched. The test harness was repaired with a bounded contender request and final cleanup before the completed 13-case RED run.
- The next command omitted Set-Location because the terminal had returned to workspace-root cwd. It collected zero tests in 0.00s with file-not-found errors (tool exit 1). This was rejected as RED evidence and immediately rerun from the correct bridge cwd.
- Ordinary plugin autoload's unrelated HA/fcntl crash was supplied as baseline context, not reproduced or counted as a regression. All valid executor pytest runs isolated plugins as required.

## Deviations and Issues

- No production scope or architectural deviation. Legacy retry/refresh, presence acceleration, automatic reset-healing, busy counter reset and breaker history-reset expectations were deliberately replaced, as required by the plan.
- The contention-test watchdog repair and explicit cwd prefix were execution-harness corrections, not production fixes. There were no repeated production repair loops and no three-attempt limit was exceeded.
- No commits, commit ledger, state handlers, requirement-marking handlers or phase advance ran, by explicit override. `commits: 0` reflects no commit operation; `plan_head_before: null` discloses that no start-time HEAD snapshot/commit ledger was captured rather than inventing a measured range. Handoff HEADs are recorded above. Parent owns final requirement/phase completion.
- A final local health hypothesis was checked: HealthRegistry.observe_speaker retains previous failure observations for non-connected states and clears them on CONNECTED. No extra edit was needed.
- Diff check passed; editor diagnostics reported no errors across all seven changed Python files. Stub scan found only the preexisting initialization warning "System D-Bus connection not available"; no new incomplete implementation or UI stub exists. No new security surface outside the plan's manager/BlueZ/cancellation trust boundaries was introduced.

## Skips, Warnings and Remaining Risk

- Existing platform skip: tests/test_media_player.py:654, `POSIX process groups are required`, on Windows. This test was not changed or newly skipped.
- Existing dependency warning: FastAPI TestClient imports Starlette's httpx integration, deprecated in favor of httpx2. No install or unrelated dependency edit was authorized or performed.
- HAOS/physical Bluetooth reconnect soak is pending separate authorized deployment. No claim is made that local tests fixed the observed live radio fault. Eventually validate speaker power loss/return, busy BlueZ, prolonged failure/half-open probes, preserved bonds, explicit reset and stable playback.
- Timeout uses cooperative asyncio cancellation; fake-BlueZ tests prove local cancellation/ownership behavior, not a hardware/daemon responsiveness guarantee. Retry history remains process-local by design.
- Parent independent re-review is clean and canonical local verification passed after the review fixes (280 passed, one existing platform skip). Paused phase24 was not resumed. Authorized HAOS soak remains pending.

## Task Commits

None. All three task changes and phase artifacts remain uncommitted as explicitly requested. No deployment occurred.

## Self-Check: PASSED

- Parsed both phase-artifact YAML frontmatters successfully and verified all 13 artifact paths exist.
- Verified three completed local tasks, zero commits and pending authorized hardware soak in structured metadata.
- Bridge diff check passed; no untracked bridge files or new source/test files remain.
- Root status still contains the preexisting parent ROADMAP/STATE/state.json changes; this executor did not edit them. Only the bridge and requested phase-local artifacts were edited.
- All required local executable gates passed with the existing platform skip and dependency warning disclosed above. Parent implementation review and hardware approval are not implied.

## Review Fix Follow-Up: CR-01 and WR-01

Recorded 2026-10-24T08:56:31Z. This section is new observed evidence, not a
replacement or independent re-observation of the historical results above.
Source review remains issues_found; the parent must rerun independent review.

### Applied Changes

- CR-01: ensure_device rechecks the cache after awaited GetAll and returns an
  already-installed live object instead of replacing the winner. connect_device
  validates selected-record identity and attachment under adapter ownership,
  after scan stop/settle, before Connect (including explicit reset settle), and
  before returning success after the awaited trust update. Withdrawal or
  replacement fails the single attempt; the existing scheduler retains failure
  history and arms backoff. No immediate retry, pairing deletion or automatic
  reset was added.
- WR-01: supported backoff values are finite initial_backoff >= 0, finite
  backoff_multiplier >= 1 and finite max_backoff > 0. Zero remains zero; tiny
  positive values remain supported. Saturation is checked in log space, then
  base-two growth is applied to the initial mantissa/exponent without forming
  an overflowing standalone multiplier power. Floor, non-negative jitter and
  final cap remain unchanged, including existing custom short delays.
- Added 27 cases in the existing manager/reconnect test files: two concurrent
  missing/detached resolution races, eight removal/replacement barriers across
  stop_scan/settle/Connect/trust, two zero/tiny-positive step-1024 regressions,
  eleven invalid-domain cases and four supported-boundary cases. The manager
  barriers exercise the real engine failure transition and drain every task.
- Only two existing production files and two existing test files were edited
  for these findings. No public signature or API contract changed. Existing
  unreleased phase-27 0.2.68 metadata and operator policy remain unchanged.

### Observed Review-Fix Commands

All runs were in the main checkout, not an isolated worktree. Each command used:

```powershell
Set-Location F:/Workspace/BL-HAOS/modules/bridge
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
```

The unchanged regression command, run immediately after the initial test edits
and immediately after each of the two production edits, was:

```powershell
F:/Workspace/BL-HAOS/.venv/Scripts/python.exe -m pytest -c pytest.ini tests/test_bluetooth_device.py tests/test_bluetooth_manager.py tests/test_auto_reconnect.py -q -k phase27_review --tb=short
```

| Checkpoint | Actual result | Exit | Duration |
| --- | --- | --- | --- |
| RED before either production edit | 23 failed, 4 passed, 64 deselected; 91 collected, 27 selected | 1 | 1.23s |
| Immediately after manager edit | 13 failed, 14 passed, 64 deselected; all 10 CR-01 cases passed | 1 | 1.07s |
| Immediately after reconnect edit | 27 passed, 64 deselected | 0 | 0.82s |

RED assertions were cache identity inequality in both resolution races,
CONNECTED instead of BACKOFF in all eight withdrawal cases, explicit pytest
failure on OverflowError for initial 0.0 and 1e-320 at step 1024, and missing
ValueError for eleven unsupported constructor values. There were no
collection/import failures, watchdog timeouts or empty selections. The four
supported-boundary cases already passed and were retained. No repair loop was
needed: each production file had one review-fix edit followed by the same check.

Required gates then ran in order, with unchanged file selections:

```powershell
F:/Workspace/BL-HAOS/.venv/Scripts/python.exe -m pytest -c pytest.ini tests/test_bluetooth_device.py tests/test_bluetooth_manager.py tests/test_auto_reconnect.py tests/test_api.py tests/test_bridge_sil.py tests/test_addon_config.py -q --tb=short
F:/Workspace/BL-HAOS/.venv/Scripts/python.exe -m pytest -c pytest.ini tests -q --tb=short -ra
```

| Gate | Actual result | Exit | Duration |
| --- | --- | --- | --- |
| Six-file focused gate | 137 passed, 1 warning | 0 | 10.28s |
| Full bridge gate | 280 passed, 1 skipped, 1 warning; 281 collected | 0 | 12.36s |

The existing skip remains test_media_player.py:654 (POSIX process groups on
Windows); the sole warning remains Starlette/httpx TestClient deprecation.
No pending-task or unawaited-coroutine warnings occurred. Editor diagnostics
were clear for all four changed Python files; bridge git diff --check passed.

All changes remain uncommitted and unstaged. No branch/worktree, dependency
install, deployment, host/radio action, reset/unpair, phase24 edit or state update
was performed. Existing parent STATE/ROADMAP/state.json changes were left alone.
Independent parent re-review and authorized HAOS/physical-speaker soak are still
pending; REVIEW.md was not edited or marked clean. See 27-REVIEW-FIX.md for the
per-finding handoff.