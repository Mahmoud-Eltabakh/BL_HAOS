# Phase 25: Saved Playlist Library - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md; this log preserves the alternatives considered.

**Date:** 2026-10-24
**Phase:** 25-saved-playlist-library
**Areas discussed:** Persistence and ownership, Playlist records and editing, Stale references and phase boundary, Reviewed project todo

---

## Persistence and Ownership

| Option | Description | Selected |
|--------|-------------|----------|
| Installation-wide library | One HA-install library; choose a speaker only at playback time. | Yes |
| Per-speaker library | Keep different playlists for each speaker. | |
| HA-owned storage and authenticated WebSocket | Versioned HA persistent storage, integration-owned CRUD commands, serialized atomic writes, and migrations. | Yes |
| Browser storage or config-entry options | Persist through browser state or integration options. | |
| Last-write-wins | Allow concurrent updates to overwrite each other. | |
| Reject schema upgrades | Fail on schema changes rather than migrate records. | |

**User's choice:** Accepted all recommendations.
**Notes:** Versioned storage migration must preserve valid opaque references and must not resolve them.

---

## Playlist Records and Editing

| Option | Description | Selected |
|--------|-------------|----------|
| Opaque IDs plus display snapshots | Ordered HA media IDs and labels, without resolved URLs. | Yes |
| IDs only or broader provider metadata | Store no display labels or copy expanded provider metadata. | |
| Allow duplicates and empty drafts | Preserve duplicates; allow empty drafts but disable playback. | Yes |
| Reject duplicates or empty drafts | Prevent repeated tracks or empty drafts. | |
| Move controls | Accessible Move Up/Move Down controls. | Yes |
| Drag-only reorder | Reorder only by drag and drop. | |
| Opaque saved reference | Keep a provider playlist as one HA-owned reference and a locally renameable/removable shortcut. | Yes |
| Expand provider items | Copy provider tracks into a BL-HAOS custom playlist. | |

**User's choice:** Accepted all recommendations.
**Notes:** Provider-owned contents remain read-only; no Phase 26 queue behavior.

---

## Stale References and Phase Boundary

| Option | Description | Selected |
|--------|-------------|----------|
| On-demand HA check | Check a saved reference through HA media-source browsing when requested. | Yes |
| Proactive checks | Check every record on library load. | |
| Preserve reference and show result | Report unavailable/stale state without deleting or rewriting saved data. | Yes |
| Remove or rewrite failed references | Mutate the library when a check fails. | |
| Keep queue/playback in Phase 26 | Phase 25 implements CRUD and availability status only. | Yes |
| Add playlist playback to Phase 25 | Start saved playlists as part of library implementation. | |
| Authenticated HA panel | Keep HA-owned operations in the existing authenticated panel. | Yes |
| Add-on Ingress | Put playlist operations in the bridge's Ingress UI. | |
| Bound and validate writes | Validate record data and limits at the integration boundary. | Yes |
| Trust client writes | Accept browser-supplied records without server validation. | |

**User's choice:** Accepted all recommendations.
**Notes:** No provider API clients, credentials, resolved playback URLs, or live-host operations.

---

## Reviewed Project Todo

| Option | Description | Selected |
|--------|-------------|----------|
| Leave deferred | Keep general pinned Linux HA SIL CI outside the playlist phase. | Yes |
| Fold into Phase 25 | Add general CI improvements to this phase. | |

**User's choice:** Leave deferred.
**Notes:** The todo matched on broad HA/SIL keywords but does not fit Phase 25's saved-playlist scope.

---

## Claude's Discretion

Concrete HA storage helper, WebSocket command schema, migration mechanics, bounded limits, UI presentation, and focused local test selection are left for research and planning against supported APIs and repository conventions.

## Deferred Ideas

- Add pinned Linux Home Assistant SIL CI remains a reviewed, deferred project todo.
- Playlist launch, sequential advancement, and queue controls remain in Phase 26.
- Live provider, physical playback, and HA-shell production acceptance remain deferred; local mock progression does not grant deployment or release approval.
