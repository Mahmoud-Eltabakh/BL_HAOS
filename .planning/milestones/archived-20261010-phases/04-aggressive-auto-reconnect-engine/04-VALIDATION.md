---
phase: "4"
slug: "aggressive-auto-reconnect-engine"
status: draft
nyquist_compliant: true
wave_0_complete: false
created: "2026-09-21"
---

# Phase 4 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.x + pytest-asyncio |
| **Config file** | `pytest.ini` |
| **Quick run command** | `pytest tests/test_auto_reconnect.py` |
| **Full suite command** | `pytest tests/` |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Run `pytest tests/test_auto_reconnect.py`
- **After every plan wave:** Run `pytest tests/`
- **Before `$gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 10 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 04-01-01 | 01 | 1 | CONN-01, CONN-02 | — | State machine transitions, backoff calculation, and fast-track discovery | unit/async | `pytest tests/test_auto_reconnect.py::test_reconnect_state_machine` | ❌ W0 | ⬜ pending |
| 04-01-02 | 01 | 1 | CONN-03 | — | Per-adapter concurrency locks and circuit breaker cooldowns | unit/async | `pytest tests/test_auto_reconnect.py::test_circuit_breaker_and_locking` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_auto_reconnect.py` — Tests for state transitions, exponential backoff with jitter, fast-tracking on device discovery, adapter locks, and circuit breaker tripping.

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 10s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** approved 2026-09-21
