# Roadmap: BL-HAOS

## Overview

BL-HAOS builds a robust, audiophile-grade Bluetooth audio streaming and multi-room broadcasting system packaged as a native Home Assistant OS Add-on. The development journey proceeds from the low-level container and host D-Bus foundation up through the PipeWire audio engine, BlueZ Bluetooth controller, auto-reconnection daemon, FastAPI backend, Ingress UI, Home Assistant `media_player` bridge, and Snapcast multi-room synchronization.

## Phases

- [x] **Phase 1: Add-on Foundation & Container Blueprint** - Establish the Debian Bookworm container, S6-Overlay supervision, add-on manifest (`config.yaml`), and verify host D-Bus / hardware access.
- [x] **Phase 2: PipeWire Audio Server & Codec Suite** - Configure PipeWire and WirePlumber with SPA Bluetooth plugin, audiophile codecs (SBC-XQ, AAC, aptX, LDAC), and AVRCP volume sync.
- [x] **Phase 3: BlueZ D-Bus Bluetooth Controller** - Implement async Python BlueZ controller (`dbus-fast`) for scanning, PIN/SSP pairing, trusting, and multi-adapter management.
- [x] **Phase 4: Aggressive Auto-Reconnect Engine** - Implement background connection health monitoring with exponential backoff and circuit breaker for waking speakers.
- [x] **Phase 5: FastAPI Backend Daemon & Real-Time Event Bus** - Build the central Python daemon with REST APIs, WebSocket live event bus, and persistent JSON configuration store.
- [x] **Phase 6: Ingress Web Dashboard UI** - Create a responsive Home Assistant Ingress web dashboard (React/Vite) for visual device discovery, pairing, and speaker management.
- [x] **Phase 7: Home Assistant Media Player Integration** - Implement MQTT Discovery bridge automatically exposing speakers as native HA `media_player` entities for TTS and streaming.
- [x] **Phase 8: Multi-Room Synchronization with Snapcast** - Integrate Snapcast server and dynamic client pipelines to enable sample-accurate multi-speaker synchronized playback.
- [x] **Phase 9: Native Integration Foundation** - Replace unsupported MQTT `media_player` discovery with a bundled Home Assistant integration and direct add-on transport contract.
- [x] **Phase 10: Native Player Control & State Sync** - Implement direct media commands, playback URL resolution, and resilient entity state synchronization.
- [ ] **Phase 11: Migration & Live Verification** - Retire the unsupported discovery path, expose diagnostics, and verify real speaker playback on HAOS.

## Phase Details

### Phase 1: Add-on Foundation & Container Blueprint
**Goal**: Package the core add-on environment with Debian Bookworm, S6-Overlay multi-process supervisor, and verified host D-Bus / Bluetooth hardware access.
**Depends on**: Nothing (first phase)
**Requirements**: SYS-01, SYS-02, SYS-03
**Success Criteria** (what must be TRUE):
  1. Add-on builds cleanly as a multi-arch container and starts under Home Assistant Supervisor.
  2. Container successfully establishes communication with the host system D-Bus socket (`/var/run/dbus/system_bus_socket`).
  3. Startup self-check verifies Bluetooth hardware privileges and logs available host HCI controllers.
**Plans**: 2 plans

Plans:
- [ ] 01-01: Container base Dockerfile, build.yaml, and S6-Overlay supervision scaffold
- [ ] 01-02: Home Assistant add-on config.yaml schema and D-Bus bootstrap validation script

---

### Phase 2: PipeWire Audio Server & Codec Suite
**Goal**: Deploy PipeWire and WirePlumber configured with SPA Bluetooth plugin, high-resolution audio codecs, and AVRCP hardware volume control.
**Depends on**: Phase 1
**Requirements**: AUD-01, AUD-02, AUD-03, AUD-04
**Success Criteria** (what must be TRUE):
  1. PipeWire and WirePlumber daemons run stably under S6-Overlay inside the container.
  2. SPA Bluetooth module successfully negotiates high-bitrate codecs (SBC-XQ, AAC, aptX, LDAC) when connected to compatible speakers.
  3. PipeWire buffer quantum is tuned for low latency without buffer underruns over 2.4GHz RF.
  4. Volume adjustments synchronize bidirectionally with speaker hardware via AVRCP.
**Plans**: 2 plans

Plans:
- [ ] 02-01: PipeWire and WirePlumber configuration profiles and SPA Bluetooth codec integration
- [ ] 02-02: Audio buffer optimization, virtual sink routing, and AVRCP volume sync handlers

---

### Phase 3: BlueZ D-Bus Bluetooth Controller
**Goal**: Build an async Python controller using `dbus-fast` to discover devices, execute PIN/SSP pairing, maintain trust, and manage multiple Bluetooth adapters.
**Depends on**: Phase 1
**Requirements**: BT-01, BT-02, BT-03, BT-04
**Success Criteria** (what must be TRUE):
  1. Asynchronous scan discovers nearby Bluetooth audio devices and reports live RSSI signal values.
  2. Interactive pairing supports both PIN authentication and numeric comparison / SSP confirmation.
  3. Paired and trusted devices persist in BlueZ and reconnect across container restarts.
  4. Multiple Bluetooth adapters (`hci0`, `hci1`, etc.) can be enumerated and independently selected.
**Plans**: 2 plans

Plans:
- [ ] 03-01: Asynchronous BlueZ D-Bus client (`dbus-fast`), adapter manager, and discovery scanner
- [ ] 03-02: Interactive PIN/SSP pairing agent, trust storage, and multi-adapter binding logic

---

### Phase 4: Aggressive Auto-Reconnect Engine
**Goal**: Create a background daemon that monitors connection health and aggressively restores connections when speakers wake from standby or enter range.
**Depends on**: Phase 3
**Requirements**: CONN-01, CONN-02, CONN-03
**Success Criteria** (what must be TRUE):
  1. Daemon receives real-time D-Bus property change signals when speaker link state changes.
  2. Reconnection loop executes exponential backoff with jitter when a speaker goes offline.
  3. Circuit breaker stops reconnection loops after persistent failures to avoid freezing the host Bluetooth adapter.
**Plans**: 1 plan

Plans:
- [ ] 04-01: Reconnection state machine, exponential backoff scheduler, and adapter circuit breaker

---

### Phase 5: FastAPI Backend Daemon & Real-Time Event Bus
**Goal**: Develop the central async Python backend service exposing REST endpoints and WebSocket live event streaming.
**Depends on**: Phase 2, Phase 3, Phase 4
**Requirements**: API-01, API-02, API-03
**Success Criteria** (what must be TRUE):
  1. REST API endpoints allow listing adapters, initiating scans, pairing devices, and toggling connections.
  2. WebSocket stream broadcasts real-time device discovery events, RSSI updates, and audio telemetry.
  3. Configuration store reliably saves speaker aliases, assigned adapters, and custom volume levels.
**Plans**: 2 plans

Plans:
- [ ] 05-01: FastAPI application setup, REST route handlers, and Pydantic configuration schemas
- [ ] 05-02: WebSocket connection manager and real-time Bluetooth/Audio event broadcaster

---

### Phase 6: Ingress Web Dashboard UI
**Goal**: Build a responsive React/Vite web dashboard embedded in Home Assistant sidebar via Ingress for complete visual speaker management.
**Depends on**: Phase 5
**Requirements**: UI-01, UI-02, UI-03, UI-04
**Success Criteria** (what must be TRUE):
  1. Dashboard loads smoothly inside Home Assistant Ingress with relative path routing.
  2. Discovery modal displays nearby speakers with live RSSI meters and one-click pairing.
  3. Speaker cards show connection state, active codec, assigned adapter, and volume sliders.
  4. Settings panel allows configuring multi-adapter routing and multi-room groups.
**Plans**: 2 plans

Plans:
- [ ] 06-01: Frontend project scaffolding (React, Vite, Tailwind CSS) with HA Ingress compatibility
- [ ] 06-02: Discovery scanner modal, speaker management cards, volume controls, and WebSocket hook

---

### Phase 7: Home Assistant Media Player Integration
**Goal**: Automatically publish MQTT Discovery payloads to create native Home Assistant `media_player` entities for TTS, local media, and web radio.
**Depends on**: Phase 2, Phase 5
**Requirements**: HA-01, HA-02, HA-03, HA-04
**Success Criteria** (what must be TRUE):
  1. Connecting a Bluetooth speaker automatically registers a `media_player` entity in Home Assistant.
  2. Playing TTS announcements in Home Assistant plays clean voice audio on the physical speaker.
  3. Web radio streams and Home Assistant media browser files stream reliably.
  4. Volume and playback state changes in Home Assistant immediately reflect on the physical speaker.
**Plans**: 2 plans

Plans:
- [ ] 07-01: MQTT Discovery bridge and media_player schema definitions
- [ ] 07-02: Audio streaming pipeline handler for TTS, web radio URLs, and state synchronization

---

### Phase 8: Multi-Room Synchronization with Snapcast
**Goal**: Integrate Snapcast server and dynamic client pipelines to enable sample-accurate multi-speaker synchronized audio streaming.
**Depends on**: Phase 2, Phase 7
**Requirements**: SYNC-01, SYNC-02, SYNC-03
**Success Criteria** (what must be TRUE):
  1. Snapserver runs inside the add-on container and accepts audio streams from Home Assistant and Music Assistant.
  2. Individual Snapclients stream synchronized audio to multiple Bluetooth speaker PipeWire sinks.
  3. Users can group speakers together and adjust per-speaker latency offsets to achieve perfect acoustic sync.
**Plans**: 2 plans

Plans:
- [ ] 08-01: Snapserver daemon integration and PipeWire sink bridge configuration
- [ ] 08-02: Dynamic multi-speaker grouping, Snapclient lifecycle manager, and latency calibration

---

### Phase 9: Native Integration Foundation
**Goal**: Ship a native Home Assistant integration that can discover BL-HAOS speakers and communicate with the add-on without using MQTT media-player discovery.
**Depends on**: Phase 5
**Requirements**: NMP-01, NMP-02, NMP-03, NMP-04
**Success Criteria**:
  1. Starting the add-on makes the bundled integration available without replacing unrelated Home Assistant configuration.
  2. Home Assistant can configure one BL-HAOS integration entry and identify the running add-on through a supported local contract.
  3. A connected trusted speaker appears as a native `media_player` with a stable identity.
**Plans**: 2 plans

Plans:
- [x] 09-01-PLAN.md — Install the bundled component safely and configure one validated native integration entry
- [x] 09-02-PLAN.md — Bridge trusted speaker inventory and state to native Home Assistant entities over REST/WebSocket

---

### Phase 10: Native Player Control & State Sync
**Goal**: Make native speaker entities control real playback and accurately represent add-on, Bluetooth, and reconnect state.
**Depends on**: Phase 9
**Requirements**: NMP-05, NMP-06, NMP-07
**Success Criteria**:
  1. Play, pause, stop, media URL, and volume commands reach the selected add-on speaker.
  2. The entity reports current playback, volume, and availability from authoritative add-on events.
  3. The entity recovers after either Home Assistant or the speaker reconnects.
**Plans**: 2 plans

Plans:
- [x] 10-01-PLAN.md — Execute authenticated native playback controls and route decoded media into the selected PipeWire A2DP sink
- [x] 10-02-PLAN.md — Resolve Home Assistant media sources and restore authoritative state after transport and speaker recovery

---

### Phase 11: Migration & Live Verification
**Goal**: Remove the unsupported entity-discovery dependency and prove native speaker control works on the live HAOS host.
**Depends on**: Phase 10
**Requirements**: MIG-01, MIG-02, MIG-03
**Success Criteria**:
  1. MQTT remains optional and no longer gates the presence of native `media_player` entities.
  2. Ingress and diagnostics clearly report native-integration readiness and transport failures.
  3. The live Logitech Bluetooth adapter appears as a media player and completes a real playback command.
**Plans**: 2 plans

  Plans:
  - [ ] 11-01-PLAN.md — Retire MQTT discovery, preserve opt-in interoperability, and expose redacted native diagnostics
  - [ ] 11-02-PLAN.md — Safely migrate the live HAOS integration and verify Logitech native media playback

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 10 → 11

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Add-on Foundation & Container Blueprint | 2/2 | Complete | 2026-09-21 |
| 2. PipeWire Audio Server & Codec Suite | 2/2 | Complete | 2026-09-21 |
| 3. BlueZ D-Bus Bluetooth Controller | 2/2 | Complete | 2026-09-21 |
| 4. Aggressive Auto-Reconnect Engine | 1/1 | Complete | 2026-09-21 |
| 5. FastAPI Backend Daemon & Real-Time Event Bus | 2/2 | Complete | 2026-09-21 |
| 6. Ingress Web Dashboard UI | 2/2 | Complete | 2026-09-21 |
| 7. Home Assistant Media Player Integration | 2/2 | Complete | 2026-09-21 |
| 8. Multi-Room Synchronization with Snapcast | 2/2 | Complete | 2026-09-21 |
| 9. Native Integration Foundation | 2/2 | Complete | 2026-09-22 |
| 10. Native Player Control & State Sync | 2/2 | Complete | 2026-09-22 |
| 11. Migration & Live Verification | 0/2 | Planned | - |
