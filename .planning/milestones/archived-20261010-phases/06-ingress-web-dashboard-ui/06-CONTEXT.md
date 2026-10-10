# Phase 6: Ingress Web Dashboard UI - Context

**Gathered:** 2026-09-21
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 6 delivers the visual web dashboard embedded inside the Home Assistant sidebar via Ingress:
- React 18 + Vite + Tailwind CSS frontend styled with Home Assistant Material/Slate theme colors.
- Strict relative path routing (`base: "./"`) and dynamic WebSocket endpoint resolution (`ws://` / `wss://` derived from `window.location`) for 100% Home Assistant Ingress proxy compatibility.
- Live Bluetooth Discovery Scanner modal with animated RSSI signal strength meters, audio device classification badges, and one-click PIN/SSP pairing.
- Speaker Management Dashboard displaying active connection status, signal strength, assigned Bluetooth adapter, and interactive volume sliders.
- Global Settings Panel allowing multi-adapter assignment, codec preference override, and auto-reconnect toggles.
- FastAPI static asset serving mounting `frontend/dist` on the root route.

</domain>

<decisions>
## Implementation Decisions

### Ingress Relative Path Architecture
- **D-01:** Build the frontend with `base: "./"` in `vite.config.ts`. All API calls must use relative paths (e.g. `./api/...`) or derive the base URL from `window.location.pathname`, and WebSocket connections must connect to `(window.location.protocol === 'https:' ? 'wss:' : 'ws:') + '//' + window.location.host + window.location.pathname.replace(/\/$/, '') + '/ws'`. This prevents broken 404 assets when proxied under `/api/hassio_ingress/{token}/`. — **Reversibility:** one-way.

### UI Design & Theme
- **D-02:** Modern Home Assistant dark/light theme (Slate-900 background, Blue-500 accents, Emerald-500 connected states) responsive for mobile and desktop screens. — **Reversibility:** reversible.

### Real-Time React State
- **D-03:** Custom React hook `useBluetoothEvents()` maintaining local state from initial REST fetch and live-updating via WebSocket event broadcasts. — **Reversibility:** reversible.

</decisions>

<canonical_refs>
## Canonical References
- `https://developers.home-assistant.io/docs/add-ons/presentation#ingress` — Home Assistant Ingress specification.
- `.planning/PROJECT.md` — BL-HAOS UI requirements.
- `.planning/REQUIREMENTS.md` — Requirements `UI-01`, `UI-02`, `UI-03`, `UI-04`.
</canonical_refs>
