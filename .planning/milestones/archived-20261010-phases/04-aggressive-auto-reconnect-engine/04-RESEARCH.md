# Phase 4: Aggressive Auto-Reconnect Engine - Research

**Phase:** 4 (Aggressive Auto-Reconnect Engine)
**Researched:** 2026-09-21
**Confidence:** HIGH

## Overview

Bluetooth audio speakers often enter low-power standby or power off completely when no audio has played for 10-15 minutes. When powered back on or when they re-enter Bluetooth RF range, typical Linux desktop setups fail to reconnect automatically.

## Reconnection Strategy

1. **Passive Event Hooking**:
   - `BluetoothManager` emits `device_updated` and `device_discovered` events.
   - When `Connected` transitions from `true` to `false`, the engine registers the device in its retry queue.
   - When a device is discovered (e.g. from background periodic inquiry scan), the retry queue fast-tracks that address.

2. **Concurrency & Adapter Protection**:
   - BlueZ adapters queue connection requests, but calling `Connect` on multiple devices concurrently can result in `org.bluez.Error.InProgress` or `org.bluez.Error.Failed`.
   - Wrapping per-adapter connections in an `asyncio.Lock` ensures serialized, clean connection handshakes.
   - A circuit breaker prevents tight reconnect loops when a device is out of range.

---
*Research for Phase 4: Aggressive Auto-Reconnect Engine*
