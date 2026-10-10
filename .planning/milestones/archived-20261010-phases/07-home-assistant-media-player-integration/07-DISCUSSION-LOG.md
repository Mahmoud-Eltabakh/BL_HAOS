# Phase 7: Home Assistant Media Player Integration - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.

**Date:** 2026-09-21
**Phase:** 07-home-assistant-media-player-integration
**Areas discussed:** MQTT Discovery topic schemas, Media streaming pipeline, State and volume synchronization.

## Decisions:
1. **MQTT Protocol:** Standard Home Assistant MQTT Discovery `homeassistant/media_player/bl_haos_{mac}/config`.
2. **Playback Engine:** Async media player stream runner routing audio to PipeWire virtual sinks.
3. **Volume Sync:** Bi-directional MQTT state reporting with AVRCP feedback.
