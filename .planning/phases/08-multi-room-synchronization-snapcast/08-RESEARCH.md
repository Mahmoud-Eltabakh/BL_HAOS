# Phase 8: Multi-Room Synchronization with Snapcast - Research

**Phase:** 8 (Multi-Room Synchronization with Snapcast)
**Researched:** 2026-09-21
**Confidence:** HIGH

## Overview

Snapcast is an open-source multi-room client-server audio player. It delivers sample-accurate synchronization across multiple audio outputs over local WiFi/LAN and PipeWire.

## Key Snapcast Architecture
1. **Snapserver**:
   - Reads PCM stream from PipeWire named sink or pipe (`pipe:///tmp/snapcast/snapfifo?name=default&sampleformat=48000:16:2`).
   - Serves synchronized chunked audio frames to connected Snapclients over TCP port 1704.
   - Provides JSON-RPC API on TCP port 1705 for volume and client group management.
2. **Dynamic Snapclients**:
   - Each Bluetooth speaker connected to PipeWire has a target sink node (e.g. `bluez_output.11_22_33_44_55_66.1`).
   - Running `snapclient -h 127.0.0.1 --player alsa/pipewire` feeds the audio stream to that sink node with microsecond precision.

---
*Research for Phase 8: Multi-Room Synchronization with Snapcast*
