# Phase 8: Multi-Room Synchronization with Snapcast - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.

**Date:** 2026-09-21
**Phase:** 08-multi-room-synchronization-snapcast
**Areas discussed:** Snapserver configuration, Dynamic Snapclient routing, Speaker grouping & latency offset.

## Decisions:
1. **Snapserver Config:** S6 longrun service `30-snapserver` configured with PipeWire audio stream source.
2. **Dynamic Client Manager:** Python `MultiroomManager` orchestrating `snapclient` processes targeting per-speaker PipeWire nodes.
3. **Latency Offsets:** Configurable latency offset (+/- milliseconds) per speaker for perfect acoustic phase alignment.
