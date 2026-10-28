# Phase 33: Authorized Reconnect Hardware Soak

**Status:** blocked pending hardware authorization and supported-matrix approval

## Discussion

This phase validates reconnect stability and pairing retention on real supported hardware. It is intentionally separated from local mock validation and is not approved by the v1.1 roadmap without explicit checkpointing.

## Scope

- link-loss/resume checks on approved hardware
- pairing retention and bounded retry behavior
- playback continuity and failure recording
- recovery and rollback conditions

## Required checkpoint

The reviewer must explicitly name the host, hardware matrix, duration, stop conditions, and evidence method before any hardware action.
