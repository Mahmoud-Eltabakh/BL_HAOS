---
phase: "24"
slug: ha-media-catalog-provider-playback
status: verified
asvs_level: 1
block_on: critical
register_authored_at_plan_time: true
audit_method: direct-local-source-and-test-audit
independent_security_auditor_invoked: false
threats_total: 17
threats_closed: 15
threats_open: 0
threats_open_total: 2
accepted_risks: []
scope: local-mock-progression-only
created: "2026-10-24"
---

# Phase 24 Security: Local Evidence, Host Acceptance Pending

The verify:post security hook is enabled at ASVS L1. By explicit user direction
for mock-only progression, the blocking threshold is temporarily critical for
local phases 24-26; restore it to high before any release/deployment workflow.
This is a direct audit of the six existing PLAN threat registers and current
source/tests, not an independent specialized security-auditor invocation or a
fresh threat-discovery review. No implementation, dependency or host changes.
`threats_open` counts only open high/critical threats; total open is two.

## Trust Boundaries

| Boundary | Audited control |
| --- | --- |
| HA session -> panel | Injected hass only; no copied browser credentials or provider client. |
| Panel -> native entity -> bridge | Original opaque ID and one explicit target; Core-only resolution, internal validated URL. |
| Integration -> HTTP/frontend | Public registration, serialized owners, final served-file removal and inert-route reuse. |
| URL/metadata -> diagnostics | Fixed category logs and bounded displayed failures; no URL/component sentinels. |
| Harness -> real HA | External distinct disposable fixtures, explicit consent/attestation; no actual execution in this audit. |

## Threat Register

| Threat | Severity | Disposition | Status | Evidence and limit |
| --- | --- | --- | --- | --- |
| T-24-01 probe disclosure | medium | mitigate | CLOSED | Earlier accepted silent mechanism probe removed; recorded sanitized evidence, not fresh host access. |
| T-24-02 public auth boundary | high | mitigate | CLOSED | User-accepted Core 2026.10.3 mechanism; final 26 real public lifecycle cases pass. |
| T-24-03 panel spoofing | high | mitigate | CLOSED locally | Injected hass setter, session-generation invalidation, forbidden-boundary Vitest assertions. |
| T-24-04 target elevation | high | mitigate | CLOSED locally | Explicit connected entity, exact ID/type and single entity_id assertions. |
| T-24-05 static lifecycle | medium | mitigate | CLOSED locally | Real HTTP 200/404/reload, partial failure, multi-owner and repeated-cancellation tests. No public static unregister is claimed. |
| T-24-06 browse tampering | medium | mitigate | CLOSED locally | Documented metadata filtering, copy/nonmutation and hierarchy/capability assertions. |
| T-24-07 resolver target | high | mitigate | CLOSED locally | Original reference plus self.entity_id; real client submits once on ambiguous acknowledgement. |
| T-24-08 error disclosure | high | mitigate | CLOSED locally | Fixed HomeAssistantError, suppressed chains, resolution/command failure sentinels. |
| T-24-09 UI target/item | high | mitigate | CLOSED locally | Current-state guard, no implicit/substitute target, manual same-item/target retry tests. |
| T-24-10 DOM/error disclosure | high | mitigate | CLOSED locally | Bounded fixed errors, safe same-origin thumbnails, no raw exception reflection. Actual host leakage remains T-24-15. |
| T-24-11 ingress authority | high | mitigate | CLOSED locally | Native _top anchor only; App tests assert no attributable catalog/play API request. |
| T-24-12 integration logs | high | mitigate | CLOSED locally | Real decorated entity/client/listener caplog and traceback sentinels; accepted labels and metadata preserved internally. |
| T-24-13 route logs | high | mitigate | CLOSED locally | Authenticated HTTP and decorated-route tests, nested reconnect-false causes, internal exact URL preserved. |
| T-24-14 player logs | high | mitigate | CLOSED locally | Parser/stderr/background/fallback-title sentinels; exact URL once after -i, whitelist and no shell; unsafe URL no effects. |
| T-24-15 host auth/evidence | high | mitigate | OPEN, HUMAN NEEDED | Local external-path/reporter/expiry predicates pass, but real-session leakage and attested-fixture rejection are unobserved. Remains release-blocking; no risk acceptance inferred. |
| T-24-16 host acceptance evidence | medium | mitigate | OPEN, below high threshold | No deployed production-provider evidence, three HA-shell screenshots, physical audio or human accessibility acceptance. |
| T-24-SC dependency tampering | high | mitigate | CLOSED at planned L1 depth | Exact package pins/lock roots and existing separate SIL pins inspected; no install or network audit. Historical registry verification is recorded, not rerun. No current CVE-clean claim. |

## ASVS L1 Coverage

V2/V3: local injected-session and fail-closed controls exist and pass; real session
acceptance remains open under T-24-15. V4: one explicit target, native auth/trust,
and Core-only resolution have behavioral tests. V5: browse/URL validation,
bounded error/logging, lifecycle and docs/version assertions pass. These are
planned L1 controls, not ASVS certification or a global third-party-log sanitizer.

WR-02 was independently reproduced with current code: live HTTP 401/403/token
rejection without a probe code is `denied`; accepted-call controls win; numeric
disconnect is not expiry. Twelve independent checks and all 33 pure tests pass.
Actual expiry is NOT cryptographically established: a separately owned attested
expired fixture plus observed HA rejection is the declared evidence model. A
never-valid fixture could look the same. Shared-session state must stay untouched.

IN-02 remains informational: the existing HTTP(S) contract permits plain HTTP,
which can expose credentials in transit. Use trusted transport/network for any
future authorized run; this audit does not accept that risk or change the contract.

## Accepted Risks

None. No user risk acceptance, transfer or threat closure is claimed. The
frontmatter `threats_open: 0` counts only critical-or-higher threats under the
temporary local-mock threshold; T-24-15 remains one open high threat and the
total open threat count remains two.

## User-Approved Local Progression Exception

On 2026-10-24 the user explicitly selected "mock-only local progression" and
directed that T-24-15 and live acceptance remain open. This permits local
phase-25/26 implementation and mock-based tests to continue. It does not
override the release/security gate: no candidate may be published or deployed,
and no production requirement is claimed satisfied until T-24-15 and live
acceptance are resolved. High findings remain visible; the temporary threshold
change only prevents them from blocking local-only mock development. Restore the
threshold to high before release, live verification, or deployment. This is a
development-scope exception, not an accepted risk or ASVS production sign-off.

Specialized auditor tooling is unavailable in this verification session; no
independent security-auditor invocation is claimed. This report preserves the
pending host decision.

## Security Audit

| Date | Total | Closed locally/previously accepted | Open total | Blocking high | Result |
| --- | --- | --- | --- | --- | --- |
| 2026-10-24 | 17 | 15 | 2 | 0 (critical threshold) | Local mock progression only; T-24-15 open/high; no production security sign-off |