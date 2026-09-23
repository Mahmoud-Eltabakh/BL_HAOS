# BL-HAOS (Bluetooth Audio Adapter for Home Assistant OS)

## Milestone Goal

### Production-Level Readiness

This milestone brings BL-HAOS from a feature-complete Bluetooth audio platform to a production-ready Home Assistant add-on. The focus is reliability, safe degraded-mode operation, strong runtime observability, explicit security boundaries, and repeatable release quality gates.

## What This Is

BL-HAOS is a Home Assistant OS Add-on and audio adapter system that enables Home Assistant to stream media, TTS voice announcements, web radio, and synchronized multi-room music directly to Bluetooth speakers. It provides a Web Ingress UI, a native Home Assistant integration, and a resilient backend runtime that safely manages BlueZ, PipeWire, and Snapcast interactions.

## Core Value

Effortless pairing, high-fidelity audio streaming, and seamless Home Assistant `media_player` playback to any Bluetooth speaker with rock-solid background auto-reconnection, safe degraded-mode behavior, and production-grade operational visibility.

## Requirements

### Validated

- [x] **Home Assistant Add-on Core**: Supervisor-compatible Docker add-on container packaging PipeWire, WirePlumber, BlueZ, and Snapcast.
- [x] **Dynamic Web Ingress UI**: Home Assistant sidebar Ingress interface to scan for nearby Bluetooth devices, initiate pairing/PIN auth, trust, connect, and view signal/connection telemetry.
- [x] **Multi-Adapter Support**: Simultaneous management of onboard Bluetooth controllers and external USB dongles with flexible adapter-to-speaker routing.
- [x] **High-Fidelity Codec Suite**: Support for SBC, SBC-XQ, AAC, aptX, aptX HD, and LDAC audio codecs with low-latency tuning.
- [x] **Native Home Assistant Media Player**: Automatic exposure of connected Bluetooth speakers as standard Home Assistant `media_player` entities for TTS, local media browser, and web radio playback.
- [x] **Multi-Room & Synchronized Playback**: Snapcast integration enabling grouped and sample-synchronized playback across multiple Bluetooth speakers and standard Snapcast clients.
- [x] **Aggressive Auto-Reconnect Engine**: Background daemon actively monitoring speaker presence, connection state, and restoring links when speakers wake from standby or re-enter range.
- [x] **Volume & Audio Control**: Per-speaker software volume normalization, hardware volume sync (AVRCP), and mute controls.
- [x] **Native Media Player Bridge**: A bundled Home Assistant custom integration that uses the add-on REST/WebSocket API as its primary control plane and exposes connected speakers as native `media_player` entities.
- [x] **Automated Deep Testing Pipeline**: Docker Compose stack that launches an isolated HAOS VM-in-Docker alongside test runners (Pytest, Playwright) and mocked Bluetooth layers for deep, end-to-end integration testing.
- [x] **CI & Local Execution**: Pipeline can run headlessly in CI and interactively on local developer environments for debugging.

### Active

- [ ] **Production Health Model**: Define explicit runtime health states for Bluetooth, PipeWire, Snapcast, HA bridge, and each tracked speaker, including degraded and unavailable states.
- [ ] **Resilient Reconnect & Recovery**: Harden auto-reconnect to handle stale BlueZ objects, transient signal loss, and sink unavailability without silent degradation.
- [ ] **Safe Input & Security Hardening**: Validate all device addresses, URLs, payloads, and auth flows before privileged operations execute.
- [ ] **Supportability & Observability**: Surface structured diagnostics, failure reasons, and per-subscriber health endpoints for troubleshooting in production.
- [ ] **Release Quality Gates**: Establish explicit regression, smoke, and rollout checks for Home Assistant add-on releases.
- [ ] **Runtime Contracts**: Publish lifecycle progress, versioned event/API contracts, and bounded failure classifications that other components and operators can trust.
- [ ] **Operator Recovery**: Provide guided recovery actions, redacted support bundles, and a deterministic demo mode for support and development.

### Out of Scope

- **Microphone / HFP Voice Satellite Input**: V1 focuses strictly on A2DP audio playback sinks; two-way voice assistant microphone input remains deferred.
- **Custom Hardware Firmware**: BL-HAOS runs on standard Home Assistant OS supported hosts with standard Linux Bluetooth controllers.

## Context

- **Home Assistant OS Environment**: HA OS runs containerized workloads managed by the Supervisor. System-level audio and Bluetooth control requires host D-Bus access (`/var/run/dbus`) and privileged access to Bluetooth hardware.
- **Modern Audio Stack**: PipeWire and WirePlumber provide native, modular Bluetooth A2DP sink support with codec negotiation and dynamic routing, superior to legacy bluez-alsa or PulseAudio setups.
- **Ecosystem Compatibility**: Works seamlessly with Home Assistant's native TTS engines, media streaming, and Music Assistant.
- **Production Goal**: Build lasting trust through predictable runtime behavior, verifiable states, safe failures, and strong operational diagnostics.

## Constraints

- **Platform**: Home Assistant OS (HAOS) with Docker add-on specifications and Host D-Bus/Bluetooth passthrough.
- **Bluetooth Stack**: Linux BlueZ 5.x with PipeWire/WirePlumber SPA Bluetooth plugins.
- **Resource Footprint**: Lightweight footprint suitable for Raspberry Pi 4/5 as well as x86_64 servers.
- **Documentation Standard**: In every step, consult the official Home Assistant developer documentation first (`https://developers.home-assistant.io/`) for add-on architecture, schema, ingress, permissions, and entity discovery.
- **Production Bar**: Stability, safety, and observability must exceed feature capability before release.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| HA Developer Docs Priority | Ensure all schemas, permissions, add-on manifests, and APIs strictly follow official HA developer guidelines (`https://developers.home-assistant.io/`) | Accepted |
| Home Assistant Add-on with Ingress | Allows containerized low-level D-Bus/PipeWire audio control on HAOS without modifying the host OS, with seamless UI integration | Accepted |
| PipeWire + WirePlumber Audio Backend | Modern, low-latency, modular audio engine with built-in codec support and audio routing | Accepted |
| Snapcast for Multi-Room Sync | Proven open-source protocol for sample-accurate multi-room audio synchronization across multiple endpoints | Accepted |
| Dynamic Ingress Web UI | Eliminates manual MAC address configuration in YAML, allowing non-technical users to discover and pair speakers visually | Accepted |
| Aggressive Background Reconnection | Overcomes Bluetooth speaker auto-sleep/idle timeouts by continuously monitoring and restoring link states | Accepted |
| Production-First Hardening | Reliability and observability are more important than adding extra feature surface before the runtime is stable | Accepted |
| Degraded-Mode Safety | The system must remain honest about missing dependencies rather than falsely reporting healthy runtime state | Accepted |
| Security by Validation | All user-controlled inputs and commands must be validated before privileged operations execute | Accepted |
| Sendspin Operational Lessons | Adopt explicit lifecycle contracts, versioned runtime boundaries, operator recovery, deterministic demo validation, and release evidence from the Sendspin BT Bridge project without taking on its Music Assistant dependency | Accepted |
| Native HA Product Boundary | BL-HAOS remains a native Home Assistant media-player platform; Sendspin is an engineering reference, not a required transport or product dependency | Accepted |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition**:
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone**:
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-09-23 for the Production-Level Readiness milestone, refined with Sendspin operational lessons*
