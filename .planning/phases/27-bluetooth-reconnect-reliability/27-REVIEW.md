---
phase: 27-bluetooth-reconnect-reliability
reviewed: "2026-10-24T08:59:27Z"
depth: standard
files_reviewed: 5
files_reviewed_list:
  - modules/bridge/backend/bl_haos/bluetooth/device.py
  - modules/bridge/backend/bl_haos/bluetooth/manager.py
  - modules/bridge/backend/bl_haos/bluetooth/reconnect.py
  - modules/bridge/tests/test_bluetooth_manager.py
  - modules/bridge/tests/test_auto_reconnect.py
findings:
  critical: 0
  warning: 0
  info: 0
  total: 0
status: clean
workflow_verdict: clean
resolved_findings:
  - CR-01
  - WR-01
review_scope: two-prior-findings-and-minimal-adjacent-regressions
review_basis: bridge-submodule-uncommitted-diff-against-HEAD
hardware_soak: pending-authorized-deployment
---

# Phase 27: Code Review Report

**Reviewed:** 2026-10-24T08:59:27Z
**Depth:** standard
**Files Reviewed:** 5
**Status:** clean (scoped independent re-review)

## Narrative Findings (AI reviewer)

### Summary

CR-01 and WR-01 are resolved in the current local implementation. No actionable
new finding was established in the fixes or the minimal adjacent paths checked.
This verdict is limited to the two prior findings, the affected manager/device/
reconnect paths and their focused regressions; it is not a repository-wide review
or evidence that the real host's Bluetooth behavior is fixed.

Read the prior review and fix report, inspected the actual uncommitted bridge
diff and affected source/tests, and independently ran the checks below. No
structural pre-pass or external reviewer evidence was supplied. Source and tests
were not edited. No commits, staging, branches, deployments, live host/radio
operations, pairing deletion, phase 24 edits or planning-state changes occurred.

### Resolved Evidence

**CR-01: resolved.** After GetAll, ensure_device reuses an already-installed live
record rather than replacing it with an older snapshot. connect_device checks
cache identity and attachment under adapter ownership, after scan stop/settle,
after explicit-reset disconnect/settle, and before reporting success after trust.
The two real-resolution barriers preserve the canonical cache record and reject
the contender as busy. Eight removal/replacement cases spanning stop_scan,
settle, Connect and trust reject stale success, retain failure history, schedule
BACKOFF and release ownership. Four additional independent in-memory probes
withdraw/replace the record during explicit disconnect or reset settle: all
raise the retryable RuntimeError, issue zero Connect calls, retain bonds and
release the adapter lock. No immediate retry or automatic reset was introduced.

**WR-01: resolved.** The constructor rejects nonfinite/unsupported delay values;
zero is explicit, and bounded logarithmic growth plus scaled mantissa/exponent
arithmetic avoids constructing the overflowing multiplier power. Independently
observed zero at step 1024 as 0.0 and 1e-320 at step 1024 as
1.7976731214730535e-12 with zero jitter; million-step values are respectively 0
and the 120-second cap. Added tests also cover invalid domains and supported
boundaries. Independent probes additionally cover minimum-subnormal input,
multiplier 1.5, the nearest float above one, step 10**20, and a maximum-finite
cap: all return finite values within bounds. Existing default exact pacing,
jitter, breaker and cancellation tests pass.

### Historical Findings (Resolved, Not Open)

The following descriptions and reproduction outputs are retained from the
2026-10-24T08:52:35Z review. They describe the pre-fix implementation and are not
current findings or current reproduction results.

#### CR-01: RESOLVED - Canonical device record ownership (original classification: BLOCKER)

**File:** [manager.py](../../../modules/bridge/backend/bl_haos/bluetooth/manager.py#L626), lines 626-645.
**Absolute file:** F:/Workspace/BL-HAOS/modules/bridge/backend/bl_haos/bluetooth/manager.py
**Related locations:** manager.py:368-397, especially the unconditional cache
assignment at 393; reconnect.py:362-372.

**Issue:** `ensure_device` runs before the adapter contention check. Two requests
for an uncached or detached address can both enter its asynchronous GetAll path.
The first result installs device A and acquires the adapter lock. The second
result installs device B at the same cache path before discovering that the
adapter is busy. The winning connection then updates A, which is no longer the
record returned by GET devices or the native speaker snapshot. Returning busy
has therefore already mutated the winner's connection state indirectly.

The selected record is also used unchanged after awaited scan stop and settle.
If InterfacesRemoved detaches it during those waits, there is no guard before
Connect or before reporting success. This is particularly relevant to the new
resolve-before-stop-scan order. An eventual successful method reply is accepted
even though the selected record still reports `connected=False` because it is
detached. The engine trusts the manager result and clears failure history,
entering CONNECTED without a future retry despite the offline inventory.

**Reproduction evidence:** Executed event-controlled, in-memory probes with the
real BluetoothManager, ensure_device, BluetoothDevice and AutoReconnectEngine;
only D-Bus boundaries were fake. No source/test file was created. For the cache
race, start two connects while both GetAll replies are pending, release the first
reply, block its Connect, then release the second reply. The second request
raises BluetoothOperationInProgress after replacing the cache. Release the
winner's Connect. Observed and asserted:

```text
RESOLUTION_RACE: first_success=True, busy_contender_replaced_cache=True, original_connected=True, cached_connected=False
```

A second probe delivers InterfacesRemoved from fake stop_scan, then permits the
fake Connect to return successfully. It demonstrates the missing state guard,
not a claim about the ordering guaranteed by physical BlueZ hardware:

```text
DETACHED_SCAN: connect_calls=1, detached=True, cached_connected=False, profile_state=connected, failures=0
```

**Fix:** Preserve a single canonical live cache object across concurrent
resolution. For example, after a pending GetAll returns, reuse a live record
already installed for that path instead of replacing it with an older snapshot.
Under adapter ownership, revalidate record identity and attachment after scan
stop/settle and before success. If the record was withdrawn or superseded, fail
the single attempt as retryable rather than connecting a known detached record
or publishing false success; do not restore an immediate retry or automatic
reset. Add barriers for concurrent missing/detached resolution and a removal
event during settle, asserting canonical cached state and no stale success.

**Coverage gap:** Existing phase27_connection contention tests prepopulate every
device and mock stop_scan. They never exercise two asynchronous resolutions of
the same address or a cache removal/replacement during the operation.

#### WR-01: RESOLVED - Custom backoff overflow (original classification: WARNING)

**File:** [reconnect.py](../../../modules/bridge/backend/bl_haos/bluetooth/reconnect.py#L139), lines 129-142.
**Absolute file:** F:/Workspace/BL-HAOS/modules/bridge/backend/bl_haos/bluetooth/reconnect.py

**Issue:** The logarithmic threshold protects the final product from exceeding
max_backoff, but the else branch still evaluates `backoff_multiplier ** step`
as a separate float. With initial_backoff=0.0 the saturation guard is skipped
entirely. With a very small positive initial value, the exponent can overflow
even when the scaled result is finite and below the cap. The constructor does
not reject either value. An exception here can interrupt failure or cancellation
cleanup before next_retry_time is updated; this is a robustness gap in the
plan's custom-constructor and huge-step guarantee, not a default-policy failure.

**Reproduction evidence:** Both cases below were executed against the actual
class with backoff_multiplier=2.0, max_backoff=120.0 and zero jitter:

```text
CUSTOM_BACKOFF: initial=0.0, step=1024, error=OverflowError: (34, 'Result too large')
CUSTOM_BACKOFF: initial=1e-320, step=1024, error=OverflowError: (34, 'Result too large')
```

For the positive case the mathematical scaled value is approximately 1.8e-12,
so exceeding the 120-second cap is not the cause. The default million-step test
passes because its ordinary initial value takes the saturation branch.

**Fix:** Define and validate the supported constructor domain, handle zero
explicitly if retained, and calculate positive growth in log space before
exponentiating the bounded final value. Preserve supported small positive
overrides and the existing floor/jitter/cap semantics. Test zero and tiny positive
initial values at an exponent that overflows independently of the product.

## Independent Re-review Verification

All pytest commands below ran from F:/Workspace/BL-HAOS/modules/bridge with
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 and the absolute interpreter shown:

```powershell
F:/Workspace/BL-HAOS/.venv/Scripts/python.exe -m pytest -c pytest.ini tests/test_bluetooth_manager.py tests/test_auto_reconnect.py -q -k phase27_review --tb=short
F:/Workspace/BL-HAOS/.venv/Scripts/python.exe -m pytest -c pytest.ini tests/test_bluetooth_device.py tests/test_bluetooth_manager.py tests/test_auto_reconnect.py tests/test_api.py tests/test_bridge_sil.py tests/test_addon_config.py -q --tb=short
```

- Review regressions: **27 passed, 53 deselected in 0.81s**, exit 0.
- Six-file focused gate: **137 passed, 1 warning in 10.26s**, exit 0.
- Direct numerical boundary probes: all assertions passed, exit 0.
- Four explicit-reset withdrawal/replacement probes: all assertions passed,
  exit 0. Real manager/device paths with fake async boundaries only; no hardware.
- Bridge git diff --check: exit 0.

The warning is the existing Starlette/httpx TestClient deprecation. The fixer's
historical 23 failed / 4 passed -> 13 failed / 14 passed -> 27 passed progression
and 280 passed / 1 skipped full suite were read as reported evidence, not
independently re-observed historical runs. The full suite was not rerun in this
scoped re-review; its Windows skip remains the reported POSIX process-group test.

## Historical Initial-review Verification

Independently executed from F:/Workspace/BL-HAOS/modules/bridge with
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1:

```powershell
F:/Workspace/BL-HAOS/.venv/Scripts/python.exe -m pytest -c pytest.ini tests/test_bluetooth_device.py tests/test_bluetooth_manager.py tests/test_auto_reconnect.py tests/test_api.py tests/test_bridge_sil.py tests/test_addon_config.py -q --tb=short
```

Result: **110 passed, 1 warning in 9.56s**, exit 0. The warning was the existing
Starlette/httpx TestClient deprecation. No plugin-autoload crash was counted.
The targeted in-memory probe command also exited 0 after asserting the observed
defects above; that exit means the reproductions succeeded, not that the
implementation met those contracts. The executor's 253 passed / 1 skipped full
suite and historical RED/GREEN sequence were read as reported evidence, not
independently re-observed historical runs.

The reviewed code and passing regressions support one scheduled manager call,
one Device1.Connect, AlreadyConnected-only profile compatibility, actual-adapter
contention on cached records, cancellation/timeout lock release, preserved bonds,
retained busy/presence/breaker pacing and half-open history. Completion checks
protect unregistered/replaced reconnect profiles. API busy remains HTTP 409 and
operator/failed-play reset remains explicit. Manifest/runtime/changelog agree
on 0.2.68; docs acknowledge pending hardware validation. No additional defect
was established in those slices at standard depth.

## Residual Risk

Fake BlueZ proves local control flow, not real daemon cancellation, reply/signal
ordering, radio stability or playback quality. Authorized HAOS/physical-speaker
soak remains explicitly pending; this review makes no claim that the real host
is fixed. No production/test fix was made by this review. Both prior findings
are locally resolved and independently re-reviewed; playlist phases remain
paused. This update does not change the fix report's historical handoff metadata
or advance planning state.

---

_Reviewer: gsd-code-reviewer_