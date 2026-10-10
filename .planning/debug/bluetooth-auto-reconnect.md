---
status: fixing
trigger: "The Bluetooth device disconnects and does not reconnect."
created: "2026-10-10"
updated: "2026-10-10"
---

# Bluetooth Auto-Reconnect Debug Session

## Symptoms

- Expected: a previously paired/trusted BL-HAOS speaker reconnects after a
  Bluetooth link dropout without requiring pairing mode again.
- Actual: auto-connect returns `br-connection-unknown`; stale recovery then logs
  `Device with address not found`.
- Live evidence: HAOS `192.168.1.18`, BL-HAOS 0.2.63. Logs show disconnect,
  two failed reconnects, stale recovery, then pair/reconnect failure. MAC is
  intentionally redacted. User reports the speaker is powered on and in range.
- Latest read-only BL-HAOS API snapshot: Logitech adapter `paired=true`,
  `trusted=true`, `connected=true`, playback idle. No live reconnect was triggered.

## Root Cause

`_recover_stale_device` called `BluetoothManager.remove_device`, which clears
BlueZ trust/bond and removes the cached object, then called `pair_and_trust`.
When BlueZ no longer advertised the device (or the speaker was not in pairing
mode), recovery failed with `Device not found` and left it unpaired. Existing
`connect_device` already refreshes stale Device1 proxies and supports an explicit
link reset without deleting the bond.

## Fix And Verification

- Replaced stale recovery's remove/unpair/re-pair sequence with
  `connect_device(address, reset_existing=True)`.
- Added a regression that simulates removal erasing cached presence/trust and
  asserts recovery instead preserves trust and performs the reset-connect.
- Focused regression passes.
- Reconnect + Bluetooth manager suites: 32 passed.
- Full Bridge suite from `modules/bridge`: 207 passed, 1 skipped, 0 failed.
- Ruff unavailable in the local venv; source/test editor diagnostics are clean.

## Live Deployment

- BL-HAOS 0.2.64 source, changelog and docs were committed as
  `79e05e32926207e9031cb4f2870f3c1da5ae0764` and pushed to `main`.
- GitHub Actions Bridge release gates passed, but release run
  `38089458361` failed in the shared npm dependency-audit step before publishing
  any architecture image; other architecture jobs were cancelled.
- The authorized semver-safe `npm audit fix` updated only
  `source-map-js` 1.2.1 -> 1.2.2. Re-scan now reports 10 findings: 2 critical,
  5 high, 3 moderate. Frontend tests pass (24/24) and frontend build passes.
- The safe lockfile-only patch was committed as `6a87c049ef6fc1411ea54335b7a645269272456d`
  and pushed. GitHub Actions run `38089458361` is still in its release-gates job.
- Remaining fixable findings require major upgrades (Vitest 4.1.11+/5 and
  Tailwind 4.3.3); these are not authorized by the user's approval of only safe
  targeted dependency updates. Stop before major migration pending approval.
- Docker Desktop's Linux engine is unavailable locally; the live update must use
  the GitHub Actions publish workflow after the audit gate is cleared.
- The live add-on remains 0.2.63; no 0.2.64 image was published, updated or
  restarted. Latest read-only API snapshot shows the Logitech adapter connected.
- Restarting the add-on briefly interrupts Bluetooth audio.
- Do not force another reconnect now: the latest read-only snapshot shows the
  Logitech adapter connected. Pairing may need a one-time manual retry only if
  BlueZ reports its bond is actually gone.

## Current Focus

- hypothesis: confirmed; recovery was deleting the bond before rediscovery.
- test: focused regression plus full bridge tests above.
- expecting: new release preserves the existing pairing across stale-link
  recovery; verify through live add-on logs after update.
- next_action: let run `38089458361` finish. If its audit fails on the same
  remaining CVEs, wait for explicit approval before the Vitest/Tailwind major
  migration; do not restart the current add-on. Parent repo was not pushed because
  its branch has four pre-existing unpushed commits and staged archive changes.
