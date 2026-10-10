# Phase 3: BlueZ D-Bus Bluetooth Controller - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.

**Date:** 2026-09-21
**Phase:** 03-bluez-d-bus-bluetooth-controller
**Areas discussed:** D-Bus async stack, Device filtering, Pairing Agent design, Multi-adapter architecture

## Decisions:
1. **D-Bus Client:** `dbus-fast` with native `asyncio` event loop.
2. **Device Discovery:** Audio sink filtering based on UUIDs (`0000110b-...`) and CoD (`0x040000`) with live RSSI streaming.
3. **Pairing Agent:** D-Bus agent `/org/bl_haos/agent` implementing `org.bluez.Agent1` supporting PIN entry, Passkey, and SSP confirmation.
4. **Multi-Adapter:** First-class per-adapter tracking and management for `hci0`, `hci1` etc.
