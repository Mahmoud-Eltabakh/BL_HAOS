# Runtime Validation Report

**Generated**: 2026-09-24
**Target**: `F:\Workspace\BL-HAOS`

## Summary

| Step | Status | Exit Code | Details |
|---|---:|---:|---|
| Frontend build | PASS | 0 | `npm run build`; Vite production build completed successfully. |
| Startup/readiness | PASS | 0 | `python -m uvicorn bl_haos.main:app --host 127.0.0.1 --port 8099 --log-level debug`; `/api/health` returned 200. |
| Bridge integration tests | PASS | 0 | `110 passed`, 4 existing runtime/deprecation warnings. |
| Integration package tests | PASS | 0 | `tests/test_package_layout.py`: `3 passed`. |
| Integration SIL tests | FAIL | 1 | Test harness installed, but Home Assistant Core imports Unix-only `fcntl` on Windows. |
| Browser E2E | PASS | 0 | 3 Playwright flows passed in Chromium. |

## Environment and Verdict

```text
environment:
  docker: UNAVAILABLE - docker daemon did not respond to `docker info`
  wsl: AVAILABLE but not configured for this repository - Ubuntu 2 is installed and stopped
  node: AVAILABLE - v24.19.0
  playwright: AVAILABLE - Chromium 1243 installed and executed successfully
  infra-tier: FALLBACK(embedded/demo mode) - Docker unavailable; BL-HAOS demo runtime used
  browser-tier: PRIMARY(Playwright) - Chromium executed against the real running FastAPI app
startup: PASS - Uvicorn on 127.0.0.1:8099; /api/health -> 200
integration: FAIL - exit_code: 1 for full integration suite; bridge 110 passed and package-layout 3 passed; SIL execution reaches Home Assistant Core but fails because Windows has no fcntl module
  scope: FastAPI TestClient/API coverage and integration package layout
  gaps: Full Home Assistant SIL/config-entry coverage requires the documented WSL 2 or devcontainer environment
 e2e: PASS - exit_code: 0, passed: 3, failed: 0
  flows: dashboard startup, diagnostics refresh/native status, unauthenticated recovery boundary plus support export
  boundaries: rendered React UI, REST health/diagnostics, authentication responses, support-bundle contract
  gaps: Bluetooth hardware and live Home Assistant Supervisor integration were not exercised
overall: FAIL - required full integration SIL tier has exit_code 2 without a named waiver; browser and bridge tiers passed
```

## Test Evidence

- Bridge suite: `modules/bridge/tests/`
- Integration package test: `modules/integration/tests/test_package_layout.py`
- Temporary browser specs: `.planning/runtime-validation/*.spec.js`
- Browser runner: `.planning/runtime-validation/node_modules/.bin/playwright`
- Frontend build output: `modules/bridge/web_ui/dist/`

## Legacy Test Assets

No legacy browser E2E suite was found. Existing repository tests are Python unit/slice/SIL tests; the new browser validation uses Playwright against the actual demo-mode runtime.

## Issues Found

| # | Severity | Description | Escalated To |
|---:|---|---|---|
| 1 | Blocker | Full Home Assistant SIL tests cannot run in native Windows because Home Assistant Core imports Unix-only `fcntl`; the official Windows path is WSL 2 or a devcontainer. | Runtime validation owner |
| 2 | Gap | Docker daemon is unavailable, so container/image validation was not executed. | HAOS validation owner |
| 3 | Gap | Live Bluetooth hardware, PipeWire, Supervisor discovery, and Home Assistant Core were not exercised. | HAOS validation owner |
