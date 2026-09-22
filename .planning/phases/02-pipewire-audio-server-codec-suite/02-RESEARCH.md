# Phase 2: PipeWire Audio Server & Codec Suite - Research

**Phase:** 2 (PipeWire Audio Server & Codec Suite)
**Researched:** 2026-09-21
**Confidence:** HIGH

## Overview

Phase 2 builds the low-latency audio processing graph for BL-HAOS using PipeWire and WirePlumber.
The core deliverables are:
1. S6-Overlay longrun service definitions for PipeWire (`10-pipewire`) and WirePlumber (`20-wireplumber`) with strict dependency ordering on `00-init-environment`.
2. PipeWire core configuration (`pipewire.conf.d/`) optimizing clock rate, quantum, and buffer constraints (`default.clock.rate = 48000`, `default.clock.quantum = 1024`, `min-quantum = 512`, `max-quantum = 2048`, `resample.quality = 4`).
3. WirePlumber Bluetooth monitoring configuration (`wireplumber.conf.d/` / SPA JSON) enabling `libspa-0.2-bluetooth`, AVRCP hardware volume synchronization (`bluez5.enable-volume-sync = true`, `bluez5.enable-hw-volume = true`), and codec priority ranking:
   - Audiophile order: `ldac`, `aptx_hd`, `aptx`, `aac`, `sbc_xq`, `sbc`.
4. Python verification script and test suite parsing PipeWire/WirePlumber configuration files, checking syntax validity, and verifying S6 service dependency topology.

## Configuration Schemas & Reference Architecture

### PipeWire Configuration (`rootfs/etc/pipewire/pipewire.conf.d/10-clock.conf`)

```spa-json
context.properties = {
    default.clock.rate = 48000
    default.clock.quantum = 1024
    default.clock.min-quantum = 512
    default.clock.max-quantum = 2048
}

context.modules = [
    {
        name = libpipewire-module-rt
        args = {
            nice.level = -11
            rt.prio = 88
        }
        flags = [ ifexists nofail ]
    }
]
```

### WirePlumber Bluetooth Configuration (`rootfs/etc/wireplumber/wireplumber.conf.d/50-bluez.conf`)

```spa-json
monitor.bluez.properties = {
    bluez5.enable-sbc-xq = true
    bluez5.enable-volume-sync = true
    bluez5.enable-hw-volume = true
    bluez5.codecs = [ ldac aptx_hd aptx aac sbc_xq sbc ]
    bluez5.default.rate = 48000
}

monitor.bluez.rules = [
    {
        matches = [
            {
                device.name = "~bluez_card.*"
            }
        ]
        actions = {
            update-props = {
                bluez5.auto-connect = [ a2dp_sink ]
                bluez5.hw-volume = [ a2dp_sink ]
            }
        }
    }
]
```

## S6 Service Layout

1. `/etc/s6-overlay/s6-rc.d/10-pipewire`:
   - `type`: `longrun`
   - `dependencies.d/00-init-environment`
   - `run`: starts `pipewire` under `PIPEWIRE_RUNTIME_DIR=/var/run/pipewire`
2. `/etc/s6-overlay/s6-rc.d/20-wireplumber`:
   - `type`: `longrun`
   - `dependencies.d/10-pipewire`
   - `run`: starts `wireplumber` under `PIPEWIRE_RUNTIME_DIR=/var/run/pipewire`
3. `/etc/s6-overlay/s6-rc.d/user/contents.d/10-pipewire`, `/etc/s6-overlay/s6-rc.d/user/contents.d/20-wireplumber`

## Validation Architecture

### Automated Verification Strategy
- **Configuration Parser**: Verify that all `.conf` files under `/etc/pipewire/` and `/etc/wireplumber/` are well-formed SPA-JSON/JSON5.
- **S6 Topology Tests**: Verify that `10-pipewire` and `20-wireplumber` have valid `run` scripts, `type=longrun`, and `dependencies.d` links.
- **Codec Priority & Quantum Tests**: Assert presence of `ldac`, `aptx_hd`, `aptx`, `aac`, `sbc_xq`, and `quantum = 1024`.

---
*Research for Phase 2: PipeWire Audio Server & Codec Suite*
