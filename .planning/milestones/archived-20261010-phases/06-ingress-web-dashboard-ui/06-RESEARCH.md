# Phase 6: Ingress Web Dashboard UI - Research

**Phase:** 6 (Ingress Web Dashboard UI)
**Researched:** 2026-09-21
**Confidence:** HIGH

## Overview

Home Assistant Ingress dynamically assigns a tokenized reverse proxy URL (e.g. `/api/hassio_ingress/mYt0kEn123/`).

## Crucial Ingress UI Best Practices
1. **Never use absolute path roots (`/`) in HTML or JS imports**:
   - In `vite.config.ts`, set `base: "./"`.
   - Index HTML must reference `./assets/...` not `/assets/...`.
2. **Dynamic WebSocket Path Derivation**:
   ```javascript
   const proto = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
   const basePath = window.location.pathname.replace(/\/+$/, '');
   const wsUrl = `${proto}//${window.location.host}${basePath}/ws`;
   ```
3. **Dynamic API Endpoint Derivation**:
   ```javascript
   const apiBase = `${window.location.pathname.replace(/\/+$/, '')}/api`;
   ```

---
*Research for Phase 6: Ingress Web Dashboard UI*
