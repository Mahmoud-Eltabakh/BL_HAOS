# Phase 4: Aggressive Auto-Reconnect Engine - Context

**Gathered:** 2026-09-21
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 4 delivers the aggressive background auto-reconnection and link health daemon (`AutoReconnectEngine`):
- Connection health monitoring subscribing to `BluetoothManager` device updates and D-Bus `PropertiesChanged` signals.
- Exponential backoff scheduler with randomized jitter (e.g., initial 2s, 4s, 8s, 16s, up to 60s max interval) when trusted audio devices drop offline.
- Immediate wake-up trigger: when BlueZ advertises device presence during discovery scan or RSSI update, immediately fast-track reconnection without waiting for backoff timer.
- Adapter reconnection lock and circuit breaker: limits concurrent connection attempts per adapter and triggers a temporary cooldown if an adapter encounters consecutive D-Bus/HCI timeouts.
- Configurable per-speaker auto-reconnect preferences (enabled/disabled, priority adapter).

</domain>

<decisions>
## Implementation Decisions

### Reconnection State Machine
- **D-01:** Track each trusted speaker through states: `CONNECTED`, `DISCONNECTED`, `RECONNECTING`, `BACKOFF`, `CIRCUIT_BROKEN`. — **Reversibility:** reversible.

### Exponential Backoff & Fast-Track
- **D-02:** When a speaker disconnects, arm the backoff timer ($t_{retry} = \min(t_{max}, t_{initial} \times 2^{n}) \pm \text{jitter}$). If a device presence signal / RSSI packet is observed from discovery while in `BACKOFF`, cancel the timer and trigger immediate fast-track connection. — **Reversibility:** reversible.

### Adapter Lock & Circuit Breaker
- **D-03:** Enforce `asyncio.Lock` per Bluetooth adapter so multiple reconnect tasks do not call `Device1.Connect` concurrently on the same HCI controller. If 5 consecutive failures occur with `InProgress` or `Timeout` errors, trip the circuit breaker for 30 seconds to prevent freezing the Linux Bluetooth stack. — **Reversibility:** reversible.

</decisions>

<canonical_refs>
## Canonical References
- `.planning/PROJECT.md` — Project requirements and reconnection strategy.
- `.planning/REQUIREMENTS.md` — Requirements `CONN-01`, `CONN-02`, `CONN-03`.
- `.planning/phases/03-bluez-d-bus-bluetooth-controller/03-VERIFICATION.md` — BluetoothManager foundation.
</canonical_refs>
