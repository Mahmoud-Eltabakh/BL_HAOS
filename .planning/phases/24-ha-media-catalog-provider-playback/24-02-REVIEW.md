---
phase: 24-ha-media-catalog-provider-playback
plan: "02"
reviewed: "2026-10-24T15:07:24Z"
previous_reviewed: "2026-10-24T14:58:18Z"
depth: deep
files_reviewed: 7
files_reviewed_list:
- modules/integration/custom_components/bl_haos/__init__.py
- modules/integration/panel_ui/src/media-panel.tsx
- modules/integration/panel_ui/src/media-panel.test.tsx
- modules/integration/tests/test_panel_registration.py
- modules/integration/panel_ui/tsconfig.json
- modules/integration/panel_ui/vite.config.ts
- modules/integration/panel_ui/vitest.config.ts
findings: {critical: 0, warning: 0, info: 0, total: 0}
status: clean
---

# Phase 24 Plan 02: Code Re-Review Report

**Reviewed:** 2026-10-24T15:07:24Z
**Depth:** deep, bounded WR-01 remediation re-review
**Status:** clean

## Summary

WR-01 is resolved. `_finish_operation` now shields a non-failing completion
signal, waits through repeated caller cancellation, and retrieves the original
task's result after settlement. Late failures are consumed without loop-handler
or Core teardown errors; caller cancellation is preserved, and uncancelled
operation errors and operation-originated cancellation still propagate.

The final bounded re-review independently passed 13 focused regressions on WSL
Python 3.14.4 / Core 2026.10.3, with no teardown errors. There are no remaining
findings. The original three BLOCKER resolutions remain accepted from the prior
review and were not broadly re-audited. This clean review does not advance phase
state or authorize plan 24-03, deployment, or live actions.

Scope was anchored to the original review and the SUMMARY remediation addendum,
then narrowed to the seven remediation source/test/config files above. The
packaged module, package metadata, package-layout tests, call-tracing wrapper and
Core runtime were supporting evidence. No source/test/global-state edits,
installation, staging, commits, branches, deployment, live access, or token
access were performed. This review artifact is the only intentional file edit.
The scope list preserves the original remediation review; this final pass
examined only the helper, its ownership call path, and focused regressions.

## Narrative Findings (AI reviewer)

### Resolved Warning History

### WR-01: A protected failure after cancellation escapes to the loop error handler (Resolved)

**Classification:** WARNING (resolved; not an open finding)

**Resolution verified:** 2026-10-24T15:07:24Z. Only the non-failing `completed`
future is shielded. Its done callback signals settlement; `task.result()` then
retrieves either the result or exception before saved caller cancellation is
re-raised. The existing regressions cover late RuntimeError with zero/one/two/
three caller cancellations, operation-originated cancellation, real registration
success/failure after one/two/three cancellations, and executor copy/removal
ownership. All 13 passed under normal Core fixture teardown. No replacement loop
handler or private asyncio callback manipulation was used.

The issue, reproduction, and proposed fix below are retained as historical
evidence from the 14:58:18Z review, not current behavior.

**File:** [modules/integration/custom_components/bl_haos/__init__.py](../../../modules/integration/custom_components/bl_haos/__init__.py#L38)

**Issue:** `_finish_operation` repeatedly shields the failure-bearing operation
task. In the exact WSL Python 3.14.4 runtime, cancelling a shield while its inner
task is pending installs asyncio's `_log_on_exception` callback on that task.
Awaiting another shield does not remove that callback. If acquisition or cleanup
subsequently raises, asyncio calls the loop exception handler with
`RuntimeError exception in shielded future` (or the corresponding exception
type), even though this helper retrieves the task failure and preserves caller
cancellation. A registration/file-operation failure during reload or shutdown
can therefore produce an unhandled-loop error and traceback outside the intended
cancellation/error boundary. Existing cancellation regressions only complete
protected work successfully or cancel the operation itself.

**Precise Reproduction:**

1. Under `/home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python`, pass the unchanged
    helper an event-gated coroutine that raises `RuntimeError` after release.
2. Wait for operation entry, cancel the wrapper, and checkpoint the event loop
    before releasing the gate. Repeat with one, two, and three cancellations.
3. Observe caller `CancelledError` plus one loop-handler invocation in every
    cancelled case. With zero cancellations, the same failure raises normally
    and does not invoke the loop handler.

```json
{"cancellations":0,"outcome":"runtime_error","loop_errors":[]}
{"cancellations":1,"outcome":"cancelled","loop_errors":[{"message":"RuntimeError exception in shielded future","exception_type":"RuntimeError","exception":"late operation failure"}]}
{"cancellations":2,"outcome":"cancelled","loop_errors":[{"message":"RuntimeError exception in shielded future","exception_type":"RuntimeError","exception":"late operation failure"}]}
{"cancellations":3,"outcome":"cancelled","loop_errors":[{"message":"RuntimeError exception in shielded future","exception_type":"RuntimeError","exception":"late operation failure"}]}
```

The real setup/rollback path independently reproduces this. Pipe this plugin
through stdin into that isolated Python runtime from `modules/integration`;
set `BLHAOS_RUN_SIL=1` and `PYTHONDONTWRITEBYTECODE=1`. It changes no test file:

```python
import pytest

class LateRegistrationFailure:
      @pytest.fixture(autouse=True)
      def inject_failure(self, monkeypatch):
            from homeassistant.components import panel_custom
            original = panel_custom.async_register_panel

            async def register_then_fail(*args, **kwargs):
                  await original(*args, **kwargs)
                  raise RuntimeError("review: registration failed after public mutation")

            monkeypatch.setattr(panel_custom, "async_register_panel", register_then_fail)

raise SystemExit(pytest.main([
      "tests/test_panel_registration.py", "-q", "-p", "asyncio",
      "--asyncio-mode=auto", "-p", "no:cacheprovider",
      "-k", "actual_cancellation", "--tb=short", "--show-capture=no",
], plugins=[LateRegistrationFailure()]))
```

Observed: **2 passed, 16 deselected, 2 teardown errors, 1.55s, exit 1**.
Both original one/two-cancel test bodies pass their lock/pending, client-close,
empty-owner, removed-panel and HTTP-404 assertions; Core's normal fixture then
raises the captured late registration `RuntimeError` at teardown. This final
reproduction uses no replacement loop handler. It does not claim resource
cleanup failed.

**Fix:** Shield a non-failing completion signal instead of the failure-bearing
task. For example, create a loop future that the operation's done callback
resolves successfully; drain that future through repeated outer cancellation,
then retrieve `task.result()` explicitly. Preserve/re-raise saved caller
cancellation after retrieving any operation failure, and propagate
operation-originated cancellation when no caller cancellation exists. Keep the
ownership lock held until acquisition/removal settles. Do not suppress this by
replacing the global loop handler or using private asyncio callbacks. Add the
late-failure-after-cancellation discriminator above alongside the successful
executor-copy/removal cases, asserting no loop error and no unfinished child.

## Original Blocker Disposition

The IDs below refer to the three findings from the original 14:41:51Z review,
not additional currently open findings.

| Original Finding | Re-review Result |
|------------------|------------------|
| CR-01: `/` plus backslash host permits off-origin thumbnail | Resolved. Standard URL normalization plus path-policy checks reject backslash, protocol-relative, controls and normalized double-slash variants. |
| CR-02: Old browse/play results survive session replacement/loss | Resolved. Connection/user/availability changes invalidate browse and play generations; ordinary same-connection updates do not reset navigation/selection. |
| CR-03: Repeated cancellation allows late executor copy to recreate a served file | Resolved for the reported race. Real executor copy/removal remain protected and lock-owned until settled, followed by final cleanup/404. The distinct late-failure reporting defect WR-01 is now also resolved. |

## Verification

### Final Bounded WR-01 Verification

Independently executed against the current helper, without source/test edits:

```text
wsl --cd /mnt/f/Workspace/BL-HAOS/modules/integration env BLHAOS_RUN_SIL=1 PYTHONDONTWRITEBYTECODE=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests/test_panel_registration.py -q -p no:cacheprovider -k 'actual_cancellation or repeated_cancellation_drains_executor or finish_operation' --tb=short --show-capture=no
```

**Result:** 13 passed, 13 deselected in 3.21s; exit 0; no teardown errors.
Installed Core version independently confirmed as **2026.10.3**.

The four helper late-failure cases include the uncancelled RuntimeError control;
the six registration cases cover success and late failure under one/two/three
cancellations with lock-held/pending, client-close, empty-owner, removed-panel,
404 and subsequent reload checks. Two executor cases verify copy/removal stay
owned until settlement. The remaining case preserves operation-originated
cancellation. Core's ordinary fixture teardown detects unhandled loop failures.

The fixer's reported 10-body RED run with six teardown errors, 10-pass GREEN,
53-pass complete Core suite, and isolated 54-pass unit suite were not rerun or
reconstructed in this bounded pass. The independent 13-case run above is the
current acceptance evidence; no extra assurance gates were run.

### Prior Review Evidence (Historical)

Linux checks used Python 3.14.4, Core 2026.10.3 and helper 0.13.374 in the exact
existing WSL environment. Bytecode and pytest cache writes were disabled for
these Python runs. Core and HA-stub units ran in separate processes.

| Check | Independently Observed Result |
|-------|-------------------------------|
| Full existing panel Vitest | **28 passed**, 1.39s |
| Core panel registration + package-layout slice | **24 passed**, 3.72s |
| Full real-Core `tests --ignore=tests/unit` | **45 passed**, no skips, 7.38s |
| Separate `tests/unit`, plugin autoload disabled | **54 passed**, no skips, 1.98s |
| Installed TypeScript `--project modules/integration/panel_ui/tsconfig.json --noEmit` | Passed, including both Vite configs; explicit exit-code assertion |
| Two Vite builds, `write:false`, `emptyOutDir:false`, runner config loader | Both byte-identical to packaged module; 225873 bytes; 1.07s / 853ms |
| Structured package/lock-root comparison | Direct dependency and devDependency pins match |
| Actual packaged module, offline-intercepted Chromium thumbnail negatives | **13 unsafe variants rejected**; zero off-origin requests or page errors |
| HA-safe thumbnail positive controls | Three same-origin image/proxy/local paths loaded; `naturalWidth=1`, displayed **48x48** each |
| Actual packaged module, offline-intercepted Chromium session probes | New session browsed once; old root/child browse ignored; eight old play success/error cases ignored after replacement/loss/disconnect/user change; zero unhandled promise rejections or page errors |
| Ordinary same-connection `hass`/user-object/state/method update | Exactly one root browse; selection retained; current service method called once |
| Exact-runtime helper late-failure discriminator | Loop error for 1/2/3 outer cancellations; zero-cancel negative control has none |
| Minimal real-Core late-registration-failure reproduction above | **2 test bodies passed, 2 teardown errors**, confirming WR-01 |

Packaged SHA256:
`3eb60c232558add8642101d97f4df3ce7f704040a251e91f692e0057c81a1d6e`.

The passing original 45 Core and 54 unit tests did not cover WR-01 and did not
constitute a green monolithic run. The historical browser routed every request locally;
no provider/HA host was contacted and no dev server remains running.

## Evidence Limits

- The fixer's reported historical assertion-level RED/GREEN runs were read, not
   reconstructed by reverting source. Independent checks exercised current code.
- At the prior review, the editor-clear claim did **not** reproduce: VS Code reported unresolved
   `./media-panel` in the test, `vite`/`@vitejs/plugin-react` in the Vite config,
   and `vitest/config`/`@vitejs/plugin-react` in the Vitest config. Actual compiler,
   Vitest and Vite resolution passed. These editor-only diagnostics are not
   classified as a production defect and were not suppressed or fixed. They were
   not rechecked in this bounded pass and remain a historical editor-only residual,
   not a new product blocker.
- Initial multiline/quoting-invalid terminal probes produced incomplete output
   or syntax errors and were discarded. One build probe initially assumed a
   single Vite return object; the successful rerun handled library-mode arrays.
- An initial instrumentation fixture changed Core fixture ordering and caused
   teardown timer errors; that run was not accepted as a clean gate. A subsequent
   instrumented run showed no pending integration tasks on successful cases but
   Core intercepted the injected failure before the observer. The final minimal
   plugin above removes that observer and is the authoritative path reproduction.
- No fresh responsive screenshot matrix, authenticated HA/provider, deployment
   or physical-speaker acceptance is claimed. No phase or global-state advancement
   was performed. Parent should not treat this review as approval for plan 24-03.

---

_Reviewer: GitHub Copilot (gsd-code-reviewer)_