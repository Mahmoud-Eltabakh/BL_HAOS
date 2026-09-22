# Phase 2: PipeWire Audio Server & Codec Suite - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-09-21
**Phase:** 02-pipewire-audio-server-codec-suite
**Areas discussed:** Codec Priority & Auto-Negotiation, Buffer Quantum & Latency Profile, Volume Sync & AVRCP, S6 Supervision & Topology

---

## Codec Priority & Auto-Negotiation

| Option | Description | Selected |
|--------|-------------|----------|
| Audiophile High-to-Low Ranking (`ldac`, `aptx_hd`, `aptx`, `aac`, `sbc_xq`, `sbc`) | Prioritize highest audio fidelity with auto-fallback to the best mutual codec supported by the speaker | ✓ |
| Conservative Stability (`aac`, `sbc_xq`) | Restrict codecs to AAC and SBC only | |
| Config-Driven Strict Codec | Enforce single codec without fallback | |

**User's choice:** Audiophile High-to-Low Ranking
**Notes:** Provides maximum fidelity for audiophile speakers while maintaining 100% compatibility with older SBC-only devices.

---

## Buffer Quantum & Latency Profile

| Option | Description | Selected |
|--------|-------------|----------|
| Balanced 1024 Quantum (~21.3ms @ 48kHz) | Optimal balance for voice TTS responsiveness and RF packet jitter tolerance | ✓ |
| Resilient 2048 Quantum (~42.6ms @ 48kHz) | Higher latency, maximal RF resilience | |
| Ultra-Low Latency 512 Quantum (~10.6ms @ 48kHz) | Minimal latency, higher risk of buffer underrun | |

**User's choice:** Balanced 1024 Quantum
**Notes:** Prevents audio crackles over standard 2.4GHz Bluetooth while keeping voice notifications instantaneous.

---

## Volume Sync & AVRCP

| Option | Description | Selected |
|--------|-------------|----------|
| Bidirectional AVRCP Absolute Volume with Perceptual Curve | Physical speaker button presses sync to Home Assistant and vice versa | ✓ |
| Software-Only Volume | PipeWire scales digital PCM amplitude, hardware volume fixed | |

**User's choice:** Bidirectional AVRCP Absolute Volume with Perceptual Curve
**Notes:** Delivers natural volume adjustment aligned with user expectations.

---

## S6 Supervision & Topology

| Option | Description | Selected |
|--------|-------------|----------|
| Chained S6-rc Longrun Services (`10-pipewire`, `20-wireplumber`) | Dedicated S6 service definitions with explicit dependency ordering on `00-init-environment` | ✓ |
| Combined Wrapper Script | Single process running both daemons in subshells | |

**User's choice:** Chained S6-rc Longrun Services
**Notes:** Ensures robust restart and lifecycle management under S6-Overlay v3.

---

## Agent Discretion

- PipeWire configuration file structure under `/etc/pipewire/` and `/etc/wireplumber/`.
- Pytest test cases and parsing utilities.

## Deferred Ideas

- None.
