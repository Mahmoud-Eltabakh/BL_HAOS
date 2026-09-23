<!-- GSD:project-start source:PROJECT.md -->

## Project

**BL-HAOS (Bluetooth Audio Adapter for Home Assistant OS)**

BL-HAOS is a Home Assistant OS Add-on and audio adapter system that enables Home Assistant to stream media, TTS voice announcements, web radio, and synchronized multi-room music directly to Bluetooth speakers. It provides an intuitive Web Ingress UI for scanning, pairing, and managing multiple Bluetooth adapters and speakers, while exposing native `media_player` entities to Home Assistant.

**Core Value:** Effortless pairing, high-fidelity audio streaming, and seamless Home Assistant `media_player` playback to any Bluetooth speaker with rock-solid background auto-reconnection and multi-room synchronization.

### Constraints

- **Platform**: Home Assistant OS (HAOS) with Docker add-on specifications and Host D-Bus/Bluetooth passthrough.
- **Bluetooth Stack**: Linux BlueZ 5.x with PipeWire/WirePlumber SPA Bluetooth plugins.
- **Resource Footprint**: Lightweight footprint suitable for Raspberry Pi 4/5 as well as x86_64 servers.

<!-- GSD:project-end -->

<!-- GSD:stack-start source:research/STACK.md -->

## Technology Stack

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
| Standalone HACS Integration / REST-WebSocket API | HA Core 2024.x+ | Entity Registration | Exposes trusted connected Bluetooth speakers as native `media_player` entities through an authenticated local bridge |

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
| Standalone HACS Integration | Bundled custom component | The separate integration is independently versioned, configured through a config entry, and does not require an add-on write mount |

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| PulseAudio 14/15 legacy stack | Broken codec negotiation with newer Bluetooth 5.x speakers and poor multi-adapter routing | PipeWire with WirePlumber |
| Direct raw ALSA hardware locks | Only one application can access the audio stream at a time, preventing multi-room and concurrent mixing | PipeWire audio server |
| Blocking Python `dbus-python` | Blocks async event loops during Bluetooth discovery scans and pairing handshakes | `dbus-fast` (pure async asyncio D-Bus) |

## Sources

- PipeWire Official Documentation & Bluetooth SPA Architecture
- Home Assistant Developer Docs (Add-on development, Ingress specification, config entries, and media player entities)
- BlueZ Linux Bluetooth Subsystem DBus API Specification (`org.bluez.Adapter1`, `org.bluez.Device1`, `org.bluez.Media1`)

<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->

## Conventions

- **Home Assistant Developer Docs**: Always consult official Home Assistant developer documentation first at `https://developers.home-assistant.io/` for all add-on specifications (`config.yaml`, Ingress, S6-overlay, D-Bus permissions), config-entry schemas, and supervisor APIs.
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->

## Architecture

Architecture not yet mapped. Follow existing patterns found in the codebase.
<!-- GSD:architecture-end -->

<!-- GSD:skills-start source:skills/ -->

## Project Skills

No project skills found. Add skills to any of: `.claude/skills/`, `.agents/skills/`, `.cursor/skills/`, `.github/skills/`, or `.codex/skills/` with a `SKILL.md` index file.
<!-- GSD:skills-end -->

<!-- GSD:workflow-start source:GSD defaults -->

## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:

- `$gsd-quick` for small fixes, doc updates, and ad-hoc tasks
- `$gsd-debug` for investigation and bug fixing
- `$gsd-execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->

<!-- GSD:profile-start -->

## Developer Profile

> Profile not yet configured. Run `$gsd-profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
