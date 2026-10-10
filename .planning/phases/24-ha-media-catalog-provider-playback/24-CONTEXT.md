# Phase 24: HA Media Catalog & Provider Playback - Context

**Gathered:** 2026-10-11
**Status:** Ready for planning
**Mode:** Autonomous smart-discuss defaults; user was unavailable. Decisions below are agent-selected defaults, not user-confirmed answers.

<domain>
## Phase Boundary

Expose Home Assistant's supported audio media sources and provider playlists through each BL-HAOS native media player and a secure catalog view associated with the existing ingress experience. Selecting a media-source reference launches it on the selected speaker through Home Assistant's authenticated media-player service path. Home Assistant remains the provider catalog, resolver, and credential authority.

This phase covers PL-01, PL-02, and PL-03 only. Persistent BL-HAOS playlist CRUD and saved provider references are Phase 25; sequential queues, advancement, and queue controls are Phase 26.
</domain>

<decisions>
## Implementation Decisions

### HA Media Catalog (autonomous defaults)

- Browse only audio-capable media and provider playlists; this product outputs A2DP audio, not video or images.
- Preserve Home Assistant `BrowseMedia` metadata, hierarchy, `can_play`, and `can_expand`; do not flatten or reinterpret provider trees.
- Preserve a provider playlist as one HA-owned playable reference; do not expand it into BL-HAOS-managed tracks or queue state in Phase 24.
- Offer search only where Home Assistant's media source advertises it; add no provider-specific search client.

### Secure HA Frontend Boundary (autonomous defaults)

- The catalog UI must execute in a Home Assistant-authenticated frontend context with the HA-provided `hass` connection; use Home Assistant WebSocket/service APIs rather than issuing or persisting a long-lived HA token.
- Reuse the existing ingress catalog UI components and visual system, but host catalog actions in an HA-owned authenticated panel/shell. Keep the add-on's privileged REST API out of browser media-resolution paths.
- On auth loss or denied/expired access, stop the request and show a reconnect/permission error; never fall back to a stored token, direct provider API, or raw provider URL.
- UI launches the selected item through native `media_player.play_media` with the original `media-source://` ID and selected speaker entity. Home Assistant owns media resolution and passes only the resolved playback URL to the existing media-player integration.
- Before implementation, research must verify the supported Core custom-panel/WebSocket registration path and how it can reuse the existing Ingress React view without relying on private frontend internals. If no supported path can meet PL-03, stop and surface the architecture blocker rather than storing HA credentials in the add-on.

### Provider Playback and Failures (autonomous defaults)

- Home Assistant resolves provider and playlist references; BL-HAOS accepts only the resolved playable request through its existing native media-player integration.
- Keep the selection bound to one explicitly selected connected BL-HAOS media-player entity; no implicit speaker selection or multi-speaker sync.
- Unavailable, denied, expired, or unresolvable media produces a visible error and no alternate URL/provider fallback.
- Do not auto-skip or retry a different media item. Preserve the user's selected reference so Home Assistant can report or retry the same action.
- Do not log resolved URLs or credential-bearing query parameters; audit and redact the existing `async_play_media` URL debug logging as part of PL-03 security acceptance.

### the agent's Discretion

- Choose bounded loading/empty/error states and catalog navigation details that preserve existing BL-HAOS Ingress design/accessibility conventions.
- Select appropriate unit, Home Assistant integration, and browser tests after confirming the supported frontend-hosting mechanism.
</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets

- `modules/integration/custom_components/bl_haos/media_player.py` already advertises `BROWSE_MEDIA`, delegates `async_browse_media` to Home Assistant `media_source`, resolves `media-source://` IDs with `async_resolve_media`, and routes native playback to the selected Bluetooth speaker.
- `modules/integration/custom_components/bl_haos/client.py` owns the authenticated native bridge REST/WebSocket client and caches trusted speakers; its native bearer remains inside Home Assistant config-entry storage.
- `modules/bridge/web_ui/src/api/client.ts` resolves HA Ingress-relative add-on URLs and WebSocket paths for the current Bluetooth dashboard. Reuse catalog view components where practical, not its unauthenticated bridge API as a media-source credential proxy.
- Existing frontend Playwright demo flows and HA integration unit/SIL tests can be extended for catalog browsing, selected-speaker launch, denied/unavailable access, and URL redaction.

### Established Patterns

- Home Assistant owns config-entry credentials; bridge API validation and token redaction are explicit security boundaries.
- The add-on backend resolves media sources only after Home Assistant's media player sends a playable URL. New catalog UI calls should retain HA auth and preserve opaque media-source IDs until the HA service call.
- Phase 23 established the ingress Neumorphic design, semantic state colors, responsive card geometry, focus visibility, reduced-motion handling, and keyboard/dialog behavior; preserve these patterns.

### Integration Points

- Native browse/play behavior: `BLHAOSMediaPlayer.async_browse_media` and `async_play_media`.
- Native speaker targeting: HA `media_player.play_media` service with one selected BL-HAOS entity.
- Existing Ingress app: `modules/bridge/web_ui/src/App.tsx`, `api/client.ts`, and the add-on `ingress_port` configuration.
- Privileged playback boundary: `modules/bridge/backend/bl_haos/api/routes.py` native command endpoint and its URL validation/logging.
</code_context>

<specifics>
## Specific Ideas

- Keep Home Assistant media-source IDs intact in browser state and requests; only HA's native media-player path resolves them.
- Do not introduce provider SDKs, provider credentials, token localStorage, or raw URL playlist records.
- Use the existing speaker selection to choose the one target for a catalog launch.

</specifics>

<deferred>
## Deferred Ideas

- Custom BL-HAOS playlist creation/edit/reorder/delete and saved provider playlist library (Phase 25, PL-04/05/06/11).
- Sequential playback, queue persistence, automatic advancement, previous/next, shuffle, and repeat (Phase 26, PL-07/08/09/10).
- Direct provider API clients, provider credentials, arbitrary URL imports, and synchronized multi-speaker queues remain out of scope.

</deferred>