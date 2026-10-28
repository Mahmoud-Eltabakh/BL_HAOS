---
phase: 24-ha-media-catalog-provider-playback
plan: "05"
subsystem: playback-security
tags: [url-privacy, logging, home-assistant, tdd, sil]
status: review_pending
completion_scope: local-verification-passed-independent-review-and-host-pending
completed: "2026-10-24"
duration: "Wall-clock duration not instrumented; executable timings below"
requires:
  - phase: "24-03"
    provides: "HA-owned media resolution and single-attempt command handoff"
provides:
  - "URL-free integration, native route, and player operation logging"
  - "Captured error/stderr/background and URL-derived-title regression coverage"
affects: [24-06]
requirements-completed: []
requirements-covered-locally: [PL-02, PL-03]
tech-stack:
  added: []
  patterns: [controlled-playback-errors, value-free-call-traces, exact-url-argv-handoff]
key-files:
  created:
    - .planning/phases/24-ha-media-catalog-provider-playback/24-05-SUMMARY.md
  modified:
    - modules/integration/custom_components/bl_haos/media_player.py
    - modules/integration/custom_components/bl_haos/client.py
    - modules/integration/tests/test_ha_integration_sil.py
    - modules/integration/README.md
    - modules/bridge/backend/bl_haos/api/routes.py
    - modules/bridge/backend/bl_haos/ha/player.py
    - modules/bridge/tests/test_api.py
    - modules/bridge/tests/test_media_player.py
    - modules/bridge/DOCS.md
    - .planning/phases/24-ha-media-catalog-provider-playback/24-VALIDATION.md
key-decisions:
  - "Keep accepted query-credential URLs exact internally; separately reject userinfo without changing policy"
  - "Bound messages at actual owning paths rather than add a global redaction abstraction"
  - "Leave the pre-existing panel package-contract failure untouched and report failed full gates"
  - "No commits, staging, branches, STATE updates, phase 27 edits, host access, installs, or release bump"
actuals:
  tokens: null
  tasks: 3
  commits: 0
actuals_scope: "Three original tasks plus four review remediations; latest local gates passed, independent review and host acceptance pending. Earlier failed gates remain historical; tokens unmeasured."
commits: 0
---

# Phase 24 Plan 05: Playback URL Log Privacy Summary

**Validated media URLs remain exact internal command/decoder values while operation logs, playback errors, child diagnostics, and fallback-title logs omit their contents.**

## Current Outcome

The three blockers and one warning in 24-05-REVIEW.md have local fixes with
test-first RED and immediate GREEN evidence. Latest complete gates pass:
**123 real-Core non-unit tests, 58 isolated units, 319 bridge passes with one
existing POSIX skip, and the actual root L1 runner** (319 bridge, 64 integration
unit/package, 26 frontend). Independent re-review and authorized host acceptance
remain pending; the review stays `issues_found`. No 24-06 execution or phase
completion is claimed. The original package-layout blocker below is historical:
the parent's ancestor rename/build is preserved, and all six strict Core package
checks now pass without weakening them. See the remediation addendum below.

## Original Outcome (Historical)

All three task implementations and focused checks pass locally. Plan acceptance
is **blocked**, not complete: the full Core suite and required L1 runner fail an
existing panel package string check unrelated to this plan. No failing case was
removed, skipped, weakened, or repaired outside scope. No phase or requirement
completion is claimed, and plan 24-06 was not executed.

## Implementation and Scope Extensions

1. Integration: log entity/operation/normalized media type, not the resolved URL
   or kwargs. Bound the playback-specific client HTTP warning and generic entity
   command failure. Tests use real decorated entity/client/send methods, faking
   only resolver and HTTP I/O. The call-trace wrapper already excludes values and
   needed no change. Existing single-attempt playback and non-play retry policies
   are unchanged.
2. Native route: omit payload URL and retain normalized address, volume, operation,
   and validated type. Use fixed playback failure detail rather than safe_detail
   on arbitrary URL fragments, and suppress displayed sensitive exception chains.
   Unexpected play_media exceptions now produce bounded HTTP 409 rather than an
   uncaught exception/500. Reconnect classification, reset_existing=True, attempt
   count, timing, bearer checks and trusted audio-sink checks are unchanged.
3. Player: omit execute URL, raw spawn exception text/cause, raw drained stderr,
   drain traceback, background exception text, and metadata title (which can be a
   URL-path fallback). Preserve severity/category/type correlation. Unexpected
   playback-start exceptions become bounded MediaPlayerError at play_url. No
   process argument, protocol whitelist, validation, lifecycle, or timeline change.

Client warning/error handling and metadata/stderr/background logging are narrowly
grounded scope extensions required to satisfy the plan's no-leak claim. There is
no new sanitizer, API, dependency, auth flow, schema, persistence, or trust boundary.
Documentation describes current local logging; version and changelog/release
work remain 24-06. Existing 0.2.68/phase 27 edits are preserved.

## Test Contract

New cases: **5 Core SIL + 10 route + 10 player = 25**. Existing tests remain.
Distinct synthetic host/path/query-key/query-value/user/password/token sentinels
are checked individually and as a full URL in captured logs and errors. Positive
handoff uses a valid query-credential HTTPS URL, not userinfo. Route and player
separately reject userinfo, file, and loopback URLs with no downstream effects.

Integration failures cover resolver, HTTP response, transport, and unexpected
exceptions; displayed tracebacks are checked. Route failures cover complete URL,
separated fragments, unexpected execution, reconnect exception, non-sink retry
failure, and retry exhaustion. Bridge captures both bl_haos explicit logs and
backend.bl_haos decorated traces. Player tests execute real start/stop, stderr
draining and task completion; fake process argv contains the exact URL once after
-i, fixed protocol whitelist, and no shell. Duration/fallback title remain in the
timeline, but not in logs. Child processes are fake; no live URL is fetched.

## RED and Immediate GREEN

| Check | Before Production Change | Immediately After Change |
|-------|--------------------------|--------------------------|
| Integration plan selector | 4 failed, 1 passed, 71 deselected, 1.95s | 5 passed, 71 deselected, 1.92s |
| Route plan selector, corrected trace namespace | 7 failed, 7 passed, 22 deselected, 0.94s | 14 passed, 22 deselected, 1 warning, 1.07s |
| Player plan selector | 9 failed, 8 passed, 52 deselected, 0.33s | 17 passed, 52 deselected, 0.43s |
| Additional metadata-title case, same player selector | 1 failed, 17 passed, 52 deselected, 0.33s | 18 passed, 52 deselected, 0.26s |

The initial route capture attempt had 7 failed/7 passed in 0.95s because the
trace assertion used only the explicit logger namespace. That is test-harness
evidence, not accepted as the intended leak RED. Before any route production
patch, enabling backend.bl_haos produced the recorded sentinel failures. An
initial multiline terminal invocation returned no pytest result; the identical
selection was rerun in one PowerShell invocation. Every production patch's next
action was its focused test. No defect/file exceeded three repair loops.

## Full Gates

| Gate | Actual Result |
|------|---------------|
| WSL Core non-unit suite | **107 passed, 1 failed**, 24.12s, no skips; 108 cases = 103 prior + 5 new |
| WSL isolated stub units | **58 passed**, 1.84s, no skips; no unit changes |
| Final Windows full bridge | **300 passed, 1 existing POSIX skip, 1 warning**, 12.64s; 280 baseline + 20 new passes |
| Required scripts/run-tests.ps1 -Layer L1 | **Failed**: bridge 300 passed/1 skip/1 warning, 13.11s; integration unit/package 63 passed/1 failed, 1.16s; frontend stage not reached |

Before the extra metadata case, bridge full was 299 passed/1 skip/1 warning in
14.38s. Initial L1 bridge was 299 passed/1 skip/1 warning in 12.88s, then
63 passed/1 failed in 0.78s. Both final bridge-containing gates were rerun after
the metadata production edit. Counts from overlapping runs are not summed.

Exact environments/commands and blocker details are in the 24-VALIDATION addendum.
The sole pytest warning is existing StarletteDeprecationWarning about httpx
TestClient. No package install was attempted. No missing infrastructure was
silently ignored; runtimes and runner launched successfully. L1 stopped normally
on its failed assertion, so its frontend stage is unrun, not green.

## Deferred Issues

The unchanged tests/test_package_layout.py:70 forbids the string parent. anywhere
in media-panel.tsx; an ordinary breadcrumb variable parent.media_content_id now
matches that check. This failure exists outside the files/behavior changed in
24-05. It blocks full Core and L1 acceptance. The original check and frontend
source are left intact for a separately authorized repair. No baseline checkout
or reset was performed; the failure's source/test files were not edited here.

## Constraints

No commits/staging/branches, installations/new dependencies, live-host/token access,
deployments/restarts, version bump, STATE/ROADMAP/REQUIREMENTS edits, phase 27 or
Bluetooth source edits occurred. Existing uncommitted work was not reverted.
No stubs or skipped tests were added. No release, physical playback, live-provider,
full-phase acceptance, or independent clean review is claimed.

## Self-Check: PASSED

Summary YAML, blocked status, three task implementations, zero commits, all
listed files, RED/GREEN/full-gate counts/timings, and both documentation additions
were checked by executable assertions. Editor diagnostics report no errors in
the seven touched Python files. Both module git diff --check commands pass.
This self-check validates the evidence and patch hygiene, not the blocked full
acceptance gates. There are no task commits to verify; no-commit was explicit.

## Review Remediation Addendum - 2026-10-24

This addendum supersedes the original blocked full-gate outcome and earlier
claims that normalized media labels and removed player-title logs were sufficient.
Earlier execution evidence above is retained, not rewritten as successful.

### Source-Grounded Fixes

- **CR-01:** The real entity and native route logged accepted but untrusted
  media-type labels. Only log values now map exact known types to constant
  `audio`/`playlist` categories, with `other` for everything else. Existing
  normalization, accepted labels, native model and exact URL payload stay intact.
- **CR-02:** The native listener logged complete events carrying the player's
  URL-path fallback title and provider title/artist. It now logs fixed event text
  and a validated speaker identifier, preserving all cached metadata. The
  adjacent real command logger maps operations to constant allowlisted values;
  sent operations are unchanged. Its malformed-event diagnostic formerly
  interpolated raw parser exceptions; that path now uses a fixed category/detail.
  These two client extensions are justified by additional intended sentinel RED,
  not a global error-hiding policy. Unrelated command errors are not suppressed.
- **CR-03:** The player reflected raw urlsplit text and chained port errors.
  Validation now selects only fixed policy messages and raises `from None`.
  Neither raw parser text nor nested causes reach displayed tracebacks. Validator
  acceptance/rejection policy itself is unchanged, with zero sink/process calls
  for rejected URLs and exact one-argument ffmpeg handoff for accepted URLs.
- **WR-01:** Reconnect returning false now explicitly suppresses the original
  playback context on its existing bounded HTTP 409. Nested-cause traceback
  assertions exercise the decorated route as well as authenticated public HTTP;
  reset_existing=True, one initial execution and no false-return retry remain.

### Intended RED and Immediate GREEN

All runs used the main checkout, not a worktree. Each production edit's next
action was its focused executable check. Each defect passed its first production
repair; no defect/file exceeded the three-repair limit.

| Finding / Real Boundary | Intended RED Before Production | Immediate GREEN |
|------------------------|--------------------------------|-----------------|
| CR-01 Core entity/client, accepted sensitive labels | 2 failed, 84 deselected, 1.31s | 15 passed, 71 deselected, 4.82s |
| CR-01 authenticated HTTP route | 2 failed, 48 deselected, 1.01s | 21 passed, 29 deselected, 1.24s |
| CR-02 listener/command/parser | 4 failed, 1 passed, 86 deselected, 0.97s | 5 passed, 86 deselected, 0.70s |
| CR-03 player validation and formatted causes | 2 failed, 3 passed, 67 deselected, 0.32s | 12 passed, 60 deselected, 0.26s |
| WR-01 reconnect false and formatted nested causes | 3 failed, 50 deselected, 1.05s | 3 passed, 50 deselected, 0.71s |

An earlier CR-02 run before the added parser regression also produced intended
RED: 3 failed, 1 passed, 86 deselected, 1.34s. All failures were sentinel leaks,
not test construction or environment failures. CR-01 GREEN widened to all
success/failure variants; CR-03 GREEN also ran existing exact-URL process cases.

### Latest Complete Gates

| Gate | Actual Result |
|------|---------------|
| WSL real Core 2026.10.3, non-units only | **123 passed**, 28.13s, zero skips: 91 native SIL + 26 lifecycle + 6 strict package |
| WSL isolated stub units, separate process | **58 passed**, 1.27s, zero skips |
| Windows full bridge, plugin autoload disabled | **319 passed, 1 existing POSIX skip, 1 warning**, 12.61s |
| Root scripts/run-tests.ps1 -Layer L1 | **Passed**: bridge 319 passed/1 skip/1 warning, 12.48s; integration unit/package 64 passed, 0.67s; frontend 26 passed across 6 files, 1.22s |
| Editor diagnostics, seven changed Python files | No errors |
| Both module git diff --check commands | Passed |

New coverage relative to the original 24-05 run is 15 Core and 19 bridge cases;
overlapping focused/full/L1 counts are not summed. The only warning remains the
existing Starlette httpx TestClient deprecation. No new environment blocker or
installation occurred. Exact commands are appended to 24-VALIDATION.md.

No review status, strict package test, frontend/build, STATE, Bluetooth/phase 27,
release/version, dependency, branch, staging or commit was changed. No live
action, provider fetch or decoder process occurred. Scope is seven existing
Python files and these two existing evidence artifacts. No clean-review or
physical-playback acceptance claim is made.