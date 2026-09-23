# Phase 17-01 Research

## Existing runtime evidence

- `BluetoothManager` owns the D-Bus connection, adapter/device caches, object-manager signals, and one-shot stale-device refresh in `connect_device`. Its `_initialized` flag is set even when D-Bus connection fails, so it cannot currently distinguish ready from degraded startup.
- `DeviceInfo.connected` is the only canonical-looking speaker availability field. `AutoReconnectEngine` separately tracks `idle`, `connected`, `reconnecting`, `backoff`, and `circuit_broken`, but these states are not published as a shared health contract.
- `AutoReconnectEngine` creates a new reconnect task from each eligible tick and protects adapter work with locks; the profile itself has no in-flight task ownership or explicit unavailable state. Repeated failures invoke stale-device removal/pairing recovery, but failure reasons are log text only.
- `MediaPlayerBridge` resolves PipeWire sinks with `pw-dump` at playback time and reports a single string error when an A2DP sink is absent. It has no dependency health snapshot and no way to distinguish PipeWire unavailable from a missing speaker sink.
- `MultiroomManager` models Snapcast clients in memory and uses the configured default group, but it does not probe or report Snapserver readiness.
- `main.py` wires startup/shutdown, BlueZ events, reconnect, native bridge, and multi-room behavior. Startup logs readiness after `BluetoothManager.initialize()` even if D-Bus was unavailable; shutdown has no lifecycle event contract.
- `api/routes.py` exposes `/api/health` and sanitized native diagnostics, but `/api/health` always returns `status=ok` and only reports counts plus whether a bus object exists. `api/ws.py` already provides the event bus required for versioned health events.

## Audio/runtime boundaries

- PipeWire runs as s6 service `10-pipewire`, with runtime sockets under `/var/run/pipewire`; WirePlumber service `20-wireplumber` waits for `pipewire-0` before starting.
- WirePlumber enables A2DP codecs and auto-connects A2DP sinks through `50-bluez.lua`. A healthy PipeWire process alone does not prove that a speaker sink exists.
- Snapserver runs as s6 service `30-snapserver`, creates `/tmp/snapcast/snapfifo`, and uses `/etc/snapcast/snapserver.conf` with TCP 1705, stream 1704, and a FIFO-backed default stream. A configured FIFO is not proof that Snapserver is accepting clients or that the sink path is usable.
- Existing tests assert these service/config contracts textually, so the health design should consume these boundaries rather than rewrite them.

## Existing test seams and commands

- Focused bridge tests live under `modules/bridge/tests` and already cover API health, D-Bus object events, stale BlueZ refresh, reconnect backoff/circuit behavior, PipeWire s6 wiring, and Snapserver config.
- The established module invocation is `python -m pytest ... -q`; the prior focused orchestration contract command was `python -m pytest tests/integration/tests/test_orchestration.py -q`.
- Planned health tests should be dependency-injected SIL tests, not host-dependent subprocess or Bluetooth tests. Full bridge regression remains `python -m pytest modules/bridge/tests/ -q` after the new tests are added.

## Proposed contract shape

- `HealthState`: component lifecycle/readiness enum with `starting`, `healthy`, `degraded`, `unavailable`, `stopping`, `stopped`, `unknown`.
- `SpeakerState`: `unknown`, `connected`, `disconnected`, `reconnecting`, `unavailable`.
- `FailureClass`: stable enum covering the D-03 taxonomy, with safe bounded detail and timestamps/attempt metadata in snapshots.
- `HealthSnapshot`: contract version, aggregate add-on state, component records for `bluetooth`, `pipewire`, `snapcast`, and `native_bridge`, speaker records keyed by normalized address, lifecycle phase, and bounded last failure.
- Aggregate precedence must be deterministic and documented: unavailable required dependencies outrank degraded dependencies, and component failure must prevent an overall healthy result.

## Failure classification matrix

| Condition | Classification | Component/state outcome | Recovery expectation |
|---|---|---|---|
| System D-Bus connect/introspection cannot complete | `dbus_unavailable` | Bluetooth unavailable; add-on degraded/unavailable | Retry/reinitialize without discarding safe snapshot |
| D-Bus transport drops after initialization | `dbus_disconnected` | Bluetooth degraded/unavailable; affected speakers unavailable or reconnecting | Reconnect bus and reload managed objects |
| Cached BlueZ path/method is no longer valid | `stale_bluez_object` | Speaker reconnecting/unavailable; cache entry invalidated | Refresh object once, then bounded stale recovery |
| PipeWire runtime/socket or `pw-dump` probe fails | `pipewire_unavailable` | PipeWire unavailable; sink-dependent playback unavailable | Keep control/API alive and report dependency failure |
| PipeWire responds but no matching A2DP sink exists | `sink_missing` | Speaker unavailable/degraded; playback blocked | Reconnect speaker and republish state |
| Snapserver/FIFO/client path is unavailable | `snapcast_unavailable` | Snapcast degraded/unavailable; Bluetooth playback may remain independent | Keep core bridge usable and report multi-room degradation |
| Reconnect attempts hit configured limit/circuit break | `reconnect_exhausted` | Speaker unavailable, not silently disconnected | Preserve failure and wait for explicit/periodic recovery |
| Any required startup step fails | `startup_failed` | Lifecycle failed/degraded; no false ready event | Publish bounded progress/failure event |
| Shutdown cleanup/task cancellation cannot complete | `shutdown_incomplete` | Lifecycle stopping with failure details | Continue bounded cleanup and publish completion outcome |

## Package legitimacy audit

No package installation or dependency change is required by this phase. The plan uses existing repository dependencies and standard-library/asyncio subprocess probes only.

## Risks and constraints

- Do not expose native tokens, raw D-Bus object payloads, media URLs, or unbounded exception text in health snapshots.
- Avoid making a transient missing sink indistinguishable from a missing BlueZ adapter; the classification must identify the failing boundary.
- Keep existing API consumers compatible while versioning new health/event fields.
- Health probes must be injectable and bounded so SIL tests do not require live HAOS, D-Bus, Bluetooth hardware, PipeWire, or Snapcast.
