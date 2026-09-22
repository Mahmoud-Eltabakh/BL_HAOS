---
phase: "2"
slug: "pipewire-audio-server-codec-suite"
status: draft
nyquist_compliant: true
wave_0_complete: false
created: "2026-09-21"
---

# Phase 2 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.x + python config validator |
| **Config file** | `pytest.ini` |
| **Quick run command** | `pytest tests/test_pipewire_config.py` |
| **Full suite command** | `pytest tests/` |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Run `pytest tests/test_pipewire_config.py`
- **After every plan wave:** Run `pytest tests/`
- **Before `$gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 10 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 02-01-01 | 01 | 1 | AUD-01 | — | PipeWire clock and quantum config parsed and validated | config | `pytest tests/test_pipewire_config.py::test_pipewire_clock_config` | ❌ W0 | ⬜ pending |
| 02-01-02 | 01 | 1 | AUD-01 | — | S6 service layout and dependency chain for PipeWire & WirePlumber | integration | `pytest tests/test_pipewire_s6.py::test_pipewire_s6_services` | ❌ W0 | ⬜ pending |
| 02-02-01 | 02 | 1 | AUD-02, AUD-03 | — | WirePlumber Bluetooth codec ranking and high-res settings | config | `pytest tests/test_pipewire_config.py::test_wireplumber_codec_ranking` | ❌ W0 | ⬜ pending |
| 02-02-02 | 02 | 1 | AUD-04 | — | AVRCP volume sync and hardware volume rules in WirePlumber | config | `pytest tests/test_pipewire_config.py::test_wireplumber_volume_sync` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_pipewire_config.py` — Tests for PipeWire clock, buffer quantum, WirePlumber codec priority, and AVRCP volume sync rules.
- [ ] `tests/test_pipewire_s6.py` — Tests for S6 service files, run script permissions, and dependencies for `10-pipewire` and `20-wireplumber`.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Real speaker codec negotiation over Bluetooth | AUD-02 | Requires physical Bluetooth speaker hardware | Connect LDAC/aptX compatible speaker and inspect `pw-cli info <node-id>` for negotiated codec format. |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 10s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** approved 2026-09-21
