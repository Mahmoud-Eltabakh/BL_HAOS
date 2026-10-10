# Phase 8: Multi-Room Synchronization with Snapcast - Context

**Gathered:** 2026-09-21
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 8 delivers the sample-accurate multi-room audio broadcasting and speaker synchronization system using Snapcast:
- Integrated `snapserver` daemon configured to accept stream inputs (PipeWire sinks, TCP streams, and Home Assistant / Music Assistant audio streams).
- S6-rc service `30-snapserver` supervised in the container and chained to `10-pipewire`.
- Dynamic `snapclient` instance supervisor (`MultiroomManager`) dynamically launching a `snapclient -d -s pipewire --soundcard <node_name>` instance for each active Bluetooth speaker sink.
- Multi-speaker grouping logic allowing users to link multiple Bluetooth speakers into a single synchronized audio zone with millisecond-level acoustic latency offsets.
- REST API endpoints for `/api/multiroom/groups`, `/api/multiroom/speakers/{address}/latency`, `/api/multiroom/streams`.

</domain>

<decisions>
## Implementation Decisions

### Snapcast Audio Pipeline
- **D-01:** Configure `snapserver` with stream source `pipewire:///var/run/pipewire/pipewire-0?name=Snapcast` and stream name `default` (sample format: 48000:16:2). — **Reversibility:** reversible.

### Dynamic Snapclient Lifecycle
- **D-02:** When a Bluetooth speaker connects and PipeWire creates its audio sink node, `MultiroomManager` attaches a dedicated `snapclient` process routing audio to that specific PipeWire target node with custom latency offset. — **Reversibility:** reversible.

### S6 Supervision
- **D-03:** S6 service `30-snapserver` (type: `longrun`) depends on `10-pipewire`. — **Reversibility:** costly.

</decisions>

<canonical_refs>
## Canonical References
- `https://github.com/badaix/snapcast` — Snapcast official protocol and server configuration.
- `.planning/PROJECT.md` — Multi-room requirements.
- `.planning/REQUIREMENTS.md` — Requirements `SYNC-01`, `SYNC-02`, `SYNC-03`.
</canonical_refs>
