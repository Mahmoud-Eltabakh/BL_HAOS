# Phase 6: Ingress Web Dashboard UI - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.

**Date:** 2026-09-21
**Phase:** 06-ingress-web-dashboard-ui
**Areas discussed:** Ingress relative pathing, WebSocket client resolution, UI component design, Theme styling.

## Decisions:
1. **Frontend Stack:** React 18, Vite, Tailwind CSS, Lucide icons.
2. **Ingress Compatibility:** Relative base path `base: "./"` and dynamic WS protocol and path calculation.
3. **Components:** DiscoveryModal, SpeakerCard, VolumeSlider, SettingsModal, AdapterStatus.
