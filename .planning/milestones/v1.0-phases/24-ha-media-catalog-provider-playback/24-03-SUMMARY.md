---
phase: 24-ha-media-catalog-provider-playback
plan: "03"
subsystem: integration
tags: [home-assistant, browse-media, audio, playlists, resolution, sil]
status: complete
completion_scope: local-plan-only
completed: "2026-10-24"
duration: "Wall-clock duration not captured; actual executable timings recorded below"
requires:
  - phase: "24-02"
    provides: "Approved and locally reviewed injected-hass panel tracer"
provides:
  - "Metadata-preserving recursive native audio/playlist browse policy"
  - "One-target opaque-reference resolution with bounded failure messages and no fallback"
affects: [24-04, 24-05, 24-06]
requirements-completed: []
requirements-covered-locally: [PL-01, PL-02]
tech-stack:
  added: []
  patterns: ["copy-based BrowseMedia filtering", "Core resolution for self.entity_id", "fixed operator errors with suppressed exception context"]
key-files:
  created:
    - .planning/phases/24-ha-media-catalog-provider-playback/24-03-SUMMARY.md
  modified:
    - modules/integration/custom_components/bl_haos/media_player.py
    - modules/integration/custom_components/bl_haos/client.py
    - modules/integration/tests/test_ha_integration_sil.py
    - modules/integration/tests/unit/test_client_commands.py
    - modules/integration/README.md
    - .planning/phases/24-ha-media-catalog-provider-playback/24-VALIDATION.md
key-decisions:
  - "Retain all expandable provider nodes without guessing from names, IDs, or URL shapes"
  - "Preserve every non-child BrowseMedia field and do not mutate the Core result"
  - "Provider playlists stay one opaque HA-owned reference; enqueue remains rejected"
  - "Validate source resolver output as HTTP(S) or HA-relative media before submission"
  - "Do not execute later plans, modify phase state, stage, commit, install, or contact the live host"
actuals:
  tokens: 6249
  tasks: 2
  commits: 0
actuals_scope: "Ceiling(chars/4) over the owned media_player/SIL git diff plus only this run's README addition; excludes prior README work and planning prose"
plan_repository: modules/integration
plan_head_before: f428a2a4df69c29080ea1515c5b706cd1af9f8a2
plan_head_after: f428a2a4df69c29080ea1515c5b706cd1af9f8a2
commits: 0
coverage:
  - id: D1
    description: "Native browse filters supported leaves without altering hierarchy or display/search/play metadata"
    requirement: PL-01
    verification:
      - kind: integration
        ref: "tests/test_ha_integration_sil.py: native_audio_browse regressions, exact Core 2026.10.3"
        status: pass
    human_judgment: false
  - id: D2
    description: "Original item/playlist reference resolves for one explicit connected entity; failed resolution sends no command"
    requirement: PL-02
    verification:
      - kind: integration
        ref: "tests/test_ha_integration_sil.py: native_play_media regressions, exact Core 2026.10.3"
        status: pass
    human_judgment: false
  - id: D3
    description: "Configured real-provider metadata and audible playback on a physical speaker"
    verification: []
    human_judgment: true
    rationale: "Requires separately authorized real-provider/HAOS host validation; not established by local Core fixtures"
---

# Phase 24 Plan 03: Native Audio Catalog and Opaque Playback Summary

**Copy-based audio/playlist BrowseMedia filtering preserves HA metadata and traversable hierarchy, with one-target opaque resolution and bounded playback failures.**

## Scope and Inventory

Both plan tasks are implemented and verified locally. This is not whole-phase,
requirement, deployment, or physical-playback acceptance. The accepted plan 24-01
and locally reviewed 24-02 work were prerequisites, not rerun host checkpoints.

- `modules/integration/custom_components/bl_haos/media_player.py`: recursive metadata policy, target guards, resolution-output validation, and bounded errors.
- `modules/integration/tests/test_ha_integration_sil.py`: initially 43 additional cases; CR-01 replaces one above-client mock case with eight real-client HTTP cases, now 71 native SIL cases total.
- `modules/integration/custom_components/bl_haos/client.py`: CR-01 restricts play_media to one attempt without changing its signature or other command policies.
- `modules/integration/tests/unit/test_client_commands.py`: four ambiguous-playback HTTP cases; existing retry expectation intentionally moved from play_media to pause.
- `modules/integration/README.md`: one concise native-browse/playback paragraph; prior panel/lifecycle documentation preserved.
- This SUMMARY and `24-VALIDATION.md`: execution evidence only.

CR-01 intentionally updates the old playback-retry unit expectation; no shared
fixture or unit import-stub contract changed. Existing lifecycle fixes, panel assets,
phase 27 work, other module changes and parent planning edits remain untouched.
No new dependencies, installs, staging, commits, branches, live-host/token access,
deployment, restart, or pairing operation occurred. STATE, ROADMAP and REQUIREMENTS
were not edited. Plans 24-04/05/06 were not executed.

## Implementation

The browse policy uses Core media classes/types and `audio/*` MIME metadata.
Audio-like playable entries and playlist classes/types survive; every expandable
node remains traversable, including unknown, empty and video-labeled containers.
Unsupported video/image/unknown leaves are removed from already returned children,
not by fetching or guessing provider content. Direct unsupported leaf browsing
raises a bounded HomeAssistantError. No provider names, IDs, extensions or URL
shapes determine browse support.

Shallow copies retain titles, thumbnails, opaque IDs, class/type, can_play,
can_expand, can_search, search_media_classes, children_media_class and not_shown;
only child sequences are filtered recursively. The original Core objects are not
mutated. This intentionally preserves Core's not_shown value rather than
inventing a different count. Search is never synthesized. No playlist expansion,
track fetching, queue state or sequential playback was introduced.

Playback still invokes Core async_resolve_media with the original ID and
self.entity_id. It requires the selected entity to be connected/available before
resolution and rechecks availability after awaiting it. A valid resolution sends
one existing client play_media command to that speaker. Empty/malformed/unresolved
source results are rejected before submission using the standard URL parser;
Core still processes legitimate HTTP(S)/HA-relative media. Existing direct-URL
handling is retained, not introduced as a fallback. Enqueue remains rejected.

Denied, expired, unavailable, timeout, unresolvable and malformed resolution errors
produce a fixed HomeAssistantError without raw exception text or displayed chained
context. Command submission failures also have fixed bounded text and no retry.
Cancellation propagates. There is no fallback, skip, second target, implicit target
or audible-playback claim. A submission failure means one attempted command, not
proof that a remote command was or was not applied.

## TDD Evidence

All production edits were preceded by relevant failing behavior checks and
immediately followed by the identical focused check. Full commands and results
are in the plan 24-03 addendum of `24-VALIDATION.md`.

| Stage | Observed Result | Semantic Assessment |
|-------|-----------------|---------------------|
| Browse RED | 2 failed, 21 deselected, 1.16s | Both entity cases retained three unsupported leaves; assertion-level intended failure |
| Immediate browse GREEN | 2 passed, 21 deselected, 0.98s | Same check after the first production edit |
| Initial playback attempt | 10 failed, 8 passed, 23 deselected, 4.16s | Five cases had an invalid Unauthorized constructor; not accepted as complete RED evidence |
| Corrected playback RED | 10 failed, 8 passed, 23 deselected, 5.56s | Raw authorization/provider errors, malformed resolver output, missing target guards, and URL-bearing command error reproduced |
| Immediate playback GREEN | 18 passed, 23 deselected, 6.49s | Same check after bounded errors/target guards |
| Resolution-validity RED | 4 failed, 22 passed, 23 deselected, 8.18s | Nonempty opaque/non-URL/missing-host/file results wrongly submitted a command; intended DID NOT RAISE assertions |
| Immediate validity GREEN | 26 passed, 23 deselected, 8.45s | Same check after source-result validation |
| Compatibility additions | 15 passed, 49 deselected, 2.13s | Audio classes/types, direct unsupported leaves and actual Core relative-URL processing |

No production repair iteration failed its immediate check. One test-construction
repair was needed before the accepted playback RED. Core signature introspection
also hit a deferred-annotation NameError; constructor source inspection supplied
the actual signature instead. No installed package was modified.

## Original Verification (Historical)

Every Python gate used Ubuntu WSL, cwd
`/mnt/f/Workspace/BL-HAOS/modules/integration`, interpreter
`/home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python`, BLHAOS_RUN_SIL=1,
`-p asyncio --asyncio-mode=auto`. Observed runtime: Python 3.14.4, Core 2026.10.3,
helper 0.13.374, pytest 9.0.3. Unit plugin autoload was disabled in its separate
process; real Core and stub units never shared a Python process.

| Gate | Final Result |
|------|--------------|
| Plan browse selection | 24 passed, 40 deselected, 3.75s |
| Plan playback selection | 28 passed, 36 deselected, 7.39s |
| Full native integration SIL file | 64 passed, 13.38s |
| Full real-Core SIL/lifecycle/package, ignoring tests/unit | 96 passed, 20.30s |
| Separate isolated units | 54 passed, 2.26s |
| README/package compatibility | 6 passed, 0.42s |
| Editor diagnostics | No errors in either touched Python file |
| Integration diff whitespace | Passed |

Original full-suite total was **150 passing tests across two processes**, with zero
skips or teardown errors. Subset runs are not added again to that total. The Core
suite includes 64 native SIL, 26 public lifecycle and six package cases. These are
fixture-backed provider results, not live-provider or physical-audio observations.

## CR-01 Transport Remediation and Latest Verification

The review exposed that the original no-retry coverage mocked async_command above
its retry loop. The user authorized the nearest root-cause scope expansion into
client.py. Only play_media now has one transport attempt; the public signature,
payload, reads, and unrelated state-command retry policies are unchanged.

Before production changes, four real-client fake-HTTP unit cases ran immediately:
**2 failed, 2 passed, 15 deselected in 0.54s**. A first applied POST followed by
ServerDisconnectedError either silently succeeded on a second POST or submitted
twice before failing. Timeout and generic ClientError controls already passed.
The next production edit changed the attempt budget; its very next action reran
the identical gate: **4 passed, 15 deselected in 0.38s**. No repair loop was needed.

The Core failure test now keeps the entity, client command loop and send method
real, stubbing only HTTP I/O and provider resolution/URL processing. Eight cases
cover both selected entities, disconnect then hypothetical success, persistent
disconnect, timeout and generic ClientError. Each verifies one untouched original
reference resolution, one target POST recorded applied before response loss, no
retry sleep, and the exact bounded HomeAssistantError with suppressed context and
no URL/credentials. The old unit retry contract intentionally tests pause instead
of play_media, retaining two attempts and one retry sleep for a state command.

All gates ran in the **main checkout**, Ubuntu WSL, existing Python 3.14.4 / Core
2026.10.3 environment. Core and stub units ran in separate Python processes.

| Latest Gate | Observed Result |
|-------------|-----------------|
| Immediate identical unit RED / GREEN | 2 failed, 2 passed / 4 passed; 0.54s / 0.38s |
| Real-Core full-path transport slice | 8 passed, 63 deselected, 2.35s |
| Client unit file | 19 passed, 1.06s |
| Full real-Core non-unit gate | **103 passed**, 18.29s; no skips/teardown errors |
| Separate complete stub-unit gate | **58 passed**, 1.29s; no skips |
| Editor diagnostics, three touched Python files | No errors |

Latest full total: **161 passing tests across two processes**, not summed subset
runs. Core is 71 native SIL + 26 lifecycle + 6 package (96 baseline + 7); units
are 54 baseline + 4. Exact commands are in the CR-01 validation addendum.
CR-01 is implemented locally; independent re-review is pending and
24-03-REVIEW.md remains `issues_found`. No live-provider/audio acceptance or
full-path operational-log redaction is claimed. No staging, commits, branches,
installs, deployment, live hosts, STATE updates or phase 27 changes occurred.

## Deviations and Remaining Acceptance

- **User execution override:** Work is intentionally uncommitted. No atomic RED/GREEN or metadata commits are claimed; the unchanged integration revision is recorded above. Phase state updates and later-plan execution were explicitly prohibited.
- **CR-01 root-cause scope:** client.py and its existing command unit file were added to the original plan's scope to enforce the one-submission contract below the retry loop. No new test file, shared stub change, or unrelated retry-policy change was needed.
- **Rule 2 - Resolution validity:** Added malformed source-result validation, explicit availability checks including loss during resolution, and cancellation regression coverage as correctness requirements for valid one-target submission.
- **Documentation sync:** Added only the README paragraph needed to describe actual new native behavior.
- **Plan 24-05 boundary:** Existing integration/client/bridge URL-bearing operational logs were not refactored. Fixed errors are verified now; this is not full-path URL-log redaction or PL-03 security sign-off.
- **Plan 24-06 boundary:** Configured provider metadata, real denied/expired sessions, production panel flows, accessibility/viewport acceptance and actual physical-speaker playback still need separately authorized host validation. No audible playback is claimed.

No new endpoint, authentication mechanism, credential persistence or schema trust
boundary was introduced. Stub scanning found no TODO/FIXME/placeholder markers in
the touched code. No implementation stub or skipped test blocks this local plan.

## Self-Check: PASSED

The seven inventory files exist, scoped Python diagnostics and executable gates
passed, and integration HEAD remains the recorded prerequisite revision. No
commit, requirement completion or whole-phase completion is claimed. Existing
out-of-scope changes remain present and unmodified by this execution.