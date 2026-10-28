---
phase: 24-ha-media-catalog-provider-playback
plan: "05"
reviewed: 2026-10-24T16:21:52Z
depth: deep
files_reviewed: 11
files_reviewed_list:
  - modules/integration/custom_components/bl_haos/media_player.py
  - modules/integration/custom_components/bl_haos/client.py
  - modules/integration/custom_components/bl_haos/call_trace.py
  - modules/integration/tests/test_ha_integration_sil.py
  - modules/integration/tests/conftest.py
  - modules/bridge/backend/bl_haos/api/routes.py
  - modules/bridge/backend/bl_haos/ha/player.py
  - modules/bridge/backend/bl_haos/health.py
  - modules/bridge/backend/bl_haos/call_trace.py
  - modules/bridge/tests/test_api.py
  - modules/bridge/tests/test_media_player.py
findings:
  critical: 0
  warning: 0
  info: 0
  total: 0
status: clean
---

# Phase 24 Plan 05: Code Review Report

## Summary

**Clean gate for the original three blockers and one warning.** Independently
repeated their precise sentinel/traceback reproductions against the current
decorated methods, plus minimal adjacent negative cases. All four are resolved;
no remaining finding was demonstrated within this explicitly bounded scope.
This is not a full security audit or a new phase-wide acceptance decision.

## Narrative Findings (AI reviewer)

No open findings in the requested re-review scope.

| Original Finding | Disposition | Independently Observed Evidence |
| --- | --- | --- |
| CR-01 (BLOCKER) | Resolved | Entity and native route log fixed `audio`, `playlist`, or `other` categories. Original host/path-shaped label and standalone token remain accepted and unchanged internally, without appearing in logs. |
| CR-02 (BLOCKER) | Resolved | Native WebSocket logs only the processed address/rejection marker. Real URL-fallback title and URL-bearing title/artist remain intact in the cache and listener notifications, without appearing in logs. |
| CR-03 (BLOCKER) | Resolved | Both original parser inputs produce fixed `MediaPlayerError` messages, `__suppress_context__ == True`, no explicit cause, and sentinel-free formatted tracebacks/logs before sink/process calls. |
| WR-01 (WARNING) | Resolved | Reconnect returning false produces the fixed 409 detail with suppressed nested context. Exception, retry-error, exhaustion and successful-recovery controls preserve reconnect arguments and attempt counts. |

## Independent Re-Review Evidence

Executed on 2026-10-24, using existing environments only:

- WSL Ubuntu: verified Core **2026.10.3**, helper **0.13.374**, Python
  **3.14.4**. Focused integration SIL selector: **18 passed, 73 deselected**,
  6.19s.
- Windows: Python **3.14.7**, pytest **9.0.3**, plugin autoload disabled.
  Focused bridge selector: **51 passed, 74 deselected**, 1.80s. One existing
  Starlette TestClient deprecation warning.
- Separate Windows integration unit invocation, also autoload-isolated:
  **58 passed**, 0.67s. Integration units were not mixed with bridge collection.

Independent stdin-only probes, separate from the checked-in regression tests:

1. **CR-01:** Used the original URL
  `https://labelhostsentinel.example/labelpathsentinel?token=labeltokensentinel`
  with `labelhostsentinel.example/labelpathsentinel` and `labeltokensentinel`
  labels through both the real entity/client and authenticated decorated route.
  Added only `audio/mpeg`, `music`, `playlist`, and `None` category controls.
  All six passed in each runtime: exact URL and normalized media-type payload
  preserved, one command handoff, no reconnect on success, no component sentinel
  in DEBUG logs. Absent/wrong bearer, untrusted sink, and an invalid full-URL
  media label still reject without command/reconnect side effects.
2. **CR-02:** Ran the real `_start_timeline`/`get_timeline` with the original
  `https://streamhostsentinel.example/pathsecret123.mp3?token=querysecret123`.
  Confirmed fallback `pathsecret123`, then delivered it and a URL-bearing
  title/artist through finite fake native WebSocket I/O to the real listener.
  Both timeline variants reached cache/listeners unchanged. No host, path,
  token, title or artist sentinel appeared in DEBUG capture. Invalid address,
  ignored event and null data controls did not leak payloads or insert an
  invalid cache entry. No real sink/process collaborator was awaited.
3. **CR-03:** Repeated exactly
  `https://[malformedhostsentinel]/path?token=malformedtokensentinel` and
  `https://valid.example:porttokensentinel/path`. Added credential-bearing,
  `file:` and loopback URL rejection controls. All five rejected before sink
  lookup/process creation, with fixed policy messages and suppressed context;
  no sentinel appeared in `traceback.format_exception(error)` or DEBUG logs.
4. **WR-01:** Injected a URL-bearing sink-unavailable `MediaPlayerError` with a
  nested URL-bearing cause into the decorated authenticated route. Tested
  reconnect false, reconnect exception, non-sink retry error, exhausted retries,
  and successful recovery. All passed; failure tracebacks/logs remained bounded.
  Reconnect was exactly once with `reset_existing=True`. Execute counts were
  one for false/exception, two for retry-error/recovery, and
  `1 + A2DP_SINK_RETRY_ATTEMPTS` for exhaustion; every attempt retained the exact
  original URL. Retry interval was patched to zero only in the probe.

Entity HTTP, transport, unexpected-exception and provider-resolution failure
controls also passed with sentinel-free displayed chains and one submission
(zero for resolution failure). The focused player tests additionally exercised
the real process-argument builder, preserving the protocol whitelist, exact
single URL argument, and non-shell execution. Both value-free trace wrappers
were inspected; they do not log arguments, return values, exception messages,
or tracebacks. The inspected validator/auth/trust/reconnect code and controls
show no relaxation introduced by these logging fixes. This does not assert
coverage of unrelated inputs or policies.

Commands independently rerun:

```powershell
wsl.exe -d Ubuntu --cd /mnt/f/Workspace/BL-HAOS/modules/integration env BLHAOS_RUN_SIL=1 PYTHONDONTWRITEBYTECODE=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests/test_ha_integration_sil.py -q -p asyncio --asyncio-mode=auto -p no:cacheprovider -k '(play_media and (log or redact)) or (native_websocket and redact)' --tb=short --show-capture=no
```

Windows commands used `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` and
`PYTHONDONTWRITEBYTECODE=1`, each from its respective module directory:

```powershell
& F:/Workspace/BL-HAOS/.venv/Scripts/python.exe -B -m pytest -c pytest.ini tests/test_api.py tests/test_media_player.py -q -p asyncio --asyncio-mode=auto -p no:cacheprovider -k '(native and (play or log or redact)) or url or redact' --tb=short --show-capture=no
& F:/Workspace/BL-HAOS/.venv/Scripts/python.exe -B -m pytest -c pytest.ini tests/unit -q -p asyncio --asyncio-mode=auto -p no:cacheprovider --tb=short --show-capture=no
```

The independent probes were piped to each existing interpreter with `-B -`;
no probe source or test file was created. Fixer-reported broad results (Core
123, bridge 319 plus one expected skip, root L1 pass, frontend 26) were not
independently rerun and are not claimed as evidence for this gate. Only this
review artifact was edited. No source/test/STATE edits, installation, staging,
commit, deployment, restart, real network/provider, Bluetooth or decoder action
was performed.

## Historical Review (Superseded)

Original review: **2026-10-24T16:10:06Z**, depth **deep**, nine files,
**3 blockers / 1 warning**, `status: issues_found`. Its findings and reproduction
evidence below are retained as history, not current open findings. The original
nine-file scope included the four implementation files, three regression-test
files, integration README and bridge DOCS. The current re-review inspected only
the four finding paths and their directly relevant helpers/tests listed above.

### Original Summary

Reviewed the actual working-tree implementation and captured-log tests against
24-05-PLAN.md and 24-05-SUMMARY.md. Scope is the three playback logging paths,
the client logging extension, bounded errors, and unchanged validated internal
handoff. Repository root for all file references is F:/Workspace/BL-HAOS.

The explicit URL fields, raw decoder stderr, spawn exception text, background
exception text, and player metadata-title log were removed as described.
However, two logging paths still disclose URL components, and the player
validation error boundary can still display URL-derived text. A fourth finding
concerns an unsuppressed reconnect exception chain, not a leaking HTTP response.
The privacy contract is not yet satisfied.

## Historical Narrative Findings (AI reviewer)

## Critical Issues

### CR-01: BLOCKER - Validated media-type labels still disclose URL components

**Files:** [media_player.py:469](modules/integration/custom_components/bl_haos/media_player.py#L469), [routes.py:363](modules/bridge/backend/bl_haos/api/routes.py#L363)

**Issue:** Both replacement log records print the caller/provider's media type.
The existing token grammar permits dots, hyphens, underscores, and one slash;
it does not establish that the string is a non-sensitive media category.
`labelhostsentinel.example/labelpathsentinel` passes both normalizers unchanged.
A provider MIME label or service/native caller can therefore put URL host/path
material, or a bare credential token, in the supposedly safe correlation field.
An entire `https://...` URL is rejected by this grammar; the demonstrated leak is
its components, which the plan also explicitly forbids.

**Reproduction:** With DEBUG capture enabled, call the real entity with
`media_type="labelhostsentinel.example/labelpathsentinel"` and
`media_id="https://labelhostsentinel.example/labelpathsentinel?token=labeltokensentinel"`.
Use the existing fake HTTP session and patch only Core URL processing to return
the same URL. The actual client sends that exact URL once. Separately construct
`NativeCommandRequest(operation="play_media", url=url, media_type=media_type)`
and call the decorated native route with an authenticated fake request and
trusted sink. The real route accepts the model and forwards the exact URL once.
Observed records from the in-memory probes:

```text
[BL-HAOS] Entity media_player.review_speaker resolving play_media: media_type=labelhostsentinel.example/labelpathsentinel
Executing media player command: play_media for 10:22:33:44:55:66 (volume: None, media_type: labelhostsentinel.example/labelpathsentinel)
```

**Fix:** Keep the existing accepted media type and URL unchanged in the command
payload. Log only a fixed, known category mapping, with `other`/`unknown` for
unrecognized values, or omit the type value. Do not tighten the playback
validator to solve a logging problem. Extend the entity and route caplog tests
with accepted URL-shaped labels and standalone token labels; assert component
absence and unchanged internal payloads. Current tests always use `audio/mpeg`.

### CR-02: BLOCKER - Native WebSocket logging reintroduces URL-derived titles

**File:** [client.py:438](modules/integration/custom_components/bl_haos/client.py#L438)

**Related path:** [player.py:376](modules/bridge/backend/bl_haos/ha/player.py#L376) -> [main.py:212](modules/bridge/backend/bl_haos/main.py#L212) -> native WebSocket -> client log.

**Issue:** The player intentionally retains its URL-path fallback title in the
timeline. Playback state publication includes that timeline in the native
speaker event. The integration then logs the complete event payload, including
`playback.title` and provider-controlled `artist`. Removing the player's own
metadata-title log does not prevent the same value being logged downstream.
This happens during ordinary successful playback when DEBUG is enabled; it does
not require malicious metadata or an exception.

**Reproduction:** In the approved WSL Core runtime, call the real bridge
`_start_timeline(address, "https://streamhostsentinel.example/pathsecret123.mp3?token=querysecret123")`
and `get_timeline(address)`. Merge that timeline into an existing valid speaker
fixture. Feed it as a `speaker_updated` message through a finite fake WebSocket
to the real decorated `BLHAOSClient._async_listen`, faking only HTTP/WebSocket
I/O. The cached title remains correct, but DEBUG capture contains:

```text
Received native speaker update event: {'event': 'speaker_updated', 'data': {..., 'playback': {..., 'title': 'pathsecret123', 'artist': None}}}
```

The probe confirmed `fallback_title == "pathsecret123"` and
`"pathsecret123" in captured_logs`. The existing player metadata test proves the
fallback title remains in the timeline, but the integration privacy test never
feeds that timeline back through the event listener.

**Fix:** Replace full native-event payload logging with fixed event/operation
metadata and a validated speaker identifier. Keep title/artist and native event
contents intact for Home Assistant display. Add a captured-log test that feeds a
real URL-derived fallback title through the native event path; also cover
URL/token-bearing embedded title/artist values.

### CR-03: BLOCKER - Player validation errors retain raw parser messages and causes

**File:** [player.py:577](modules/bridge/backend/bl_haos/ha/player.py#L577)

**Issue:** The player assumes every validator `ValueError` is already bounded
and safe, then reflects `str(error)` and chains the original error. That is not
true for parser errors. `urlsplit` can raise an input-bearing error for bracketed
hosts; the explicit port check wraps an input-bearing parser error as a safe
message but retains it as a cause. The player's outer chain exposes both.
This fails the plan's bounded player-error and nested-cause requirements even
though no sink lookup or subprocess occurs.

**Reproduction:** Run the following against the real player with DEBUG enabled
and `AsyncMock` sink/process collaborators; no process or network is used:

```python
for url in (
    "https://[malformedhostsentinel]/path?token=malformedtokensentinel",
    "https://valid.example:porttokensentinel/path",
):
    try:
        await bridge.play_url("10:22:33:44:55:66", url)
    except MediaPlayerError as error:
        displayed = "".join(traceback.format_exception(error))
        print(str(error), "sentinel" in displayed)
```

Observed on Windows Python 3.14.7:

```text
'malformedhostsentinel' does not appear to be an IPv4 or IPv6 address True
Media URL must be a safe HTTP(S) URL True
```

Both collaborators remained unawaited. In the second case, the top-level message
is safe but its displayed cause includes `porttokensentinel`. Native HTTP model
validation currently returns a fixed 422 and masks these cases; this finding is
specifically the direct player error boundary that the plan and player tests
claim to cover, not an HTTP-response disclosure or SSRF bypass.

**Fix:** At the player validation boundary, preserve only the known fixed policy
reasons, use a fixed fallback for unexpected parser errors, and raise the bounded
`MediaPlayerError` with `from None`. Preserve URL rejection policy and
no-side-effect behavior. Extend the existing rejected-URL caplog/traceback cases
with malformed bracketed hosts and nonnumeric ports, checking each component
sentinel rather than only the top-level message.

## Warnings

### WR-01: WARNING - Reconnect returning false leaves sensitive context displayable

**File:** [routes.py:386](modules/bridge/backend/bl_haos/api/routes.py#L386)

**Issue:** The `if not reconnected` branch raises a fixed HTTP 409 inside the
original `except MediaPlayerError` without `from None`. Neighboring reconnect
exception/retry branches suppress their context. Consequently this branch can
still display the original playback exception and its nested causes whenever a
caller formats/logs the resulting exception. The standard FastAPI HTTP response
remains bounded and does not itself disclose the context; this is an incomplete
exception-boundary guarantee, not a demonstrated normal-response leak.

**Reproduction:** Call the real decorated route with an authenticated fake
request, a trusted sink, `ha_bridge.execute = AsyncMock(side_effect=MediaPlayerError("Connected Bluetooth audio sink is unavailable " + url))`,
and `bt_manager.connect_device = AsyncMock(return_value=False)`. Capture the
raised `HTTPException` and format it using `traceback.format_exception`.
Observed:

```text
detail=Auto-reconnect failed: could not re-establish the Bluetooth connection
suppress_context=False
url_in_formatted_chain=True
```

This is the same sensitive-error injection used by the route regression tests,
but their reconnect case raises an exception instead of returning false, and
they inspect only response text and logs, not this formatted route exception.

**Fix:** Add `from None` to this fixed HTTP exception and a false-return
reconnect test that checks both bounded response text and the displayed nested
exception chain. Do not change reconnect arguments, classification, or retries.

## Historical Verification

Reviewer executions, independent of the executor's reported counts:

- WSL Ubuntu, approved existing Core environment, Python 3.14.4 / helper
  0.13.374: integration privacy selector **5 passed, 71 deselected**, 1.77s.
- Windows existing bridge environment, Python 3.14.7,
  `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`: combined privacy/URL selector
  **32 passed, 74 deselected**, 0.92s.
- Complete touched bridge test files: **105 passed, 1 existing skip**, 2.50s.
  One existing Starlette TestClient deprecation warning.
- In-memory bridge probe reproduced CR-01, CR-03, and WR-01 with real decorated
  methods and fake collaborators; asserted exact single URL handoff and no
  sink/process calls for rejected URLs.
- In-memory WSL/Core probe reproduced CR-01 and CR-02 with real entity/client
  methods, fake HTTP/WebSocket I/O, and the real bridge fallback-title code.
  It asserted exact client URL handoff and preservation of the cached title.

Commands for the pytest checks:

```powershell
wsl.exe -d Ubuntu --cd /mnt/f/Workspace/BL-HAOS/modules/integration env BLHAOS_RUN_SIL=1 PYTHONDONTWRITEBYTECODE=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests/test_ha_integration_sil.py -q -p asyncio --asyncio-mode=auto -p no:cacheprovider -k 'play_media and (log or redact)' --tb=short --show-capture=no
```

From modules/bridge, with `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`:

```powershell
& F:/Workspace/BL-HAOS/.venv/Scripts/python.exe -B -m pytest -c pytest.ini tests/test_api.py tests/test_media_player.py -q -p asyncio --asyncio-mode=auto -p no:cacheprovider -k '(native and (play or log or redact)) or url or redact' --tb=short --show-capture=no
& F:/Workspace/BL-HAOS/.venv/Scripts/python.exe -B -m pytest -c pytest.ini tests/test_api.py tests/test_media_player.py -q -p asyncio --asyncio-mode=auto -p no:cacheprovider --tb=short --show-capture=no
```

The value-free call-trace wrappers were inspected in both runtimes and do not
log arguments, return values, exception messages, or tracebacks. The examined
24-05 changes do not alter bearer/trust checks, URL acceptance policy, reconnect
classification/arguments/timing, or ffmpeg's protocol whitelist and exact single
URL argument. The earlier single-attempt integration submission change belongs
to prior work and was not treated as a new 24-05 regression.

The previous package-layout false positive is explicitly excluded: the user
reports the parent is repairing the local ancestor name and rebuilding without
weakening the guard. No finding is made about that old failure. Full L1/Core
acceptance is left to the parent; this review did not rerun those broad gates.
No live host, provider, Bluetooth radio, real decoder, deployment, restart,
installation, source/test edit, STATE edit, commit, or staging action was used.
Only this review artifact was written. Prior phase 27 and other uncommitted
changes were preserved.

---

_Reviewer: gsd-code-reviewer_
