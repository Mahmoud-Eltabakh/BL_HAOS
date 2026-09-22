---
phase: "5"
slug: "fastapi-backend-daemon-real-time-event-bus"
status: draft
nyquist_compliant: true
wave_0_complete: false
created: "2026-09-21"
---

# Phase 5 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.x + httpx / fastapi.testclient |
| **Config file** | `pytest.ini` |
| **Quick run command** | `pytest tests/test_api.py` |
| **Full suite command** | `pytest tests/` |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Run `pytest tests/test_api.py`
- **After every plan wave:** Run `pytest tests/`
- **Before `$gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 10 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 05-01-01 | 01 | 1 | API-01, API-03 | — | Persistent JSON configuration store and REST routes | unit/api | `pytest tests/test_api.py` | ❌ W0 | ⬜ pending |
| 05-01-02 | 01 | 1 | API-01 | — | S6 supervision service layout for backend daemon | integration | `pytest tests/test_backend_s6.py` | ❌ W0 | ⬜ pending |
| 05-02-01 | 02 | 1 | API-02 | — | WebSocket connection manager, subscription, and event broadcasting | unit/ws | `pytest tests/test_ws.py` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_api.py` — Tests for all REST routes (`/api/adapters`, `/api/devices`, `/api/scan`, `/api/settings`).
- [ ] `tests/test_backend_s6.py` — Tests for S6 service `40-bl-haos-daemon` files and dependencies.
- [ ] `tests/test_ws.py` — Tests for WebSocket connection lifecycle and event broadcast delivery.

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 10s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** approved 2026-09-21
