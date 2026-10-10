---
phase: 18-security-safe-execution-hardening
plan: 02
subsystem: bridge-security
status: complete
tags: [authentication, redaction, configuration, dependencies, cve, npm, pip]
requires:
  - phase: 18-security-safe-execution-hardening
    provides: strict input validation and safe process boundaries from plan 18-01
provides:
  - constant-time REST and WebSocket native authentication
  - recursive secret and URL redaction for health, diagnostics, errors, and logs
  - restrictive configuration persistence and bounded runtime settings
  - pinned Python, Debian, and frontend dependency inputs with blocking audit policy
affects: [native-api, websocket-transport, health, addon-build, release-gates]
actuals:
  tokens: 5200
  tasks: 3
  commits: 0
tech-stack:
  added: [pip-audit CI gate, Trivy filesystem scan]
  patterns: [excluded internal secrets, atomic mode-600 config persistence, exact dependency pins, fail-closed audit thresholds]
key-files:
  created:
    - modules/bridge/backend/requirements.txt
  modified:
    - modules/bridge/backend/bl_haos/api/routes.py
    - modules/bridge/backend/bl_haos/api/ws.py
    - modules/bridge/backend/bl_haos/config.py
    - modules/bridge/backend/bl_haos/health.py
    - modules/bridge/Dockerfile
    - modules/bridge/config.yaml
    - modules/bridge/web_ui/package.json
    - modules/bridge/web_ui/package-lock.json
    - modules/bridge/.github/workflows/builder.yaml
    - modules/bridge/README.md
    - modules/bridge/tests/test_api.py
    - modules/bridge/tests/test_health.py
    - modules/bridge/tests/test_dockerfile.py
    - modules/bridge/tests/test_addon_config.py
key-decisions:
  - Keep the native token internal to SystemSettings serialization while persisting it explicitly for restart continuity.
  - Use generic unauthorized and support-facing error text, with constant-time comparisons and recursive redaction before serialization or logging.
  - Upgrade the frontend to Vite 7.3.6 and the compatible React plugin after npm audit identified Vite 5/esbuild high and moderate advisories.
  - Keep high/critical dependency findings blocking in CI; no default bypass or unowned exception was added.
requirements-completed: [SAFE-03, SAFE-04, SAFE-05]
coverage:
  - id: D1
    description: REST and WebSocket native authentication rejects malformed, missing, wrong, and near-match credentials without exposing the configured token.
    requirement: SAFE-03
    verification:
      - kind: unit
        ref: modules/bridge/tests/test_api.py and modules/bridge/tests/test_native_transport.py
        status: pass
    human_judgment: false
  - id: D2
    description: Health, diagnostics, errors, logs, and serialized settings exclude credentials and sensitive URL material.
    requirement: SAFE-04
    verification:
      - kind: unit
        ref: modules/bridge/tests/test_health.py and modules/bridge/tests/test_api.py
        status: pass
    human_judgment: false
  - id: D3
    description: Runtime settings are bounded, persistence is restrictive, and dependency drift or high/critical findings block release.
    requirement: SAFE-05
    verification:
      - kind: unit
        ref: modules/bridge/tests/test_addon_config.py and modules/bridge/tests/test_dockerfile.py
        status: pass
      - kind: other
        ref: npm --prefix web_ui ci --ignore-scripts && npm --prefix web_ui audit --audit-level=high
        status: pass
    human_judgment: false
---

# Phase 18 Plan 02: Safe execution hardening summary

**Fail-closed native auth, recursive secret redaction, restrictive runtime settings, and reproducible dependency/CVE gates for the bridge add-on.**

## Performance

- **Duration:** ongoing session
- **Started:** 2026-09-23
- **Completed:** 2026-09-23
- **Tasks:** 3
- **Files modified:** 14 planned files plus the new backend requirements lock artifact

## Accomplishments

- REST and native WebSocket authentication now use constant-time credential checks with stable generic failures; near-match, malformed, and missing credentials are covered by tests.
- Native tokens are excluded from public settings/diagnostics, persisted explicitly with atomic mode-600 writes, and regenerated safely when persisted or environment configuration is invalid.
- Nested health/error values, credentials, bearer material, URL userinfo, and URLs are redacted before support-facing serialization or logging; speaker settings reject extra control fields and unsafe values.
- Debian, Python, and frontend dependency inputs are pinned. CI now blocks high/critical pip, npm, and filesystem dependency findings, and README documents stable/preview handling and exception ownership/expiry requirements.

## Verification

- `python -m pytest tests/test_api.py tests/test_health.py tests/test_ws.py tests/test_native_transport.py -q`: 21 passed.
- `python -m pytest tests/test_api.py tests/test_addon_config.py tests/test_health.py -q`: passed as part of the focused security run.
- `python -m pytest tests/test_dockerfile.py tests/test_addon_config.py -q`: passed as part of the focused security run.
- Expanded focused security/dependency suite: 29 passed.
- `python -m pytest tests/ -q`: 84 passed, 0 failed, 0 skipped, 4 warnings.
- `npm --prefix web_ui ci --ignore-scripts`: passed.
- `npm --prefix web_ui audit --audit-level=high`: passed with 0 vulnerabilities after the Vite/PostCSS remediation.
- `git diff --check`: passed; only existing CRLF normalization warnings were reported.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing critical supply-chain gate] Added a dedicated backend requirements lock artifact.**
- **Found during:** Task 3
- **Issue:** The Dockerfile had no reproducible Python dependency source, so pip installs could drift.
- **Fix:** Added exact-version `backend/requirements.txt` and changed the Dockerfile to install it with `--requirement`.
- **Files modified:** `modules/bridge/backend/requirements.txt`, `modules/bridge/Dockerfile`
- **Verification:** Dockerfile regression tests and full bridge suite pass.

**2. [Rule 1 - Vulnerable dependency] Upgraded the frontend toolchain after the audit gate identified Vite/esbuild and PostCSS advisories.**
- **Found during:** Task 3
- **Issue:** The initial exact pins caused `npm audit --audit-level=high` to fail with one high and two moderate findings.
- **Fix:** Updated PostCSS to 8.5.28, Vite to 7.3.6, and `@vitejs/plugin-react` to 4.7.0; regenerated the lockfile.
- **Files modified:** `modules/bridge/web_ui/package.json`, `modules/bridge/web_ui/package-lock.json`
- **Verification:** `npm ci` and high-severity audit both pass with zero vulnerabilities.

**Total deviations:** 2 auto-fixed. All were required to make the planned security gates effective.

## Issues Encountered

- Local `pip-audit` is not installed, so the Python audit command could not be replayed in this Windows environment without installing tooling. The builder workflow installs pinned `pip-audit==2.7.3` and runs the blocking audit in CI.
- The bridge submodule contains unrelated dirty changes from prior work, including Plan 18-01 files and test updates. They were preserved and not reverted; no commits were created per the parent instruction.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

The bridge security implementation and automated checks are ready for parent review. The only unexecuted local check is the CI-only Python audit because `pip-audit` is unavailable in the current environment; CI will enforce it as a blocking gate.

## Self-Check: PASSED

- Summary file exists at `.planning/phases/18-security-safe-execution-hardening/18-02-SUMMARY.md`.
- Full bridge suite passed: 84 passed, 0 failed, 0 skipped.
- Frontend clean install and high-severity audit passed with zero vulnerabilities.
- No task or metadata commits were created, as requested.

---
*Phase: 18-security-safe-execution-hardening*
*Completed: 2026-09-23*
