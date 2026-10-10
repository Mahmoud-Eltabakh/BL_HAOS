# Phase 7: Home Assistant Media Player Integration - Research

**Phase:** 7 (Home Assistant Media Player Integration)
**Researched:** 2026-09-21
**Confidence:** HIGH

## Overview

Home Assistant supports zero-configuration entity creation via MQTT Discovery.
When a Bluetooth speaker connects to BL-HAOS, the add-on publishes an MQTT discovery payload that instantly registers a `media_player` entity in Home Assistant.

## MQTT Discovery Payload Specification

```json
{
  "name": "Living Room Speaker",
  "unique_id": "bl_haos_112233445566",
  "state_topic": "bl_haos/112233445566/state",
  "command_topic": "bl_haos/112233445566/command",
  "volume_state_topic": "bl_haos/112233445566/volume",
  "volume_command_topic": "bl_haos/112233445566/volume_set",
  "device": {
    "identifiers": ["bl_haos_112233445566"],
    "name": "Living Room Speaker",
    "manufacturer": "BL-HAOS",
    "model": "Bluetooth Audio Sink",
    "sw_version": "0.1.0"
  }
}
```

---
*Research for Phase 7: Home Assistant Media Player Integration*
