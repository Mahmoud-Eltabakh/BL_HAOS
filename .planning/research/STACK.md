# Stack Research

**Domain:** Home Assistant OS Bluetooth Audio Adapter & Multi-Room Add-on
**Researched:** 2026-09-21
**Confidence:** HIGH

## Recommended Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| Home Assistant Add-on Base (Debian Bookworm) | 12 / Bookworm | Base Container OS | Superior package availability for PipeWire 1.0+, WirePlumber, BlueZ 5.66+, and proprietary codec libraries compared to Alpine |
| PipeWire & WirePlumber | 1.0+ / 0.5+ | Audio Server & Session Manager | Modern, modular audio graph manager. Built-in SPA Bluetooth plugin provides native A2DP sink support, hardware volume sync (AVRCP), and dynamic codec switching |
| BlueZ | 5.66+ | Bluetooth Protocol Stack | Linux standard Bluetooth subsystem communicating via Host D-Bus (`/var/run/dbus`) to discover, pair, trust, and manage RFCOMM/A2DP links |
| Snapcast | 0.28+ (snapserver & snapclient) | Multi-Room Audio Synchronization | Sample-accurate multi-room audio streaming engine over WiFi/LAN with PipeWire sink routing |
| Python / FastAPI + Uvicorn | 3.11+ / 0.110+ | Backend Daemon & HA Gateway | Lightweight, high-performance async daemon managing D-Bus Bluetooth signals, state machine, REST API, and WebSocket event bus |
| Frontend Web UI (Ingress) | React 18+ or Lit 3.0 / Tailwind CSS | Ingress Web Dashboard | HA-themed responsive UI embedded directly inside Home Assistant sidebar via Ingress |
| Home Assistant MQTT Discovery / WebSocket API | HA Core 2024.x+ | Entity Registration | Exposes connected Bluetooth speakers as native `media_player` entities without requiring custom component restarts |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `dbus-fast` | 2.22+ | High-speed Async D-Bus Client | Python async interface to BlueZ ObjectManager (`org.bluez`), adapter scanning, and device properties |
| `pydantic` | 2.6+ | Data Validation & Settings Schemas | Speaker profiles, adapter assignments, connection states, and add-on configuration validation |
| `libspa-0.2-bluetooth` | 1.0+ | PipeWire Bluetooth Audio Plugin | Handles SBC, SBC-XQ, AAC, aptX, aptX HD, and LDAC encoding directly in the audio pipeline |
| `libfdk-aac` / `libfreeaptx` / `libldac` | Latest | High-Fidelity Audio Codecs | Required for hardware-level high-quality Bluetooth streaming |
| `avahi-daemon` / mDNS | Latest | Local Service Discovery | Zero-conf discovery for Snapcast and local network audio streams |

### Development & Operational Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| `pw-cli` / `pw-top` / `wpctl` | PipeWire diagnostics and inspect audio graph | Real-time monitoring of active audio nodes, stream formats, and latency |
| `bluetoothctl` / `btmon` | Low-level Bluetooth debug CLI | Inspecting HCI packets, pairing requests, and adapter states |
| Docker / HA Add-on Testing Framework | Local add-on build and verification | Build multi-arch images (`aarch64`, `amd64`, `armv7`) with QEMU |

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| PipeWire + WirePlumber | `bluez-alsa` (ALSA directly to BlueZ) | `bluez-alsa` is ultra-lightweight but lacks dynamic multi-stream mixing, software volume curve normalization, and multi-endpoint routing |
| PipeWire | PulseAudio (legacy `pulseaudio-module-bluetooth`) | PulseAudio has higher latency, erratic A2DP codec negotiation on newer Linux kernels, and is being superseded across Linux distributions |
| MQTT Auto-Discovery | Custom Integration (HACS) only | MQTT Discovery creates instant `media_player` entities with zero custom component installation needed; hybrid HACS integration can optionally enhance UI cards later |

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| PulseAudio 14/15 legacy stack | Broken codec negotiation with newer Bluetooth 5.x speakers and poor multi-adapter routing | PipeWire with WirePlumber |
| Direct raw ALSA hardware locks | Only one application can access the audio stream at a time, preventing multi-room and concurrent mixing | PipeWire audio server |
| Blocking Python `dbus-python` | Blocks async event loops during Bluetooth discovery scans and pairing handshakes | `dbus-fast` (pure async asyncio D-Bus) |

## Sources

- PipeWire Official Documentation & Bluetooth SPA Architecture
- Home Assistant Developer Docs (Add-on development, Ingress specification, MQTT Discovery for media_player)
- BlueZ Linux Bluetooth Subsystem DBus API Specification (`org.bluez.Adapter1`, `org.bluez.Device1`, `org.bluez.Media1`)

---
*Stack research for: Home Assistant OS Bluetooth Audio Adapter*
*Researched: 2026-09-21*
