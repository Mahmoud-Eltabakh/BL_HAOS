# Phase 24: HA Media Catalog & Provider Playback - Pattern Map

**Mapped:** 2026-10-11
**Files analyzed:** 16 likely new or modified files
**Analogs found:** 14 / 16 (2 architecture-dependent files have no local analog)

## File Classification

| New/Modified File | Role | Data Flow | Closest Tracked Analog | Match Quality |
|---|---|---|---|---|
| `modules/integration/custom_components/bl_haos/__init__.py` | integration setup/lifecycle | request-response + lifecycle | same file | exact |
| `modules/integration/custom_components/bl_haos/media_player.py` | entity/controller | request-response, resolve/play, browse | same file | exact |
| `modules/integration/custom_components/bl_haos/panel_static/bl-haos-media-panel.js` | generated static asset | browser bundle | `modules/bridge/web_ui/dist/` (generated; do not copy as source) | partial |
| `modules/integration/panel_ui/src/media-panel.tsx` | frontend custom element | request-response over HA WebSocket/service | `modules/bridge/web_ui/src/App.tsx`, `src/main.tsx` | role-match |
| `modules/integration/panel_ui/vite.config.ts` | frontend build config | transform/build | `modules/bridge/web_ui/vite.config.ts` | role-match |
| `modules/integration/panel_ui/package.json` | frontend build/test config | build/test | `modules/bridge/web_ui/package.json` | role-match |
| `modules/integration/tests/test_ha_integration_sil.py` | integration test | request-response + lifecycle | same file | exact |
| `modules/integration/tests/test_panel_registration.py` | integration test | lifecycle/static registration | `modules/integration/tests/test_ha_integration_sil.py` | role-match |
| `modules/integration/tests/test_package_layout.py` | packaging test | static inspection | same file | exact |
| `modules/integration/requirements-sil.txt` | dependency/config | test environment | same file | exact |
| `modules/bridge/backend/bl_haos/api/routes.py` | API boundary | authenticated request-response | same file | exact |
| `modules/bridge/backend/bl_haos/ha/player.py` | playback service | process I/O | same file | exact |
| `modules/bridge/tests/test_api.py` | backend security test | request-response/log capture | same file | exact |
| `modules/bridge/tests/test_media_player.py` | playback security test | process I/O/log capture | same file | exact |
| `modules/bridge/web_ui/e2e/specs/catalog.spec.ts` | browser test | authenticated browser flow | `modules/bridge/web_ui/e2e/specs/dashboard.spec.ts` | role-match |
| `modules/bridge/web_ui/src/components/*` or extracted shared catalog components | React component | render/state | `modules/bridge/web_ui/src/components/DiscoveryModal.tsx` and tests | role-match |

The exact `panel_ui` directory, bundle filename, and whether catalog presentation is extracted from the bridge UI are implementation choices. Keep those paths conditional until the HA custom-panel/static-serving gate passes. Do not claim an add-on Ingress panel registration contract: the research supports the public Home Assistant `panel_custom` and `async_register_static_paths` APIs, but the packaged integration must still be validated against the target HA host.

## Pattern Assignments

### `modules/integration/custom_components/bl_haos/__init__.py` (setup/lifecycle, lifecycle)

**Analog:** `modules/integration/custom_components/bl_haos/__init__.py` lines 22-75.

**Setup pattern:** Construct the per-entry runtime client, initialize it, assign `entry.runtime_data`, and forward platforms only after initialization succeeds. Fail with `ConfigEntryNotReady` and close the client on setup failure (lines 22-50).

**Unload pattern:** Unload platforms first; only after a successful unload close entry-owned resources and remove stale entity states (lines 58-75). A panel/static registration added here must have an entry-scoped unload callback or equivalent cleanup, and cleanup must happen on partial setup failure as well.

**Conditional HA registration pattern:** If the researched public APIs remain available on the target Core, register one deterministic static module through `hass.http.async_register_static_paths` and one `panel_custom.async_register_panel` per integration setup, after the required HA services are available. Store no HA credential or resolved URL. If registration cannot be proven on the target host, stop at the architecture gate rather than adding a bridge fallback.

### `modules/integration/custom_components/bl_haos/media_player.py` (entity, request-response)

**Analog:** same file lines 221-406.

**Feature declaration:** `_attr_supported_features` includes `PLAY_MEDIA` and `BROWSE_MEDIA` alongside transport and volume features (lines 221-234). Preserve this native HA surface.

**Browse pattern** (lines 396-406):

```python
async def async_browse_media(
    self, media_content_type: str | None = None, media_content_id: str | None = None
) -> BrowseMedia:
    """Let the Home Assistant UI browse folders/media sources for this speaker."""
    return await async_browse_media(self.hass, media_content_id)
```

Keep the HA `BrowseMedia` hierarchy and capability fields. Any audio/playlist policy belongs at this boundary, using HA metadata rather than provider-specific type guesses; preserve `can_play`, `can_expand`, `can_search`, titles, thumbnails, and opaque IDs.

**Resolution/play pattern** (lines 368-394): detect `media-source://`, call `async_resolve_media(self.hass, media_id, self.entity_id)`, process relative URLs with HA's configured URL, normalize the media type, then call `_async_command(COMMAND_PLAY_MEDIA, ...)`. The browser must send the original opaque ID to `media_player.play_media`; only this entity may receive the resolved URL.

**Required security adjustment:** the current debug record includes `url=%s` (lines 387-394). Replace it with operation/entity/media-type metadata only. Do not put the resolved URL in exceptions, state, or logs. Existing enqueue rejection and bounded media-type normalization remain the local error-handling pattern.

### `modules/integration/panel_ui/src/media-panel.tsx` (custom element, request-response)

**Closest analogs:** `modules/bridge/web_ui/src/App.tsx` lines 1-25, 33-55, and `src/main.tsx` lines 1-9; no existing HA custom element exists in the repository.

**React pattern:** use typed state, bounded loading/error states, and `useEffect` for initial data loading as `App.tsx` does for diagnostics. Reuse visual classes, semantic state colors, focus behavior, and responsive geometry from the bridge components only where extraction is practical.

**Authentication boundary:** accept the HA-supplied `hass` property from the documented custom-panel element contract. Browse with `hass.callWS({ type: 'media_source/browse_media', media_content_id })`; play with `hass.callService('media_player', 'play_media', { media_content_id, media_content_type }, { entity_id })`. Do not import HA private frontend modules, use `window` globals, use `apiClient`, call the bridge REST API, resolve media in the browser, or write to `localStorage`/`sessionStorage`.

**Rendering/error pattern:** render the returned browse tree without flattening it; navigate only expandable entries, enable play only for playable entries and one explicitly selected connected BL-HAOS entity, and expose search only when HA reports it. On authorization/connection/resolution failure, stop and show a reconnect/permission error while retaining the selected opaque reference. No raw provider URL or URL-bearing error text should enter browser state.

This is an architecture-dependent new file. It is permitted only if the documented Core custom-panel/static path and an HA-host smoke test confirm the injected authenticated `hass` contract.

### `modules/integration/panel_ui/vite.config.ts`, `package.json` (build/test config, transform/build)

**Analog:** `modules/bridge/web_ui/vite.config.ts` lines 1-16 and `package.json` lines 1-35.

Copy the existing React plugin, TypeScript build-before-Vite build, and pinned dependency style. The bridge config's `base: './'` is specifically for Ingress; a Core-served module needs a deterministic fixed output filename and should not rely on guessed Vite hashes. Add the smallest separate custom-element entry/build needed; do not add provider SDKs or new authentication libraries. Use Vitest if the panel has a unit harness, with the existing jsdom/testing-library configuration as the model (`vitest.config.ts` lines 1-13).

### `modules/integration/custom_components/bl_haos/panel_static/bl-haos-media-panel.js` (generated asset, browser bundle)

**Analog:** `modules/bridge/web_ui/dist/` only as a packaging/output example; it is generated and is not a source pattern.

The bundle must have a stable filename matching `module_url`, be included in the shipped integration package, and be checked by package-layout tests. Do not cite or copy the generated `dist/assets/index-*.js` naming scheme for registration. The build/package contract is conditional on the static-path registration gate.

### `modules/integration/tests/test_ha_integration_sil.py` (integration test, request-response/lifecycle)

**Analog:** same file lines 31-52, 63-87, 404-466.

Use `_setup_entry()` with `MockConfigEntry`, patched `FakeSession`, and `hass.config_entries.async_setup`, then settle with `await hass.async_block_till_done()`. Existing tests inspect entity state/attributes and call the entity directly. Extend this style for audio/playlist BrowseMedia metadata, opaque-ID resolution targeted to one entity, unavailable/denied failures, and URL-free `caplog` assertions. Keep SIL collection constraints: `conftest.py` lines 15-27 skip Home Assistant runtime tests on native Windows unless `BLHAOS_RUN_SIL=1`; final validation belongs in Linux/WSL2 or an HAOS-compatible environment.

### `modules/integration/tests/test_panel_registration.py` (integration test, lifecycle/static)

**Analog:** `test_ha_integration_sil.py` setup/unload coverage and `test_package_layout.py` static checks.

Test the public registration calls with mocks or the target Core test helpers: one fixed static path, one panel, expected module URL, and unload cleanup. Include setup failure/partial cleanup. This is a new test surface because no current panel/static registration test exists. Gate it on the official documented API and exact target Core version; do not test or encode private frontend internals.

### `modules/integration/tests/test_package_layout.py`, `requirements-sil.txt` (packaging/config, static/test environment)

**Analog:** same files, especially `test_package_layout.py` lines 8-27 and `requirements-sil.txt` lines 1-6.

Extend required-file assertions for the fixed panel bundle/source manifest and ensure no credential-bearing bridge client is part of the panel. Upgrade the `homeassistant` SIL pin only together with compatible `pytest-homeassistant-custom-component` tooling, as research requires; retain the documented Linux/WSL2-only behavior.

### `modules/bridge/backend/bl_haos/api/routes.py` and `ha/player.py` (backend, process I/O/request-response)

**Analogs:** `routes.py` lines 313-360 and `ha/player.py` lines 461-510.

The route currently logs `payload.url` while executing native commands; the player logs `url` while executing operations. Preserve validation, authenticated command flow, reconnect behavior, process lifecycle, and safe URL validation, but remove URL values from logs. Log only operation, normalized speaker address, volume presence/normalized media type, and bounded failure details. The bridge must continue accepting only the resolved URL from the existing native entity path; it must not gain catalog, browse, provider, or token endpoints.

### `modules/bridge/tests/test_api.py` and `test_media_player.py` (security tests, request-response/process I/O)

**Analogs:** same files. `test_api.py` lines 204-276 demonstrates bounded error/detail assertions and native command validation; `test_media_player.py` lines 63-132 demonstrates URL validation, process non-spawn assertions, and accepted HTTP media URLs.

Add `caplog`/log-capture tests using URL host/path/query/token/password sentinels and assert every sentinel is absent while command execution still receives the URL. Keep existing positive/negative URL validation and no-side-effect tests. Do not assert that the URL is absent from the internal subprocess argument: the security requirement is logs/browser/add-on catalog boundaries, while the decoder necessarily needs the resolved stream URL.

### `modules/bridge/web_ui/src/components/*` and tests (React component, request-response/render)

**Analogs:** `DiscoveryModal.tsx` and `DiscoveryModal.test.tsx`.

Follow the existing testing-library pattern: mock the boundary client, render with controlled props, use `waitFor`, role-based queries, and `vi.clearAllMocks()` in cleanup. Preserve hook ordering; `test_frontend_assets.py` explicitly guards against hooks declared after early returns. If catalog components are extracted from the bridge UI, keep the existing `neu-*` classes and accessibility behavior, but remove bridge `apiClient` usage from the HA panel entry.

### `modules/bridge/web_ui/e2e/specs/catalog.spec.ts` (browser test, authenticated browser request-response)

**Analog:** `dashboard.spec.ts` lines 1-20 and `diagnostics.spec.ts` lines 1-18; runner setup is `e2e/playwright.config.ts` lines 1-42.

Use `test.describe`, `test.step`, `page.goto`, role/text assertions, and bounded timeouts. The current Playwright server boots the unauthenticated demo bridge, so it cannot prove HA authentication by itself. Add a separate HA-host smoke configuration or mark the catalog spec conditional until it can run against a real target HA session. Required assertions include browse tree rendering, exactly one selected entity in `callService`, denied/expired failure state, no bridge catalog requests, and no resolved URL/token in browser-visible state or captured logs.

## Shared Patterns

### HA Credential and Resolution Boundary
**Sources:** `media_player.py` lines 368-394; `panel_ui` research contract.

HA owns provider credentials and media-source resolution. The panel retains only opaque `media-source://` IDs; Home Assistant invokes one selected native entity; the entity resolves and forwards the playable URL to the bridge. No provider SDK, copied HA bearer, browser storage, bridge proxy, or raw provider URL is allowed.

### Setup/Unload Ownership
**Source:** `modules/integration/custom_components/bl_haos/__init__.py` lines 22-75.

Resources registered for a config entry must be registered after successful initialization and removed on unload. A failed panel registration must not leave a static route or panel behind.

### Bounded Errors
**Sources:** `media_player.py` lines 326-366; `modules/bridge/web_ui/src/api/client.ts` lines 82-109.

Convert transport/auth failures to short operator-facing messages, retain actionable categories, and never include credentials, resolved URLs, or provider details. Preserve the selected opaque reference for HA retry/reporting; do not auto-skip or fallback.

### URL-Free Logging
**Sources:** `routes.py` lines 326-330; `ha/player.py` lines 471-478.

Keep operation/entity correlation logs, but omit URL and query values at every integration-to-bridge boundary. Add regression tests at both bridge paths and the native integration path.

## No Analog Found

| File/Surface | Role | Data Flow | Reason |
|---|---|---|---|
| `modules/integration/panel_ui/src/media-panel.tsx` | HA custom element | authenticated WebSocket/service | No tracked Home Assistant custom-panel or custom-element source exists in this repository. Use only the documented public `hass`, `callWS`, and `callService` contract, pending host validation. |
| `modules/integration/custom_components/bl_haos/panel_static/*` registration/package contract | static serving | browser bundle/lifecycle | No tracked integration-owned static asset registration exists. Treat `panel_custom` and `async_register_static_paths` as research-backed but architecture-gated, not as an existing local convention. |

## Metadata

**Analog search scope:** `modules/integration/custom_components/bl_haos`, `modules/integration/tests`, `modules/bridge/backend/bl_haos`, `modules/bridge/tests`, `modules/bridge/web_ui/src`, and `modules/bridge/web_ui/e2e`.
**Tracked-source check:** all named existing analogs were verified with `git ls-files`; generated `dist/` output is identified as non-source and is not used as a copied implementation analog.
**Pattern extraction date:** 2026-10-11