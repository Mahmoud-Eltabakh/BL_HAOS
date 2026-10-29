# Phase 31: Authorized HA & Provider Playback Acceptance

**Status:** human_needed; scoped host approvals recorded, provider/expiry prerequisites missing

## Current-state correction (2026-10-29)

The host and earlier actions were authorized through explicit chat checkpoints.
Integration0.2.27/bridge0.2.71 are deployed. Local MP3 audibility, custom queue
controls and idle/no-queue service gating have partial live evidence.
Genuine provider-playlist and independent disposable expired-session fixtures
remain missing; the historical planning-only statements below do not erase
those approvals or authorize new live actions.

## Discussion

This phase is the first live-acceptance gate. It requires an explicitly approved Home Assistant OS test host, a scoped playback matrix, and a record of allowed actions and stop conditions.

The project state deliberately forbids live provider or session manipulation without a separate checkpoint. This phase is therefore planning-only unless the host, identities, actions, and limits are explicitly authorized.

## Required checkpoint before any live action

- approved host identity
- selected connected speaker
- provider/session identities and limits
- stop/rollback conditions
- evidence collection method

## Non-goals

- unapproved Core restarts
- provider credential changes
- hidden browser/session manipulation
- broad host activity outside the approved cases
