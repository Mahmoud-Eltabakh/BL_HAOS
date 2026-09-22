# Phase 5: FastAPI Backend Daemon & Real-Time Event Bus - Research

**Phase:** 5 (FastAPI Backend Daemon & Real-Time Event Bus)
**Researched:** 2026-09-21
**Confidence:** HIGH

## Overview

The backend daemon serves as the central API gateway and bridge between the web Ingress frontend, the BluetoothManager, the AutoReconnectEngine, and Home Assistant.

## Key Components

1. **FastAPI Lifespan Management**:
   - `lifespan(app)` initializes `BluetoothManager`, `AutoReconnectEngine`, and configuration store on server startup, and gracefully shuts them down upon SIGTERM.
2. **REST Endpoints**:
   - `/api/health`: Health status.
   - `/api/adapters`: Lists all HCI adapters and toggles power.
   - `/api/scan`: Start/stop discovery scanning.
   - `/api/devices`: List, pair, connect, disconnect, and remove devices.
   - `/api/settings`: Read/update persistent settings.
3. **WebSocket Event Gateway**:
   - Multi-client subscription model broadcasting device discovery, RSSI signals, and connection state transitions.
4. **Persistent JSON Storage**:
   - Saves custom speaker names, default adapter assignments, and auto-reconnect preferences.

---
*Research for Phase 5: FastAPI Backend Daemon & Real-Time Event Bus*
