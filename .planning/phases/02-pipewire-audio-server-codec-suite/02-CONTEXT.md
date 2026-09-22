# Phase 2: PipeWire Audio Server & Codec Suite - Context

**Gathered:** 2026-09-21
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 2 delivers the PipeWire and WirePlumber audio server infrastructure configured for low-latency, high-fidelity Bluetooth A2DP audio streaming:
- PipeWire daemon configuration with SPA Bluetooth plugin (`libspa-0.2-bluetooth`).
- WirePlumber session manager configuration for Bluetooth codec priority (LDAC, aptX HD, aptX, AAC, SBC-XQ, SBC) and auto-negotiation.
- PipeWire buffer quantum and clock tuning (`default.clock.quantum = 1024`) for low-latency voice and jitter-free music streaming.
- AVRCP hardware and software volume synchronization (`bluez5.enable-volume-sync = true`) with perceptual volume curves.
- S6-rc v3 longrun service definitions for PipeWire (`10-pipewire`) and WirePlumber (`20-wireplumber`) with explicit dependency chaining on `00-init-environment`.
- Automated test suites verifying configuration syntax, codec priority matrices, and S6 service topology.

</domain>

<decisions>
## Implementation Decisions

### Audio Daemon Topology & Supervision
- **D-01:** Supervise PipeWire and WirePlumber as dedicated S6-rc longrun services:
  - `10-pipewire` (type: `longrun`, depends on `00-init-environment`)
  - `20-wireplumber` (type: `longrun`, depends on `10-pipewire`)
  Both run under `XDG_RUNTIME_DIR=/var/run/pipewire` and `PIPEWIRE_RUNTIME_DIR=/var/run/pipewire`. — **Reversibility:** costly — changes to daemon supervision affect all downstream audio stream routing.

### Bluetooth Codec Priority & Auto-Negotiation
- **D-02:** WirePlumber Bluetooth policy prioritizes audiophile codecs descending by fidelity: `ldac`, `aptx_hd`, `aptx`, `aac`, `sbc_xq`, `sbc`. WirePlumber will auto-negotiate the highest mutual codec supported by both the adapter and the connected speaker, while honoring the add-on `default_codec` option when overridden by the user. — **Reversibility:** reversible — codec lists are configuration-driven.
- **D-03:** Enable high-bitrate SBC-XQ (e.g. Dual Channel HD mode) by default as the baseline fallback for non-proprietary Bluetooth devices. — **Reversibility:** reversible.

### Buffer Quantum, Latency & Audio Quality
- **D-04:** Set PipeWire clock parameters to `default.clock.rate = 48000`, `default.clock.quantum = 1024`, `default.clock.min-quantum = 512`, `default.clock.max-quantum = 2048`, and `resample.quality = 4`. This delivers ~21.3ms processing latency, making TTS chimes responsive while remaining resilient against 2.4GHz RF packet retransmissions. — **Reversibility:** reversible.

### Volume Control & AVRCP Synchronization
- **D-05:** Configure WirePlumber with `bluez5.enable-volume-sync = true` and `bluez5.enable-hw-volume = true`. When absolute volume is supported by the speaker (via AVRCP), physical button presses on the speaker will immediately update the PipeWire sink volume (and vice versa for Home Assistant commands), mapped over a cubic perceptual volume curve. — **Reversibility:** reversible.

### Agent Discretion
- Exact configuration file naming under `/etc/pipewire/pipewire.conf.d/` and `/etc/wireplumber/wireplumber.conf.d/` (or WirePlumber Lua/SPA-JSON rules depending on WirePlumber 0.4/0.5 syntax).
- Python test fixtures and configuration validation helpers.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### PipeWire & WirePlumber Documentation
- `https://docs.pipewire.org/page_bluetooth.html` — PipeWire SPA Bluetooth architecture and codec configuration.
- `https://pipewire.pages.freedesktop.org/wireplumber/daemon-configuration.html` — WirePlumber configuration schema and BlueZ monitor settings.

### Home Assistant Developer Standards
- `https://developers.home-assistant.io/docs/add-ons/configuration` — Add-on permissions and S6-overlay conventions.

### Project Architecture & Requirements
- `.planning/PROJECT.md` — Project scope and constraints.
- `.planning/REQUIREMENTS.md` — Requirements `AUD-01`, `AUD-02`, `AUD-03`, `AUD-04`.
- `.planning/phases/01-add-on-foundation-container-blueprint/01-VERIFICATION.md` — Phase 1 container foundation.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `rootfs/etc/s6-overlay/s6-rc.d/00-init-environment` creates `/var/run/pipewire` and `/var/run/user/0` on container bootstrap.
- `Dockerfile` installs `pipewire`, `pipewire-audio-client-libraries`, `pipewire-pulse`, `wireplumber`, `libspa-0.2-bluetooth`, `libfdk-aac2`, `libfreeaptx0`, and `libldacbt-enc2`.

### Established Patterns
- S6-rc services use `dependencies.d/` directory links for ordering.
- Pytest test suite in `tests/` tests configuration files and schema validation.

### Integration Points
- `/var/run/pipewire/pipewire-0` — PipeWire UNIX socket used by WirePlumber, Snapcast clients, and Python audio controllers.
- Host D-Bus (`/var/run/dbus/system_bus_socket`) — Used by PipeWire SPA Bluetooth module to register endpoints with BlueZ.
</code_context>
