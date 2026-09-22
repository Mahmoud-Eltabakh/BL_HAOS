# BL-HAOS (Bluetooth Audio Adapter for Home Assistant OS)

## What This Is

BL-HAOS is a Home Assistant OS Add-on and audio adapter system that enables Home Assistant to stream media, TTS voice announcements, web radio, and synchronized multi-room music directly to Bluetooth speakers. It provides an Ingress UI for Bluetooth management and a native Home Assistant integration that exposes speakers as `media_player` entities.

## Core Value

Effortless pairing, high-fidelity audio streaming, and seamless Home Assistant `media_player` playback to any Bluetooth speaker with rock-solid background auto-reconnection and multi-room synchronization.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] **Home Assistant Add-on Core**: Supervisor-compatible Docker add-on container packaging PipeWire, WirePlumber, BlueZ, and Snapcast.
- [ ] **Dynamic Web Ingress UI**: Home Assistant sidebar Ingress interface to scan for nearby Bluetooth devices, initiate pairing/PIN auth, trust, connect, and view signal/connection telemetry.
- [ ] **Multi-Adapter Support**: Simultaneous management of onboard Bluetooth controllers and external USB dongles with flexible adapter-to-speaker routing.
- [ ] **High-Fidelity Codec Suite**: Support for SBC, SBC-XQ, AAC, aptX, aptX HD, and LDAC audio codecs with low-latency tuning.
- [ ] **Native Home Assistant Media Player**: Automatic exposure of connected Bluetooth speakers as standard Home Assistant `media_player` entities for TTS, local media browser, and web radio playback.
- [ ] **Multi-Room & Synchronized Playback**: Snapcast integration enabling grouped and sample-synchronized playback across multiple Bluetooth speakers and standard Snapcast clients.
- [ ] **Aggressive Auto-Reconnect Engine**: Background daemon actively monitoring speaker presence, connection state, and instantly restoring connections when speakers wake from standby or re-enter range.
- [ ] **Volume & Audio Control**: Per-speaker software volume normalization, hardware volume sync (AVRCP), and mute controls.
- [ ] **Native Media Player Bridge**: A bundled Home Assistant custom integration that uses the add-on REST/WebSocket API as its primary control plane and exposes connected speakers as native `media_player` entities.

### Out of Scope

- **Microphone / HFP Voice Satellite Input**: V1 focuses strictly on A2DP audio playback sinks; two-way voice assistant satellite microphone input is deferred to future milestones.
- **Custom Hardware Firmware**: BL-HAOS runs directly on standard Home Assistant OS supported hosts (Raspberry Pi, x86 Mini PCs, NUCs) with standard Linux Bluetooth controllers.

## Context

- **Home Assistant OS Environment**: HA OS runs containerized workloads managed by the Supervisor. System-level audio and Bluetooth control requires host D-Bus access (`/var/run/dbus`) and privileged access to Bluetooth hardware.
- **Modern Audio Stack**: PipeWire and WirePlumber provide native, modular Bluetooth A2DP sink support with codec negotiation and dynamic routing, superior to legacy bluez-alsa or PulseAudio setups.
- **Ecosystem Compatibility**: Works seamlessly with Home Assistant's native TTS engines (Piper, Cloud TTS), media streaming, and Music Assistant.

## Constraints

- **Platform**: Home Assistant OS (HAOS) with Docker add-on specifications and Host D-Bus/Bluetooth passthrough.
- **Bluetooth Stack**: Linux BlueZ 5.x with PipeWire/WirePlumber SPA Bluetooth plugins.
- **Resource Footprint**: Lightweight footprint suitable for Raspberry Pi 4/5 as well as x86_64 servers.
- **Documentation Standard**: In every step, consult the official Home Assistant developer documentation first (`https://developers.home-assistant.io/`) for add-on architecture, schema, ingress, permissions, and entity discovery.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| HA Developer Docs Priority | Ensure all schemas, permissions, add-on manifests, and APIs strictly follow official HA developer guidelines (`https://developers.home-assistant.io/`) | — Pending |
| Home Assistant Add-on with Ingress | Allows containerized low-level D-Bus/PipeWire audio control on HAOS without modifying the host OS, with seamless UI integration | — Pending |
| PipeWire + WirePlumber Audio Backend | Modern, low-latency, modular audio engine with built-in high-quality Bluetooth codec support (SBC-XQ, AAC, aptX, LDAC) | — Pending |
| Snapcast for Multi-Room Sync | Proven open-source protocol for sample-accurate multi-room audio synchronization across multiple endpoints | — Pending |
| Dynamic Ingress Web UI | Eliminates manual MAC address configuration in YAML, allowing non-technical users to discover and pair speakers visually | — Pending |
| Aggressive Background Reconnection | Overcomes Bluetooth speaker auto-sleep/idle timeouts by continuously monitoring and restoring link states | — Pending |
| Native Integration over MQTT Discovery | Current Home Assistant Core does not support MQTT `media_player` discovery; MQTT remains optional interoperability transport, not the primary entity bridge | Accepted |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `$gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `$gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-09-22 for Native Media Player Bridge milestone*
