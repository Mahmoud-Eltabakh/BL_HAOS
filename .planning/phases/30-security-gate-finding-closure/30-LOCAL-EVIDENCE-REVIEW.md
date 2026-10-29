# Phase 30: Local Security Evidence Review

## Current-state correction (2026-10-29)

The review below is a historical2026-10-28 snapshot. Current read-only local
config inspection confirms security_block_on=high, security_enforcement=true,
security_asvs_level=1; the critical-only override described below is no longer
active. No configuration change was made during this reconciliation.

Scoped live approvals and partial evidence now exist: native401/legacy404,
local audible MP3, custom queue controls, no-queue feature gating, deployed
card layout and measured foreground contrast. These observations do not close
the findings: genuine provider-playlist, real-session leakage, independently
attested disposable expired-session rejection and full human acceptance remain
incomplete. Phase30 remains human_needed and no finding status is changed.

**Date:** 2026-10-28
**Scope:** Local, read-only review of planning artifacts. No live host, provider, session, playback, or hardware action was taken.
**Outcome:** NOT CLOSED. Phase 30 stays blocked; no finding is closed and no override is changed.

## Threshold

| Item | Current | Required | Status |
|------|---------|----------|--------|
| `.planning/config.json` `security_block_on` | `critical` | `high` | OVERRIDE ACTIVE |
| `security_enforcement` | `true` | `true` | OK |
| `security_asvs_level` | `1` | `1` | OK |

The `critical` value is the temporary local-mock override recorded in STATE.md. It must be restored to `high` before any live verification, publication, or deployment. It is not risk acceptance. The config was left unchanged here; restoring it is a reviewer-authorized step for PRD-03.

## Findings (source: v1.0 `24-SECURITY.md`)

| ID | Severity | Status | Evidence present locally | Evidence still required |
|----|----------|--------|--------------------------|-------------------------|
| T-24-15 host auth/evidence | high | OPEN, HUMAN NEEDED | External-path, reporter and expiry predicates pass in local/mock tests | Real-session leakage observation and attested-fixture rejection on a live HA host |
| T-24-16 host acceptance evidence | medium | OPEN | None beyond mock Playwright captures | Deployed production-provider evidence, three HA-shell screenshots, physical audio and human accessibility acceptance |

Both need live evidence that depends on Phases 31-33 and explicit authorization. They cannot be closed from local artifacts.

## Local gate status

- Phase 29 hosted CI (PR #1): L1 bridge, L1 integration, L2 SIL, L3 frontend and repo hygiene all passed.
- T-24-SC (dependency tampering) is closed at planned L1 depth only; it makes no current CVE-clean claim.

## Required to unblock PRD-03

1. Reviewer authorizes live evidence collection (see Phases 31-33).
2. Evidence bundle for T-24-15 and T-24-16 is collected and reviewed.
3. `security_block_on` is restored to `high` with no remaining override.
