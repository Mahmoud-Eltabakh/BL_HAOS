# Phase 1: Add-on Foundation & Container Blueprint - Research

**Phase:** 1 (Add-on Foundation & Container Blueprint)
**Researched:** 2026-09-21
**Confidence:** HIGH

## Overview

Phase 1 establishes the structural and container foundation for BL-HAOS as an official Home Assistant OS Add-on. The core deliverables are:
1. Dockerfile packaging Debian 12 Bookworm with S6-Overlay v3.
2. Home Assistant add-on metadata and configuration schema (`config.yaml`, `build.yaml`).
3. Multi-daemon supervisor services architecture under `/etc/s6-overlay/s6-rc.d/`.
4. Container startup environment validation script that probes the host system D-Bus socket (`/var/run/dbus/system_bus_socket`), tests BlueZ access, and verifies Bluetooth HCI controllers.

## Official Home Assistant Developer Documentation Alignment

References: `https://developers.home-assistant.io/docs/add-ons/configuration` and `https://developers.home-assistant.io/docs/add-ons/presentation`

### Key Manifest Configuration (`config.yaml`)

- `name`: "BL-HAOS Bluetooth Audio Adapter"
- `slug`: "bl_haos"
- `version`: "0.1.0"
- `description`: "High-fidelity Bluetooth audio streaming and multi-room adapter for Home Assistant OS"
- `url`: "https://github.com/melta/BL-HAOS"
- `arch`: `["aarch64", "amd64", "armv7"]`
- `init`: `false` (required when using S6-overlay v3)
- `ingress`: `true`
- `ingress_port`: `8099`
- `panel_icon`: `mdi:bluetooth-audio`
- `host_dbus`: `true` (enables host system D-Bus socket passthrough)
- `full_access`: `true` (enables required low-level device access)
- `udev`: `true` (enables kernel device event tracking for hotplugged USB dongles)
- `stage`: `experimental`

### Build Configuration (`build.yaml`)

```yaml
build_from:
  aarch64: "ghcr.io/home-assistant/aarch64-base-debian:bookworm"
  amd64: "ghcr.io/home-assistant/amd64-base-debian:bookworm"
  armv7: "ghcr.io/home-assistant/armv7-base-debian:bookworm"
```

## S6-Overlay Service Topology

Home Assistant Base Debian images incorporate S6-Overlay v3. We define services under `/etc/s6-overlay/s6-rc.d/`:

1. `00-init-environment` (type: `oneshot`):
   - Probes `/var/run/dbus/system_bus_socket`.
   - Runs startup hardware audit (`hciconfig` or `bluetoothctl list`).
   - Prepares runtime directories (`/var/run/pipewire`, `/var/run/user/0`, `/tmp/snapcast`).
2. `user/contents.d/`:
   - Enrolls `00-init-environment` into the default `user` bundle.

## Validation Architecture

### Automated Verification Strategy

1. **Schema Validation**: Validate `config.yaml` and `build.yaml` against Home Assistant Add-on schema using Python script and `yamllint`.
2. **Dockerfile & S6 Structure**: Lint Dockerfile with `hadolint` (or custom rule check) and verify all S6 service directories contain valid `type`, `up`, and executable `run` scripts.
3. **D-Bus & Hardware Self-Check Unit Test**: Python test suite mocking D-Bus socket presence and verifying graceful handling when D-Bus is connected vs disconnected.

---
*Research for Phase 1: Add-on Foundation & Container Blueprint*
