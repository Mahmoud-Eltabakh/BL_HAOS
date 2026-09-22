---
phase: "6"
slug: "ingress-web-dashboard-ui"
status: draft
nyquist_compliant: true
wave_0_complete: false
created: "2026-09-21"
---

# Phase 6 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.x + static asset verification |
| **Config file** | `pytest.ini` |
| **Quick run command** | `pytest tests/test_frontend_assets.py` |
| **Full suite command** | `pytest tests/` |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Run `pytest tests/test_frontend_assets.py`
- **After every plan wave:** Run `pytest tests/`
- **Before `$gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 10 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 06-01-01 | 01 | 1 | UI-01 | — | React/Vite dashboard structure with relative Ingress base paths | build/config | `pytest tests/test_frontend_assets.py::test_ingress_relative_paths` | ❌ W0 | ⬜ pending |
| 06-02-01 | 02 | 1 | UI-02, UI-03, UI-04 | — | Discovery modal, speaker cards, volume sliders, and settings panel | component/unit | `pytest tests/test_frontend_assets.py::test_ui_components_exist` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_frontend_assets.py` — Tests for Vite configuration, relative HTML entrypoint paths, component markup, and static asset mount in FastAPI.

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 10s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** approved 2026-09-21
