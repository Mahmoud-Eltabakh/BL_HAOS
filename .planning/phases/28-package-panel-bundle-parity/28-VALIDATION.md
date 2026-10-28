---
phase: "28"
slug: "package-panel-bundle-parity"
status: validated
nyquist_compliant: true
wave_0_complete: true
created: "2026-10-28"
---

# Phase 28 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|---------|-------|
| **Framework** | Vitest 5.0.4, pytest, and Home Assistant SIL |
| **Config file** | `modules/integration/panel_ui/vitest.config.ts`; `modules/integration/pytest.ini` |
| **Quick run command** | `npm --prefix modules/integration/panel_ui test` |
| **Focused package command** | `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest modules/integration/tests/test_package_layout.py -q` |
| **Full relevant gate** | Panel Vitest, fresh temporary Vite build parity, package-layout tests, and WSL panel-registration SIL |
| **Estimated runtime** | 60 seconds |

---

## Sampling Rate

- **After every task:** Run the narrowest modified Vitest or focused package-layout test.
- **After every plan wave:** Run the fresh-build parity check and full panel Vitest suite.
- **Before `/gsd:verify-work`:** Run package-layout assertions and WSL panel-registration SIL.
- **Max feedback latency:** 60 seconds.

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 28-01-01 | 01 | 1 | PRD-01 | T-28-01 | Fresh build does not overwrite the tracked artifact before comparison | build/parity | `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 .\.venv\Scripts\python.exe -m pytest modules/integration/tests/test_package_layout.py::test_panel_bundle_matches_fresh_build -q` | Yes | green |
| 28-01-02 | 01 | 1 | PRD-01 | T-28-02 | Packaged output contains no credentials or resolved playback URLs | package-layout | `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 .\.venv\Scripts\python.exe -m pytest modules/integration/tests/test_package_layout.py -q` | Yes | green |
| 28-01-03 | 01 | 1 | PRD-01 | T-28-03 | The isolated build cannot clear or replace unrelated package assets | package/SIL | `wsl.exe -d Ubuntu -- bash -c 'cd /mnt/f/Workspace/BL-HAOS/modules/integration && env BLHAOS_RUN_SIL=1 PYTHONDONTWRITEBYTECODE=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests/test_panel_registration.py -q -p asyncio --asyncio-mode=auto --tb=short --show-capture=no'` | Yes | green |

*The planner may split or renumber tasks; it must retain PRD-01 coverage and all three threat behaviors.*

---

## Wave 0 Requirements

- [x] Add a deterministic test that builds to a fresh temporary output directory, asserts the expected single JS bundle, and compares bytes with the tracked `panel_static` artifact.
- [x] Extend package assertions to cover the saved-playlist launch and `Playback queue` UI while retaining secret/URL safety checks.
- [x] Document the Node/npm runtime used by the local panel build; Phase 29 owns CI runtime standardization.

---

## Manual-Only Verifications

All Phase 28 behavior is verifiable through local source, build, package, and SIL checks. Live Home Assistant shell and playback acceptance are outside this phase and remain separately authorized Phase 31/32 work.

---

## Validation Sign-Off

- [x] All tasks have automated verification or Wave 0 dependencies.
- [x] Sampling continuity: no 3 consecutive tasks without automated verification.
- [x] Wave 0 covers all missing references.
- [x] No watch-mode flags.
- [x] Feedback latency < 60 seconds.
- [x] `nyquist_compliant: true` set in frontmatter after validation.

**Approval:** approved 2026-10-28 (automated local validation)

## Local Runtime Evidence

- Node.js: `v24.19.0`
- npm: `11.17.0`
- These are observed local build versions only, not a Phase 29 CI support pin.
- The Python-only CI job skips the fresh-build comparison when panel npm dependencies are absent; Phase 29 must install the chosen Node/npm toolchain so CI runs this parity check rather than skipping it.

---

## Security Scope

- **ASVS:** Level 1.
- **Blocking threshold:** critical, as currently configured in `.planning/config.json`.
- **Threats:** wrong/stale bundle tampering, credential or playable-URL disclosure, and destructive build-output cleanup.
- **Controls:** exact temporary-build comparison, package boundary assertions, and non-destructive output isolation.