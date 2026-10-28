# Phase 27: Bluetooth Reconnect Reliability - Context

**Gathered:** 2026-10-24
**Status:** Ready for planning

<domain>
## Phase Boundary

Fix nested connection retries, share connection ownership between manual and automatic requests, and apply longer backoff that recovery cannot bypass. This is a dedicated phase-27-only autonomous run; playlist phases 24-26 remain paused.
</domain>

<decisions>
## Implementation Decisions

### Retry Ownership
- The reconnect scheduler owns repeated automatic attempts. Remove retry amplification in manager/device paths instead of merely slowing the outer loop.
- A BlueZ operation-in-progress response must not immediately launch ConnectProfile against the same connection.
- Preserve bonds. No automatic unpairing, controller resets, or host restarts.

### Shared Connection Ownership
- Put serialization at the manager boundary used by operator and automatic connections, not only inside the reconnect engine.
- Busy operations must defer safely and locks must be released after cancellation and exceptions.
- Keep existing public API contracts and use the existing BluetoothOperationInProgress exception where appropriate.

### Backoff and Recovery
- Use conservative exponential retry delays and a substantially longer circuit-breaker cooldown than the current ten seconds.
- Failed recovery must not return to a one-second delay. Presence and busy responses must not erase accumulated failure pacing.
- Preserve successful-link settle windows and flap suppression.

### Agent Discretion
- The user is unavailable and explicitly requested autonomous decisions. Choose exact timing constants and implementation details from local patterns and risk.
- Reuse existing tests and test helpers. Keep changes limited to the Bluetooth/reconnect slice and required documentation/version metadata.
- Do not commit, branch, deploy, reset the live adapter, or use the access token previously shared in chat.
</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- BluetoothOperationInProgress in bluetooth/device.py and existing API HTTP 409 handling.
- AutoReconnectEngine per-speaker inflight tracking, adapter locks, grace windows, and circuit breaker.
- Existing tests in test_auto_reconnect.py, test_bluetooth_manager.py, test_bluetooth_device.py, test_api.py, and test_bridge_sil.py.

### Established Patterns
- asyncio synchronization, pytest-asyncio, AsyncMock, deterministic monkeypatched clocks.
- User-visible bridge fixes require a patch version bump and CHANGELOG.md update under the repository docs skill.

### Integration Points
- bluetooth/device.py: connect calls ConnectProfile after many Connect errors, including busy responses.
- bluetooth/manager.py: connect_device performs three immediate retries plus a refreshed-proxy retry, without a shared connection lock.
- bluetooth/reconnect.py: recovery adds another manager connection call and resets failed-recovery retry time to initial_backoff.
- constants.py: one-second initial delay, twenty-second cap, and ten-second breaker cooldown.
</code_context>

<specifics>
## Specific Ideas

Live read-only diagnosis found a paired, bonded, trusted Logitech BT Adapter with repeated br-connection-unknown failures. BlueZ logs repeatedly reported AVDTP Operation already in progress (114); a direct bluetoothctl attempt also failed. The Intel controller was powered and checked kernel logs showed no firmware or USB failure. This supports investigating retry pressure but does not prove causation or whole-adapter failure. Hardware soak validation requires an authorized deployment and is not satisfied by local tests.
</specifics>

<deferred>
## Deferred Ideas

- Playlist/catalog phases 24-26.
- Live deployment, adapter recovery/reset, physical receiver checks, and reconnect soak testing.
</deferred>