# Phase 17-01 Context

## Goal

Make runtime behavior deterministic under reconnect churn, stale BlueZ objects, and degraded dependencies by defining one canonical health contract that operators, the API, and the reconnect runtime can trust.

## Decisions

### D-01: One canonical aggregate health contract

Represent add-on, Bluetooth manager/BlueZ, PipeWire, Snapcast, HA/native bridge, and each tracked speaker through one versioned Pydantic health snapshot. Component health is aggregated from explicit observations rather than inferred from process startup or a single `connected` boolean.

### D-02: Separate component health from speaker connection state

Component states describe dependency readiness (`starting`, `healthy`, `degraded`, `unavailable`, `stopping`, `stopped`, `unknown`). Speaker states follow the required deterministic lifecycle (`unknown`, `connected`, `disconnected`, `reconnecting`, `unavailable`) and retain bounded transition/failure metadata.

### D-03: Stable machine-readable failure classifications

Every degraded or unavailable observation carries a bounded failure class and safe detail. The initial taxonomy must cover at least `dbus_unavailable`, `dbus_disconnected`, `stale_bluez_object`, `pipewire_unavailable`, `sink_missing`, `snapcast_unavailable`, `reconnect_exhausted`, `startup_failed`, and `shutdown_incomplete`. Free-form exception text is diagnostic context, not the contract identifier.

### D-04: Honest publication through existing control planes

Expose the canonical snapshot through the existing health/diagnostics API and publish versioned health events through the existing WebSocket bus. Keep native speaker records compatible while adding explicit availability/health information rather than silently converting dependency failure into `status=ok`.

### D-05: Preserve the current runtime stack

Use the existing Pydantic, asyncio, FastAPI, dbus-fast, PipeWire command probes, Snapcast configuration, and s6 service boundaries. Do not add a new runtime package or replace PipeWire/WirePlumber/Snapcast.

### D-06: Recovery is bounded and observable

Stale BlueZ cache refresh, transient D-Bus loss, missing PipeWire sinks, and reconnect exhaustion must result in explicit state transitions and classified events. Recovery attempts may continue in the background, but no path may report healthy while its required dependency is unavailable or leave a speaker silently stuck in a reconnect state.

## Boundaries

- Phase 17-01 defines and wires the health contract and degraded-mode behavior.
- Phase 17-02 will expand reconnect-loop hardening and stress/regression coverage using this contract.
- Phase 18 owns validation of user-controlled addresses, URLs, command payloads, and privileged actions; this phase must avoid broad input-validation redesign.
- Phase 19 owns the broader support bundle and operational summary; this phase provides the bounded health facts those surfaces consume.

## Open implementation choices for the planner/executor

- Keep component probes injectable so SIL tests can model missing BlueZ, PipeWire, Snapcast, or sink conditions without host services.
- Derive aggregate add-on state deterministically from component states and preserve the most actionable failure class when several dependencies fail.
- Ensure reconnect task ownership is keyed by normalized speaker address so one speaker cannot accumulate duplicate workers.
