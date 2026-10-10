---
phase: "3"
slug: "bluez-d-bus-bluetooth-controller"
status: draft
nyquist_compliant: true
wave_0_complete: false
created: "2026-09-21"
---

# Phase 3 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.x + pytest-asyncio |
| **Config file** | `pytest.ini` |
| **Quick run command** | `pytest tests/test_bluetooth_manager.py` |
| **Full suite command** | `pytest tests/` |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Run `pytest tests/test_bluetooth_manager.py`
- **After every plan wave:** Run `pytest tests/`
- **Before `$gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 10 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 03-01-01 | 01 | 1 | BT-01, BT-04 | — | Multi-adapter enumeration and discovery scanning with RSSI reporting | unit/async | `pytest tests/test_bluetooth_adapter.py` | ❌ W0 | ⬜ pending |
| 03-01-02 | 01 | 1 | BT-01 | — | Audio device classification, filtering, and model parsing | unit | `pytest tests/test_bluetooth_device.py` | ❌ W0 | ⬜ pending |
| 03-02-01 | 02 | 1 | BT-02, BT-03 | — | D-Bus agent pairing (PIN, SSP) and device trust persistence | unit/async | `pytest tests/test_bluetooth_agent.py` | ❌ W0 | ⬜ pending |
| 03-02-02 | 02 | 1 | BT-01, BT-02, BT-03, BT-04 | — | Integrated BluetoothManager lifecycle and mock bus test | integration | `pytest tests/test_bluetooth_manager.py` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_bluetooth_adapter.py` — Tests for adapter enumeration, power toggling, and scanning lifecycle.
- [ ] `tests/test_bluetooth_device.py` — Tests for device property parsing, audio sink detection, and RSSI signals.
- [ ] `tests/test_bluetooth_agent.py` — Tests for BlueZ pairing agent callbacks and authorization methods.
- [ ] `tests/test_bluetooth_manager.py` — Tests for top-level `BluetoothManager` lifecycle and events.

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 10s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** approved 2026-09-21
