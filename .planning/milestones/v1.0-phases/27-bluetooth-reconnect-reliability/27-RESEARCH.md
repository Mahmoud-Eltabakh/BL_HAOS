# Phase 27: Bluetooth Reconnect Reliability

Date: 2026-10-24. Discovery level 0: existing asyncio, pytest-asyncio,
dbus-fast and module-local patterns; no new dependency or install is needed.
This is planner-local source analysis, not an independent research/checker verdict.

## Controlling Evidence

- `bluetooth/device.py:BluetoothDevice.connect` falls through from Connect errors
  (including InProgress) to ConnectProfile. Preserve the existing AlreadyConnected
  profile-activation contract, but propagate busy immediately and do not fall back
  on arbitrary failures.
- `bluetooth/manager.py:BluetoothManager.connect_device` performs three Connect
  attempts followed by a refreshed-proxy Connect; missing-device resolution can
  additionally call Adapter.ConnectDevice on multiple adapters. It has no shared
  lock. Remove both retry paths from this boundary. Read-only resolution may
  refresh a detached/stale record for a later scheduled attempt, not reconnect now.
- `bluetooth/reconnect.py:AutoReconnectEngine` owns only automatic adapter locks,
  performs a second manager call with reset_existing=True during self-healing,
  schedules failed healing at initial_backoff, clears counters on busy, and lets
  RSSI events move retry deadlines earlier. These independent bypasses explain
  retry pressure; source evidence does not establish the live radio fault's cause.
- Existing tests explicitly expect four manager connects, automatic reset-based
  healing, busy counter resets, presence fast-tracking and breaker counter resets.
  Rewrite those assertions to the new behavior rather than retain conflicting
  contracts or weaken call-count checks.

## Design Contract

R1. Scheduler is the only repeated-automatic-attempt owner. One manager call per
scheduled attempt; one Device1.Connect, with at most one ConnectProfile only for
AlreadyConnected. InProgress, In Progress, br-connection-busy and operation-already-
in-progress text defer via BluetoothOperationInProgress with no profile call.

R2. Manager-local per-adapter asyncio locks cover all connect_device callers,
including operator reset. Use actual resolved adapter identity, not a preferred
adapter label that does not select the underlying device. Fail fast on contention
with BluetoothOperationInProgress; do not queue stale requests. Release ownership
on success, exception, timeout and cancellation. Bound one complete manager
operation to 30 seconds, including read-only resolution and optional operator
disconnect; cancellation cannot publish success. No scheduler lock in parallel
with manager ownership. Pairing consent and unrelated operations remain unchanged.

R3. Defaults: initial 10s, multiplier 2, max 120s, minimum 10s, eight failures,
breaker 300s. Keep 15% jitter but use non-negative jitter and clamp the final delay
to 120s; jitter never shortens the nominal delay. These allow BlueZ/A2DP to settle
and avoid the previous 1s/20s/10s retry pressure. Busy preserves failure/step counts
and waits at least max(current-step delay, 15s settle); it never moves a deadline
earlier. Presence never shortens a pending deadline. Automatic recovery does not
disconnect, unpair, reset a controller, or add an extra Connect. Breaker expiry
permits one half-open attempt without clearing history; failure reopens for 300s.
Only confirmed connection success clears failure pacing. Retain dropout grace,
successful-link settle and flap suppression. Arithmetic must saturate before
exponentiation to avoid overflow during prolonged offline operation.

R4. Preserve connect_device(address, reset_existing=False), explicit operator
reset semantics, HTTP 409 busy mapping, bonds, trusted offline records and existing
API contracts. Cache invalidation on classified stale-object errors is read-only
and preserves the offline speaker; failed generic connects must not delete it.

R5. Update existing DOCS.md stability prose (currently promises 10s breaker and
automatic reset healing) and README.md aggressive/instant-reconnect promise.
Add CHANGELOG.md 0.2.68 and bump both config.yaml and constants.VERSION from
0.2.67 to 0.2.68. Historical changelog entries remain historical.

## Validation Architecture

Reuse test_bluetooth_device.py, test_bluetooth_manager.py and
test_auto_reconnect.py, AsyncMock, fake D-Bus interfaces, asyncio.Event barriers
and monkeypatched clocks. Add regressions first and immediately run them red
before production edits. A plugin/import/collection error is NOT red evidence.
Then run focused tests including test_api.py and test_bridge_sil.py, followed by
the entire bridge suite with its own pytest.ini. No hardware or network is needed
for new tests. A real scheduler -> manager -> device -> fake BlueZ regression
must count calls, not replace manager.connect_device with a mock.

Interpreter: F:/Workspace/BL-HAOS/.venv/Scripts/python.exe. Initial baseline with
normal plugin autoload stopped before collection: Home Assistant's plugin imports
Linux-only fcntl. Disable third-party plugin autoload and explicitly enable asyncio
(the bridge pytest.ini already supplies -p asyncio). Record a rerun before claiming
the baseline passed. Never change production/tests or install packages to fix this
planning-only environment issue.

Verified rerun: pytest 9.0.3 / asyncio 1.4.0 / Python 3.14.7, **43 passed in
5.42s** across the three Bluetooth test files. The equivalent invocation through
pytest.main with PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 collected and ran successfully.
Use the environment setting before the plan's python.exe -m pytest commands.
All planned source paths were verified tracked inside modules/bridge, whose
status remained clean. History digest was empty; graphify was disabled, so neither
supplied additional evidence. Estimate calibration: factor 1, zero samples, low
confidence. No changes to global/project configuration were made.

## Scope and Assumptions

- REQUIREMENTS.md is playlist-only; PROD-04/PROD-05 descriptions are grounded in
  ROADMAP phases 17 and 27, not fabricated playlist requirements.
- CONTEXT.md has unnumbered locked bullets. The plan uses descriptive group
  references instead of editing the source to invent decision IDs.
- One bounded plan with three tasks is sufficient; no new production/test files,
  public API options, persistent retry metadata or general locking framework.
- No commits/branches, deployment, token use, adapter reset or pairing deletion.
  STATE.md phase 24's paused checkpoint and preexisting phase metadata stay intact.
- Live hardware soak is deferred until separately authorized, never proven by SIL.
- Parent runs the independent checker. No independent checker has run here.