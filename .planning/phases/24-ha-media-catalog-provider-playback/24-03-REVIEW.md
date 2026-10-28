---
phase: 24-ha-media-catalog-provider-playback
plan: "03"
reviewed: 2026-10-24T15:30:21Z
depth: standard
review_scope: CR-01-only
files_reviewed: 4
files_reviewed_list:
  - modules/integration/custom_components/bl_haos/client.py
  - modules/integration/custom_components/bl_haos/media_player.py
  - modules/integration/tests/test_ha_integration_sil.py
  - modules/integration/tests/unit/test_client_commands.py
findings:
  critical: 0
  warning: 0
  info: 0
  total: 0
status: clean
---

# Phase 24 Plan 03: Code Review Report

## Narrative Findings (AI reviewer)

No open findings in this CR-01-only re-review. **CR-01 is resolved.** The clean
status closes the sole prior blocker; it does not represent a broad re-review,
whole-phase acceptance, or live-provider/physical-audio verification. Previously
approved metadata filtering was not re-reviewed.

### CR-01 Resolution Evidence

The controlling change in
[modules/integration/custom_components/bl_haos/client.py](modules/integration/custom_components/bl_haos/client.py#L225)
sets one attempt for `play_media` inside the real command loop. All other
operations retain `COMMAND_ATTEMPTS`. The production diff preserves the public
signature `(self, address: str, operation: str, **options: Any) -> dict[str, Any]`,
payload construction, and send method. Timeout and generic client errors also
leave this loop without retrying.

Independently reran the original-style in-memory ambiguous-POST probe under WSL
Python 3.14.4 / Home Assistant Core **2026.10.3**. A real BLHAOSClient and real
BLHAOSMediaPlayer used one explicitly selected connected/available speaker.
Only provider resolution, URL processing, HTTP session I/O and retry sleep were
patched; entity command, client command loop and send method remained real.
The fake recorded the POST and simulated its application before losing the
acknowledgement. No network requests or files were created by this probe.

```text
ServerDisconnectedError, hypothetical second succeeds: POST=1 applied=1 resolve=1 sleep=0
ServerDisconnectedError, persistent disconnect:        POST=1 applied=1 resolve=1 sleep=0
TimeoutError, hypothetical second succeeds:           POST=1 applied=1 resolve=1 sleep=0
ClientError, hypothetical second succeeds:            POST=1 applied=1 resolve=1 sleep=0
```

Every case preserved the untouched original opaque playlist reference and
selected entity ID, sent exactly the expected target URL/payload, and raised the
exact bounded HomeAssistantError with suppressed context and no explicit cause.
No duplicate POST or silent success occurred. A lost acknowledgement still does
not establish whether actual remote playback was applied.

Independent executable checks against the current main checkout:

| Check | Result |
|-------|--------|
| Real-Core HTTP-failure slice, both selected speakers | **8 passed**, 63 deselected, 2.41s |
| Separate client unit file, including four ambiguous-POST cases | **19 passed**, 1.00s |
| Adjacent native playback cases, excluding the eight above | **26 passed**, 45 deselected, 8.76s |

The client unit run confirms `pause` still makes two attempts and awaits one
retry sleep after a disconnect; persistent state-command disconnects still
exhaust two attempts. Adjacent Core cases cover normal playback, target guards,
resolution failures and cancellation. All runs completed without skips or
teardown errors. Core and stub units ran in separate Python processes.

Commands used the existing WSL interpreter
`/home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -B -m pytest -c pytest.ini`
from `/mnt/f/Workspace/BL-HAOS/modules/integration`, with `-p no:cacheprovider`:

```text
BLHAOS_RUN_SIL=1 ... tests/test_ha_integration_sil.py -q -p asyncio --asyncio-mode=auto -k command_failure_is_bounded_without_retry --tb=short --show-capture=no
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 ... tests/unit/test_client_commands.py -q --tb=short
BLHAOS_RUN_SIL=1 ... tests/test_ha_integration_sil.py -q -p asyncio --asyncio-mode=auto -k 'native_play_media and not command_failure_is_bounded_without_retry' --tb=short --show-capture=no
```

The fixer's RED **2 failed / 2 passed** to GREEN **4 passed**, full Core **103
passed**, and separate full units **58 passed** remain supplied historical
evidence, not independently rerun full gates in this re-review. The focused
checks and independent probe above establish the CR-01 verdict.

Only this review artifact was edited. No source/tests, STATE, dependencies,
commits, branches, installations, deployment or live actions were changed or
performed.

## Historical Finding (Resolved)

The following preserves the original 2026-10-24T15:24:40Z review evidence. Its
failure observations describe the pre-fix implementation, not the current code.

### CR-01: BLOCKER (Resolved) - Opaque playback automatically retried HTTP submission

**File:** [modules/integration/custom_components/bl_haos/media_player.py](modules/integration/custom_components/bl_haos/media_player.py#L473)

**Issue:** The plan's one-command/no-automatic-retry contract is not enforced at
the transport boundary. The entity calls `_async_command` once, but that method
calls the real `BLHAOSClient.async_command`, whose existing retry loop at
[modules/integration/custom_components/bl_haos/client.py](modules/integration/custom_components/bl_haos/client.py#L224)
repeats the HTTP POST after `aiohttp.ServerDisconnectedError` (two attempts by
default). The new exception wrapper runs only after that loop returns or exhausts
its attempts; it cannot prevent the second submission.

A connection closing before the response does not establish that the bridge
rejected the first command. If it already applied playback, resubmission can
restart the item or playlist. If the second attempt succeeds, the service can
also report success despite silently taking the prohibited recovery action.
This is not a new defect in unrelated lifecycle code: it is an unchanged callee
that contradicts the explicit contract claimed by the new playback work.

**Reproduction:** Confirmed in an in-memory probe using WSL Python 3.14.4 and
Home Assistant Core 2026.10.3. No live requests, test-file changes, integration
setup, or installations were used.

1. Create the real `BLHAOSClient` and `BLHAOSMediaPlayer`; seed one connected,
   available speaker and assign its explicit entity ID.
2. Patch only the resolver to return a valid `PlayMedia` for an opaque playlist,
   and the Core URL-processing helper to return that resolved URL.
3. Keep the entity command method, client command method, and client send method
   real. Patch `client.async_get_clientsession` with a fake session that records
   `post()` calls and raises `ServerDisconnectedError` on context entry.
4. Replace the retry sleep with an `AsyncMock`, then await one
   `player.async_play_media("playlist", original_reference)` call.

Observed output:

```text
Core: 2026.10.3
CONFIRMED CONTRACT FAILURE: one opaque playlist resolve produced TWO identical HTTP POST attempts after ServerDisconnectedError
POST operation: play_media target: media_player.selected_speaker attempts: 2
```

The resolver was awaited exactly once with the untouched original reference and
selected entity ID. Both POSTs had identical target URLs and command payloads;
one retry sleep was awaited. The final displayed error was bounded, but the
second submission had already happened.

**Coverage gap:** The new
[modules/integration/tests/test_ha_integration_sil.py](modules/integration/tests/test_ha_integration_sil.py#L698)
failure test replaces `client.async_command` with an `AsyncMock` raising a generic
`ClientError`. It therefore bypasses the retry loop and cannot establish the
claimed no-retry property. The corresponding README and summary claims are
stronger than the actual transport behavior.

**Fix:** Give this playback submission an explicit one-attempt transport path,
for example a dedicated no-retry method or a keyword-only retry policy consumed
by `BLHAOSClient.async_command`, not serialized into the bridge payload. Leave
other command retry policies unchanged. Exercise the real client command loop
with fake HTTP I/O: first POST raises `ServerDisconnectedError`, a hypothetical
second would succeed, and the required assertion is exactly one POST, no retry
sleep, and a bounded `HomeAssistantError`. Also cover repeated disconnects and
confirm one original-reference resolution and one selected target.

## Original Scope And Evidence (Historical)

Reviewed the plan 24-03 local changes in the integration subrepository, the new
README paragraph, and the 24-03 summary against 24-03-PLAN.md. Prior clean
panel/lifecycle work was not re-reviewed. The unchanged client and Core helpers
were read only to trace the new playback contract to its actual behavior.

No additional concrete defect was established in metadata-based filtering,
unknown expandable hierarchy retention, opaque IDs, capability preservation,
playlist handling, or resolver failure conversion. The read-only in-memory probe
also passed these focused checks:

- Copy-based hierarchical filtering preserved retained display/capability fields
  and left the original Core tree unchanged.
- Denied, expired, unavailable, unresolvable, and timeout resolver errors yielded
  bounded messages with suppressed displayed exception context and no command.
- Resolver cancellation propagated without submission.

The reported 96 Core SIL and 54 separate unit passes were existing execution
evidence supplied for this review, not rerun here. Their success does not cover
the transport retry case above. No live-provider or physical-audio acceptance is
claimed. Full-path operational log redaction remains outside this plan's review.

Only this review artifact was written. Source, tests, global planning state,
phase 27, dependencies, commits, and live systems were not modified.