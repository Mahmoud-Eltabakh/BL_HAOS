# Feature Research

**Domain:** Home Assistant OS Bluetooth Audio Adapter & Multi-Room Add-on
**Researched:** 2026-09-21
**Confidence:** HIGH

## Feature Landscape

### Table Stakes (Users Expect These)

Features users assume exist. Missing these = product feels incomplete or broken.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Web UI Discovery & Pairing | Users need a visual way to scan, discover, authenticate, and pair speakers without CLI commands | MEDIUM | Web Ingress UI showing RSSI, device name, MAC address, and pairing status |
| Home Assistant `media_player` Entity | Standard entity for playing TTS, radio streams, local audio files, and automations | MEDIUM | Auto-registered via MQTT Discovery or native HA API |
| Aggressive Auto-Reconnect | Bluetooth speakers power down or sleep when idle; reconnection must happen automatically upon waking | HIGH | Persistent background loop with exponential backoff and BlueZ D-Bus state change hooks |
| Audio Playback (A2DP Sink) | Stream clean, jitter-free stereo audio to paired speakers | MEDIUM | PipeWire + BlueZ SPA Bluetooth audio graph |
| Volume Control & Sync | Adjusting volume in HA updates the speaker, and pressing buttons on speaker updates HA (AVRCP) | MEDIUM | PipeWire volume node binding + AVRCP profile tracking |
| Playback Controls (Play/Pause/Stop) | Media player state controls in Lovelace cards | LOW | Standard media_player control pipeline |

### Differentiators (Competitive Advantage)

Features that set the product apart. Not required, but provide immense user value.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Multi-Adapter Routing | Utilize multiple USB Bluetooth dongles to stream to different speakers without adapter contention | HIGH | BlueZ multi-HCI binding (`hci0`, `hci1`, etc.) mapped to specific audio sinks |
| Sample-Synchronized Multi-Room (Snapcast) | Group multiple Bluetooth speakers (and other Snapcast clients) for perfectly synced whole-home audio | HIGH | Integrated Snapserver + Snapclient instances forwarding to PipeWire Bluetooth sinks |
| Audiophile Codec Negotiation (SBC-XQ, AAC, aptX, LDAC) | High-resolution streaming with selectable bitrate and codec preferences in UI | MEDIUM | PipeWire WirePlumber Bluetooth configuration profiles |
| TTS Audio Ducking & Priority Stream | Lowers background music volume when a voice alert or doorbell chime is triggered | MEDIUM | PipeWire audio filter / stream priority policy |
| Signal Quality & RSSI Telemetry | Visual indicator of Bluetooth signal strength and connection health in the Ingress UI | LOW | Polled from BlueZ D-Bus RSSI properties |

### Anti-Features (Commonly Requested, Often Problematic)

Features that seem good on paper but create severe stability or usability problems.

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| Bidirectional HFP Microphone Input in v1 | Users ask for two-way voice communication for HA voice satellites | HFP/HSP forces 8kHz/16kHz mono audio codec, drastically degrading music quality and causing BlueZ audio profile flipping instabilities | Focus on crystal-clear A2DP stereo playback in v1; use dedicated ESPHome/S3 micro-satellites for microphones |
| Raw Linux CLI-only Configuration | Easy for developer to build quickly | Unusable for mainstream Home Assistant users on HAOS where host terminal access is restricted | Provide full Ingress Web UI with zero YAML requirement |
| Single Global Bluetooth Device Lock | Hardcoding one speaker in config | Limits scalability and breaks multi-room setups | Multi-device registry supporting dynamic add/remove |

## Feature Dependencies

```
[BlueZ D-Bus Adapter Controller]
    └──requires──> [PipeWire + WirePlumber Audio Server]
                       └──requires──> [Speaker Connection & Reconnect Engine]
                                          ├──enables──> [HA media_player Discovery]
                                          └──enables──> [Snapcast Multi-Room Sync]
```

## MVP Definition

### Launch With (v1)

- [ ] Add-on container with PipeWire, WirePlumber, and BlueZ integration
- [ ] Ingress Web Dashboard with device scanning, pairing, trusting, and connection state
- [ ] Multi-adapter detection and assignment
- [ ] Automatic HA `media_player` entity creation with TTS, URL stream, and volume controls
- [ ] High-fidelity codec support (SBC, SBC-XQ, AAC, aptX, LDAC)
- [ ] Aggressive background auto-reconnect engine
- [ ] Multi-speaker Snapcast synchronization for grouped playback

### Add After Validation (v1.x)

- [ ] Software DSP equalizer and per-speaker latency offset adjustment
- [ ] Automated TTS notification audio ducking
- [ ] Custom Lovelace UI card for Home Assistant dashboard

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| Web Ingress UI (Scan/Pair/Connect) | HIGH | MEDIUM | P1 |
| PipeWire Bluetooth A2DP Playback | HIGH | MEDIUM | P1 |
| Auto-reconnection Daemon | HIGH | MEDIUM | P1 |
| Home Assistant `media_player` Bridge | HIGH | MEDIUM | P1 |
| Multi-Adapter Support | HIGH | HIGH | P1 |
| Snapcast Multi-Room Synchronization | HIGH | HIGH | P1 |
| Audiophile Codec Selection | MEDIUM | MEDIUM | P1 |
| Latency Calibration & Equalizer | MEDIUM | MEDIUM | P2 |
| Audio Ducking Policy | MEDIUM | MEDIUM | P2 |

---
*Feature research for: Home Assistant OS Bluetooth Audio Adapter*
*Researched: 2026-09-21*
