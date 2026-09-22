# Architecture Research

**Domain:** Home Assistant OS Bluetooth Audio Adapter & Multi-Room Add-on
**Researched:** 2026-09-21
**Confidence:** HIGH

## Standard Architecture

### System Overview

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                             Home Assistant Frontend & Core                        │
│   • Lovelace Media Cards  • Automations / Scripts  • Voice TTS (Piper/Cloud)     │
└──────────────────────────┬────────────────────────────┬──────────────────────────┘
                           │ Ingress Web UI (HTTP/WS)   │ MQTT / Home Assistant API
┌──────────────────────────▼────────────────────────────▼──────────────────────────┐
│                         BL-HAOS Add-on Container Layer                           │
├──────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────┐     ┌────────────────────────────────────────────┐  │
│  │   Ingress Web Dashboard │     │         FastAPI Backend Daemon             │  │
│  │  (Scan / Pair / Volume) │◄───►│  • BlueZ Manager  • Auto-Reconnect Engine   │  │
│  │                         │     │  • HA Bridge API  • Snapcast Sync Manager  │  │
│  └─────────────────────────┘     └──────┬──────────────────────┬──────────────┘  │
│                                         │                      │                 │
│  ┌──────────────────────────────────────▼──────┐   ┌───────────▼──────────────┐  │
│  │        PipeWire & WirePlumber Audio         │   │   Snapcast Audio Server  │  │
│  │   • SPA Bluetooth Plugin (SBC, AAC, LDAC)   │◄──┤   • Multi-room Streamer  │  │
│  │   • Virtual Media Sinks & Audio Graph       │   │   • Sample-Accurate Sync │  │
│  └───────────────────┬─────────────────────────┘   └──────────────────────────┘  │
│                      │ D-Bus / Audio PCM                                         │
├──────────────────────┴───────────────────────────────────────────────────────────┤
│                             Host Operating System (HAOS)                         │
├──────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────┐  ┌───────────────────────────────────────────────┐  │
│  │  Host BlueZ Subsystem   │  │  Bluetooth HCI Controllers                    │  │
│  │  (/var/run/dbus/system) │◄─┤  • hci0 (Onboard BT)  • hci1..N (USB Dongles) │  │
│  └─────────────────────────┘  └───────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Responsibility | Implementation Details |
|-----------|----------------|------------------------|
| **FastAPI Backend Daemon** | Core controller coordinating D-Bus BlueZ events, managing speaker connection states, executing background auto-reconnection, and providing REST/WS endpoints for UI and HA | Python 3.11+, `dbus-fast`, `asyncio`, Uvicorn |
| **Ingress Web UI** | Visual management dashboard embedded in HA for scanning devices, entering pairing PINs, assigning adapters, managing speaker groups, and adjusting volumes | React/Vite + Tailwind CSS / Lit elements |
| **PipeWire + WirePlumber** | Low-latency audio processing graph, Bluetooth A2DP encoding with hardware AVRCP volume sync, and dynamic sink lifecycle | PipeWire 1.0+, WirePlumber 0.5+, `libspa-0.2-bluetooth` |
| **Snapcast Engine** | Multi-room streaming server (`snapserver`) feeding synchronized audio to internal and external `snapclient` instances routing to individual Bluetooth sinks | Snapcast 0.28+ native C++ binaries |
| **Home Assistant Bridge** | Publishes MQTT Discovery packets for each active speaker, creating Home Assistant `media_player` entities that accept play/pause/TTS/volume commands | Async MQTT client / HA REST & WebSocket API |

## Recommended Project Structure

```
BL-HAOS/
├── build.yaml                 # Home Assistant Add-on build manifest
├── config.yaml                # Home Assistant Add-on configuration & permissions schema
├── Dockerfile                 # Multi-arch Debian Bookworm base with PipeWire, BlueZ, Snapcast
├── rootfs/
│   ├── etc/
│   │   ├── pipewire/          # PipeWire & WirePlumber audio profiles
│   │   │   ├── pipewire.conf.d/
│   │   │   └── wireplumber.conf.d/
│   │   ├── s6-overlay/        # S6 supervision scripts for background daemons
│   │   │   └── s6-rc.d/
│   │   │       ├── 00-dbus/
│   │   │       ├── 10-pipewire/
│   │   │       ├── 20-wireplumber/
│   │   │       ├── 30-snapserver/
│   │   │       └── 40-bl-haos-daemon/
│   │   └── snapcast/
│   └── usr/
│       └── bin/
├── backend/                   # Python FastAPI service
│   ├── bl_haos/
│   │   ├── bluetooth/         # BlueZ D-Bus manager, scanning, pairing, adapter enumeration
│   │   ├── audio/             # PipeWire node management, volume control, codec query
│   │   ├── multiroom/         # Snapcast server/client lifecycle and speaker grouping
│   │   ├── ha/                # Home Assistant MQTT discovery and entity bridge
│   │   ├── api/               # REST API & WebSocket endpoints for UI
│   │   ├── config.py          # Persistent speaker & adapter settings store
│   │   └── main.py            # Async application entrypoint & background tasks
│   ├── requirements.txt
│   └── tests/
├── frontend/                  # React / Vite Web Dashboard for Ingress
│   ├── src/
│   │   ├── components/        # SpeakerCard, AdapterSelector, ScanModal, VolumeSlider
│   │   ├── hooks/             # WebSocket real-time connection state hooks
│   │   ├── api/               # Client API calls
│   │   └── App.tsx
│   ├── package.json
│   └── vite.config.ts
└── .planning/                 # Project governance & roadmap
```

## Architectural Patterns

### Pattern 1: Event-Driven Bluetooth State Machine (D-Bus ObjectManager)

**What:** Listen asynchronously to BlueZ `org.freedesktop.DBus.ObjectManager.InterfacesAdded` and `PropertiesChanged` events to maintain a real-time reactive state model of all adapters and connected speakers without polling.

**Benefits:** Instant UI feedback on connection state, zero lag when a speaker powers on/off, low CPU overhead.

### Pattern 2: Virtual Audio Graph Routing with WirePlumber

**What:** Dynamically spawn dedicated PipeWire virtual audio sinks (`sink.media`, `sink.tts`, `sink.snapcast`) and connect them via WirePlumber policy to the physical Bluetooth A2DP sinks.

**Benefits:** Allows stream priority mixing (e.g. ducking music when TTS plays) and individual per-speaker routing without lockups.

### Pattern 3: Self-Healing Auto-Reconnect Loop

**What:** When a trusted speaker disconnects, transition its state to `DISCONNECTED` and arm an exponential backoff probe timer that tests adapter visibility and reconnects the A2DP profile (`org.bluez.Device1.Connect`) as soon as the device advertises.

---
*Architecture research for: Home Assistant OS Bluetooth Audio Adapter*
*Researched: 2026-09-21*
