---
phase: "1"
slug: "add-on-foundation-container-blueprint"
status: draft
nyquist_compliant: true
wave_0_complete: false
created: "2026-09-21"
---

# Phase 1 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.x + python schema validator |
| **Config file** | `pytest.ini` / `pyproject.toml` |
| **Quick run command** | `pytest tests/test_addon_config.py` |
| **Full suite command** | `pytest tests/` |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Run `pytest tests/test_addon_config.py`
- **After every plan wave:** Run `pytest tests/`
- **Before `$gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 10 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 01-01-01 | 01 | 1 | SYS-01 | — | Container base builds with S6-Overlay and required packages | build/lint | `python -m pytest tests/test_dockerfile.py` | ❌ W0 | ⬜ pending |
| 01-01-02 | 01 | 1 | SYS-01 | — | S6 supervision scripts have correct file modes and bundle definitions | integration | `python -m pytest tests/test_s6_structure.py` | ❌ W0 | ⬜ pending |
| 01-02-01 | 02 | 1 | SYS-02 | — | Add-on config.yaml adheres to official HAOS Add-on schema | schema | `python -m pytest tests/test_addon_config.py` | ❌ W0 | ⬜ pending |
| 01-02-02 | 02 | 1 | SYS-03 | — | Startup self-check probes D-Bus socket and logs Bluetooth controller state | unit | `python -m pytest tests/test_dbus_probe.py` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_addon_config.py` — Verifies `config.yaml` and `build.yaml` syntax, ingress settings, and permissions.
- [ ] `tests/test_s6_structure.py` — Validates S6-rc service definitions and script permissions.
- [ ] `tests/test_dbus_probe.py` — Tests D-Bus socket presence checks and graceful diagnostics.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Home Assistant Add-on Store install test | SYS-01 | Requires running HAOS instance | Add local repository in HAOS add-on store and verify install dialog renders without schema errors. |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 10s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** approved 2026-09-21
