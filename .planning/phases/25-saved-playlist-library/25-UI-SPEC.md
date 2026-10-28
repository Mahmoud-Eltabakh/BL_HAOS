---
phase: "25"
slug: "saved-playlist-library"
status: approved
shadcn_initialized: false
preset: none
created: "2026-10-25"
---

# Phase 25 — UI Design Contract

> Visual and interaction contract for the Saved Playlist Library. Keep the existing Home Assistant custom panel and its injected `hass` context. This contract covers PL-04, PL-05, PL-06, and PL-11 only. Local/mock progression does not establish production host acceptance.

---

## Design System

| Property | Value |
|----------|-------|
| Tool | none |
| Preset | not applicable; no shadcn configuration or package |
| Component library | none; React with semantic HTML controls |
| Icon library | `lucide-react` 0.344.0 |
| Font | Existing `ui-sans-serif, sans-serif` panel stack; no new font |

Retain the dark, restrained Neumorphic surface language and inline custom-element styling in `modules/integration/panel_ui/src/media-panel.tsx`. Reuse the existing `neu-page`, `neu-surface`, `neu-inset`, `neu-button`, and `:focus-visible` vocabulary. Keep one primary raised library surface; playlist rows should remain a scannable list, not nested cards. Do not add a component library, provider SDK, or new authentication surface.

---

## Library and Editing Contract

### Navigation and library

- Keep the feature inside the existing HA-owned panel, using its supplied `hass` object for all Home Assistant operations. Do not move library actions into add-on Ingress or introduce a separate token/session flow.
- Provide two clearly named views, `Library` and `Browse media`, using a keyboard-operable tab/segmented navigation pattern with a visible selected state. Open the panel on `Library`. Preserve the existing catalog hierarchy and navigation when browsing.
- Treat the library as installation-wide: show no speaker selector or speaker-specific library grouping. Do not add a Play, Launch, queue, or playback-status action; Phase 26 owns playback and queue behavior.
- Divide populated library content into `Your playlists` and `Saved Home Assistant playlists`. Custom rows show the local name and item count. Provider shortcuts show the local name, identify the reference as a Home Assistant playlist, and state that provider contents are managed by Home Assistant.
- Give each custom playlist `Edit playlist` and `Delete playlist` actions. Editing exposes its name and ordered media references. Give each provider shortcut `Rename shortcut`, `Check availability`, and `Remove shortcut`; do not expose provider tracks as editable local entries.
- A provider playlist encountered in `Browse media` has a `Save to library` action. Save one opaque Home Assistant playlist reference as a local shortcut; never expand or copy its tracks. Allow the shortcut's local display name to be edited without changing provider-owned content.

### Create and edit custom playlists

- `Create playlist` opens the editor with an empty, editable name and zero entries. Require a non-empty playlist name to save, but allow saving an empty playlist draft. An empty playlist is simply an empty library record in this phase; do not imply it can be played.
- The editor contains a labelled `Playlist name` input, an ordered list of entries, `Add media`, and explicit `Save playlist` or `Save changes` actions. A new draft uses `Discard draft` to leave without saving; an existing playlist uses `Stop editing` to leave without saving. Rename uses this same editor.
- `Add media` opens the existing HA media catalog in selection mode. Show an `Add media` action only for playable audio media items; folders remain navigable. Adding the same reference more than once is allowed and must not be blocked or silently deduplicated. Preserve each item's opaque Home Assistant media ID and display snapshot.
- Each custom entry is a stable ordered list item with its title and available display metadata, plus `Check availability`, `Move entry up`, `Move entry down`, and `Remove media item` controls. `Check availability` is user-triggered for that specific reference and follows the same non-destructive status behavior as a saved provider shortcut. Move controls are explicit and keyboard-operable; never make dragging the only reorder method. Disable `Move entry up` for the first entry and `Move entry down` for the last. Announce successful movement and its new position without moving focus away from the operated entry.
- Removing an entry changes only the unsaved editor draft. `Discard draft` or `Stop editing` restores the persisted version. When a dirty editor is closed or navigated away from, ask before discarding; offer `Keep editing` and `Discard changes`, and default focus to `Keep editing`.
- Saving preserves the entry order and reference identity. Keep the editor contents and all valid draft data visible on validation or save failure; do not report success before the HA-owned operation succeeds. For correctable validation errors, require the stated correction before saving again. Offer retry without changes only for transient operation failures.

### Availability and non-destructive behavior

- Show an explicit status for each saved provider reference and each custom media reference: `Not checked`, `Available`, or `Unavailable in Home Assistant`. Do not imply an unchecked item is available.
- Availability is checked only after the user activates `Check availability`, through the existing authenticated Home Assistant media-source path. Do not proactively check every item on panel load.
- While checking, label the in-progress action and prevent duplicate submissions for that item. On success or failure, update only the visible status and announce the result. A failed or denied check leaves the original reference and ordering intact; never delete, rewrite, or disable editing of the saved reference because it is unavailable.
- Keep availability distinct from playability. Do not add a playback CTA or imply provider playback, host acceptance, or production verification.

### Destructive actions

- Deleting a custom playlist requires a confirmation dialog naming the playlist and explaining that its local playlist definition and references will be removed. Use `Keep playlist` and `Delete playlist`; focus `Keep playlist` initially. Delete only after explicit confirmation.
- Removing a saved provider shortcut also requires confirmation and must say that only the BL-HAOS library shortcut is removed; the Home Assistant provider playlist is unchanged. Use `Keep shortcut` and `Remove shortcut`, with focus initially on `Keep shortcut`.
- Dialogs use native dialog semantics, a labelled heading, focus containment, Escape handling, and focus restoration to the invoking action. If the persistent operation fails, close no dialog as though successful and retain the library row.

---

## Spacing Scale

Declared values (multiples of 4):

| Token | Value | Usage |
|-------|-------|-------|
| xs | 4px | Icon and compact metadata gaps |
| sm | 8px | Row control gaps and compact field spacing |
| md | 16px | Default row padding, editor fields, and control spacing |
| lg | 24px | Page padding on narrow screens and section spacing |
| xl | 32px | Major layout gaps |
| 2xl | 48px | Empty-state and major section separation |
| 3xl | 64px | Page-level separation only |

Exceptions: All interactive controls must retain a minimum 44px hit area, including Move Up/Down, row actions, tab controls, and dialog actions. Use only the declared spacing values for page padding at every width; use 24px on narrow screens.

---

## Typography

Use exactly four sizes and two weights, consistent with the current panel.

| Role | Size | Weight | Line Height |
|------|------|--------|-------------|
| Metadata and status | 12px | 400 | 1.5 |
| Body, input, and row title | 14px | 400 | 1.5 |
| Section heading and selected navigation | 16px | 600 | 1.2 |
| Page heading | 24px | 600 | 1.2 |

---

## Color

| Role | Value | Usage |
|------|-------|-------|
| Dominant (60%) | `#151a23` | Page background and unframed space |
| Secondary (30%) | `#242d3b` | Main library surface and section surfaces |
| Accent (10%) | `#3b82f6` | Selected `Library`/`Browse media` view, selected entry, and primary `Create playlist` action only |
| Destructive | `#e11d48` / existing rose semantic | Delete and remove confirmation actions and error states |

Accent reserved for: the selected view, the selected custom entry when applicable, and the primary `Create playlist` action. Do not use accent blue for provider facts, availability labels, every button, or destructive actions. Reuse existing semantic colors sparingly: emerald for confirmed available status, amber for unchecked/in-progress attention, rose for unavailable/errors/destructive actions, and cyan `#67e8f9` for focus-visible outlines. Status meaning must also be expressed in text or icons, not color alone. Preserve readable contrast on raised and inset surfaces.

---

## Copywriting Contract

| Element | Copy |
|---------|------|
| Primary CTA | Create playlist |
| Custom playlist row actions | `Edit playlist`; `Delete playlist` |
| Saved shortcut row actions | `Rename shortcut`; `Check availability`; `Remove shortcut` |
| Editor actions | New draft: `Save playlist` / `Discard draft`. Existing playlist: `Save changes` / `Stop editing`. |
| Dirty editor confirmation | `Keep editing` / `Discard changes`. Default focus: `Keep editing`. |
| Delete confirmation actions | `Keep playlist` / `Delete playlist`. Default focus: `Keep playlist`. |
| Remove shortcut confirmation actions | `Keep shortcut` / `Remove shortcut`. Default focus: `Keep shortcut`. |
| Empty library heading | Your library is empty |
| Empty library body | Create a playlist or browse Home Assistant media to save a playlist reference. |
| Empty custom playlist | No media added yet. Add media to build this playlist, or save it as an empty draft. |
| Empty saved-provider section | No Home Assistant playlists saved. Browse media to save a playlist reference. |
| Empty media picker | No playable audio media are available in this Home Assistant source. |
| Name validation | Enter a playlist name before saving. |
| Record-shape validation | This playlist has details that can't be saved yet. Review the playlist name and entries, correct any marked fields, then select `Save playlist` or `Save changes`. Your valid draft data is still here. |
| Identifier/reference validation | The selected playlist or a media item couldn't be matched. Return to Your playlists and select `Edit playlist` on the intended row; for an affected media item, remove it or add it again from Browse media. Your valid draft data is still here. |
| Ordering validation | The item order couldn't be saved. Use `Move entry up` or `Move entry down` to arrange the entries, then select `Save playlist` or `Save changes`. Your draft and valid entries are still here. |
| Size validation | This playlist is too large to save. Remove some entries or shorten the playlist name, then select `Save playlist` or `Save changes`. Your remaining draft data is still here. |
| Availability default | Not checked |
| Availability success | Available in Home Assistant |
| Availability failure | Unavailable in Home Assistant. The saved reference was kept. |
| Create operation failure (transient) | Couldn't save this playlist right now. Your draft is still here. Select `Save playlist` to try again, or `Discard draft` to leave without saving. |
| Edit or rename operation failure (transient) | Couldn't save changes to “{playlist name}” right now. Your edits are still here. Select `Save changes` to try again, or `Stop editing` to leave without saving. |
| Save provider shortcut operation failure (transient) | Couldn't save “{playlist name}” to your library right now. Nothing was added. Select `Save to library` to try again, or return to Browse media. |
| Delete playlist operation failure (transient) | Couldn't delete “{playlist name}” right now. It remains in your library. Select `Delete playlist` to try again, or `Keep playlist`. |
| Remove shortcut operation failure (transient) | Couldn't remove “{playlist name}” right now. The shortcut remains in your library, and the Home Assistant playlist is unchanged. Select `Remove shortcut` to try again, or `Keep shortcut`. |
| Load error | Couldn't load your library. Reconnect Home Assistant, then select Retry loading. |
| Corrupt or unsupported storage | Couldn't read saved playlists. No data was changed. Ask a Home Assistant administrator to check storage, then select Retry loading. Keep library mutations disabled until the library loads successfully. |
| Access error | Home Assistant couldn't access the library. Reconnect Home Assistant or ask an administrator to restore access, then select Retry loading. |
| Destructive confirmation | Delete playlist: Delete “{playlist name}” from your BL-HAOS library? Its saved entries will be removed. This cannot be undone. |
| Provider shortcut confirmation | Remove shortcut: Remove “{playlist name}” from your BL-HAOS library? The Home Assistant playlist itself will not be changed. |
| Discard confirmation | Discard changes: Discard unsaved changes to “{playlist name}”? The saved playlist will remain unchanged. Use `Keep editing` or `Discard changes`; default focus: `Keep editing`. |

---

## UI Considerations
Applicable state considerations resolved: 26 explicit, 10 backstop, 0 unresolved. Classifications and coverage were checked with the GSD UI consideration probe. Backstop items require local rendered-panel assertions; they are not evidence of production HA-shell acceptance.

| Element / category | Status | Resolution |
|--------------------|--------|------------|
| library / empty | resolved | Show the exact empty-library copy and offer Create playlist and Browse media. |
| library / loading | resolved | Show operation progress, prevent duplicate submission for the affected action, and retain unrelated rows. |
| library / error | resolved | Use the specified actionable load or mutation error copy; preserve valid records and offer the stated recovery. For corrupt or unsupported storage, do not show an empty state or enable mutations; preserve stored data until an administrator resolves the issue. |
| library / populated | resolved | Separate custom playlists and saved Home Assistant playlists into named sections with stable scannable rows. |
| library / partial | resolved | Keep per-reference availability independent; retain valid rows and actions if another check or operation fails. |
| library / overflow | resolved | Scroll the library region without horizontal overflow and keep row actions reachable. `verification: backstop` |
| library / zero-one-many | resolved | Use stable row geometry for zero, one, or many records and the specified empty state for zero. |
| library / long-text | resolved | Wrap long playlist/provider labels without clipping controls; preserve complete accessible names. `verification: backstop` |
| editor / empty | resolved | Start with a named empty draft state; permit saving an empty draft while keeping it non-playable in this phase. |
| editor / loading | resolved | Show save progress, prevent duplicate submissions, and keep the current draft visible. |
| editor / error | resolved | Distinguish correctable validation errors from transient failures; preserve valid draft data and show the specified recovery copy. |
| editor / populated | resolved | Show the ordered entries and their display metadata with explicit save and edit actions. |
| editor / partial | resolved | Preserve usable draft fields and entries when references are incomplete; show their individual unavailable status. |
| editor / overflow | resolved | Allow the editor and entry list to scroll while save and entry controls remain reachable. `verification: backstop` |
| editor / zero-one-many | resolved | Keep entry layout stable for zero, one, or many items; use the empty-draft copy for zero. |
| editor / long-text | resolved | Wrap long names and titles within the editor while preserving accessible labels. `verification: backstop` |
| media picker / empty | resolved | Show `No playable audio media are available in this Home Assistant source.` and retain source navigation. |
| media picker / loading | resolved | Show browse progress and prevent duplicate requests while keeping the current source context visible. |
| media picker / error | resolved | Show the specified HA access or browse recovery message; do not discard the playlist draft or stored references. |
| media picker / populated | resolved | Preserve the HA hierarchy and show add actions only for playable audio media. |
| media picker / partial | resolved | Keep available browse results usable if another item lacks metadata or is unavailable; do not invent a reference. |
| media picker / overflow | resolved | Scroll and wrap picker content without horizontal overflow or obscured add actions. `verification: backstop` |
| media picker / zero-one-many | resolved | Keep navigation and item geometry stable across no results, one result, and many results. |
| media picker / long-text | resolved | Wrap or safely reflow long provider and media titles without clipping actions. `verification: backstop` |
| availability / empty | resolved | Show the section's explicit empty state when there are no saved provider references; never infer availability from absence of data. |
| availability / loading | resolved | Label the active availability check, disable duplicate submission for that reference, and leave other rows usable. |
| availability / error | resolved | Report denied, unavailable, or transient failures with recovery copy while preserving the exact saved reference and order. |
| availability / populated | resolved | Show `Not checked`, `Available`, or `Unavailable in Home Assistant` for each checked or unchecked reference. |
| availability / partial | resolved | Display mixed statuses independently; one failed check does not overwrite other results or hide valid rows. |
| availability / overflow | resolved | Keep status text and check actions reachable in a scrollable list without horizontal overflow. `verification: backstop` |
| availability / zero-one-many | resolved | Keep status and action alignment stable for zero, one, or many references. |
| availability / long-text | resolved | Wrap long status and media labels without clipping the check action or accessible name. `verification: backstop` |
| confirmation / loading | resolved | While deletion/removal is pending, identify the operation and prevent duplicate destructive submissions. |
| confirmation / error | resolved | On failure, retain the target row and dialog context, show the exact recovery copy, and do not imply success. |
| confirmation / overflow | resolved | Constrain long confirmation content to a scrollable dialog while keeping both actions reachable. `verification: backstop` |
| confirmation / long-text | resolved | Wrap long playlist names in the dialog without obscuring the target identity or actions. `verification: backstop` |

Accessibility contract: use semantic navigation, labelled inputs, ordered-list semantics for custom entries, native buttons, and visible focus outlines. Every icon-only control needs an accessible name and tooltip. Announce save results, availability results, and reorder changes in a polite atomic live region; expose blocking errors with an alert. Keep focus on the operated entry after reordering; after removal, move focus to the next entry, previous entry, or `Add media` when the list becomes empty. On deletion, return focus to the nearest remaining library row or `Create playlist`. Honor keyboard operation, Escape behavior, dialog focus restoration, and `prefers-reduced-motion`; keep transitions within the existing 150ms vocabulary and remove them when reduced motion is requested. Verify contrast and keyboard flow in the rendered panel at mobile and desktop widths.

---

## Registry Safety

| Registry | Blocks Used | Safety Gate |
|----------|-------------|-------------|
| none | none | not applicable; no shadcn or third-party registry is used |

---

## Phase Boundary and Verification

- All library operations remain in the existing HA-authenticated panel context and use its injected `hass` connection. This contract specifies visible interaction behavior only; it does not prescribe new authentication or persistence implementation details.
- Custom playlists contain ordered opaque Home Assistant media references and display snapshots only. Do not show, store, or render resolved playback URLs, provider credentials, or credential-bearing request data.
- Saved provider playlists are opaque local shortcuts. Their provider-owned contents are read-only and are never expanded into custom tracks.
- Phase 25 covers create, rename, edit, reorder, remove/delete, save provider reference, and explicit availability status. Phase 26 owns launching, playback, sequential advancement, and queue controls.
- Verify UI behavior locally with mocked Home Assistant behavior at desktop and mobile widths. This local/mock verification is not production host acceptance. Do not perform live-host operations or mark production acceptance.

---

## Checker Sign-Off

- [x] Dimension 1 Copywriting: PASS
- [x] Dimension 2 Visuals: PASS
- [x] Dimension 3 Color: PASS
- [x] Dimension 4 Typography: PASS
- [x] Dimension 5 Spacing: PASS
- [x] Dimension 6 Registry Safety: PASS
- [x] Dimension 7 Inventory Provenance: PASS (not applicable: Tool is none)

**Approval:** approved 2026-10-25
