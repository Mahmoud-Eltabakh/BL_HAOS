# Production-Level Readiness Research

## Goal

Raise BL-HAOS from a functionally capable Bluetooth audio platform to a production-grade Home Assistant add-on by improving reliability, operational honesty, security, and release confidence.

## Why this milestone matters

The project already demonstrates the core feature set: Bluetooth pairing, PipeWire playback, HA entity integration, reconnect logic, and multi-room support. The next decisive gap is not feature breadth; it is the runtime quality bar that determines whether a user can trust the system under real-world conditions.

## Production quality bar

A production-grade BL-HAOS system should:

- report truthful runtime health instead of assuming everything is healthy
- degrade safely when BlueZ, PipeWire, or a sink is unavailable
- recover predictably from stale device and D-Bus transient failures
- validate all user-controlled inputs before privileged execution
- provide enough diagnostics for support to reason about failures quickly
- pass release-level regression checks before shipping

## Reference lessons from Sendspin Bluetooth Bridge

The linked Sendspin BT Bridge demonstrates several production practices worth importing without importing its Music Assistant/Sendspin product dependency:

- explicit startup and shutdown lifecycle events with progress status
- canonical diagnostics and telemetry endpoints
- versioned API, event, and subprocess contracts
- isolated per-speaker playback and recovery boundaries
- guided onboarding and recovery actions
- redacted support-bundle export
- deterministic demo mode for UI and support validation
- pinned dependencies, CVE rationale, and stable/preview release policy
- reproducible multi-platform deployment and release evidence

These practices are now release-blocking requirements for BL-HAOS.

## Workstreams

1. Runtime stability, lifecycle contracts, and degraded-mode handling
2. Security, dependency governance, and safe execution boundaries
3. Diagnostics, guided recovery, support bundles, and deterministic demo mode
4. Release quality gates, compatibility policy, and regression evidence

## Key risk areas

- silent failure when Bluetooth or PipeWire is partially unavailable
- reconnect loops that hide stale-state errors
- unsafe command execution without strict payload validation
- support scenarios where the app fails without enough evidence to diagnose it
- release drift caused by a lack of explicit quality gates
- duplicate reconnect workers or unbounded subprocess failure propagation
- support data that is either too sparse to diagnose or too broad to export safely

## Success condition

The milestone is successful when the app can be trusted under real-world reconnect, auth, failure, and degraded-mode scenarios; lifecycle and runtime contracts are observable; support can recover common failures without SSH; and every release has repeatable evidence from build, upgrade, rollback, and regression gates.
