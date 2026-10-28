---
phase: "29"
slug: "pr-safe-root-bridge-integration-ci"
status: validated
nyquist_compliant: false
wave_0_complete: true
created: "2026-10-28"
---

# Phase 29 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|---------|-------|
| **Framework** | pytest, Vitest, GitHub Actions workflow validation |
| **Config file** | `.github/workflows/tests.yml`; module pytest configs; panel `package.json` |
| **Quick run command** | `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest modules/integration/tests/test_package_layout.py -q` |
| **Full local gates** | Bridge Python 3.12 L1; integration Python 3.12 L1 with active parity; integration Python 3.14 SIL; bridge frontend tests/build/E2E on local Node 24 |
| **Estimated runtime** | 10 minutes |

---

## Sampling Rate

- **After each workflow task:** Validate YAML and run the narrowest affected local gate.
- **After the workflow change:** Run all root CI-equivalent suites on their declared runtimes where available.
- **Before phase verification:** Confirm the PR workflow's triggers/permissions/steps cannot invoke publishing and collect a passing PR-event run when authorized and available.
- **Max feedback latency:** 10 minutes per local gate.

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 29-01-01 | 01 | 1 | PRD-02 | T-29-01/T-29-02 | Node setup cannot silently skip parity; workflow remains non-publishing and checkout tokens are not persisted | workflow/static | `py -3.12 -m pytest tests/test_package_layout.py -q` after Node/Vite preflight | Yes | pending hosted Node 22 check |
| 29-01-02 | 01 | 1 | PRD-02 | T-29-SC | Declared-runtime client, bridge, and SIL gates pass with the reviewed lock unchanged | CI/runtime | Integration: `py -3.12 -m pytest tests/unit tests/test_package_layout.py -q -p asyncio --asyncio-mode=auto`; bridge: `py -3.12 -m pytest tests -q` (fail on nonzero); SIL: PowerShell asserts `wsl.exe -d Ubuntu -- /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python --version` reports Python 3.14, then runs the pinned WSL `tests/test_ha_integration_sil.py` suite and fails on nonzero. | Yes | pending hosted PR check |

---

## Wave 0 Requirements

- [x] Add Node 22 setup and `npm ci --prefix modules/integration/panel_ui --ignore-scripts` before integration package-layout tests.
- [x] Add a preflight that fails when Node, npm, Vite, or TypeScript is missing, preventing the parity test's defensive skip from producing a false-green CI result.
- [x] Add a non-publishing workflow contract assertion using an existing suitable static-test surface, or record evidence from complete workflow review if no suitable local assertion pattern exists.
- [x] Record that the old run cause cannot be established from public annotations; do not infer a root cause.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Confirm a real pull-request event passes the non-publishing workflow | PRD-02 | Requires an authorized PR/check run; local workflow inspection cannot prove hosted-runner behavior | Review PR checks and workflow permissions/steps; do not dispatch the nested image publisher. |

## Local Execution Evidence

- Bridge L1: Python `3.12.10`, 357 passed, 1 skipped, 1 non-fatal deprecation warning.
- Integration L1: Python `3.12.10`, 89 passed, including 12 package-layout tests; parity ran and did not skip. `voluptuous` was installed only to a temporary target from the workflow-declared test dependency list.
- Integration SIL: Python `3.14.4`, 95 passed.
- Bridge frontend: local Node `v24.19.0`, npm `11.17.0`; 39 Vitest passed, production build passed, and 4 Playwright E2E passed. These are not Node 22 CI evidence.
- Hosted PR event: not run. Current work is uncommitted and State forbids commit/push; the Node 22 hosted check remains a manual deferred gate.

---

## Validation Sign-Off

- [x] All tasks have automated verification or explicit hosted-check dependencies.
- [x] Sampling continuity: no 3 consecutive tasks without automated verification.
- [x] Wave 0 covers all local missing references; hosted PR event remains explicitly deferred.
- [x] No watch-mode flags.
- [x] PR workflow grants only required read permissions and contains no publishing edge.
- [ ] `nyquist_compliant: true` set only after the hosted PR evidence is recorded.

**Approval:** pending

---

## Security Scope

- **ASVS:** Level 1.
- **Blocking threshold:** critical, as currently configured in `.planning/config.json`.
- **Threats:** PR source reaching an image publisher or persisted checkout token, missing toolchain silently skipping required parity, and dependency lifecycle/install supply-chain risk.
- **Controls:** read-only root workflow permissions, `persist-credentials: false` on each checkout, Node 22 preflight, `npm ci --ignore-scripts`, locked dependencies, and no publisher trigger or invocation.
- **Package review:** Nine existing `SUS: too-new` entries were screened in `29-RESEARCH.md`; locked versions matched registry versions, sources were canonical, adoption was high, and no relevant lifecycle scripts were found. Keep the lock unchanged; no additional human checkpoint is required.