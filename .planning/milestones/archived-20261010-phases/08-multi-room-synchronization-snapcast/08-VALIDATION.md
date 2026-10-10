---
phase: "8"
slug: "multi-room-synchronization-snapcast"
status: draft
nyquist_compliant: true
wave_0_complete: false
created: "2026-09-21"
---

# Phase 8 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.x + pytest-asyncio |
| **Config file** | `pytest.ini` |
| **Quick run command** | `pytest tests/test_multiroom_manager.py` |
| **Full suite command** | `pytest tests/` |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Run `pytest tests/test_multiroom_manager.py`
- **After every plan wave:** Run `pytest tests/`
- **Before `$gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 10 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 08-01-01 | 01 | 1 | SYNC-01 | — | Snapserver configuration and S6 service supervision | config/integration | `pytest tests/test_snapserver_config.py` | ❌ W0 | ⬜ pending |
| 08-02-01 | 02 | 1 | SYNC-02, SYNC-03 | — | Dynamic Snapclient lifecycle, speaker grouping, and latency calibration | unit/async | `pytest tests/test_multiroom_manager.py` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_snapserver_config.py` — Tests for snapserver.conf stream definitions and S6 service `30-snapserver`.
- [ ] `tests/test_multiroom_manager.py` — Tests for speaker group creation, dynamic client process lifecycle, and latency offset calculations.

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 10s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** approved 2026-09-21
