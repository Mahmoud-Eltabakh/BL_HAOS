# Phase 25: Saved Playlist Library - Context

**Gathered:** 2026-10-24
**Status:** Ready for planning

<domain>
## Phase Boundary

Implement the saved playlist library for the existing authenticated Home Assistant media panel: custom playlists of ordered Home Assistant media references, saved provider-playlist references, persistent CRUD, and explicit availability/stale-reference status. This phase covers PL-04, PL-05, PL-06, and PL-11. Phase 26 owns playlist launch, sequential playback, and queue controls; this phase must not implement queue state or playback advancement.

Work is authorized for local/mock-only progression. Phase 24 production acceptance remains pending: PL-01/02/03 are not production-verified, T-24-15 remains OPEN/HIGH, T-24-16 remains OPEN/MEDIUM, and release/deployment are blocked. Do not perform live-host operations or describe mock results as production acceptance.

**Autonomous-run commit override (2026-10-27):** Do not stage or commit Phase 25 work in this run. The integration panel/source tree contains pre-existing untracked and modified baseline files that overlap the planned task outputs, so even explicit-path staging could absorb work not created by this run. Preserve the current index and worktree; record completed local work in summaries. Any commits require a later user review and explicit scope approval.
</domain>

<decisions>
## Implementation Decisions

### Persistence and Ownership
- **D-01:** The library is installation-wide, not scoped to a speaker. A target speaker is selected when a playlist is played in Phase 26.
- **D-02:** Keep playlist data in Home Assistant-owned persistent storage and expose CRUD through an authenticated Home Assistant WebSocket boundary. Do not persist playlist data in browser storage or the add-on bridge.
- **D-03:** Serialize concurrent mutations and save atomically.
- **D-04:** Version the stored record schema and migrate valid references forward without resolving them.

### Playlist Records and Editing
- **D-05:** Custom playlist entries preserve ordered opaque Home Assistant media IDs and the display metadata needed by the library. Never store resolved playback URLs, provider credentials, or credential-bearing request data.
- **D-06:** Allow duplicate entries and empty drafts. Empty drafts are not playable.
- **D-07:** Reordering must be keyboard-accessible; provide explicit Move Up/Move Down controls rather than drag-only operation.
- **D-08:** A saved provider playlist is one opaque Home Assistant playlist reference, not an expanded copy of its provider tracks. Users may rename or remove the local shortcut; provider contents remain read-only.

### Availability and Phase Boundary
- **D-09:** Availability is checked on demand through Home Assistant's media-source browsing path, not by contacting providers directly or checking every record on panel load.
- **D-10:** A failed or denied check is visible as unavailable/stale, but never deletes or rewrites the saved reference. Rechecking remains explicit.
- **D-14:** Define `Available` narrowly as a successful authenticated HA browse response for the exact saved reference. This means browse availability at check time only; it does not claim playability or future provider availability.
- **D-15:** Any active authenticated Home Assistant user may read and edit the installation-wide library. Do not store a per-user copy or add an admin-only gate; the library contains media references and display metadata, not credentials.
- **D-16:** Use initial server-side limits of 100 total records, 250 entries per custom playlist, 2 MiB serialized library size, 128 UTF-8 bytes per name, 2,048 bytes per media-source ID, 256 bytes per display title, and 128 bytes each for media class/content type. Reject over-limit input without truncation or loss of existing data; keep limits centralized and covered at boundaries.
- **D-17:** Treat an unreadable, corrupt, or unsupported-version store as an error, never as an empty library eligible for overwrite. Preserve the stored data, disable mutations until the issue is resolved, and show a bounded recovery message.
- **D-18:** A deliberate custom-playlist create allocates one stable local ID; retries using that ID update or return the same record rather than creating duplicates. Separate deliberate creates may have identical names and content.
- **D-19:** Save at most one provider shortcut per exact opaque media-source ID. Repeating a save is idempotent and must not duplicate the shortcut or overwrite its locally chosen name.
- **D-20:** Serialize all library mutations. Independent record updates must not overwrite one another; a stale concurrent edit to the same record returns a conflict and preserves the newer saved version.
- **D-21:** Accept media references only from Home Assistant browse results and require HA media-source ID shape. Reject raw playback URLs and references with recognizable credential-bearing query keys; preserve accepted IDs byte-for-byte and never log IDs. Do not claim arbitrary third-party IDs are credential-free; a reference identified as credential-bearing is not saved.
- **D-22:** Before the first Store load, record whether the public `Store.path` exists. A missing file may initialize an empty library; if a previously existing file yields `None`, or an unsupported-version/load error occurs, fail closed, preserve the file/quarantine, and disable mutations. Verify this distinction in Core 2026.10.3 SIL.
- **D-23:** Migrate only explicitly supported older schema versions. Preserve unknown newer major versions unchanged and surface a recovery error; never downgrade or initialize over an unsupported version.
- **D-24:** Availability results are transient panel state, reset to `Not checked` after panel reload, and are never persisted in playlist records.
- **D-11:** Phase 25 owns CRUD and availability status only. Phase 26 owns launch, sequential playback, and queue controls.
- **D-12:** Keep HA-owned operations in the existing authenticated Home Assistant panel context; do not move them into the add-on Ingress UI.
- **D-13:** Validate and bound all mutations at the Home Assistant integration boundary, including record shape, identifiers, ordering, and size.

### Reviewed Todos
- `Add pinned Linux Home Assistant SIL CI` was reviewed and left deferred. It is a general CI improvement, not a playlist-library requirement.

### Claude's Discretion
- Choose the concrete Home Assistant storage helper, WebSocket command schema, and migration mechanics after researching current supported APIs and nearby integration conventions.
- Select focused unit, Home Assistant integration/SIL, component, and mock-browser tests. Do not claim live provider, host, or playback verification.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Scope and requirements
- `.planning/ROADMAP.md` - Phase 25 goal and success criteria; Phase 26 boundary.
- `.planning/REQUIREMENTS.md` - PL-04, PL-05, PL-06, and PL-11 definitions and traceability.
- `.planning/PROJECT.md` - HA-owned media-reference decision and production constraints.

### Prior phase and security boundary
- `.planning/phases/24-ha-media-catalog-provider-playback/24-CONTEXT.md` - HA authentication, opaque media-source IDs, and Phase 25/26 boundaries.
- `.planning/phases/24-ha-media-catalog-provider-playback/24-VERIFICATION.md` - Explicit local-mock-only completion scope, pending production requirements, and open security findings.

### Existing integration and panel
- `modules/integration/custom_components/bl_haos/__init__.py` - Config-entry lifecycle and authenticated custom-panel registration.
- `modules/integration/panel_ui/src/media-panel.tsx` - Existing HA-injected browse panel, reference handling, and interaction patterns.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `modules/integration/panel_ui/src/media-panel.tsx` already browses HA media with the injected `hass` connection and retains opaque `media-source://` IDs. Extend this authenticated experience for library operations.
- `modules/integration/custom_components/bl_haos/__init__.py` owns integration setup and panel lifecycle. No playlist persistence or custom storage/WebSocket CRUD implementation was found in the integration; research and tests must establish the supported HA boundary before implementation.

### Established Patterns
- Home Assistant remains the media-source catalog, resolver, authentication, and credential authority. Never proxy provider credentials or store resolved playback URLs.
- Phase 24 deliberately uses an HA-authenticated panel for media actions, distinct from the add-on Ingress UI.
- Existing panel tests and mock Playwright harness cover injected HA behavior and responsive keyboard interactions; they can be extended for local playlist CRUD and persistence scenarios.

### Integration Points
- The authenticated panel connects to Home Assistant's media-source browse APIs and the selected BL-HAOS integration entity.
- Persistent playlist storage and validated CRUD commands belong to the integration; browser components should receive data through authenticated HA APIs.
- Phase 26 will consume the saved library for playlist playback. Keep the record format usable by that phase without adding queue state here.
</code_context>

<specifics>
## Specific Ideas

- Preserve each original opaque media-source reference and order exactly; display snapshots are labels, not alternate playback sources.
- Treat provider playlists as saved shortcuts, not as editable lists of provider-owned tracks.
- Make availability checks explicit and non-destructive. Never silently remove inaccessible media from a user's library.
</specifics>

<deferred>
## Deferred Ideas

### Reviewed Todos (not folded)
- `Add pinned Linux Home Assistant SIL CI` - reviewed but not included because it is a general CI improvement outside Phase 25's saved-playlist scope.

- Playlist launch, sequential advancement, and queue controls remain assigned to Phase 26.
- Live provider, production-panel, physical playback, and HA-shell acceptance remain post-milestone production work. No deployment or release approval is implied.
</deferred>

---

*Phase: 25-saved-playlist-library*
*Context gathered: 2026-10-24*
