# Phase 5: FastAPI Backend Daemon & Real-Time Event Bus - Context

**Gathered:** 2026-09-21
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 5 delivers the central FastAPI backend daemon, REST API endpoints, real-time WebSocket event broadcaster, and persistent JSON configuration store:
- REST API endpoints for:
  - Adapter management: `GET /api/adapters`, `POST /api/adapters/{name}/power`, `POST /api/scan/start`, `POST /api/scan/stop`.
  - Device management: `GET /api/devices`, `POST /api/devices/pair`, `POST /api/devices/{address}/connect`, `POST /api/devices/{address}/disconnect`, `DELETE /api/devices/{address}`.
  - Settings & Persistent Store: `GET /api/settings`, `PUT /api/settings/speakers/{address}`.
- WebSocket Event Bus on `/ws`:
  - Live broadcast of device discovery (`device_discovered`), signal updates (`device_updated`), connection state changes, and adapter status.
- Persistent Config Storage:
  - JSON configuration stored at `/data/bl_haos_config.json` (or `/tmp/bl_haos_config.json` fallback) saving speaker custom names, auto-reconnect toggles, and preferred adapters.
- S6-rc Supervision Service:
  - `40-bl-haos-daemon` supervising `uvicorn bl_haos.main:app --host 0.0.0.0 --port 8099` depending on `20-wireplumber`.

</domain>

<decisions>
## Implementation Decisions

### API Design & Routing
- **D-01:** Use FastAPI with async route handlers. Group routes logically under `/api/adapters`, `/api/devices`, `/api/settings`, and `/ws`. Ingress path prefix handling will be supported via relative root paths. — **Reversibility:** reversible.

### WebSocket Connection Management
- **D-02:** Implement `ConnectionManager` handling multiple active browser clients, broadcasting JSON frames: `{"event": "<type>", "data": <payload>}` with heartbeat ping/pong. — **Reversibility:** reversible.

### Storage Persistence
- **D-03:** Store user configurations in Home Assistant OS add-on `/data` volume partition (`/data/bl_haos_config.json`) with atomic write updates and fallback for local unit tests. — **Reversibility:** reversible.

### S6 Supervision
- **D-04:** S6 longrun service `40-bl-haos-daemon` depends on `20-wireplumber` and runs on port `8099` (matching `ingress_port` in `config.yaml`). — **Reversibility:** costly.

</decisions>

<canonical_refs>
## Canonical References
- `https://developers.home-assistant.io/docs/add-ons/presentation` — Ingress port mapping & proxy headers.
- `.planning/PROJECT.md` — Core architecture.
- `.planning/REQUIREMENTS.md` — Requirements `API-01`, `API-02`, `API-03`.
</canonical_refs>
