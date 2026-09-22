# Phase 5: FastAPI Backend Daemon & Real-Time Event Bus - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.

**Date:** 2026-09-21
**Phase:** 05-fastapi-backend-daemon-real-time-event-bus
**Areas discussed:** REST API schema, WebSocket broadcast protocol, Persistent configuration store, S6 daemon integration.

## Decisions:
1. **REST & WS Framework:** FastAPI + Uvicorn on port 8099.
2. **WebSocket Format:** JSON envelope `{"event": str, "data": Any}`.
3. **Storage:** `/data/bl_haos_config.json` with Pydantic serialization.
4. **S6 Supervision:** `40-bl-haos-daemon` depending on `20-wireplumber`.
