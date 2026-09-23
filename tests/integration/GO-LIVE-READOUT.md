# BL-HAOS Go-Live Readout

**Decision: HOLD**

**Candidate:** 0.2.23, amd64 local candidate; manifest confirms config/build
parity, while the image digest remains unavailable locally.

**Evidence directory:** `tests/integration/reports/release/` (validator: valid;
decision: HOLD; blockers: 7)

## Gate disposition

| Gate | Status | Evidence / blocker |
|---|---|---|
| REGRESSION | Fail | Collection blocked by missing `playwright` |
| SIL-CONTRACT | Pass | Focused evidence/orchestration contract suite passed |
| SIL-CONTAINER | Pass | Bridge 6 and integration 5 passed; all five reports retained |
| DEPENDENCY-AUDIT | Blocked pending tools | npm audit passed; `pip_audit` and Trivy are unavailable |
| ARCH-BUILD | Blocked: Windows-local | Run aarch64, amd64, and armv7 builder workflow in CI |
| ARTIFACT-COMPAT | Pass | Release contract passed and retained report set is complete |
| DEMO-OFFLINE | Pass | 4 deterministic demo tests passed |
| DEEP-HAOS | Blocked: missing provisioning image | `/dev/kvm` exists, but `tests/integration/config_usb` has no config image |
| LIVE-HARDWARE | Blocked: credentials/hardware unavailable | Run with approved HAOS, adapter, speaker, and media item |
| HAOS-PREFLIGHT | Blocked: HA credentials unavailable | `python query_ha.py preflight` |
| UPGRADE-ROLLBACK | Blocked: HAOS lane unavailable | Rehearse against known-good version/backup |

## Required blocker records

The machine-readable `evidence.json` must include an owner and exact rerun
command for each blocked or failed gate. Missing reports, stale evidence,
unredacted secrets, or contradictory candidate identity are evidence failures.
They are not waivers.

## Release owner sign-off

- Owner: ____________________
- Evidence reviewed at (UTC): ____________________
- Candidate version/image/architecture confirmed: `NO`
- Upgrade and rollback outcome confirmed: `NO`
- Redaction reviewed: `NO`
- Final decision: `HOLD`
- Signature: ____________________

This readout must be changed to `GO` only when the validator passes, all
blocking gates are `pass`, all required artifacts exist, and no blocker remains.