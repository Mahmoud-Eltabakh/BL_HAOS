---
phase: "24"
slug: "ha-media-catalog-provider-playback"
status: draft
shadcn_initialized: false
preset: none
created: "2026-10-11"
---

# Phase 24 -- UI Design Contract

> Visual and interaction contract for HA Media Catalog & Provider Playback. Generated from autonomous agent defaults, the Phase 23 Neumorphic direction, and the current ingress and integration surfaces; it covers PL-01, PL-02, and PL-03 only.

---

## Design System

| Property          | Value                                                                  |
| ----------------- | ---------------------------------------------------------------------- |
| Tool              | none                                                                   |
| Preset            | not applicable; no `components.json` or shadcn package is present      |
| Component library | none; React 18 with semantic native controls                           |
| Icon library      | `lucide-react` 0.344.0                                                 |
| Font              | existing Tailwind sans-serif browser stack; no new font for this phase |

The component inventory is not applicable because this project has no installed UI component library or shadcn design system. Use the existing React components, semantic HTML controls, Tailwind utilities, and shared Neumorphic CSS tokens; do not introduce a registry or component-library dependency in this phase.

---

## Catalog Experience Contract

### Supported HA-host architecture and gate

The catalog is an integration-owned custom panel/view registered by the HACS integration through Home Assistant's supported public panel-registration path. The integration packages and serves an integration-owned catalog UI bundle from a static URL. Home Assistant loads that bundle as a standard custom element and supplies the official `hass` property with the current authenticated frontend APIs.

The existing BL-HAOS ingress shell remains a discovery surface only. It presents the visible top-level `Open Media Catalog` CTA near `Home Assistant Native integration` and opens the registered Home Assistant panel. The ingress application and `modules/bridge/web_ui/src/api/client.ts` do not browse, resolve, proxy, or play catalog media through add-on routes.

The HA-owned panel uses the authenticated `hass` connection to browse Home Assistant media sources and invoke `media_player.play_media` for one selected BL-HAOS entity. It preserves opaque `media-source://` IDs in UI state and sends the original ID to the service. Home Assistant retains provider authentication, resolves the reference, and passes any resolved playable request to the native media-player integration.

Before source implementation, verify in a supported live HA environment: (1) the public Core API for a HACS integration to register the custom panel/view, (2) its supported static-bundle packaging and module-URL discovery mechanism, and (3) the authenticated `hass` APIs for media browsing and `media_player.play_media`. The currently verified documentary evidence is [Creating custom panels](https://developers.home-assistant.io/docs/frontend/custom-ui/creating-custom-panels/): it establishes that panels are custom elements and that Home Assistant supplies `hass`, `narrow`, and `panel` properties. Its `panel_custom` example is supporting evidence for the custom-element contract, not proof that the integration registration/static-serving mechanism is verified.

If any public registration, static-serving, URL-discovery, or authenticated `hass` API cannot be verified, fail closed and report PL-03 blocked. Do not substitute private frontend globals, undocumented imports, iframe-parent access, an ingress proxy, add-on REST endpoints, browser persistence, copied/stored HA bearer tokens, provider credentials, direct provider APIs, or raw provider URLs.

### Entry and target selection

- Keep a visible `Open Media Catalog` command in the existing ingress experience near the Home Assistant Native integration status. It is an entry point only: it opens the registered HA-owned custom panel/view and makes no media-source, resolution, or provider request through `api/client.ts` or the bridge REST API.
- The HA-owned panel/shell opens with an explicit selected-target control for exactly one connected BL-HAOS `media_player` entity. It has no implicit target, remembered cross-session target, or multi-speaker option.
- Label the control `Play on` and render its placeholder as `Select a connected speaker`. Do not enable the `Play` action until a connected BL-HAOS entity is selected. If the selected entity becomes unavailable, retain the selection label, show its unavailable state, and disable `Play` until the user selects an available target.
- Preserve HA's catalog hierarchy, titles, thumbnails, `can_expand`, and `can_play` metadata. Show expandable sources as navigation rows and playable sources or provider playlists as rows with an explicit play action. Do not flatten provider trees, expand a provider playlist into tracks, or create a local queue.
- Preserve the original `media-source://` identifier in UI state and pass it unchanged to native `media_player.play_media` for the selected entity. Home Assistant alone resolves the reference and supplies the playable URL to the integration.

### Layout and interaction

- Use the existing responsive shell and Neumorphic vocabulary: `neu-page` for the page, one raised `neu-surface` catalog container, `neu-inset` for the target selector and search field when HA exposes search, and `neu-button` for actions. Avoid nested raised/inset cards around every list row; catalog rows are a stable list with a single hover or selection treatment.
- The catalog header contains the hierarchy breadcrumb/back control, `Play on` selector, and a close/back-to-ingress action. On narrow viewports, stack these controls in that order; preserve a minimum 44px hit area for back, close, target selection, and play actions.
- Render catalog entries with list semantics. Each row exposes its full title, provider/source label when available, audio/playlist type, and one action. Long titles wrap to two lines before truncation; the original source label remains available as accessible text or a tooltip.
- Render `Play` with the existing lucide play icon plus visible label. Expandable rows use a familiar chevron icon and visible source name. Icon-only close or back controls require an accessible name and hover/focus tooltip.
- Only expose search when the current HA media source advertises it. Use its HA-provided search capability; never add provider-specific search, URL search, or client-side scraping.
- A successful play request reports `Starting playback on {speaker name}` in a polite live region and leaves the current catalog selection in place. Do not claim playback succeeded until the HA service reports success or the media-player state confirms it.
- A failed resolution or play request keeps the same selected media reference and target visible, reports the error inline with `Retry {item title} on {speaker name}`, and performs no fallback URL/provider lookup, auto-retry, auto-skip, or next-item action. This retry appears only after that selected item's resolution or playback request fails, and retries that same item on that same connected target once per activation.

### Scope exclusions

This phase contains no saved playlist creation, rename, edit, reorder, delete, save-provider-reference, sequential queue, automatic advancement, previous/next, shuffle, repeat, or multi-speaker controls. It does not render resolved playback URLs, credentials, or credential-bearing query parameters.

---

## Spacing Scale

Declared values (all multiples of 4):

| Token | Value | Usage                                              |
| ----- | ----- | -------------------------------------------------- |
| xs    | 4px   | Icon-to-label gaps and compact metadata separation |
| sm    | 8px   | Row internals, compact controls, and status gaps   |
| md    | 16px  | Default control and list-row padding               |
| lg    | 24px  | Catalog header and section padding                 |
| xl    | 32px  | Primary layout gaps                                |
| 2xl   | 48px  | Empty-state and major section separation           |
| 3xl   | 64px  | Page-level separation only                         |

Exceptions: 44px minimum target size for catalog navigation, target selection, close, and play controls; existing page padding remains `24px` mobile and `40px` at the current medium breakpoint.

---

## Typography

Use exactly these four sizes and two weights. Preserve the existing high-contrast text token roles rather than adding raw slate text classes for catalog content.

| Role                                | Size | Weight | Line Height |
| ----------------------------------- | ---- | ------ | ----------- |
| Metadata and status                 | 12px | 400    | 1.5         |
| Body, input, and row title          | 14px | 400    | 1.5         |
| Section heading and selected target | 16px | 600    | 1.2         |
| Page/catalog heading                | 24px | 600    | 1.2         |

---

## Color

| Role                 | Value                                               | Usage                                                                                              |
| -------------------- | --------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Dominant (60%)       | `#151a23`                                           | Page background and unframed background space                                                      |
| Secondary (30%)      | `#242d3b`                                           | Raised catalog surface and existing shell surfaces                                                 |
| Accent (10%)         | `#3b82f6`                                           | `Open Media Catalog`, selected catalog row, active breadcrumb, and the selected target detail only |
| Destructive          | `#e11d48` / existing rose semantic classes          | Not used by Phase 24; reserved for destructive actions only                                        |
| Success semantic     | existing emerald classes                            | Connected target and confirmed playback state only                                                 |
| Warning semantic     | existing amber classes                              | Target becoming unavailable or action requiring attention                                          |
| Error semantic       | existing rose classes                               | Denied, expired, unavailable, unresolved, and failed playback states                               |
| Information semantic | `#67e8f9` focus outline / existing cyan diagnostics | Keyboard focus and non-error HA connection guidance                                                |

Accent reserved for: entry command, selected catalog row, active catalog path, and the selected target detail. Do not use blue for provider facts, source metadata, disabled states, errors, or all interactive elements. Preserve the audited `--neu-*` surface and text tokens, visible focus outline, and WCAG AA contrast.

---

## Copywriting Contract

| Element                            | Copy                                                                                                                         |
| ---------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| Primary CTA                        | Open Media Catalog                                                                                                           |
| Target placeholder                 | Select a connected speaker                                                                                                   |
| Target unavailable state           | {speaker name} is unavailable. Select a connected speaker to play media.                                                     |
| Catalog loading state              | Loading media sources...                                                                                                     |
| Catalog empty state heading        | No audio sources are available                                                                                               |
| Catalog empty state body           | Home Assistant did not return a playable audio source. Check the media provider and try again.                               |
| Playback pending state             | Starting playback on {speaker name}...                                                                                       |
| Resolution/playback error          | Home Assistant could not play this item on {speaker name}. Check the provider access and speaker connection, then try again. |
| HA authentication/permission error | Your Home Assistant session cannot access this media source. Reconnect or ask an administrator for access, then try again.   |
| Unsupported source state           | This source cannot play audio on a BL-HAOS speaker. Choose an audio item or provider playlist.                               |
| Destructive confirmation           | None in Phase 24; no destructive actions are in scope.                                                                       |

---

## URL Redaction Acceptance Contract

Phase 24 must change the following implementation surfaces. This is an acceptance requirement, not a claim that current behavior is already compliant:

| File                                                            | Current sensitive-log surface to remediate                         | Required replacement                                                                                                     |
| --------------------------------------------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------ |
| `modules/integration/custom_components/bl_haos/media_player.py` | `async_play_media` debug logging includes the final resolved `url` | Log only operation, safe entity/target correlation, and normalized media type; omit the resolved URL entirely.           |
| `modules/bridge/backend/bl_haos/api/routes.py`                  | Native speaker command debug logging includes `payload.url`        | Log only operation, normalized target/safe correlation, and media type where available; omit the URL and query entirely. |
| `modules/bridge/backend/bl_haos/ha/player.py`                   | Player `execute` debug logging includes `url`                      | Log only operation, safe target correlation, and media type where available; omit the URL and query entirely.            |

No application log written by these paths may contain a complete resolved media URL, its host/path/query, credentials, tokens, passwords, authorization values, or a raw URL supplied for `play_media`. Error handling must not reflect these values. Use operation, target-safe correlation, and media type where useful; otherwise omit URL-derived detail.

Required tests must capture logs while exercising credential-bearing resolved URLs and prove that each path above omits the raw URL, host/path, query, credential, token, and password values. Cover integration `async_play_media`, bridge native speaker command handling, and bridge player execution. Tests may assert the allowed operation, target-safe correlation, and media type without asserting a URL-derived value.

---

## UI Considerations

Probe result: 14 applicable element-category proposals resolved (12 explicit, 2 backstop, 0 unresolved). The cross-cutting checks below preserve additional accessibility and interaction requirements outside the probe taxonomy.

| Category      | Element(s)                                                          | Status      | Resolution / Reason                                                                                                                 |
| ------------- | ------------------------------------------------------------------- | ----------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| empty         | Catalog root, expanded source, and target selector                  | ✅ covered  | Show the documented no-audio-sources copy without inventing local items; with no selected target, disable Play and require explicit selection. |
| loading       | Catalog/child-source rows and target/play controls                  | ✅ covered  | Show progress, retain the last stable hierarchy, and keep Play disabled until a connected target and playable reference are available. |
| error         | HA session, browse, resolve, target, and `play_media` requests       | ✅ covered  | Show a bounded inline error, preserve the selected item and target, and offer retry of the same request only.                         |
| populated     | Browseable sources, folders, playable items, and provider playlists | ✅ covered  | Preserve HA hierarchy, titles, thumbnails, and capability metadata; distinguish expand from play without creating a queue.           |
| partial       | Failed source with valid ancestor path or selected target            | ✅ covered  | Keep valid ancestor navigation, target, and unrelated sources available; show the failed child-source error in context.               |
| overflow      | Catalog body and hierarchy                                           | ✅ covered  | Scroll the catalog body within the viewport while keeping header actions reachable; catalog rows require no horizontal scrolling.   |
| overflow      | HA target selector/menu                                              | 🧪 backstop | Verify the target selector remains operable within the viewport at 375px, 768px, and 1440px.                                       |
| zero-one-many | Catalog result list                                                  | ✅ covered  | Use stable semantic list rows and control placement for zero, one, or many results; zero uses the documented empty state.            |
| long-text     | Provider/source names, playlist titles, and error detail             | ✅ covered  | Titles wrap to two lines before truncation; accessible text exposes the complete label and errors stay bounded.                      |
| long-text     | Selected speaker names and status announcements                     | 🧪 backstop | Verify unusually long speaker names remain fully perceivable in the target selector and status announcement at supported viewports. |
| unavailable   | Selected speaker or selected media reference                        | ✅ covered  | Disable play, retain the user's selection, and show the documented unavailable/error state with no target substitution.              |
| keyboard      | Breadcrumb, list rows, selector, play button, and dialogs            | ✅ covered  | Use semantic controls, visible focus, predictable tab order, Escape close behavior, and focus restoration for any dialog.             |
| motion        | Loading, list updates, and panel entry                               | ✅ covered  | Keep transitions within the existing 150ms vocabulary and honor the global reduced-motion override.                                  |
| responsive    | 320px mobile, tablet, and desktop catalog shell                      | 🧪 backstop | Verify at 375px, 768px, and 1440px that controls stack without overlap and 44px targets remain usable.                              |
| accessibility | HA-owned panel/shell and failure announcements                       | 🧪 backstop | Verify keyboard traversal, focus return, screen-reader labels, polite status announcements, and contrast in the supported HA host.   |

---

## Registry Safety

| Registry | Blocks Used | Safety Gate                                                         |
| -------- | ----------- | ------------------------------------------------------------------- |
| none     | none        | not applicable; no shadcn or third-party component registry is used |

---

## Implementation Verification Contract

- Verify the panel registration, integration static-bundle serving, static URL discovery, authenticated `hass` media browsing, and `media_player.play_media` invocation against the official custom-panel documentation and target supported Core API. Record the exact verified API path before implementation; fail closed if it is unsupported.
- Unit/SIL coverage must exercise `async_browse_media`, supported audio/provider-playlist metadata, media-source resolution, original media-source ID handoff to one selected entity, unavailable items, and denied or expired access.
- Add log-capture tests required by the URL Redaction Acceptance Contract for `media_player.py`, `api/routes.py`, and `ha/player.py`. Use representative URLs with query credentials and prove the URL, host/path, query, credentials, tokens, and passwords are absent from captured logs.
- Frontend/host coverage must prove the ingress CTA opens the registered HA-owned panel; the panel receives its supplied `hass` property; it sends no media-source request through `modules/bridge/web_ui/src/api/client.ts` or an add-on route; and it stores no HA/provider token, resolved URL, or credential in browser persistence.
- Exercise target-required play disabling, hierarchy navigation, provider playlist as one playable reference, loading, empty, unavailable, permission, resolution, and playback-failure states. Confirm the exact retry label targets the same item and speaker, and does not auto-retry, auto-skip, fall back, or queue another item.
- Run supported HA-host interaction validation at 375px, 768px, and 1440px with keyboard and reduced-motion checks.

---

## Checker Sign-Off

- [x] Dimension 1 Copywriting: PASS
- [x] Dimension 2 Visuals: PASS
- [x] Dimension 3 Color: PASS
- [x] Dimension 4 Typography: PASS
- [x] Dimension 5 Spacing: PASS
- [x] Dimension 6 Registry Safety: PASS
- [x] Dimension 7 Inventory Provenance: PASS (not applicable: Tool is none)

**Checker result:** UI-SPEC VERIFIED; 2 non-blocking flags (make the catalog's visual focal point explicit and review the one-word `Play` CTA).

**Approval:** approved 2026-10-11
