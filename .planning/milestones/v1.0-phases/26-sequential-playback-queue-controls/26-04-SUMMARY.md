---
phase: 26-sequential-playback-queue-controls
plan: 04
subsystem: queue-ui
tags: [react, ingress, home-assistant-panel, queue-controls, accessibility]
requires:
  - phase: 26-03
    provides: authenticated saved-playlist launch and capability-gated native queue state
provides:
  - explicit-target Library queue launch with active-queue replacement confirmation
  - URL-free authoritative queue snapshot display in the HA panel
  - typed ingress queue commands and sanitized playback event reconciliation
  - accessible per-speaker ingress queue controls with pending/error truth
affects: [26-05, mock-acceptance, queue-operations]
tech-stack:
  added: []
  patterns: [identity-only-panel-commands, bridge-snapshot-reconciliation, queue-payload-allowlist, explicit-user-recovery]
key-files:
  modified:
    - modules/integration/panel_ui/src/media-panel.tsx
    - modules/integration/panel_ui/src/media-panel.test.tsx
    - modules/bridge/web_ui/src/api/client.ts
    - modules/bridge/web_ui/src/api/client.test.ts
    - modules/bridge/web_ui/src/constants.ts
    - modules/bridge/web_ui/src/hooks/useBluetoothEvents.ts
    - modules/bridge/web_ui/src/hooks/useBluetoothEvents.test.tsx
    - modules/bridge/web_ui/src/components/SpeakerCard.tsx
    - modules/bridge/web_ui/src/components/SpeakerCard.test.tsx
decisions:
  - The Library sends only a saved record ID and explicit entity ID; it never receives resolved playback URLs.
  - Active queue replacement requires explicit consent; pending/error states never mutate the displayed snapshot optimistically.
  - Ingress queue state is sanitized and merged by normalized speaker address, preserving unrelated cached metadata.
  - A command error requires checking the current queue before another explicit user action; the UI does not auto-retry.
metrics:
  duration: not-measured
  completed: 2026-10-28
status: complete
actuals:
  tokens: null
  tasks: 3
  commits: 0
commits: 0
---

# Phase 26 Plan 04: HA Library and Ingress Queue UI Summary

**The HA Library and ingress SpeakerCard now control and display the bridge-owned queue without browser-side sequencing or resolved URL state.**

## Accomplishments

- Added an initially empty `Play on` selector listing only connected BL-HAOS media players in the Library and Browse views.
- Added custom-playlist and provider-shortcut launch actions that send only `record_id` and the explicitly selected `entity_id` through authenticated HA WebSocket.
- Added active-queue replacement confirmation with `Keep current queue` as default focus, Escape cancellation, focus restoration, pending status, and bounded failure copy.
- Rendered the selected speaker's current queue, item count, timeline, modes, completion, and disconnected state directly from HA-injected state; no queue is persisted or changed optimistically.
- Added a typed ingress queue command client for play, pause, stop, next, previous, shuffle, and repeat via the protected add-on route, with no native bearer header.
- Sanitized queue/playback snapshots before exposing WebSocket events and device snapshots to React; partial device events preserve unrelated cached fields and playback events update only the normalized matching speaker.
- Added per-speaker queue controls, 44px targets, pending/live status, bounded command errors, explicit Play/Next recovery, and final-item/disconnect disabling.

## Verification

- HA panel: `src/media-panel.test.tsx` — 46 passed.
- Ingress client, event hook, and SpeakerCard tests — 28 passed.
- HA panel TypeScript/Vite production build — passed to a temporary output directory.
- Ingress TypeScript/Vite production build — passed to a temporary output directory.
- VS Code diagnostics: no errors in touched UI files.
- `git -C modules/integration diff --check` — passed; `git -C modules/bridge diff --check` — passed with existing CRLF normalization warnings only.

No live Home Assistant/provider, deployment, restart, or physical playback was performed.

## Deviations from Plan

**1. Kept command errors explicitly ambiguous.** A lost acknowledgement can occur after the bridge has applied a queue command, so the UI says it could not confirm and asks the user to check the current queue before acting again. It does not claim the prior queue is unchanged or retry automatically.

**2. Kept generated bundle output untouched.** Builds were directed to temporary directories. The existing untracked `panel_static` artifact remains unchanged as required by Plan 26-05's no-generated-bundle instruction.

## Residuals

- Plan 26-05 still owns origin-restricted mock-browser acceptance, API coverage audit, and user-facing documentation.
- The generated `custom_components/bl_haos/panel_static/bl-haos-media-panel.js` remains the pre-Plan-26 source bundle until a separately authorized packaging step; it was intentionally not rewritten here.
- Live HA-shell accessibility, provider access, audible playback, deployment, and release acceptance remain unverified and unauthorized.

## Git State

- No files staged; no commits created.
- Existing dirty and untracked bridge/integration work, including `panel_static`, was preserved.
- Phase 26 remains local/mock-only; the temporary local security-threshold override remains release-ineligible.

## Self-Check: PASSED

- Panel identity-only launch, replacement consent, non-optimistic queue display, ingress command mapping, event sanitization, and card controls are covered by passing tests.
- Both touched UI test suites and both temporary-output builds passed after final edits.