# Phase 25: Saved Playlist Library - Pattern Map

**Mapped:** 2026-10-25  
**Files analyzed:** 8 proposed implementation/test surfaces  
**Tracked analogs found:** 4 partial matches / 8 surfaces; no exact playlist-library analog exists

## File Classification

| New/Modified File or Surface | Role | Data Flow | Closest Tracked Analog | Match Quality |
|------------------------------|------|-----------|------------------------|---------------|
| `modules/integration/custom_components/bl_haos/playlist_library.py` | service/store | persistent CRUD, migration, serialized mutations | `custom_components/bl_haos/__init__.py::_PanelOwners` | partial: integration-global `hass.data` ownership and lock only; no Store or records |
| `modules/integration/custom_components/bl_haos/websocket_api.py` | request handler | authenticated request-response | none | no custom integration WebSocket commands found |
| `modules/integration/custom_components/bl_haos/playlist_library.py` validation/migration | utility/model | bounded transform and version migration | `custom_components/bl_haos/media_player.py::_normalize_media_type` | partial: one bounded scalar, not record validation or migration |
| `modules/integration/tests/test_playlist_library.py` | SIL test | Home Assistant API, storage, lifecycle, concurrency | `tests/test_ha_integration_sil.py::_setup_entry`; `tests/test_panel_registration.py::test_owned_panel_serializes_multiple_entries` | role-match for Core fixtures/lifecycle only; no playlist Store/WebSocket tests |
| `modules/integration/tests/unit/test_playlist_library.py` | unit test | validation/migration transform | none | no tracked playlist bounds or migration tests |
| `modules/integration/panel_ui/src/media-panel.tsx` | panel component | HA request-response and view state | none tracked | no tracked panel implementation; requested CRUD flows are absent |
| `modules/integration/panel_ui/src/media-panel.test.tsx` | Vitest component test | mocked injected-HA state transitions | none tracked | no tracked Vitest suite in this submodule |
| `modules/integration/panel_ui/mock-harness.html`, `panel_ui/e2e/mock-catalog.spec.ts` | mock harness / browser test | mock request-response and UI flow | none tracked | no tracked mock Playwright harness in this submodule |

## Pattern Assignments

### Integration-global manager: partial ownership pattern only

**Analog:** `modules/integration/custom_components/bl_haos/__init__.py::_PanelOwners` (`_PANEL_DATA`, `_PanelOwners.acquire`, `_PanelOwners.release`, `async_setup_entry`, `async_unload_entry`)

`_PanelOwners` is kept in `hass.data` with `setdefault` and has an `asyncio.Lock` around shared panel acquire/release. This is a concrete pattern for integration-lifetime shared state and serialized lifecycle operations, not a Store manager: it is initialized from config-entry setup and owns panel registration, not installation-wide persisted records or WebSocket handlers.

```python
@dataclass
class _PanelOwners:
    lock: asyncio.Lock = field(default_factory=asyncio.Lock)
    owners: set[str] = field(default_factory=set)
    ...

panel = hass.data.setdefault(_PANEL_DATA, _PanelOwners())
```

**Guidance:** Reuse only the shared `hass.data` ownership and lock concept. D-02/D-03/D-20 require the playlist manager to outlive entry unload, and its lock must cover the complete library read/validate/replace/save transaction. No tracked pattern exists for `Store`, atomic save/read-back, startup-wide command registration, or custom WebSocket response/error handling; follow Phase 25 RESEARCH rather than copying panel lifecycle code as if it implemented these contracts.

### Bounded validation: scalar-only partial pattern

**Analog:** `modules/integration/custom_components/bl_haos/media_player.py::_normalize_media_type` and `modules/integration/custom_components/bl_haos/const.py::MEDIA_TYPE_MAX_LENGTH`

```python
candidate = media_type.strip()
if not candidate or len(candidate) > MEDIA_TYPE_MAX_LENGTH or not _MEDIA_TYPE_PATTERN.fullmatch(candidate):
    return None
return candidate.lower()
```

This centralizes one 128-character scalar limit and accepts/rejects without truncation. It is not a template for playlist mutation semantics: it normalizes a media type and drops an unusable value. D-13/D-16 require full record/identifier/order/aggregate-size validation at the HA boundary, exact byte-count limits, and rejection that preserves existing data. No tracked playlist record validator or boundary tests were found.

**Migration:** No tracked integration Store, schema version, or migration callback was found. D-04/D-17 require deterministic forward migration of valid opaque references, and unreadable/corrupt/unsupported data must not become an empty writable library. There is no local migration code to copy.

### Home Assistant SIL: fixture and lifecycle test patterns

**Analogs:** `modules/integration/tests/test_ha_integration_sil.py::_setup_entry`, `test_native_play_media_resolves_one_opaque_reference`, `test_native_play_media_resolution_failure_is_bounded`; `modules/integration/tests/test_panel_registration.py::panel_environment`, `test_owned_panel_http_unload_and_reload`, `test_owned_panel_serializes_multiple_entries`

`_setup_entry` creates and adds a real `MockConfigEntry`, patches the bridge session, calls `hass.config_entries.async_setup`, and drains pending HA work. The SIL cases use real Core entities/APIs while mocking external transport. The panel registration suite pins the Core version, asserts reload/unload lifecycle behavior, and uses `asyncio.gather` to exercise concurrent setup.

```python
entry = MockConfigEntry(domain=DOMAIN, ...)
entry.add_to_hass(hass)
with client_patch, flow_patch:
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
```

**Guidance:** Follow these fixtures for real-Core Store, registration, authentication, and lifecycle SIL once playlist commands exist. Add focused assertions for malformed and over-limit mutations, all-user authenticated access (D-15), create retry identity (D-18), provider-reference idempotency/name preservation (D-19), serialized independent updates and same-record conflicts (D-20), corruption/future-version preservation (D-17), and restart/reload persistence. Existing SIL coverage proves none of those playlist behaviors; keep the tests in the pinned Linux/WSL SIL, not the minimal `tests/unit/ha_stubs` environment.

### Panel state, Vitest, and mock Playwright

**Tracked analogs:** none in `modules/integration` for the HA panel source/test or mock browser harness. The workspace contains a local `panel_ui` tree, but `git ls-files` from the integration submodule returns no tracked files under `panel_ui/`; it is therefore excluded from pattern assignments under the tracked-source gate. No panel CRUD state flow, Vitest fixture, mock library persistence, or mock Playwright CRUD case can be treated as an established tracked convention.

**Guidance:** Treat Phase 25's authenticated injected-`hass` panel CRUD, per-reference status, dirty-draft/confirmation behavior, and Vitest/Playwright test structure as new patterns guided by `25-UI-SPEC.md` and `25-RESEARCH.md`. Do not infer that existing browser-local storage or add-on Ingress is acceptable; D-02/D-12 prohibit both for library operations. The UI contract requires server acknowledgment before success, manual non-destructive availability checks, keyboard Move Up/Move Down, and preservation of draft/row state on failures.

## Shared Constraints for the Planner

- **D-14:** `Available` means only a successful authenticated HA browse response for the exact saved reference at check time. It is not playability or future provider availability; do not use media resolution.
- **D-15:** Any active authenticated HA user may read/edit the installation-wide library. Do not add admin-only authorization or per-user copies.
- **D-16:** Centralize and enforce all initial limits without truncation: 100 total records; 250 entries per custom playlist; 2 MiB serialized library; name 128 UTF-8 bytes; media-source ID 2,048 UTF-8 bytes; title 256 UTF-8 bytes; media class and content type 128 UTF-8 bytes each.
- **D-17:** Corrupt, unreadable, or unsupported-version storage is an error, not an empty library. Preserve data, disable mutation, and show bounded recovery guidance.
- **D-18:** A deliberate create has one stable local ID; retries with that ID update/return the same record. Separate creates may have equal names/content.
- **D-19:** Save at most one provider shortcut per exact opaque ID. Repeated save is idempotent and must not replace its local name.
- **D-20:** Serialize every mutation. Independent record changes must not be lost; stale same-record edits conflict while preserving the newer version.
- Keep the library installation-wide in HA-owned storage, preserve opaque IDs and custom-entry order, and store only allowlisted display snapshots. No resolved URLs, provider credentials, or credential-bearing request data.
- Phase 25 is local/mock-only and owns CRUD plus availability status. Phase 26 owns launch, sequential playback, and queue controls. Do not perform or claim live-host/provider/playback acceptance, deployment, or release.

## No Analog Found

| Surface | Missing pattern |
|---------|-----------------|
| HA Store and custom WebSocket manager | No tracked Store-backed integration-global manager, command registration, payload schema, or result/error handler. |
| Playlist record bounds and schema migration | No tracked aggregate/record validator, versioned library document, migration path, corruption recovery, or corresponding boundary tests. |
| Playlist CRUD panel and tests | No tracked HA panel component, CRUD/state tests, Vitest suite, or mock Playwright harness in the integration submodule. |

## Metadata

**Analog search scope:** `modules/integration/custom_components/bl_haos/`, `modules/integration/tests/`, and `modules/integration/panel_ui/`; panel source tree excluded as untracked.  
**Tracked analogs read:** 5 source/test files.  
**Pattern extraction date:** 2026-10-25