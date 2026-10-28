# Phase 26: Sequential Playback & Queue Controls - Pattern Map

**Mapped:** 2026-10-27  
**Files analyzed:** 18 target/source-test homes  
**Tracked analogs found:** 15 / 18; the three panel/library implementation and mock-browser homes noted below are workspace-only, not canonical tracked analogs.

## Scope and Boundary

This map covers PL-07 through PL-10 and local/mock-only work. Phase 25 owns durable playlist definitions; Phase 26 owns only transient, per-speaker playback sessions. Home Assistant remains the resolver/authentication boundary, and the bridge remains the sole queue/process owner.

- Resolve every saved reference in HA before submitting a replacement. A resolution failure sends no queue command and leaves the existing queue untouched.
- A provider shortcut is one opaque, atomic queue item. Do not expand provider tracks or claim provider-internal next/previous semantics.
- Never persist queue/session state. Do not store queue state in HA Store, browser storage, URLs, or query state; restart does not restore a queue.
- Resolved playback URLs are transient command/process inputs only. They must not reach browser state, snapshots, events, visible errors, or logs. Use allowlisted display metadata and bounded error copy.
- Do not pass the native bearer to browser code. Native HA commands use the existing bearer-authenticated client; ingress controls use the existing ingress-scoped add-on API path.
- Do not access live HA/provider services, deploy, restart, or perform physical playback. Local SIL and mock-browser evidence is not production acceptance.

## File Classification

| New/Modified File or Test Home | Role | Data Flow | Closest Tracked Analog | Match Quality |
|---|---|---|---|---|
| `modules/bridge/backend/bl_haos/ha/player.py` | playback service/runtime owner | process I/O, streaming, event-driven | same file | exact |
| `modules/bridge/backend/bl_haos/api/routes.py` | API route/schema | request-response | same file | exact |
| `modules/bridge/backend/bl_haos/main.py` | lifecycle/event coordinator | event-driven, pub-sub | same file | exact |
| `modules/integration/custom_components/bl_haos/media_player.py` | HA entity/controller | request-response, state projection | same file | exact |
| `modules/integration/custom_components/bl_haos/client.py` | authenticated client/cache | request-response, event-driven | same file | exact |
| `modules/integration/custom_components/bl_haos/playlist_library.py` (workspace-only source) | HA library/command handler | storage, request-response | `modules/integration/custom_components/bl_haos/media_player.py`; `modules/integration/tests/test_playlist_library_sil.py` | partial; source is untracked in the integration index |
| `modules/integration/panel_ui/src/media-panel.tsx` (workspace-only source) | HA panel component | request-response, state projection | `modules/integration/custom_components/bl_haos/media_player.py`; `modules/integration/panel_ui/src/playlist-library.test.tsx` | partial; component is untracked in the integration index |
| `modules/bridge/web_ui/src/components/SpeakerCard.tsx` | ingress component | command-response, event-driven display | same file | exact |
| `modules/bridge/web_ui/src/api/client.ts` | ingress API client/types | request-response | same file | exact |
| `modules/bridge/web_ui/src/hooks/useBluetoothEvents.ts` | event/state hook | event-driven | same file | exact |
| `modules/bridge/tests/test_media_player.py` | bridge unit tests | process lifecycle, event-driven | same file | exact |
| `modules/bridge/tests/test_api.py` | API contract/security tests | request-response | same file | exact |
| `modules/bridge/tests/test_native_transport.py` | native auth/snapshot tests | request-response, event-driven | same file | exact |
| `modules/integration/tests/test_ha_integration_sil.py` | Core SIL tests | request-response, entity lifecycle | same file | exact |
| `modules/integration/tests/test_playlist_library_sil.py` | Core SIL/WebSocket tests | storage, authenticated request-response | same file | exact test analog; tests the workspace-only library source |
| `modules/integration/panel_ui/src/playlist-library.test.tsx` | panel Vitest tests | request-response, component state | same file | exact test analog; file has existing user changes, preserve them |
| `modules/integration/panel_ui/src/media-panel.test.tsx` (workspace-only test) | panel Vitest tests | request-response, session lifecycle | `modules/integration/panel_ui/src/playlist-library.test.tsx` | partial; test is untracked |
| `modules/integration/panel_ui/e2e/playlist-library.spec.ts` and `mock-harness.html` (workspace-only) | mock Playwright acceptance | browser flow, request/response | none tracked | no tracked analog; current workspace harness/spec are untracked |

## Pattern Assignments

### Bridge playback owner and process lifecycle

**Targets:** `modules/bridge/backend/bl_haos/ha/player.py`  
**Analog:** same tracked file. The bridge already normalizes speaker addresses, owns `active_processes` per address, serializes starts with `_address_lock`, starts a decoder/player pair through an injected process factory, and keeps strong references to watcher tasks. Extend this owner with an in-memory queue session/generation; do not add a second queue service or frontend sequencing.

**Per-address ownership and locking** (`player.py#L241-L300`):

```python
self.active_processes: dict[str, tuple[asyncio.subprocess.Process, asyncio.subprocess.Process]] = {}
self._address_locks: dict[str, asyncio.Lock] = {}

def _address_lock(self, address: str) -> asyncio.Lock:
    """Return the serialization lock for one speaker's command stream."""
    lock = self._address_locks.get(address)
    if lock is None:
        lock = asyncio.Lock()
        self._address_locks[address] = lock
    return lock
```

**Start and teardown** (`player.py#L568-L641`, `player.py#L1360-L1385`): `play_url()` validates the URL and acquires the per-address lock before `_play_url_locked()`. `_play_url_locked()` cancels sink warm-up, resolves the selected sink, stops the prior pair, spawns decoder/player, records the pair, starts timeline state, and notifies listeners. `_stop_processes()` removes the pair from `active_processes` before signaling and uses bounded waits/reaping. Keep that ordering and reuse `_play_url_locked()` only under the existing lock discipline; do not hold the speaker lock while awaiting natural completion.

**Watcher fence** (`player.py#L1474-L1488`):

```python
async def _watch_processes(self, address, decoder, player):
    await asyncio.gather(decoder.wait(), player.wait(), return_exceptions=True)
    if self.active_processes.get(address) == (decoder, player):
        is_abnormal = (player.returncode not in (0, None)) or (
            decoder.returncode not in (0, None, -15, 255)
        )
        self.active_processes.pop(address, None)
        self.states[address] = PLAYBACK_IDLE
        self._clear_timeline(address)
        await self._notify(address)
```

Preserve the process-pair identity fence and add a queue-generation/session fence. Replacement, stop, disconnect, and shutdown must invalidate the generation before any await or process teardown. The current watcher always clears to idle and tolerates decoder `-15`/`255` for its abnormal-log predicate; that is not a natural-success contract. Advancement must require explicitly accepted natural-success exit codes from both children, current generation ownership, and current pair ownership. Cancellation never advances; abnormal completion retains the failed item.

**Disconnect wiring:** `modules/bridge/backend/bl_haos/main.py#L263-L277` currently schedules `execute(..., COMMAND_STOP)` after a BlueZ disconnect. Reuse this lifecycle hook but synchronously invalidate the queue generation when loss is detected, before scheduling asynchronous stop. `main.py#L215-L240` already sends playback state to both native HA and ingress listeners; extend the shared snapshot rather than publishing a separate queue event.

### Bridge API, snapshot, and command boundaries

**Targets:** `modules/bridge/backend/bl_haos/api/routes.py`, `modules/bridge/backend/bl_haos/main.py`  
**Analogs:** same tracked files.

**Request contract:** `routes.py#L170-L202` defines `NativeCommandRequest` with a literal operation allowlist, bounded URL/media fields, field validation, and operation-specific payload checks. Extend this schema with bounded queue operations/items/modes and explicit capability/version data; retain strict allowlists and validate item count, per-field lengths, aggregate payload size, and every transient URL before queue replacement.

**Auth and native route:** `routes.py#L71-L77` provides `require_native_auth`; `routes.py#L338-L435` validates the speaker is trusted and an audio sink, dispatches through the bridge, publishes the updated snapshot, and returns the post-command record. The route also has sink auto-reconnect/re-execution at `routes.py#L376-L426`. Exclude non-idempotent queue start/next/previous from automatic re-execution, or add explicit command deduplication. Never forward the browser's ingress request to the native bearer route.

**One shared, sanitized envelope** (`routes.py#L204-L267`):

```python
def playback_envelope(bridge, address):
    if bridge is None:
        return {"state": PLAYBACK_IDLE, "volume": None}
    return {
        "state": bridge.get_state(address),
        "volume": bridge.get_volume(address),
        **native_playback_timeline(bridge, address),
    }
```

`native_speaker_record()` embeds this envelope for HA; `ui_speaker_record()` embeds it for ingress. Extend this allowlisted envelope with queue display fields and no internal item URLs, media-source IDs, credentials, raw exceptions, or generation token. Keep queue lifecycle status separate from the ordinary HA media-player state.

**Dual publication:** `main.py#L212-L240` calls the native speaker publisher and broadcasts `EVENT_PLAYBACK_UPDATED` with `playback_envelope(...)`. Retain this path and address matching so both clients reconcile to the same bridge-owned state.

**Ingress REST path:** `routes.py#L563-L585` is the current per-device command route shape: normalize address, fail clearly if the bridge is unavailable, dispatch, publish, and return a bounded result. Add ingress queue controls alongside this add-on API family, not with the integration bearer. Browser requests and responses must contain no resolved media URL.

### HA resolver, client, and native entity

**Targets:** `modules/integration/custom_components/bl_haos/media_player.py`, `modules/integration/custom_components/bl_haos/client.py`  
**Analogs:** same tracked files.

**HA single-item resolution:** `media_player.py#L435-L475` is the current resolver boundary. It checks an explicit connected entity, calls `async_resolve_media(hass, media_id, entity_id)`, runs `async_process_play_media_url`, normalizes relative HA URLs, rechecks speaker availability, and submits one `play_media` command. It rejects `enqueue`. Keep the URL resolution in HA; the queue-start handler should load the selected saved record, resolve every reference in order, and submit only after all succeed. If any item fails, send no native command and leave the old bridge queue untouched.

```python
media = await async_resolve_media(self.hass, media_id, self.entity_id)
media_id = media.url
url = async_process_play_media_url(self.hass, media_id)
await self._async_command(COMMAND_PLAY_MEDIA, url=url, media_type=media_type)
```

**Native feature/state projection:** `media_player.py#L252-L352` defines current features, maps bridge state to HA `idle/playing/paused/off`, and projects title/artist/timeline. Add queue methods and `NEXT_TRACK`, `PREVIOUS_TRACK`, `SHUFFLE_SET`, and `REPEAT_SET` only when a trusted bridge queue capability is cached. Preserve standard HA state mapping; expose queue status and metadata separately. Verify exact Core 2026.10.3 method dispatch in SIL before advertising the flags.

**Bearer client and event cache:** `client.py#L112-L148` owns bearer headers and the identity check before credential use. `client.py#L211-L245` sends versioned commands; today `play_media` is single-attempt while other state operations may retry. Queue start/next/previous must also be single-attempt or deduplicated because replaying an acknowledgment-ambiguous command can restart or skip. `client.py#L305-L330` normalizes/caches speaker records and notifies entity listeners; `client.py#L418-L449` processes authenticated `speaker_updated` events. Reuse those paths for the queue snapshot and capability; do not send the bearer to the panel.

**Saved-library/WebSocket analog:** The workspace contains a Phase 25 `playlist_library.py` implementation, but it is untracked in the integration repository and is not a canonical source analog. The tracked `modules/integration/tests/test_playlist_library_sil.py#L112-L175` is the appropriate test pattern for authenticated HA WebSocket commands, structured results, idempotency, and Store assertions. Its provider test at `#L263-L365` verifies one opaque reference remains one saved record. Reuse the HA Store for playlist definitions only; never put the active queue or resolved URLs in it. There is no tracked source analog for a new resolve-all/start WebSocket handler.

### Ingress state and controls

**Targets:** `modules/bridge/web_ui/src/api/client.ts`, `modules/bridge/web_ui/src/hooks/useBluetoothEvents.ts`, `modules/bridge/web_ui/src/components/SpeakerCard.tsx`  
**Analogs:** same tracked files and their neighboring tests.

`api/client.ts#L52-L93` defines `PlaybackInfo` and the per-speaker payload; `api/client.ts#L102-L115` centralizes JSON/error handling; `api/client.ts#L176-L202` shows the existing path-relative device command calls. Add queue snapshot typings and protected ingress API methods there. Do not put a playback URL or native token in request state.

`useBluetoothEvents.ts#L98-L120` merges `playback_updated` by normalized speaker address and patches only the bridge snapshot. Extend this merge for queue fields. `SpeakerCard.tsx#L1-L225` currently owns volume/connect/remove/settings command state, pending/error feedback, and no playback queue. Add display and command controls that read `device.playback`; do not add browser-owned item arrays, timers, advancement, or optimistic queue/order changes.

**Tests:** `SpeakerCard.test.tsx#L35-L160` covers rendered state, authoritative playback updates, pending/failed volume actions; `useBluetoothEvents.test.tsx#L52-L110` covers address-matched event updates and preservation across BlueZ property events. Extend these existing suites for queue snapshots, bounded errors, disabled disconnected controls, command mapping, and URL non-disclosure.

### HA Library start UI and browser tests

**Targets:** `modules/integration/panel_ui/src/media-panel.tsx`, its Vitest and mock Playwright tests.  
**Tracked analog:** `modules/integration/panel_ui/src/playlist-library.test.tsx#L8-L44` (tracked but modified in the workspace); `modules/integration/tests/test_ha_integration_sil.py#L694-L924` for the resolver/target contract.

The current panel implementation, `media-panel.test.tsx`, mock harness, and `e2e/playlist-library.spec.ts` were inspected in the workspace, but those files are untracked in the integration repository and must not be used as canonical analogs. The tracked Vitest tracer demonstrates an injected `Hass` seam, typed `callWS`, and assertions that library work stays on HA's authenticated connection. Extend the existing panel surface with an explicit connected-target selector and saved-record launch; send record/entity identity only. Display the authoritative URL-free queue snapshot and keep session-generation guards, pending state, bounded errors, and no implicit target substitution.

The workspace Playwright flow is local/mock-only and currently asserts that the Phase 25 Library has no playback controls. It is not a tracked analog. Do not add a new E2E framework or reuse any live-host configuration. If the existing local harness is retained by the phase owner, extend it with deterministic queue state/events, strict local-origin routing, URL/bearer sentinel checks, replacement/failure/disconnect scenarios, and the 375/768/1440 layouts from `26-UI-SPEC.md`. Treat its result as mock evidence only.

## Shared Patterns

### Generation-fenced process completion

**Sources:** `modules/bridge/backend/bl_haos/ha/player.py#L1360-L1385`, `#L1474-L1488`; `modules/bridge/tests/test_media_player.py#L996-L1008`  
**Apply to:** queue start, replacement, stop, disconnect, shutdown, and every watcher completion. Invalidate queue ownership before process teardown can yield. A completion may advance only when both the generation and process pair still own that speaker and both child exits satisfy the accepted natural-success contract.

### URL-free shared state and logs

**Sources:** `modules/bridge/backend/bl_haos/api/routes.py#L204-L267`; `modules/bridge/backend/bl_haos/main.py#L215-L240`; `modules/bridge/tests/test_media_player.py#L48-L117`; `modules/bridge/tests/test_api.py#L337-L420`  
**Apply to:** native snapshots, ingress snapshots/events, HA entity cache, UI errors, and command logs. Extend an explicit allowlist; use sentinel URLs/query values in tests and assert absence from every serialized/client-visible/logged surface.

### HA authorization and resolve-all-before-replace

**Sources:** `modules/integration/custom_components/bl_haos/media_player.py#L435-L475`; `modules/integration/custom_components/bl_haos/client.py#L112-L148`, `#L211-L245`; `modules/integration/tests/test_ha_integration_sil.py#L756-L924`  
**Apply to:** saved custom playlists and provider shortcuts. Recheck one explicitly selected connected target, resolve the complete sequence in HA, and only then issue one native queue-start command. A failed resolution must produce zero bridge commands. The browser never sees the resolved batch.

### Non-idempotent command policy

**Sources:** `modules/bridge/backend/bl_haos/api/routes.py#L376-L426`; `modules/integration/custom_components/bl_haos/client.py#L211-L245`; `modules/integration/tests/test_ha_integration_sil.py#L840-L886`  
**Apply to:** queue start, next, and previous. Bypass route auto-reconnect/re-execution and client retry unless a command ID is deduplicated by the bridge. On ambiguous acknowledgement, reconcile from the next authoritative snapshot.

### Atomic provider shortcut and transient queue

**Sources:** `modules/integration/tests/test_playlist_library_sil.py#L263-L365`; `modules/integration/tests/test_playlist_library_sil.py#L112-L175`  
**Apply to:** provider launch and persistence boundaries. The shortcut is a single opaque media-source reference; HA resolves it as one item. Keep ordered custom entries as the queue input, but do not expand provider contents. Persist playlist references only, never queue state or resolved URLs.

## No Tracked Analog Found

| File/Capability | Role | Reason |
|---|---|---|
| Resolve-all/start HA WebSocket handler | HA command/service | The Phase 25 implementation exists only as untracked workspace source; no tracked integration handler owns this full flow. Use `media_player.py` for resolution and the tracked playlist-library SIL test for the authenticated WebSocket contract. |
| HA panel queue-start implementation | panel component | The current panel source is untracked; the tracked panel Vitest file covers library commands but not queue launch or snapshot display. |
| Queue mock Playwright behavior | browser acceptance | The current harness/spec are untracked and no tracked panel Playwright analog exists. Keep implementation planning local/mock-only and avoid a new test framework. |

## Metadata

**Analog search scope:** bridge playback/API/main, bridge ingress API/components/hooks/tests, integration entity/client/tests, panel Vitest and mock-browser workspace.  
**Tracked-source check:** ran `git ls-files` in the bridge and integration repositories and checked panel/library paths in the integration index. All named analogs above are tracked; the identified Phase 25 working-tree source/test/harness files are explicitly marked non-canonical.  
**Pattern extraction date:** 2026-10-27