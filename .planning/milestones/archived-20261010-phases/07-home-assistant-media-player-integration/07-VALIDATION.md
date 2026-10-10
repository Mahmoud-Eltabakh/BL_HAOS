---
phase: "7"
slug: "home-assistant-media-player-integration"
status: draft
nyquist_compliant: true
wave_0_complete: false
created: "2026-09-21"
---

# Phase 7 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.x + pytest-asyncio |
| **Config file** | `pytest.ini` |
| **Quick run command** | `pytest tests/test_mqtt_discovery.py` |
| **Full suite command** | `pytest tests/` |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Run `pytest tests/test_mqtt_discovery.py`
- **After every plan wave:** Run `pytest tests/`
- **Before `$gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 10 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 07-01-01 | 01 | 1 | HA-01, HA-04 | — | MQTT discovery payload generation, unique IDs, and topic contracts | unit | `pytest tests/test_mqtt_discovery.py` | ❌ W0 | ⬜ pending |
| 07-02-01 | 02 | 1 | HA-02, HA-03, HA-04 | — | Media playback command router for TTS URL streaming & volume state sync | unit/async | `pytest tests/test_media_player.py` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_mqtt_discovery.py` — Tests for Home Assistant MQTT Discovery configuration schemas and device payload generation.
- [ ] `tests/test_media_player.py` — Tests for TTS/radio URL stream handlers, command routing, and state publishing.

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 10s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** approved 2026-09-21
