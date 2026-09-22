# Phase 7: Home Assistant Media Player Integration - Context

**Gathered:** 2026-09-21
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 7 delivers the Home Assistant integration bridge exposing each connected Bluetooth speaker as a native `media_player` entity via Home Assistant MQTT Discovery:
- Automatic MQTT Discovery publisher registering devices under `homeassistant/media_player/bl_haos_{mac}/config` with device registry metadata (`identifiers: ["bl_haos_{mac}"]`, `manufacturer: "BL-HAOS"`, `model: "Bluetooth Speaker"`).
- Command & state topics:
  - `command_topic`: `bl_haos/{mac}/set` (`PLAY`, `PAUSE`, `STOP`, `VOLUME:x`, `PLAY_MEDIA:url`)
  - `state_topic`: `bl_haos/{mac}/state` (`playing`, `paused`, `idle`, `off`)
  - `volume_state_topic`: `bl_haos/{mac}/volume`
- Audio playback engine for TTS announcements, web radio streaming URLs, and local media browser content routed to the speaker's PipeWire node.
- Bi-directional synchronization: volume adjustments in Home Assistant update the PipeWire audio sink and speaker AVRCP, and physical button clicks update the Home Assistant entity state.

</domain>

<decisions>
## Implementation Decisions

### Entity Discovery Protocol
- **D-01:** Implement Home Assistant standard MQTT Discovery protocol per `https://developers.home-assistant.io/docs/core/entity/media-player/` and `https://www.home-assistant.io/integrations/media_player.mqtt/`. Each speaker entity is created dynamically upon connection and updated on alias changes. — **Reversibility:** reversible.

### Media Streaming Pipeline
- **D-02:** When Home Assistant dispatches a `play_media` command (TTS MP3/WAV URL or radio stream), `MediaPlayerBridge` spawns an asynchronous playback stream feeding raw PCM directly into PipeWire targeting the speaker's A2DP sink node (`pw-play` / `ffmpeg` / `mpv`). — **Reversibility:** reversible.

</decisions>

<canonical_refs>
## Canonical References
- `https://developers.home-assistant.io/docs/core/entity/media-player/` — Home Assistant Media Player entity model.
- `https://www.home-assistant.io/integrations/media_player.mqtt/` — Home Assistant MQTT Media Player documentation.
- `.planning/PROJECT.md` — BL-HAOS core architecture.
- `.planning/REQUIREMENTS.md` — Requirements `HA-01`, `HA-02`, `HA-03`, `HA-04`.
</canonical_refs>
