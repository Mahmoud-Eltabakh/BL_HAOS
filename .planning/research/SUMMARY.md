# Project Research Summary

**Project:** BL-HAOS (Bluetooth Audio Adapter for Home Assistant OS)
**Domain:** Home Assistant OS Add-on, Linux Bluetooth Subsystem (BlueZ), PipeWire Audio Graph & Multi-Room Sync (Snapcast)
**Researched:** 2026-09-21
**Confidence:** HIGH

## Executive Summary

BL-HAOS delivers a containerized Bluetooth audio and multi-room broadcasting solution tailored specifically for Home Assistant OS (HAOS). Running as a managed Home Assistant Add-on, it bridges the host's Linux BlueZ Bluetooth subsystem to a PipeWire audio server and Snapcast multi-room distribution pipeline. This allows Home Assistant users to stream TTS announcements, music, and web radio to any Bluetooth speaker with low latency, audiophile-grade codecs (AAC, aptX, LDAC, SBC-XQ), and rock-solid background reconnection.

The architecture addresses common pitfalls of Linux Bluetooth audio by pairing asynchronous D-Bus communication (`dbus-fast`) with PipeWire's modern SPA Bluetooth architecture, completely eliminating legacy PulseAudio instabilities. An integrated Ingress Web Dashboard provides effortless device discovery, pairing, and volume management without requiring manual YAML configuration.

## Key Findings

### Recommended Stack

- **Base Container**: Debian 12 (Bookworm) with S6-Overlay for robust multi-daemon process management.
- **Audio Stack**: PipeWire 1.0+ and WirePlumber 0.5+ with `libspa-0.2-bluetooth` and codec libraries (`libfdk-aac`, `libfreeaptx`, `libldac`).
- **Bluetooth Control**: Linux BlueZ via Host System D-Bus socket (`/var/run/dbus/system_bus_socket`) using Python `dbus-fast`.
- **Backend Service**: Python 3.11+ / FastAPI with WebSockets for real-time state and REST APIs.
- **Frontend UI**: React + Vite + Tailwind CSS embedded inside Home Assistant sidebar via Ingress.
- **Multi-Room Synchronization**: Snapcast 0.28+ (Snapserver & Snapclients) routing directly into PipeWire Bluetooth sinks.
- **Home Assistant Gateway**: Automatic MQTT Discovery registering standard `media_player` entities for each paired speaker.

### Expected Features

**Must Have (Table Stakes):**
- Web Ingress UI for discovery, pairing, PIN entry, trusting, and connecting Bluetooth speakers.
- Standard Home Assistant `media_player` entity exposure for TTS, URL streaming, and media controls.
- Aggressive background auto-reconnect engine with exponential backoff for waking/sleeping speakers.
- Clean, jitter-free A2DP stereo playback.
- Hardware & software volume synchronization (AVRCP).

**Should Have (Differentiators):**
- Multi-Bluetooth adapter support (onboard + multiple USB dongles).
- High-fidelity audiophile codec negotiation (SBC-XQ, AAC, aptX, aptX HD, LDAC).
- Synchronized multi-room playback across multiple Bluetooth speakers via Snapcast.
- Real-time RSSI signal strength monitoring and connection telemetry.

**Defer (v2+):**
- HFP/HSP two-way microphone voice satellite input (to avoid degrading music playback quality).
- Per-speaker parametric equalizer and dynamic DSP filters.

### Architecture Approach

The system employs an event-driven design around the BlueZ D-Bus ObjectManager. The Python FastAPI backend tracks adapter/speaker states asynchronously. When a speaker is connected, PipeWire dynamically creates an A2DP sink node, while the HA Bridge publishes MQTT Discovery definitions to create Home Assistant `media_player` entities. For multi-room playback, Snapcast feeds synced streams to each speaker's virtual sink.

### Critical Pitfalls

1. **Host D-Bus Isolation**: Must declare `host_dbus: true`, `full_access: true`, and `udev: true` in `config.yaml` to communicate with host Bluetooth controllers.
2. **Audio Endpoint Conflicts**: Prevent multiple daemons from registering competing BlueZ endpoints; standardize entirely on PipeWire SPA Bluetooth.
3. **Reconnection Storms**: Use circuit breakers and exponential backoff to avoid freezing the Bluetooth adapter when speakers power down.
4. **HA Ingress Path Routing**: Use relative asset base paths (`./`) and dynamic WebSocket resolution to support HA Ingress proxying.

## Implications for Roadmap

### Suggested Phase Structure (Fine Granularity):

1. **Phase 1: Add-on Foundation & Container Blueprint**: Debian Bookworm container setup, S6-overlay supervision, HA add-on manifest (`config.yaml`), host D-Bus, and audio permissions.
2. **Phase 2: PipeWire & WirePlumber Audio Stack**: PipeWire daemon configuration, SPA Bluetooth plugins, audiophile codec support (AAC, aptX, LDAC), and audio test pipelines.
3. **Phase 3: BlueZ D-Bus Manager & Device Controller**: Asynchronous Python Bluetooth client using `dbus-fast` for adapter enumeration, device scanning, pairing, and trust management.
4. **Phase 4: Aggressive Auto-Reconnect & Health Daemon**: Background state machine with presence detection, link monitoring, and auto-reconnection for sleeping speakers.
5. **Phase 5: FastAPI Backend & Real-Time Event Bus**: REST API and WebSocket gateway providing control, telemetry, and status endpoints.
6. **Phase 6: Ingress Web Dashboard UI**: Responsive, HA-themed React/Vite dashboard embedded via Ingress for visual scan, pair, connect, and speaker management.
7. **Phase 7: Home Assistant Media Player Bridge**: MQTT Discovery and API bridge creating native HA `media_player` entities for TTS and streaming audio.
8. **Phase 8: Multi-Room Synchronization (Snapcast)**: Integrated Snapserver/Snapclient pipeline enabling sample-synchronized multi-speaker playback.
9. **Phase 9: Multi-Adapter Routing & Audio Polish**: Adapter-to-speaker assignment, AVRCP volume sync, and latency calibration.
10. **Phase 10: End-to-End Verification & HAOS Packaging**: Full system validation, release packaging, documentation, and installation testing.

### Sources

- PipeWire Official Documentation & SPA Bluetooth Architecture
- Home Assistant Add-on Developer Guidelines
- BlueZ D-Bus API Specification
- Snapcast Multi-room Audio Architecture

---
*Summary for: Home Assistant OS Bluetooth Audio Adapter*
*Researched: 2026-09-21*
