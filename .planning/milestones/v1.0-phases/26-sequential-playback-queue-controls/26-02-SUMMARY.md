---
phase: 26-sequential-playback-queue-controls
plan: 02
subsystem: bridge-api
tags: [python, fastapi, native-transport, ingress, queue]
requires:
  - phase: 26-01
    provides: generation-fenced playback sessions and authenticated queue_start
provides:
  - versioned native and ingress queue controls dispatched to the existing session
  - shared allowlisted playback and queue snapshots with capability negotiation
  - synchronous queue invalidation before speaker-loss stop scheduling
affects: [26-03, native-transport, ingress-playback]
tech-stack:
  added: []
  patterns: [queue-version capability negotiation, strict control schemas, single-dispatch queue operations, allowlisted shared envelope]
key-files:
  created:
    - .planning/phases/26-sequential-playback-queue-controls/26-02-SUMMARY.md
  modified:
    - modules/bridge/backend/bl_haos/ha/player.py
    - modules/bridge/backend/bl_haos/api/routes.py
    - modules/bridge/backend/bl_haos/main.py
    - modules/bridge/tests/test_media_player.py
    - modules/bridge/tests/test_api.py
    - modules/bridge/tests/test_native_transport.py
decisions:
  - Queue contract version 1 is advertised only when the bridge exposes queue support; legacy bridge snapshots remain usable without queue fields.
  - Native queue start/navigation/mode operations dispatch once and bypass sink reconnect/re-execution.
  - Queue error display is limited to the fixed playback failure status; timeline and queue fields are independently allowlisted.
metrics:
  duration: not-measured
  completed: 2026-10-28
status: complete
actuals:
  tokens: null
  tasks: 2
  commits: 0
commits: 0
plan_head_before: 97a0130916ad8203903c6cb0e539f69b0a7c99f5
plan_head_after: 97a0130916ad8203903c6cb0e539f69b0a7c99f5
---

# Phase 26 Plan 02: Versioned Bridge Queue Controls Summary

**The existing per-speaker session now serves versioned native and ingress controls through a shared URL-free playback envelope.**

## Accomplishments

- Added bounded, strict queue-control schemas with queue contract version 1 and validated shuffle/repeat values.
- Routed native and Supervisor-ingress controls to the existing `MediaPlayerBridge` queue session; retained native bearer, trusted speaker, and A2DP sink checks.
- Prevented queue start, next, previous, shuffle, and repeat operations from entering native sink reconnect/re-execution.
- Advertised queue version on native identity and trusted speaker records only when the bridge supports `get_queue`; legacy bridge snapshots omit queue capability and queue state.
- Applied allowlists and bounds to queue and timeline snapshots. Queue errors expose only the fixed playback-failure status; URLs, media-source IDs, credentials, raw errors, and generation data are omitted.
- Invalidated the playback generation synchronously when speaker loss is detected, before scheduling asynchronous stop.
- Canonicalized BlueZ addresses during queue invalidation so case or separator differences cannot leave a queue active.
- Enforced a 2 MiB raw native-command body ceiling before JSON parsing, including chunked requests without `Content-Length`.
- Applied ordinary timeline numeric bounds to queue snapshots and retained nullable fields for invalid values.

## Verification

Working directory: `modules/bridge`.

- Queue-only selectors passed after the transport implementation; added regressions cover mixed-case BlueZ invalidation, oversized queue timeline values, raw padded JSON, and chunked bodies without `Content-Length`.
- Focused call-tracing, timeline projection, and request-body tests: 6 passed across the final focused runs.
- Full touched bridge boundary: `python -m pytest tests/test_media_player.py tests/test_api.py tests/test_native_transport.py tests/test_call_trace.py -q` — 169 passed, 1 skipped.
- VS Code diagnostics: no errors in the touched bridge implementation and test files.
- Each pytest run emitted one existing Starlette `BlockingPortal` deprecation warning.

No live HA/provider, deployment, restart, or physical playback was performed.

## Deviations from Plan

**1. Tightened shuffle validation to strict booleans.** Pydantic otherwise coerces strings such as `"yes"`; the focused test exposed this, and the request schema now rejects coerced values.

**2. Sanitized ordinary playback timeline fields as well as queue fields.** The existing timeline helper passed through arbitrary mapping keys, which could bypass the required shared-envelope allowlist. It now emits only bounded timing and validated display metadata.

**3. Added pre-parse request buffering and a hard native command body cap.** Field-level Pydantic limits cannot bound whitespace-heavy JSON before parsing. The ASGI middleware limits native command bodies to 2 MiB and replays bounded payloads to FastAPI; both declared-length and streamed bodies are tested.

**4. Tightened queue invalidation and queue timeline projection.** Address normalization now matches BlueZ casing/separator variants, and queue timeline values use the same numeric bounds as the ordinary timeline.

## Residuals

- The Home Assistant integration client/entity remains untouched as required; Plan 26-03 must advertise/use `queue_version` and disable client-side retries for ambiguous queue-start/next/previous acknowledgements before native controls are considered end-to-end single-attempt.
- Ingress command authorization relies on the existing Supervisor-protected Ingress route boundary; no live Supervisor authentication probe was authorized.
- Token actuals are recorded as `null`: pre-existing dirty edits overlap the modified routes and API test files, so an isolated Plan 26-02 diff-character count cannot be reconstructed without altering the preserved baseline.

## Git State

- No files staged; no commits created.
- Bridge HEAD remains `97a0130916ad8203903c6cb0e539f69b0a7c99f5`.
- STATE.md and ROADMAP.md now record Plan 26-02 complete and Phase 26 at 2/5 plans.
- Pre-existing dirty and untracked files were preserved.

## Self-Check: PASSED

- Summary artifact exists.
- The complete touched bridge player/API/native/tracing test set passed after final edits.
- No staging, commits, integration edits, UI changes, or release metadata changes were made.
