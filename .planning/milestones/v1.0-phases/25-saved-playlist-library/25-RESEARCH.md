<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** The library is installation-wide, not scoped to a speaker. A target speaker is selected when a playlist is played in Phase 26.
- **D-02:** Keep playlist data in Home Assistant-owned persistent storage and expose CRUD through an authenticated Home Assistant WebSocket boundary. Do not persist playlist data in browser storage or the add-on bridge.
- **D-03:** Serialize concurrent mutations and save atomically.
- **D-04:** Version the stored record schema and migrate valid references forward without resolving them.
- **D-05:** Custom playlist entries preserve ordered opaque Home Assistant media IDs and the display metadata needed by the library. Never store resolved playback URLs, provider credentials, or credential-bearing request data.
- **D-06:** Allow duplicate entries and empty drafts. Empty drafts are not playable.
- **D-07:** Reordering must be keyboard-accessible; provide explicit Move Up/Move Down controls rather than drag-only operation.
- **D-08:** A saved provider playlist is one opaque Home Assistant playlist reference, not an expanded copy of its provider tracks. Users may rename or remove the local shortcut; provider contents remain read-only.
- **D-09:** Availability is checked on demand through Home Assistant's media-source browsing path, not by contacting providers directly or checking every record on panel load.
- **D-10:** A failed or denied check is visible as unavailable/stale, but never deletes or rewrites the saved reference. Rechecking remains explicit.
- **D-11:** Phase 25 owns CRUD and availability status only. Phase 26 owns launch, sequential playback, and queue controls.
- **D-12:** Keep HA-owned operations in the existing authenticated Home Assistant panel context; do not move them into the add-on Ingress UI.
- **D-13:** Validate and bound all mutations at the Home Assistant integration boundary, including record shape, identifiers, ordering, and size.

### Reviewed Todos
- `Add pinned Linux Home Assistant SIL CI` was reviewed and left deferred. It is a general CI improvement, not a playlist-library requirement.

### Claude's Discretion
- Choose the concrete Home Assistant storage helper, WebSocket command schema, migration mechanics, bounded size limits, and UI presentation after researching current supported APIs and nearby integration conventions.
- Select focused unit, Home Assistant integration/SIL, component, and mock-browser tests. Do not claim live provider, host, or playback verification.

### Deferred Ideas (OUT OF SCOPE)
### Reviewed Todos (not folded)
- `Add pinned Linux Home Assistant SIL CI` - reviewed but not included because it is a general CI improvement outside Phase 25's saved-playlist scope.

- Playlist launch, sequential advancement, and queue controls remain assigned to Phase 26.
- Live provider, production-panel, physical playback, and HA-shell acceptance remain post-milestone production work. No deployment or release approval is implied.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| PL-04 | Users can create, rename, reorder, edit, and delete custom ingress playlists containing ordered Home Assistant media references. | Store schema, validated custom commands, mutation serialization, and panel editor/testing patterns. |
| PL-05 | Users can save existing Home Assistant provider playlist references in the BL-HAOS playlist library. | Opaque-reference record model and existing HA media browse interaction. |
| PL-06 | Saved playlist definitions persist across Home Assistant and add-on restarts; unavailable or stale media references are identified to the user. | HA-owned persistent Store, on-demand media-source browse check, and reload/restart SIL cases. |
| PL-11 | Saved playlists store Home Assistant media references and required display/order metadata, not resolved playback URLs or provider credentials. | Allowlisted metadata, strict identifier validation, and prohibition on media resolution/provider requests. |
</phase_requirements>

# Phase 25: Saved Playlist Library - Research

**Researched:** 2026-10-25  
**Domain:** Home Assistant custom integration storage, authenticated WebSocket APIs, media-source browsing, React panel  
**Target Core:** 2026.10.3  
**Confidence:** MEDIUM overall; version-specific Store internals below are explicitly LOW pending focused SIL confirmation.

## Summary

Use Home Assistant's `homeassistant.helpers.storage.Store` for the installation-wide library, and expose CRUD through namespaced custom WebSocket commands registered once from integration `async_setup`. Keep the Store and mutation lock at integration/Hass lifetime, not in `ConfigEntry.runtime_data`, `ConfigEntry.data`, browser storage, or the add-on bridge. Store one versioned document containing opaque references, allowlisted display snapshots, local names, and custom-entry order. Do not add packages.

Reuse the panel's injected `hass.callWS` media-source browse path for explicit availability checks. Browsing is separate from `async_resolve_media`, which returns a playable URL. A browse result is not a universal guarantee of future playability; keep status explicitly about HA browse availability, treat failures as unavailable, and never modify the saved ID. Phase 26 playback and production/host validation remain out of scope.

**Primary recommendation:** Implement one shared versioned Store, one `asyncio.Lock` around each complete read/validate/replace/save transaction, explicit atomic writes, strict server validation, and a read-back check before returning mutation success. The read-back is important because the exact tagged Core source inspected here appears to log and swallow storage `WriteError`; that implementation detail is LOW-confidence per the research source classifier and must be verified against the pinned SIL runtime.

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Playlist records, migration, mutation validation | API / Backend (HA integration) | HA storage | Installation-wide data and mutation authority belong on the HA side. |
| Authenticated CRUD transport | API / Backend (HA WebSocket) | Browser / Client | HA WebSocket supplies the authenticated connection; the panel sends commands through injected `hass`. |
| Explicit reference availability | Browser / Client using HA media-source WebSocket browse | HA media-source integration | Reuses the already-authenticated catalog path and avoids resolving a playback URL. |
| Editing, ordering, status and confirmations | Browser / Client panel | API / Backend | Panel owns interaction; server remains authoritative for shape, identity, limits, and saved order. |
| Persistence across HA/add-on restart | Database / Storage (HA `.storage`) | HA integration | The library must outlive panel/config-entry unload and remain outside add-on state. |

## Project Constraints (from applicable project instructions)

- `.planning/AGENTS.md` requires official Home Assistant developer documentation first; this research used the official developer docs/Context7 corpus before consulting local patterns. `[VERIFIED: .planning/AGENTS.md:83]` Exact instruction: “**Home Assistant Developer Docs**: Always consult official Home Assistant developer documentation first at `https://developers.home-assistant.io/` for all add-on specifications (`config.yaml`, Ingress, S6-overlay, D-Bus permissions), config-entry schemas, and supervisor APIs.”
- The same instructions require starting file-changing work through a GSD workflow. This artifact is the requested Phase 25 research output; no implementation files or other repository files were changed. `[VERIFIED: .planning/AGENTS.md:102-109]` Exact instruction: “Before using Edit, Write, or other file-changing tools, start work through a GSD command” and “Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.”
- No root `copilot-instructions.md` was found. No commits, host access, deployment, credentials, or live URLs are part of this research.

## Standard Stack

| Component | Version | Purpose | Why Standard |
|-----------|---------|---------|--------------|
| Home Assistant Core | 2026.10.3 | Integration runtime, Store, WebSocket API, and media-source API | Explicit phase target and the existing SIL pin. `[VERIFIED: modules/integration/requirements-sil.txt:5]` Quote: `homeassistant==2026.10.3`. |
| `homeassistant.helpers.storage.Store` | Core 2026.10.3 | HA-owned persistent versioned data | Official Home Assistant storage helper; release-tagged implementation supports version fields, migrations, and optional atomic writes. `[CITED: https://github.com/home-assistant/developers.home-assistant/blob/master/blog/2025-11-25-storage-helper-opt-in-serialize-in-executor.md]` Atomic/error details are separately classified LOW below. |
| `homeassistant.components.websocket_api` | Core 2026.10.3 | Authenticated custom CRUD commands | Official integration extension point with schema validation, `connection.user`, and result/error methods. `[CITED: https://github.com/home-assistant/developers.home-assistant/blob/master/docs/frontend/extending-websocket-api.md]` |
| `homeassistant.components.media_source` | Core 2026.10.3 | Non-resolving browse checks for opaque IDs | Official API exposes separate browse and resolve methods. `[CITED: https://github.com/home-assistant/developers.home-assistant/blob/master/docs/core/platform/media_source.md]` |
| React / Vitest / Playwright | Existing project pins | Panel, component tests, and local mock-browser E2E | Existing panel stack; no new frontend package is needed. `[VERIFIED: modules/integration/panel_ui/package.json:17,21,31]` Quotes: `"react": "18.2.0"`, `"@playwright/test": "1.63.0"`, `"vitest": "5.0.4"`. |

**Installation:** None. Do not add an external package for persistence, validation, or UI. Core already supplies the storage, WebSocket, and media-source APIs.

### Package Legitimacy Audit

Not applicable: this phase needs no new external packages.

## Documented Guarantees

### Storage and schema evolution

- Home Assistant's developer material identifies `Store` as the supported integration storage helper and documents its serialization/threading behavior. `[CITED: https://github.com/home-assistant/developers.home-assistant/blob/master/blog/2025-11-25-storage-helper-opt-in-serialize-in-executor.md]`
- **Recommendation:** Use a single Store keyed to the integration/domain and held in integration-global `hass.data`. Keep it installation-wide and independent of a config entry. Do not use `entry.runtime_data` (runtime-only) or config-entry options/data for the library. `[CITED: https://contributors.home-assistant.io/core/integrations/config-entries/]`
- Start with a versioned library document. The proposed initial Store versions `version=1`, `minor_version=1` and a namespaced key are design choices, not existing project constants. Keep migrations deterministic and structural: preserve each media ID byte-for-byte and retain list order; never resolve references while migrating. `[ASSUMED]`
- Use a migration callback for known stored versions. Do not silently reset an unsupported future major schema to an empty library. Home Assistant's config-entry major/minor migration docs are about config entries; they are not a substitute for versioning this separate Store. `[CITED: https://contributors.home-assistant.io/core/integrations/config-entries/]`

### WebSocket registration, authentication, and responses

- Register custom commands with `websocket_api.async_register_command` during integration `async_setup`; define the namespaced command and payload schema with `websocket_command`/`probatio`. Use `async_response` for handlers that await storage. `[CITED: https://github.com/home-assistant/developers.home-assistant/blob/master/docs/frontend/extending-websocket-api.md]`
- The WebSocket connection is authenticated before command handling. The handler can inspect `connection.user`; `require_admin` is an explicit extra restriction, not an automatic property of every authenticated command. Decide whether the installation-wide library is shared among all active authenticated HA users or admin-only before locking the policy. `[CITED: https://github.com/home-assistant/developers.home-assistant/blob/master/docs/auth_permissions.md]`
- Validate fields in both the HA command schema and application logic. Return success only with `connection.send_result(msg["id"], result)`; return a stable, bounded error with `connection.send_error(msg["id"], code, message)`. The frontend `hass.callWS` promise resolves with the result or rejects on a WebSocket error. Do not serialize access tokens or raw provider exceptions into responses/logs. `[CITED: https://contributors.home-assistant.io/core/internals/websocket-api/]`
- Proposed shape: separate namespaced `list`, `save_custom`, `save_provider`, and `delete` commands. A save response should contain the server-accepted canonical record; a check result should contain only availability/status. These names and exact payload/result shapes are recommendations, not existing contracts. `[ASSUMED]`

### Media-source availability

- The official media-source API distinguishes `async_browse_media` (returns a browse model or browse error) from `async_resolve_media` (returns `PlayMedia`, including a playable URL). Use the browse command only; never call the resolver for availability or store its output. `[CITED: https://github.com/home-assistant/developers.home-assistant/blob/master/docs/core/platform/media_source.md]`
- The current panel already sends `media_source/browse_media` through the injected HA connection, including the exact `media_content_id`; reuse this for an explicit user-triggered check. `[VERIFIED: modules/integration/panel_ui/src/media-panel.tsx:28-30,123,164-166]` The ID fixture includes encoded path/query characters and is preserved verbatim: `[VERIFIED: modules/integration/panel_ui/src/media-panel.test.tsx:7-10]` Quote: `media-source://provider/opaque%2Fid?order=a%2Bb`.
- Mark status only, never delete/reorder/rewrite the record. A successful browse means “available in HA's browse path now,” not “playable,” “provider playback verified,” or “available to every HA user.” Browse is provider-defined and can have account/permission behavior; verify the chosen success criterion with a synthetic media-source provider in SIL. `[CITED: https://github.com/home-assistant/developers.home-assistant/blob/master/docs/core/platform/media_source.md]` The status semantics are an implementation decision. `[ASSUMED]`

### Config-entry lifecycle and persistence boundaries

- On startup, HA runs normal integration setup before `async_setup_entry`; config-entry reload is an in-process unload/setup cycle. `runtime_data` is runtime-only and cleanup belongs in `async_unload_entry`. `[CITED: https://contributors.home-assistant.io/core/integrations/config-entries/]`
- Put global Store initialization and one-time WS registration in integration `async_setup`; preserve the shared Store in `hass.data` across a config-entry reload. Do not remove the library in `async_unload_entry` or `async_remove_entry`. A Home Assistant process restart reconstructs the Store from HA-owned storage; add-on restart does not own or clear that file. The latter storage-lifetime details are supported by the Store helper but require the version-specific confirmation listed below. `[CITED: https://contributors.home-assistant.io/core/integrations/config-entries/]`
- Local `__init__.py` currently owns entry setup/unload and panel lifecycle; no playlist Store or custom command is present. `[VERIFIED: modules/integration/custom_components/bl_haos/__init__.py:141-198]` Exact lifecycle symbols: `async def async_setup_entry(...)` and `async def async_unload_entry(...)`.

## Version-Specific Core Source Observations (LOW)

The official docs page historically linked as integration storage did not resolve in this session. I inspected the exact Core 2026.10.3 source URLs below. The GSD confidence seam classifies the `webfetch` provider LOW even with cross-checking, so these implementation details are useful planning leads, **not elevated here to documented guarantees**. Add focused SIL tests against the pinned runtime before depending on them.

- `[ASSUMED]` `Store` uses HA's `.storage` area and its saved envelope has `version`, `minor_version`, `key`, and `data`. The helper supports a migration callback for version mismatches and saves migrated data. Source: [Core 2026.10.3 storage.py](https://github.com/home-assistant/core/blob/2026.10.3/homeassistant/helpers/storage.py).
- `[ASSUMED]` `atomic_writes` defaults to false; opt in with `atomic_writes=True`. That selects HA's `write_utf8_file_atomic`, whose source describes all-or-nothing replacement and `fsync`. This is a single-file atomic replacement, not a multi-record transaction or a guarantee against storage-device loss. Source: [Core 2026.10.3 storage.py](https://github.com/home-assistant/core/blob/2026.10.3/homeassistant/helpers/storage.py) and [util/file.py](https://github.com/home-assistant/core/blob/2026.10.3/homeassistant/util/file.py).
- `[ASSUMED]` `Store` has an instance-level write lock, but that lock serializes writes, not whole read/modify/write operations across handlers. Keep one Store instance per HA runtime and add an integration-level `asyncio.Lock` around load/copy/validate/save/read-back. The lock also prevents stale snapshots overwriting each other.
- `[ASSUMED]` Core 2026.10.3's write path catches/logs `WriteError` rather than propagating it from `async_save`. Awaiting `async_save` alone therefore may not prove that storage changed. While HA is running, read the Store back and compare the persisted document before returning success; reject work during shutdown and test write failures. Avoid private Store internals. Source: [Core 2026.10.3 storage.py](https://github.com/home-assistant/core/blob/2026.10.3/homeassistant/helpers/storage.py).
- `[ASSUMED]` A corrupt JSON Store file is renamed with a `.corrupt` suffix and `async_load` returns `None` while Core creates a storage-corruption issue. `None` can therefore be ambiguous between an absent file and corrupt data. Do not let a load failure look like a trustworthy empty library; test how the public integration path can preserve/report this distinction without relying on private APIs. Source: [Core 2026.10.3 storage.py](https://github.com/home-assistant/core/blob/2026.10.3/homeassistant/helpers/storage.py).
- `[ASSUMED]` `async_browse_media(hass, media_content_id)` validates/parses the URI and calls the media source's browse method; it does not call the resolver. The public browse API does not promise a uniform “item exists and is playable” result across provider implementations. Sources: [Core 2026.10.3 media-source helper](https://github.com/home-assistant/core/blob/2026.10.3/homeassistant/components/media_source/helper.py), [models](https://github.com/home-assistant/core/blob/2026.10.3/homeassistant/components/media_source/models.py).

## Recommended Architecture Patterns

### Ownership and mutation flow

1. In `async_setup`, create/reuse one integration-global library manager containing one Store, one lazy-loaded document, and one `asyncio.Lock`; register WebSocket handlers once. `[CITED: https://github.com/home-assistant/developers.home-assistant/blob/master/docs/frontend/extending-websocket-api.md]`
2. For a mutation, validate the incoming command schema, then under the shared lock load the current document, validate the complete record and aggregate bounds, make a new document preserving array order, call `await store.async_save(document)`, and verify read-back before sending success. Return a bounded validation/storage error without discarding the caller's draft. `[ASSUMED]`
3. Store custom entries as ordered arrays of opaque media-source IDs plus a small allowlist of display snapshots (for example title, content type, and media class). Store provider playlists as one opaque reference and local label. Do not copy provider tracks, thumbnails that may be signed URLs, resolved URLs, auth headers, or raw request/error data. `[ASSUMED]`
4. Availability uses a separate explicit `hass.callWS({type: 'media_source/browse_media', media_content_id})` request. Keep its result in panel state as `Not checked`, `Available`, or `Unavailable in Home Assistant`; reset to `Not checked` after panel reload unless product explicitly wants a timestamped cached status. `[ASSUMED]`

### Command semantics

| Command class | Request | Successful result | Error handling |
|---------------|---------|-------------------|----------------|
| List | Namespaced type only | Versioned library document/records | HA WS authorization/load error; do not turn an unreadable store into empty data. |
| Save custom | Playlist ID for edit or omitted for create, local name, ordered entries | Accepted record and/or updated library revision | Schema errors before handler; bounded stable validation errors for bad IDs/order/size; transient storage errors preserve draft. |
| Save provider shortcut | Exact HA playlist ID and local display name | One stored shortcut | Reject non-media-source identifiers; never expand its children into local tracks. |
| Delete/remove | Stable local record ID | Confirmation of deleted local record only | Unknown ID is not-found; deletion occurs only after panel confirmation. |
| Availability | Exact saved media-source ID via the existing HA browse API | Browse-derived status only | Failure maps to unavailable without exposing exception contents or altering stored data. |

The names, exact fields, and response envelopes in this table are proposed, not source-defined. `[ASSUMED]` Every HA WS request uses the standard connection `id` and `type`; the command handler validates its own payload, then sends one result/error for that ID. Do not put user IDs, tokens, or provider request data in the saved schema.

### Bounds to take into planning

All values below are initial proposals for the discussion/plan, not Home Assistant limits. `[ASSUMED]` Tune against representative provider IDs and the approved UI copy, then centralize them as constants and test exact boundaries.

| Bound | Proposed value | Enforcement |
|-------|----------------|-------------|
| Total records (custom + provider shortcuts) | 100 | Reject create when reached; edits/deletes remain possible. |
| Custom entries per playlist | 250 | Count before allocation/save; allow duplicates and zero entries. |
| Serialized complete library | 2 MiB | Measure encoded JSON before Store write; prevents aggregate growth. |
| Playlist/shortcut name | 128 UTF-8 bytes | Non-empty after trim; reject control chars and excess length, do not silently truncate. |
| Media-source ID | 2,048 UTF-8 bytes | Require HA's `is_media_source_id`; preserve exact string without URL decoding or normalization. |
| Snapshot title | 256 UTF-8 bytes | Bound display text; no thumbnail URL in persistent records. |
| Media class/content type | 128 UTF-8 bytes each | Allowlisted scalar string fields only; reject extra keys. |

**Security caveat:** `is_media_source_id` is a URI-shape check, not an existence or secret-scrubbing function. Since references must remain opaque and exact, the public contract does not establish that every third-party media ID is credential-free. Accept IDs sourced from HA browse results, reject raw HTTP(S) URLs, avoid logs/errors containing IDs, and confirm whether providers can embed credentials in IDs before asserting an absolute no-credential guarantee. `[ASSUMED]`

### Suggested files (proposed, not existing)

```text
modules/integration/custom_components/bl_haos/
  playlist_library.py   # Store manager, schema migration, validation and serialized mutation
  websocket_api.py      # Namespaced command registration and handlers
modules/integration/tests/
  test_playlist_library.py          # Real Core SIL, Store and WS contract
  unit/test_playlist_library.py    # Pure bounded validation/migration transforms
modules/integration/panel_ui/src/
  media-panel.tsx      # Library views and explicit availability actions
  media-panel.test.tsx # Component behavior through injected hass mocks
```

`websocket_api.py` can be named `ws_api.py` if that matches the implementation plan. These paths are recommendations only. `[ASSUMED]`

### Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| HA-owned persistent file, version envelope, migration | Ad hoc JSON path, custom temp/rename logic | `homeassistant.helpers.storage.Store` with explicit atomic write option | HA-owned storage lifecycle and version/migration helper; Core source details require SIL confirmation. |
| Media-source browsing or resolving | Provider-specific clients, direct provider HTTP, manually constructed playback URLs | Existing authenticated HA media-source browse API only | HA remains catalog/auth authority; resolution materializes a URL and is outside this phase. |
| Authentication/session | Browser token, bridge proxy, custom session storage | Injected `hass` WebSocket connection and HA's `connection.user` | Retains the approved HA auth boundary. |
| Concurrent record replacement | Unlocked read/modify/write or a custom database | Shared HA-runtime `asyncio.Lock` plus one Store instance | Store's write serialization is not a logical mutation transaction. `[ASSUMED]` |

## Common Pitfalls

1. **Per-entry persistence:** Reload/unload drops entry runtime resources; placing the library in `runtime_data` or deleting it on unload breaks installation-wide survival. Keep it global and HA-owned. `[CITED: https://contributors.home-assistant.io/core/integrations/config-entries/]`
2. **Assuming Store is atomic by default:** Explicitly set `atomic_writes=True`; verify behavior against Core 2026.10.3 in SIL. `[ASSUMED; source confidence LOW]`
3. **Treating an awaited `async_save` as a durable acknowledgment:** The fetched tagged implementation appears to swallow `WriteError`; test persistence failures and read back before success. `[ASSUMED; source confidence LOW]`
4. **Using HA browse as proof of playability:** Browse and resolve have different contracts; availability must not be named or styled as playable and must never call `async_resolve_media`. `[CITED: https://github.com/home-assistant/developers.home-assistant/blob/master/docs/core/platform/media_source.md]`
5. **Normalizing opaque IDs:** Do not URL-decode, strip query components, deduplicate, or recompose IDs; existing fixture IDs deliberately include encoded separators and query syntax. `[VERIFIED: modules/integration/panel_ui/src/media-panel.test.tsx:7-10]` Exact fixture: `media-source://provider/opaque%2Fid?order=a%2Bb`.
6. **Last-write-wins race:** One Store lock alone does not prove a whole mutation is serialized; test concurrent commands and ensure no lost updates. `[ASSUMED; source confidence LOW]`
7. **Publishing raw errors/IDs:** Provider exceptions or opaque IDs may contain sensitive values. Return generic mapped errors and keep reference data out of logs/telemetry. `[ASSUMED]`
8. **False empty state after storage failure:** Core's corruption path may return `None`; distinguish uninitialized from failure and do not silently overwrite recoverable data. `[ASSUMED; source confidence LOW]`

## Code Examples

Official pattern: register from `async_setup`, validate the schema at the command boundary, and use async response handling for storage I/O. The names/shape below are illustrative proposed API values. `[CITED: https://github.com/home-assistant/developers.home-assistant/blob/master/docs/frontend/extending-websocket-api.md] [ASSUMED: command name]`

```python
@websocket_api.websocket_command(
    {probatio.Required("type"): "bl_haos/playlist_library/list"}
)
@websocket_api.async_response
async def websocket_list_library(hass, connection, msg):
    result = await library_manager.async_list()
    connection.send_result(msg["id"], result)


async def async_setup(hass, config):
    library_manager = get_or_create_library_manager(hass)
    websocket_api.async_register_command(hass, websocket_list_library)
    return True
```

For availability, call the browse path with the saved ID; do not use the resolver:

```python
result = await media_source.async_browse_media(hass, saved_media_source_id)
```

`async_browse_media`/`async_resolve_media` separation is documented; exact “available” success semantics remain provider-defined and need a synthetic-provider SIL test. `[CITED: https://github.com/home-assistant/developers.home-assistant/blob/master/docs/core/platform/media_source.md]`

## State of the Art

| Old/unsafe approach | Current approach | Impact |
|---------------------|------------------|--------|
| Voluptuous WebSocket schemas from older examples | Home Assistant developer docs now demonstrate `probatio.Required`/`Optional` with `websocket_command` | Follow the target Core's current schema decorator API. `[CITED: https://github.com/home-assistant/developers.home-assistant/blob/master/docs/frontend/extending-websocket-api.md]` |
| Custom browser token or add-on storage | Injected authenticated `hass` WebSocket context | No new credential/session flow. `[CITED: https://contributors.home-assistant.io/core/internals/websocket-api/]` |
| Resolve media IDs to test availability | Browse media IDs explicitly | Avoids creating/reserving playback URLs in a CRUD-only phase. `[CITED: https://github.com/home-assistant/developers.home-assistant/blob/master/docs/core/platform/media_source.md]` |

## Validation Architecture

Nyquist validation is enabled. `[VERIFIED: .planning/config.json:24]` Exact value: `"nyquist_validation": true`. The current SIL is pinned to Core 2026.10.3 and requires Linux/WSL2; native Windows skips it. `[VERIFIED: modules/integration/requirements-sil.txt:4-7]` Exact pins: `pytest-homeassistant-custom-component==0.13.374`, `homeassistant==2026.10.3`, `aiohttp==3.14.5`, `pytest==9.0.3`. The local test guide states SIL uses real Core and the `ha_stubs` tree is only for `tests/unit/`. `[VERIFIED: TESTING.md:11-57]`

| Requirement | Behavior | Test Type | Automated Command | File Exists? |
|-------------|----------|-----------|-------------------|-------------|
| PL-04 | CRUD, rename, order preservation, duplicate/empty draft rules, validation and concurrent mutation | unit + SIL + Vitest | `pytest tests/test_playlist_library.py -q -p asyncio --asyncio-mode=auto`; `npm --prefix modules/integration/panel_ui test` | New backend test needed; existing panel unit file exists. |
| PL-05 | Save and rename one opaque provider playlist shortcut without copying tracks | SIL + Vitest + mock Playwright | SIL command above; `npm --prefix modules/integration/panel_ui run test:mock-panel` | Extend mock harness and current mock E2E. |
| PL-06 | HA Store persistence/reload, migration, explicit browse status and non-destructive failure | SIL + Vitest + mock Playwright | SIL command above; frontend commands above | New Store/SIL and panel cases needed. |
| PL-11 | Only IDs plus allowlisted display/order metadata persist; no resolve URL/provider credentials in data/errors/logs | unit + SIL | `pytest tests/test_playlist_library.py -q -p asyncio --asyncio-mode=auto` | New tests needed; existing native playback tests are adjacent but resolve path is out of scope. |

**Test layers:**

- Pure validator/migration-transform tests may live under `tests/unit/`; they must avoid HA fixtures because this directory activates deliberately minimal HA stubs. Exercise actual `Store`, config-entry lifecycle, media-source APIs, and WebSocket schema/authorization in the real-Core SIL suite. `[VERIFIED: TESTING.md:45-57]`
- SIL should register the custom command and exercise valid/malformed requests, authenticated user policy, CRUD, `asyncio.gather` concurrency, storage/read-back failures, version migration, unload/reload, and a synthetic in-process media-source provider. Assert availability never calls `async_resolve_media` and leaves record bytes/order unchanged on denial/failure. Use existing `MockConfigEntry` and `hass` patterns. `[VERIFIED: modules/integration/tests/test_panel_registration.py:21-38; modules/integration/tests/test_ha_integration_sil.py:1-40]`
- Vitest should mock the injected `hass.callWS`: verify exact reference preservation, no proactive checks, explicit per-item checks, duplicate references, keyboard move buttons, dirty-draft/dialog focus behavior, optimistic-state rollback, transient retry, and no success before the HA response. Existing test harness defines `callWS` as a typed mock. `[VERIFIED: modules/integration/panel_ui/src/media-panel.test.tsx:1-50]`
- Extend `mock-harness.html` to return deterministic library-command results and fake persistence in memory; Playwright should cover create/edit/delete/provider shortcut/status plus responsive geometry and keyboard interactions at 375/768/1440 widths. This remains mock-only and must not be called host/provider acceptance. `[VERIFIED: modules/integration/panel_ui/mock-harness.html:109-150; modules/integration/panel_ui/e2e/mock-catalog.spec.ts:1-165]`

**Focused commands:**

```powershell
# From repository root; L2 is skipped on native Windows.
npm --prefix modules/integration/panel_ui test
npm --prefix modules/integration/panel_ui run build
npm --prefix modules/integration/panel_ui run test:mock-panel
```

```bash
# From modules/integration in the documented Ubuntu WSL2 environment.
BLHAOS_RUN_SIL=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests/test_playlist_library.py -q -p asyncio --asyncio-mode=auto
```

Local source documents the SIL command and WSL2 requirement. `[VERIFIED: TESTING.md:59-87]` No tests were run for this research-only task.

**Wave 0 gaps:**
- [ ] Add bounded record validation/migration unit coverage.
- [ ] Add Core 2026.10.3 SIL for Store, custom WebSocket commands, auth policy, media-source browse checks, storage failures, and reload/restart persistence.
- [ ] Extend `media-panel.test.tsx` and the mock harness/Playwright suite for the approved Library workflows.
- [ ] Verify whether the current pytest-homeassistant-custom-component pin exposes an authenticated WS test client; no local custom-integration WS command test pattern was found. If not, use Core's test WebSocket helper through the SIL dependency or test the registered handler with a real-Core `ActiveConnection` fixture, not a homemade auth implementation.

## Security Domain

Security enforcement is enabled; ASVS baseline is level 1. `[VERIFIED: .planning/config.json:48-49]` Exact values: `"security_enforcement": true`, `"security_asvs_level": 1`.

| ASVS Category | Applies | Standard Control |
|---------------|---------|------------------|
| V2 Authentication | Yes | HA-authenticated WebSocket connection; test anonymous rejection. |
| V3 Session Management | Yes | Reuse injected `hass`; no new token persistence or session channel. |
| V4 Access Control | Yes | Check `connection.user`; explicitly decide all-active-user vs admin-only access to this installation-wide library. |
| V5 Input Validation | Yes | Typed WS schema plus backend allowlist/length/count/aggregate checks. |
| V6 Cryptography | No new cryptography | No custom token or encryption mechanism; rely on HA storage/auth boundaries. |

| Threat | STRIDE | Mitigation |
|--------|--------|------------|
| Forged/malformed media ID, record ID, or ordering | Tampering | Validate every mutation server-side; only accept media-source URI shape and preserve exact accepted IDs. |
| Oversized names, ID arrays, or full-library replacement | Denial of service | Enforce per-field, per-playlist, and whole-document byte limits before save. |
| Cross-user access to a shared library | Information disclosure | Choose access policy; authenticated does not imply admin-only. Avoid exposing sensitive provider fields. |
| Provider error contains signed URL/credential detail | Information disclosure | Map errors to bounded generic text; never log raw IDs or provider exception bodies. |
| Concurrent writes discard one user's changes | Tampering / availability | Shared async mutation lock around full read/modify/write; concurrent SIL test. |
| Browse success presented as guaranteed playable | Elevation of claims | Label only browse availability; no playback CTA or resolve call in Phase 25. |

## Assumptions Log

| # | Claim | Resolution | Status |
|---|-------|------------|--------|
| A1 | Initial record and byte bounds | Locked in D-16; reject over-limit records without truncation or altering saved data. | Resolved |
| A2 | Initial HA Store schema | Use a new installation-wide versioned Store at major version 1; only explicit older-version migrations are supported. D-23 governs future versions. | Resolved for planning; verify migration with SIL |
| A3 | Availability result lifetime | Locked in D-24; status is panel state and resets to `Not checked` after reload. | Resolved |
| A4 | Shared-library access | Locked in D-15; all authenticated HA users share and edit the same library; no admin-only gate. | Resolved |
| A5 | Meaning of `Available` | Locked in D-14; successful browse response for the exact ID means browse-available now, not playable or guaranteed later. | Resolved; verify provider-shaped responses with SIL |
| A6 | Store write acknowledgment | Do not trust `async_save` completion alone; compare persisted state through the supported path and test write failures against Core 2026.10.3. | Resolved for planning; verify with SIL |
| A7 | Credential-bearing media IDs | Locked in D-21; accept only HA-browse references, reject raw URLs and recognizable credential query keys, preserve accepted IDs exactly, and never log IDs. Do not claim arbitrary third-party IDs are universally credential-free. | Resolved; boundary tests required |
| A8 | Persistence guarantees | PL-06 is tested through HA-owned Store reconstruction/reload in SIL. Do not claim protection against backup loss, config-directory replacement, disk corruption, or device loss. | Resolved |

## Resolved Questions and Remaining Verification

1. **Shared-library access:** Any authenticated HA user may read and edit the single installation-wide library (D-15). Confirm the command handlers use HA's authenticated connection and test two users plus anonymous rejection in SIL.
2. **Availability semantics:** A successful browse response for the exact saved reference is `Available` only at check time, regardless of playability; missing/nonmatching results, denied access, and browse errors are `Unavailable` (D-14). Test a synthetic media source for provider playlist and custom audio references without invoking resolve.
3. **Credential-bearing IDs:** Save only references originating in HA browse results. Reject raw playback URLs and recognizable auth-bearing query keys, preserve accepted IDs byte-for-byte, and never log identifiers (D-21). There is no universal detector for arbitrary secrets embedded in third-party opaque values; do not claim that guarantee for nonconforming providers.
4. **Corrupt storage:** Snapshot the public `Store.path` existence before load. A genuinely absent file may initialize empty; an existing file followed by `None`, a load error, or unsupported version fails closed and cannot be overwritten (D-17, D-22). Confirm corrupt-file quarantine and recovery behavior against Core 2026.10.3 SIL without private APIs.
5. **Migration and downgrade:** Migrate only explicitly supported older schemas. Unsupported newer major versions remain untouched and surface a recovery error; never downgrade or replace them with empty state (D-23). Verify repeat migration and future-version preservation in SIL.
6. **Write failures:** Core 2026.10.3 source indicates `async_save` may log write errors instead of raising. Test the safe acknowledgment/read-back behavior and corruption/failure paths in the pinned SIL; no success response may be sent until stored data is confirmed.

## Environment Availability

No new external runtime or package is required. Existing target dependency pin is `homeassistant==2026.10.3`; its SIL is documented for Linux/WSL2 and is auto-skipped on native Windows. `[VERIFIED: modules/integration/requirements-sil.txt:5; modules/integration/tests/test_panel_registration.py:13,27]` This task did not probe or install a runtime, start a server, or connect to a Home Assistant host.

## Sources

### Primary official developer documentation (MEDIUM)

- [WebSocket API extension](https://github.com/home-assistant/developers.home-assistant/blob/master/docs/frontend/extending-websocket-api.md) - registration, schema, async handlers, results.
- [WebSocket permissions](https://github.com/home-assistant/developers.home-assistant/blob/master/docs/auth_permissions.md) - `connection.user` and opt-in admin control.
- [Media source platform](https://github.com/home-assistant/developers.home-assistant/blob/master/docs/core/platform/media_source.md) - browse/resolve distinction and opaque IDs.
- [Config entry lifecycle](https://contributors.home-assistant.io/core/integrations/config-entries/) - setup, runtime data, unload, reload, and entry migration.
- [Storage helper serialization update](https://github.com/home-assistant/developers.home-assistant/blob/master/blog/2025-11-25-storage-helper-opt-in-serialize-in-executor.md) - Store helper and serialization threading behavior.
- [WebSocket protocol](https://contributors.home-assistant.io/core/internals/websocket-api/) - auth handshake, standard result/error envelopes.

### Version-specific Core source inspected (LOW via source-confidence seam; verify in SIL)

- [Core 2026.10.3 storage.py](https://github.com/home-assistant/core/blob/2026.10.3/homeassistant/helpers/storage.py)
- [Core 2026.10.3 atomic file writer](https://github.com/home-assistant/core/blob/2026.10.3/homeassistant/util/file.py)
- [Core 2026.10.3 media-source helper](https://github.com/home-assistant/core/blob/2026.10.3/homeassistant/components/media_source/helper.py)
- [Core 2026.10.3 media-source models](https://github.com/home-assistant/core/blob/2026.10.3/homeassistant/components/media_source/models.py)
- [Core 2026.10.3 WebSocket API registration/decorators](https://github.com/home-assistant/core/tree/2026.10.3/homeassistant/components/websocket_api)

### Local evidence (read this session)

- [25-CONTEXT.md](25-CONTEXT.md), [25-UI-SPEC.md](25-UI-SPEC.md), [.planning/REQUIREMENTS.md](../../REQUIREMENTS.md), [.planning/ROADMAP.md](../../ROADMAP.md), [.planning/STATE.md](../../STATE.md), and [.planning/AGENTS.md](../../AGENTS.md).
- [Integration entry lifecycle](../../../modules/integration/custom_components/bl_haos/__init__.py), [panel media API](../../../modules/integration/panel_ui/src/media-panel.tsx), [panel component tests](../../../modules/integration/panel_ui/src/media-panel.test.tsx), [SIL tests](../../../modules/integration/tests/test_ha_integration_sil.py), [panel lifecycle tests](../../../modules/integration/tests/test_panel_registration.py), [mock harness](../../../modules/integration/panel_ui/mock-harness.html), and [TESTING.md](../../../TESTING.md).

## Metadata

**Confidence breakdown:**
- Standard stack: MEDIUM - official Home Assistant docs and repository pins agree; no new dependency proposed.
- Architecture: MEDIUM - official setup, auth, browse and lifecycle docs align with the local authenticated panel; exact Store lifecycle advice includes LOW-tier source observations.
- Pitfalls: MEDIUM - media browse/resolve and config-entry lifecycles are documented; Store error/corruption details are LOW until exercised in SIL.

**Research date:** 2026-10-25  
**Valid until:** 2026-11-24 for stable Core APIs; recheck version-specific Store behavior if the target Core pin changes.