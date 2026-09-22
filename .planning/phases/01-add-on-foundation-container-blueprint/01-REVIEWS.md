---
phase: "01"
reviewers: [adversarial-plan-review]
reviewed_at: "2026-09-21T12:00:00Z"
plans_reviewed:
  - 01-01-PLAN.md
  - 01-02-PLAN.md
models:
  adversarial-plan-review: "Gemini 3.7 Flash"
model_sources:
  adversarial-plan-review: "runtime"
---

# Cross-AI Plan Review — Phase 01: Add-on Foundation & Container Blueprint

<!-- gsd:plan-revision-conflicts:begin -->
## Plan-Revision Conflicts
None.
<!-- gsd:plan-revision-conflicts:end -->

## 01-01

### Summary
Plan `01-01` covers the container foundation and multi-process supervision architecture. It defines the multi-architecture Debian 12 Bookworm base image in `Dockerfile` and `build.yaml`, and implements the S6-Overlay v3 service layout with the oneshot `00-init-environment` service. The design correctly isolates container setup, prepares runtime directories for PipeWire and Snapcast, and verifies structure through automated pytest suites.

### Strengths
- **Multi-Arch Compliance** ([build.yaml:1-5](build.yaml#L1-L5)): Declares official `ghcr.io/home-assistant/{arch}-base-debian:bookworm` base images covering `aarch64`, `amd64`, and `armv7`, meeting HAOS multi-architecture deployment standards.
- **Dependency Completeness** ([Dockerfile:7-25](Dockerfile#L7-L25)): Installs all necessary system packages in a single cached layer, including BlueZ, PipeWire, WirePlumber, SPA Bluetooth plugins, Snapcast, and proprietary codec packages (`libfdk-aac2`, `libfreeaptx0`, `libldacbt-enc2`).
- **S6-rc v3 Architecture** ([rootfs/etc/s6-overlay/s6-rc.d/00-init-environment/type](rootfs/etc/s6-overlay/s6-rc.d/00-init-environment/type)): Correctly declares service type as `oneshot` and creates prerequisite runtime directories with strict permissions (`/var/run/pipewire`, `/var/run/user/0`, `/var/run/snapcast`) in [rootfs/etc/s6-overlay/s6-rc.d/00-init-environment/up:8-10](rootfs/etc/s6-overlay/s6-rc.d/00-init-environment/up#L8-L10).
- **Automated Verification** ([tests/test_dockerfile.py:4-22](tests/test_dockerfile.py#L4-L22), [tests/test_s6_structure.py:3-16](tests/test_s6_structure.py#L3-L16)): Pytest tests ensure no missing packages or broken bundle links during future refactoring.

### Concerns
- **LOW** — Package Availability on Specific Debian Architectures ([Dockerfile:22-24](Dockerfile#L22-L24)): `libfreeaptx0` and `libldacbt-enc2` may require Debian `non-free-firmware` or `contrib` component repositories enabled on certain ARM architectures (e.g. `armv7`).
- **LOW** — Ephemeral `/tmp` Snapcast Buffer ([rootfs/etc/s6-overlay/s6-rc.d/00-init-environment/up:8](rootfs/etc/s6-overlay/s6-rc.d/00-init-environment/up#L8)): Creating `/tmp/snapcast` on startup is fine, but Snapcast FIFO named pipes in Phase 8 should ensure proper write-lock permissions if non-root user switching is introduced.

### Suggestions
- In Phase 2, verify PipeWire SPA codec discovery when building on `armv7` architecture in CI.
- Ensure S6 longrun daemon service definitions in upcoming phases (PipeWire, FastAPI, Snapserver) define explicit dependency chains on `00-init-environment` via `dependencies` files.

### Risk Assessment
- **Overall Risk:** LOW. The container blueprint is lean, follows official Home Assistant Debian base guidelines, and passes automated structural tests.

---

## 01-02

### Summary
Plan `01-02` specifies the Home Assistant add-on configuration manifest (`config.yaml`) and implements the startup D-Bus / Bluetooth controller hardware audit script (`bl-haos-probe`). The plan ensures strict adherence to Home Assistant developer standards and provides a mockable diagnostic interface for continuous automated testing.

### Strengths
- **HAOS Developer Schema Alignment** ([config.yaml:1-21](config.yaml#L1-L21)): Declares `init: false` (mandatory for S6-Overlay v3), `ingress: true` with port `8099`, `host_dbus: true` for host BlueZ access, `full_access: true`, and `udev: true` for dynamic USB Bluetooth dongle detection.
- **Resilient D-Bus Probing** ([rootfs/usr/bin/bl-haos-probe:31-72](rootfs/usr/bin/bl-haos-probe#L31-L72)): Implements robust fallback checking for `/var/run/dbus/system_bus_socket`, structured JSON output formatting, and environment variable override `BL_HAOS_MOCK_PROBE` for headless CI/CD environments.
- **Complete Test Coverage** ([tests/test_addon_config.py:4-21](tests/test_addon_config.py#L4-L21), [tests/test_dbus_probe.py:15-28](tests/test_dbus_probe.py#L15-L28)): Automated tests validate YAML syntax against mandatory HAOS add-on keys and verify mock mode behavior.

### Concerns
- **MEDIUM** — Host D-Bus Permission Failures on Core/Container Installs ([rootfs/usr/bin/bl-haos-probe:35-42](rootfs/usr/bin/bl-haos-probe#L35-L42)): If a user runs BL-HAOS outside of HAOS (e.g. Home Assistant Supervised on unsupported Linux distributions), the system D-Bus socket path might differ or have restrictive AppArmor profiles. The probe should provide clear troubleshooting messages indicating that `host_dbus: true` is active.
- **LOW** — Synchronous Import in Probe Script ([rootfs/usr/bin/bl-haos-probe:45-56](rootfs/usr/bin/bl-haos-probe#L45-L56)): The lazy import of `dbus_fast` inside `probe_bluetooth_adapters` handles missing packages gracefully, but full BlueZ object introspection in Phase 3 should transition to the core `bl_haos.bluetooth` async manager.

### Suggestions
- Add a `--json` and `--verbose` CLI flag to `bl-haos-probe` to facilitate both machine-readable output for the future Ingress backend and human-readable logs in the Home Assistant add-on log panel.
- Ensure Phase 3 reuses the probe's D-Bus validation logic when initializing the persistent `dbus-fast` ObjectManager connection.

### Risk Assessment
- **Overall Risk:** LOW. The manifest configuration and diagnostic probe strictly adhere to official Home Assistant guidelines and allow seamless offline testing.

---

## Consensus Summary

### Agreed Strengths
1. **Developer Docs Compliance**: Strict alignment with `https://developers.home-assistant.io/docs/add-ons/configuration` for S6-overlay v3 (`init: false`), Ingress, and host D-Bus passthrough.
2. **Deterministic Testability**: Full pytest test suite ensuring that container specs, manifest schemas, and D-Bus probe fallbacks are tested and pass in virtualized development environments.
3. **Modular Process Architecture**: Clean separation between oneshot environment initialization and downstream daemon lifecycles.

### Agreed Concerns
1. **Dynamic D-Bus / BlueZ State Evolution**: As Phase 3 introduces live BlueZ device discovery and pairing, error handling must account for adapter resets and absent Bluetooth controllers without crashing the container.
2. **S6 Dependency Chaining**: Ensure that all upcoming services (PipeWire in Phase 2, FastAPI in Phase 5, Snapcast in Phase 8) properly declare S6 dependencies so daemons start in strict deterministic order.

### Recommendations for Phase 2
- When creating PipeWire and WirePlumber S6 services in Phase 2, define `dependencies.d/00-init-environment` to guarantee runtime directory readiness before audio daemons spawn.
- Tune PipeWire audio buffer parameters (`default.clock.quantum = 1024` or `2048`) specifically for Bluetooth A2DP stability over 2.4GHz RF.
