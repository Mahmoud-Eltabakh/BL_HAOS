# Phase 38: Headless Add-on & Ingress UI Retirement — Context

**Gathered:** 2026-10-28
**Status:** Ready for planning/execution review; no implementation or release authorization
**Requirements:** NUX-04, NUX-05

<domain>
## Phase Boundary and Authority

Retire the bridge's ingress management application while preserving the native integration, internal service discovery, watchdog, diagnostics, playback and reconnect behavior. Add explicit product-version compatibility reporting in Home Assistant and migration notes. Deliver local candidates bridge **0.2.71** and integration **0.2.22**; do not publish them.

STATE.md still identifies Phase 30's v1.1 security/authorization pause. This explicitly requested Phase 38 planning belongs to ROADMAP.md's parallel v1.2 track, depends on locally completed Phase 37, and neither advances Phase 30 nor changes STATE.md, requirement completion, or live acceptance. No host changes, add-on/integration installation, restart, Bluetooth operations, provider activity, playback, release, or deployment is authorized. Phase 39 retains live acceptance and release gates.
</domain>

<research>
## Findings from the Current Checkout

### Serving and packaging the old UI

- `modules/bridge/config.yaml`: version `0.2.70`, `ingress: true`, `ingress_port: 8099`, `panel_icon: "mdi:speaker-bluetooth"`; no current `panel_title` or `panel_admin`, but retirement must prohibit all `panel_*` keys. No host `ports` mapping. `discovery: [bl_haos]` and watchdog `http://[HOST]:[PORT:8099]/api/health` are separate service contracts, not reasons to keep ingress.
- `backend/bl_haos/main.py`: includes API and websocket routers, then mounts `StaticFiles(..., html=True)` at `/` if a candidate contains `index.html`. `constants.py` candidates are `web_ui/dist`, `/var/www/bl-haos`, `frontend/dist`. Removing only files from the image is insufficient: the local-development fallback would still mount them.
- `Dockerfile`: `node:22-bookworm-slim AS web_ui_build`, npm lockfile install and Vite build, then `COPY --from=web_ui_build /build/dist /var/www/bl-haos`. The runtime remains Debian/Python/audio packages. Remove the Node stage and static COPY, not the backend service or port 8099.
- `web_ui/` contains the retired React/Vite application, lockfile, unit tests and demo Playwright harness. The **different** `modules/integration/panel_ui/` and `custom_components/bl_haos/panel_static/` implement the HA-native media/speaker panel and must remain.

### HTTP/WebSocket consumer audit

All route suffixes below are prefixed by `/api`, including `/native/*`; the public websocket is `/ws`, native events are `/ws/native`.

| Current surface | Evidence / consumer | Phase 38 disposition |
|---|---|---|
| `GET /adapters`, `POST /adapters/{adapter_name}/power` | Ingress UI; Phase 37 supplies authenticated native counterparts | Remove legacy route registrations; keep shared models/helpers needed by native endpoints. |
| `POST /scan/start`, `POST /scan/stop` | Ingress UI; native scan endpoints exist | Remove legacy registrations. |
| `GET /devices`, `POST /devices/pair`, `POST /devices/{address}/connect`, `/disconnect`, `/volume`, `DELETE /devices/{address}` | Ingress UI/tests; integration uses native devices or speaker commands instead | Remove legacy registrations; migrate backend/SIL assertions to authenticated native routes, preserving behavior coverage. |
| `POST /devices/{address}/queue/command` | Explicit ingress-only unauthenticated queue adapter added in Phase 35 | Remove; retain authenticated `/native/speakers/{address}/command` including queue controls. |
| `GET /settings`, `PUT /settings/speakers/{address}` | Ingress UI; Phase 37 native settings endpoints exist | Remove legacy registrations. |
| `GET /health` | Supervisor watchdog; integration client and config flow first verify `service` here **before sending any bearer token** | Keep unauthenticated, HTTP 200 while daemon alive even when degraded; preserve payload/identity preflight. |
| `GET /diagnostics/native`, `GET /incidents` | Operational/support surfaces; health itself embeds native diagnostics; no integration management dependency | Keep existing bounded/sanitized read-only contracts in this phase; not management UI endpoints. Do not expand disclosure. |
| `/native/identity`, `/native/speakers`, speaker commands, Phase 37 scan/devices/adapters/settings | `modules/integration/custom_components/bl_haos/client.py` | Keep bearer auth and protocol contracts. Add only additive compatibility metadata to identity. |
| `/ws/native` | Integration `client.py` snapshot/event transport | Keep bearer-authenticated. |
| `/ws` plus `ws_manager` | Old UI subscriber, but publisher is also wired into `main.py`, `health.py`, demo/telemetry and tests | Retain as a deprecated operational event stream in Phase 38; no UI bundle ships. Removing event infrastructure is a separate consumer audit, not a prerequisite for retiring UI-only HTTP management. |

`client.py` uses `/api/health`, `/api/native/identity`, `/api/native/speakers`, `/api/native/speakers/{address}/command`, its generic bearer-authenticated `/api/native{resource}` management helper, and `/ws/native`. It does **not** call the legacy scan/devices/settings/adapters routes. Config flow duplicates health-before-identity validation and must share the compatibility decision. Apparent `http://127.0.0.1:8099/api/devices?audio_only=false` references in `test_api.py`/`test_media_player.py` are fixture media URLs, not a production bridge HTTP client; preserve their arbitrary-media-url coverage without retaining a UI route. Native device listing calls the misleadingly named `ui_speaker_record`; do not delete that shared serializer by name alone.

### Identity and compatibility gap

- `api/routes.py:get_native_identity` currently returns `bridge_id`, integer `version: NATIVE_BRIDGE_VERSION` (**1**, a wire-protocol version), `credential_fingerprint`, and conditional `queue_version` (**1**). It does not expose the add-on release or a minimum integration release.
- Bridge `constants.VERSION` is `0.2.70`, also used by FastAPI app metadata and `backend/bl_haos/__init__.py`; `config.yaml` must stay synchronized. `NATIVE_BRIDGE_VERSION` must NOT become `0.2.71`.
- Integration `manifest.json` is `0.2.21`. Client initialization validates bridge ID but not product versions; config flow also only checks bridge ID. `__init__.py:async_setup_entry` catches generic failures and maps them to "add-on is unavailable", masking a compatibility reason. `diagnostics.py` has no compatibility section. No existing repair helper was found in the component; add a small isolated helper rather than pretending a repair lifecycle exists.
- Reconnect currently reopens `/ws/native`; compatibility must also be rechecked after bridge restart/reconnect, not just first install. This protects running HA from an add-on update changing requirements underneath it.

### Coupled tests, CI and documentation

- Bridge `tests/test_frontend_assets.py` and `test_theme_contrast.py` require UI source; replace old-presence guards with headless/retirement assertions, rather than silently dropping all coverage.
- `tests/test_addon_config.py` asserts ingress is true, ingress port, watchdog port derived from ingress, frontend npm audit and version `0.2.70`. Decouple watchdog from removed ingress config; keep Python audit, Trivy and architecture guards.
- `tests/test_dockerfile.py` asserts built UI COPY; change to no Node/UI stage/static copy plus retained backend/runtime contracts.
- `tests/test_api.py`, `test_bridge_sil.py`, `test_native_transport.py` exercise legacy routes and ingress event parity. Port management assertions to native endpoints with tokens; add explicit absent-route/no-side-effect checks; keep operational `/ws` and sanitized telemetry coverage under accurate names.
- Bridge `.github/workflows/builder.yaml` installs/tests/builds/audits `web_ui`; remove only retired frontend steps. Root `.github/workflows/tests.yml` has a frontend job in `modules/bridge/web_ui`; retarget frontend unit/build coverage to integration `panel_ui`, do not run the old demo Playwright harness against the native panel or trigger real-HA `test:host`.
- Root `scripts/run-tests.ps1` and `scripts/run-tests.sh` hardcode bridge `web_ui` for L0/L1/L3/all. Update them with CI and `TESTING.md`; native panel unit/build stays local, real-HA browser tests stay explicitly authorized.
- Integration `tests/test_package_layout.py` asserts manifest `0.2.21` and existence of bridge `web_ui/e2e/playwright.config.ts`. Replace only retired-harness assertion with native panel harness/headless contracts; preserve fresh-build byte parity and Phase 36/37 markers.
- Bridge `DOCS.md` explicitly promises legacy ingress routes until Phase 38; `README.md` has old frontend build-hook wording. Both need migration cleanup. Bridge/integration Phase 25/26 docs tests protect safety and non-acceptance statements; keep these guards and add Phase 38 migration/version tests. No dedicated docs-fingerprint test was found in module test trees; do not invent a hash workflow, but refresh any existing docs-drift inputs discovered at execution.
</research>

<decisions>
## Implementation Decisions

- **D-01 — Headless runtime:** Delete tracked `modules/bridge/web_ui/`, remove static discovery/mount/constants and Docker frontend stage/COPY. Remove `ingress`, `ingress_port`, and every `panel_*` manifest key. Keep internal HTTP port, discovery, watchdog, audio and permissions unchanged. No host port exposure or new reverse proxy.
- **D-02 — Route boundary:** Remove only legacy HTTP management routes enumerated above. Keep health, diagnostics, incidents, native routes and native events; retain `/ws` operational transport for now. Do not accidentally remove shared serializer/models, reconnect registration, settings persistence, or publishers. Prove removals with 404 (or non-routable 405 where FastAPI matches another method), no side effects, and route-table assertions.
- **D-03 — Staged migration, one-way door:** Removing ingress breaks bookmarked dashboards and users not yet using the integration; snapshots cannot undo user disruption without coordinated package rollback. Put a `checkpoint:decision` before destructive retirement execution. Recommended release order: prepare/install integration 0.2.22 first, verify native speaker/settings access with the existing bridge, then update bridge to 0.2.71 only under Phase 39 authorization. This planning run does not approve that gate. An old integration cannot be forced to honor metadata it never reads.
- **D-04 — Message page, not another UI:** Serve a tiny inline, dependency-free read-only `GET /` retirement notice explaining HA Settings > Devices & services > BL-HAOS and the native media/speaker panel. No JS, assets, controls, token fields, dynamic host/address data, redirects or API fallback/catch-all. This helps direct internal URLs; **once ingress keys are removed Supervisor's old Open Web UI link/bookmark may not reach the notice at all**. Docs/release notices and integration-first staging are mandatory; a truly reachable ingress grace release would require a separately approved earlier release, not re-enabling ingress in 0.2.71.
- **D-05 — Additive identity contract:** Keep `version: 1`, `bridge_id`, fingerprint and conditional queue metadata. Add `addon_version` sourced from bridge `VERSION` and `min_integration_version: "0.2.22"`. Auth remains mandatory. Integration's local version is read from its installed manifest, not another unsynchronized hardcoded copy.
- **D-06 — Compatibility policy:** Integration 0.2.22 supports native protocol 1 and has minimum add-on release `0.2.70` (the current Phase 37 candidate). Compare semantic numeric releases with HA's existing version utility (e.g. `AwesomeVersion`, already present with HA); no new package. Test .9 vs .10, equality, supported later patches and malformed/prerelease inputs. Only stable x.y.z product versions are release-compatible in this phase; unsupported protocol, malformed metadata, or explicitly too-old product versions are incompatible. For older identity payloads with BOTH new fields absent, report `unknown_legacy` warning and preserve existing protocol-1 behavior so integration-first upgrades work; never label this positively compatible. One missing field or invalid types are incompatible, not legacy. Do not interpret protocol or queue versions as package versions.
- **D-07 — User-visible reporting and recovery:** One compatibility evaluator is shared by client and config flow. Known mismatch/invalid protocol fails initialization before snapshot, websocket, entities or commands; create a non-fixable HA repair with observed/required versions and update direction instead of generic offline text. New config flows show a translated specific incompatible-version error/abort; existing-entry setup creates the repair before runtime_data exists. Unknown legacy is a warning repair but does not stop existing behavior. Recheck authenticated identity before websocket reconnection, and gate all command/management entry points on known incompatibility. Cache only whitelisted version/status/reason fields. Delete/update the stable per-entry issue when a later successful validation recovers; clear on entry removal, not on ordinary unload so setup failure remains visible. Diagnostics reports current/required versions and compatible/incompatible/unknown_legacy without token/fingerprint/endpoint/raw identity. Config-entry setup errors must distinguish compatibility, auth and connectivity.
- **D-08 — Release/docs parity:** Final local metadata: bridge config/constants `0.2.71`, integration manifest `0.2.22`; keep protocol 1. Add bridge DOCS/CHANGELOG and integration README upgrade matrix, integration-first steps, limitations, internal API and watchdog behavior, repair instructions, settings preservation and coordinated rollback. Update bridge README plus root TESTING docs where stale UI harness/build claims exist. Version bump is packaging, not publication.
- **D-09 — Validation boundaries:** Bridge pytest and integration unit/package-layout tests run from their module roots (several tests read relative paths). HA runtime/SIL requires the existing pinned Linux/WSL environment; keep panel Vitest/build and byte parity. No Docker integration tests, VM operations, hardware, real-HA browser harness, network dependency additions, or publication in local plan verification. If dependencies are missing, use existing documented environment/restore policy rather than silently skipping or introducing tools.
</decisions>

<risks>
## Reversibility and Deferred Risks

| Risk | Rating | Gate / mitigation |
|---|---|---|
| Ingress users lose their only control surface; old bookmark may never reach notice | one-way | Explicit execution checkpoint; migration announcement; prove integration-first staged path; Phase 39 release go/no-go. |
| Old integration ignores new minimum-version metadata | costly | Document limitation; do not claim server-side enforcement; update integration first. |
| Legacy identity cannot prove installed bridge release | costly | Visible unknown_legacy warning, not silent success; verify native UI locally and require new metadata for release acceptance. |
| Removing UI handlers deletes native/shared helpers or damages reconnect/volume | costly | Native tracer plus regression suite; preserve serializers, broadcasts and persisted settings. |
| CI runners still depend on deleted web_ui | reversible | Retarget scripts, root CI and builder gates together; retain native panel parity; never replace mock browser E2E with unauthorized host tests. |
| Default codec persists but has no known playback consumer (Phase 37 finding) | deferred | Do not imply this phase fixes codec application or claims audible acceptance. |
| Rollback overwrites tokens/pairings/settings | costly | Preserve data, recommend snapshots and coordinated package rollback; do not delete speakers or regenerate credentials. |

No new management UI, config migration, schema wipe, auth redesign, public networking, complete event-bus removal, playback feature change or live acceptance is in scope.
</risks>

<planning>
## Plan Decomposition

1. **38-01:** Bridge headless retirement, route contract and local CI/test-harness closure (NUX-04); destructive execution checkpoint.
2. **38-02:** Additive identity + shared integration compatibility, HA repairs/diagnostics and recovery tests (NUX-05), after 01 because routes/constants/tests overlap.
3. **38-03:** Migration documentation, candidate versions 0.2.71/0.2.22, docs-drift/version tests and final local regression evidence (NUX-04, NUX-05), after 01/02.

The order of source implementation is not deployment order. Integration-first rollout is specified in D-03 and is separately gated in Phase 39.
</planning>
