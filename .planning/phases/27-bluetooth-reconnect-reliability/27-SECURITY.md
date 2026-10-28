---
phase: "27"
slug: bluetooth-reconnect-reliability
status: verified
threats_open: 0
asvs_level: 1
created: "2026-10-24"
register_authored_at_plan_time: true
scope: local-code-mitigations
hardware_soak: pending-authorized-deployment
---

# Phase 27 - Security

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| Operator/scheduler to manager | Concurrent connection callers share actual-adapter ownership | Device address and reset intent |
| Manager/device to BlueZ | Failed or busy D-Bus replies must not multiply requests | Connection and profile operations |
| Cancellation to ownership cleanup | Stopped workers release resources without reviving removed profiles | Task and profile identity |

## Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation | Status |
|-----------|----------|-----------|----------|-------------|------------|--------|
| T-27-01 | Denial of Service | Connection manager/scheduler | high | mitigate | Manager timeout and actual-adapter lock; one Connect per request; scheduler-only retry ownership, retained 10-120s pacing and 300s breaker. Canonical resolution and attachment guards prevent stale-success resets. Tests cover call counts, contention, busy/presence and half-open behavior. | closed |
| T-27-02 | Tampering | Automatic recovery | high | mitigate | Automatic reset recovery removed; scheduler invokes connect_device without reset_existing. Operator reset stays explicit and shares ownership. Pairing-preservation tests remain passing. | closed |
| T-27-03 | Denial of Service | Cancellation/timeout | medium | mitigate | Complete operation uses asyncio.timeout(30.0) and async lock cleanup. Identity-aware scheduler cancellation avoids resurrecting removed profiles. Tests block real manager operations and verify lock reuse after cancellation/timeout. | closed |
| T-27-04 | Spoofing | Busy/stale connection state | medium | mitigate | Busy is classified before profile fallback; generic errors cannot set Connected. Withdrawn/replaced records cannot report success. Existing API busy handling remains HTTP 409. | closed |
| T-27-SC | Tampering | Dependency installation | high | accept | No dependency installation, manifest changes or new dependency were introduced by this scoped fix. A future dependency change requires its own review. | closed |

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|
| R-27-SC | T-27-SC | Supply-chain change surface is absent: no installs or dependency updates in this phase. | Phase-27 plan | 2026-10-24 |

## Evidence and Limits

- The parent directly inspected manager connection/ensure_device ownership, device busy/profile handling, scheduler deadlines/cancellation and phase27 regression coverage.
- Independent code re-review is clean. Independent verifier ran the complete bridge suite: 280 passed, one existing POSIX-only skip on Windows and one dependency deprecation warning.
- The security subagent was attempted but had no filesystem tools and assessed no threats. This report records the parent's direct L1 verification, not a successful independent security-agent audit. The configured ASVS L1 workflow permits direct closure when the plan-authored register has no open mitigations.
- No claim is made about physical radio stability, daemon-side cancellation, or sustained playback. Authorized HAOS deployment and hardware soak remain pending. No live changes or commits occurred.

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-10-24 | 5 | 5 | 0 | Parent orchestrator, direct L1 code/test verification |

## Sign-Off

- [x] All plan threats have a disposition and local mitigation evidence.
- [x] Accepted risk documented.
- [x] threats_open: 0 for the scoped local register.
- [x] status: verified; hardware validation explicitly pending.

**Approval:** Local mitigations verified 2026-10-24.