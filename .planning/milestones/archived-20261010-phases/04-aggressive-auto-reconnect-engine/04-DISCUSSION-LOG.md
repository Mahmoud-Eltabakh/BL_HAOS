# Phase 4: Aggressive Auto-Reconnect Engine - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.

**Date:** 2026-09-21
**Phase:** 04-aggressive-auto-reconnect-engine
**Areas discussed:** Backoff timing, Fast-track discovery triggers, Adapter lock concurrency, Circuit breaker parameters.

## Decisions:
1. **Backoff**: Base 2.0s, multiplier 2.0, maximum 60.0s, jitter ±15%.
2. **Fast-Track**: Immediate connection attempt upon receiving any RSSI or interface discovery packet for trusted speakers.
3. **Adapter Safety**: `asyncio.Lock` per adapter + 5-failure circuit breaker threshold with 30s reset.
