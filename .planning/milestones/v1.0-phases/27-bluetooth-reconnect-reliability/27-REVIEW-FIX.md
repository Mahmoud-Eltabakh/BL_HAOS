---
phase: 27-bluetooth-reconnect-reliability
fixed_at: "2026-10-24T08:56:31Z"
review_path: .planning/phases/27-bluetooth-reconnect-reliability/27-REVIEW.md
iteration: 1
findings_in_scope: 2
fixed: 2
skipped: 0
status: all_fixed
commit_policy: prohibited-by-user
commits: 0
independent_review: pending-parent-rerun
hardware_soak: pending-authorized-deployment
---

# Phase 27: Code Review Fix Report

**Fixed at:** 2026-10-24T08:56:31Z
**Source review:** 27-REVIEW.md, unchanged (issues_found)
**Iteration:** 1
**Summary:** 2 findings in scope, 2 addressed, 0 skipped, 0 commits.

## Fixed Issues

### CR-01: Adapter ownership does not protect the resolved device record

**Status:** fixed: requires human verification / independent parent re-review
**Files modified:** modules/bridge/backend/bl_haos/bluetooth/manager.py,
modules/bridge/tests/test_bluetooth_manager.py
**Commit:** None; explicitly prohibited. Changes remain unstaged/uncommitted.
**Applied fix:** After awaited GetAll, reuse the live cache winner. Under the
actual-adapter connection lock, reject a selected record that is detached or no
longer the cached object, including after scan stop/settle, before Connect after
explicit-reset settle, and before success after the trust update. Fail this
attempt to the existing scheduler without re-resolution or immediate retry.
No bonds are removed; automatic reset and API contracts are unchanged.
**Regression evidence:** Two missing/detached concurrent-resolution barriers and
eight removal/replacement barriers during stop_scan, settle, Connect and trust.
All ten initially failed with cache identity or false-success assertions; all
ten passed immediately after the manager edit. The real scheduler now retains
failure history, enters BACKOFF and schedules a future retry. Early withdrawal
issues zero Connect calls; late withdrawal issues only the one in-flight call.

### WR-01: Custom backoff values can overflow before saturation

**Status:** fixed: requires independent parent re-review
**Files modified:** modules/bridge/backend/bl_haos/bluetooth/reconnect.py,
modules/bridge/tests/test_auto_reconnect.py
**Commit:** None; explicitly prohibited. Changes remain unstaged/uncommitted.
**Applied fix:** Validate finite initial_backoff >= 0, finite multiplier >= 1,
and finite max_backoff > 0. Preserve zero and tiny-positive initial values,
constant multiplier one, caps below the floor and initial delays above the cap.
Use bounded logarithmic growth and scaled mantissa/exponent arithmetic instead
of constructing an independently overflowing multiplier power. Preserve floor,
non-negative jitter, final cap and existing default exact power-of-two pacing.
**Regression evidence:** Zero and 1e-320 at step 1024 explicitly failed on
OverflowError before the fix; eleven invalid-domain assertions also failed.
All pass after the edit, including million-step saturation/zero behavior and
four already-green supported-boundary cases. No tests were weakened or skipped.

## Verification

All checks ran in the **main checkout**, F:/Workspace/BL-HAOS/modules/bridge;
no isolated worktree was created under the explicit no-branch/worktree override.
Every pytest invocation set PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 and used
F:/Workspace/BL-HAOS/.venv/Scripts/python.exe with -m pytest -c pytest.ini.
Exact commands are retained in 27-01-SUMMARY.md and 27-VALIDATION.md.

| Check | Actual result | Exit | Duration |
| --- | --- | --- | --- |
| Immediate test-first phase27_review RED | 23 failed, 4 passed, 64 deselected | 1 | 1.23s |
| Same command immediately after manager edit | 13 failed, 14 passed, 64 deselected | 1 | 1.07s |
| Same command immediately after reconnect edit | 27 passed, 64 deselected | 0 | 0.82s |
| Unchanged six-file focused gate | 137 passed, 1 warning | 0 | 10.28s |
| Full bridge suite | 280 passed, 1 skipped, 1 warning | 0 | 12.36s |

Re-read changed production sections; surrounding code intact. Editor diagnostics
are clear for all four changed Python files; bridge git diff --check passed.
The existing Windows skip is test_media_player.py:654 (POSIX process groups).
The warning is the existing Starlette/httpx TestClient deprecation. No pending
tasks, unawaited coroutines, collection failures or repair loops were observed.

## Handoff Limits

No commit, staging, branch, deployment, install, host operation, reset/unpair,
phase24 edit or state update was performed. Existing user edits were preserved.
Only this report is a new file; no source/test file or dependency was created.
The existing unreleased phase-27 version remains 0.2.68. REVIEW.md was not marked
clean. all_fixed records local remediation, not independent approval. The parent
must rerun the reviewer; authorized HAOS/physical-speaker soak remains pending.