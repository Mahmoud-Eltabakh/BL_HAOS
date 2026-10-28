# Phase 31: Authorized HA & Provider Playback Acceptance

**Status:** blocked pending explicit host authorization

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
