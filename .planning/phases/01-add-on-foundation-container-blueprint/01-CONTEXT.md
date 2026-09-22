# Phase 1: Add-on Foundation & Container Blueprint - Context

**Gathered:** 2026-09-21
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 1 delivers the container foundation and Home Assistant OS Add-on blueprint:
- Multi-architecture Dockerfile based on Debian 12 Bookworm with S6-Overlay v3.
- Official Home Assistant Add-on manifest (`config.yaml`) and builder configuration (`build.yaml`).
- S6-rc service hierarchy for initialization and runtime directory preparation.
- Container startup D-Bus and Bluetooth hardware audit probe (`bl-haos-probe`) verifying host system bus access and enumerating Bluetooth controllers.

</domain>

<decisions>
## Implementation Decisions

### Container & Supervisor Base
- **D-01:** Use official `ghcr.io/home-assistant/{arch}-base-debian:bookworm` base image for standard multi-arch (`aarch64`, `amd64`, `armv7`) support and full package availability for PipeWire 1.0+, WirePlumber, BlueZ 5.66+, Snapcast, and Python 3.11+. — **Reversibility:** costly — changing base image requires rebuilding all package dependencies and service layouts.
- **D-02:** Use S6-Overlay v3 service architecture (`/etc/s6-overlay/s6-rc.d/`) with `init: false` in `config.yaml` as required by modern Home Assistant add-on guidelines. — **Reversibility:** costly — S6-rc service layout drives all background daemon lifecycles.

### Add-on Permissions & Configuration Manifest
- **D-03:** Manifest `config.yaml` strictly implements official Home Assistant Developer standards with `host_dbus: true`, `full_access: true`, `udev: true`, `ingress: true` on port 8099, and configurable `log_level` and `default_codec` options. — **Reversibility:** reversible — schema and options can be adjusted in YAML without breaking underlying code.
- **D-04:** Enforce official Home Assistant Developer Documentation (`https://developers.home-assistant.io/`) as the single source of truth for all metadata, ingress proxy headers, and supervisor communications. — **Reversibility:** one-way — foundational architecture standard across all phases.

### Startup Probe & D-Bus Diagnostics
- **D-05:** Implement `bl-haos-probe` as a standalone Python utility using `dbus-fast` that probes `/var/run/dbus/system_bus_socket`, checks `org.bluez` service availability, enumerates all HCI adapters (`hci0`, `hci1`, etc.), and returns formatted JSON diagnostic output with clear error guidance if D-Bus is unavailable. — **Reversibility:** reversible — modular standalone diagnostic script.
- **D-06:** Support mock/fallback mode in `bl-haos-probe` and test suites so automated CI tests pass reliably in container and virtualized test environments without physical Bluetooth hardware. — **Reversibility:** reversible.

### Agent Discretion
- Packaging details, temporary runtime directory structures (`/var/run/pipewire`, `/var/run/user/0`, `/var/run/snapcast`), and test scaffolding structure are left to the agent's technical discretion.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Home Assistant Developer Documentation
- `https://developers.home-assistant.io/docs/add-ons/configuration` — Official add-on `config.yaml` schema, permissions, hardware flags (`host_dbus`, `full_access`, `udev`), and ingress options.
- `https://developers.home-assistant.io/docs/add-ons/presentation` — Add-on presentation, icon guidelines, and repository metadata standards.
- `https://developers.home-assistant.io/docs/add-ons/testing` — Add-on local build and testing methodologies.

### BlueZ & D-Bus Documentation
- `https://git.kernel.org/pub/scm/bluetooth/bluez.git/tree/doc/adapter-api.txt` — BlueZ `org.bluez.Adapter1` D-Bus API specification.

### Project Architecture & Requirements
- `.planning/PROJECT.md` — BL-HAOS project context and constraints.
- `.planning/REQUIREMENTS.md` — v1 Requirements (SYS-01, SYS-02, SYS-03).
- `.planning/research/SUMMARY.md` — Executive summary and critical pitfalls.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- None (Greenfield project).

### Established Patterns
- All add-on metadata follows Home Assistant OS Add-on standard file structure (`config.yaml`, `build.yaml`, `Dockerfile`, `rootfs/`).
- Python scripts utilize `pytest` for unit testing with mocked D-Bus and filesystem layers.

### Integration Points
- `/var/run/dbus/system_bus_socket` — Mounted from host OS for BlueZ communication.
- `rootfs/etc/s6-overlay/s6-rc.d/` — Startup scripts managed by S6-Overlay v3.
- Ingress on port `8099` — Proxied by Home Assistant Supervisor for the web dashboard.
</code_context>
