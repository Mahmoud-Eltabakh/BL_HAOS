# Phase 1: Add-on Foundation & Container Blueprint - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-09-21
**Phase:** 01-add-on-foundation-container-blueprint
**Areas discussed:** Container Base & Supervision, Permissions & Manifest Schema, D-Bus Diagnostics & Testing Strategy

---

## Container Base & Supervision

| Option | Description | Selected |
|--------|-------------|----------|
| Debian 12 Bookworm + S6-Overlay v3 | Standard Home Assistant base container with full PipeWire, BlueZ, Snapcast, and Python 3.11+ package support | ✓ |
| Alpine Linux Base | Minimal footprint but lacks native pre-built packages for PipeWire Bluetooth SPA codecs and Snapcast | |

**User's choice:** Debian 12 Bookworm + S6-Overlay v3
**Notes:** Selected for robust ecosystem package support required by modern Linux audio stacks and BlueZ.

---

## Permissions & Manifest Schema

| Option | Description | Selected |
|--------|-------------|----------|
| Official Home Assistant Developer Schema (`config.yaml`) | Full compliance with `https://developers.home-assistant.io/docs/add-ons/configuration` including `host_dbus: true`, `full_access: true`, `udev: true`, `ingress: true` | ✓ |
| Custom / Minimal schema | Unofficial schema format | |

**User's choice:** Official Home Assistant Developer Schema (`config.yaml`)
**Notes:** Strictly aligned with Home Assistant developer standards as requested.

---

## D-Bus Diagnostics & Testing Strategy

| Option | Description | Selected |
|--------|-------------|----------|
| Standalone `bl-haos-probe` with mockable test modes | Standalone Python probe returning structured JSON telemetry, with mock fallbacks for headless CI/tests | ✓ |
| Raw shell script inline | Simple bash check without structured JSON reporting | |

**User's choice:** Standalone `bl-haos-probe` with mockable test modes
**Notes:** Ensures automated pytest test suites can validate behavior in virtualized environments.

---

## Agent Discretion

- Internal runtime directories structure (`/var/run/pipewire`, `/var/run/user/0`, `/var/run/snapcast`).
- Pytest test organization and fixtures.

## Deferred Ideas

- None.
