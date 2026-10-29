# Phase 37 Context — Native Pairing, Speaker & Settings UI

**Phase goal:** Pairing, speaker management and settings are available in the integration.
**Requirement:** NUX-03
**Planning scope:** Local implementation and verification only. No commit, deployment, HA-host action, or live acceptance is part of this planning run.

## Decisions

### Locked decisions

- **D-01 — UI/service ownership boundary.** All user-facing UI moves into the Home Assistant integration (`modules/integration`): services, options flow, and the integration panel. The add-on (`modules/bridge`) remains a separate headless service because it requires BlueZ, D-Bus, and audio access; it only gains authenticated API endpoints. Phase 37 must not add new add-on UI.
- **D-02 — Scope and parity.** From HA a user can scan, pair (with optional PIN), connect, disconnect, remove, and rename speakers, toggle adapter power, and edit per-speaker settings (`custom_alias`, `auto_reconnect`, `preferred_adapter`, `default_volume`, `codec_override`). Parity reference is the add-on web UI: `modules/bridge/web_ui/src/components/DiscoveryModal.tsx`, `SettingsModal.tsx`, `SpeakerCard.tsx`, `AdapterStatus.tsx` and `api/client.ts`.
- **D-03 — Authenticated native endpoints only.** The legacy bridge routes (`/scan/start`, `/scan/stop`, `/devices`, `/devices/pair`, `/devices/{address}/connect|disconnect|volume`, `DELETE /devices/{address}`, `/settings`, `PUT /settings/speakers/{address}`, `/adapters`, `/adapters/{name}/power` in `modules/bridge/backend/bl_haos/api/routes.py`) do **not** call `require_native_auth`. The integration must never call them. Phase 37 adds authenticated `/native/*` equivalents that call `require_native_auth` first and share the underlying manager/config-store logic. Legacy routes stay unchanged for the add-on UI until Phase 38.
- **D-04 — Safe error text.** Native management endpoints return only whitelisted, user-safe reasons, following the Phase 35 `SAFE_QUEUE_CONTROL_REASONS` pattern; raw BlueZ/D-Bus text (the legacy pair/connect routes forward `safe_detail(e)`) is logged server-side only and never returned to the integration. The integration likewise surfaces only bridge-whitelisted reasons or its own fixed fallback.
- **D-05 — Rename via existing model.** Rename uses `SpeakerSettings.custom_alias` (validated in `modules/bridge/backend/bl_haos/config.py`); no new storage field. Native API and tests must explicitly cover rename, alias clearing, and invalid aliases (control chars, over-length).
- **D-06 — Transport.** The integration talks to the bridge only through `modules/integration/custom_components/bl_haos/client.py` (`BLHAOSClient`) with the native bearer token from the config entry. Panel actions go through admin-only HA WebSocket commands; HA services are admin services.
- **D-07 — System settings boundary.** `log_level`, `default_codec`, and `auto_reconnect_enabled` are bridge-managed `ConfigStore` / `SystemSettings` fields and must be editable from HA through an authenticated native endpoint and admin integration service/panel controls. Do not write Supervisor add-on options, handle Supervisor tokens, or expose secrets. Other settings (demo, player tuning) remain read-only; `native_token` is never returned.
- **D-08 — Prior phases.** Phases 35 and 36 are complete locally. Do not redo queue gating, error reasons, playlist, or browse-and-play work. Phase 38 owns ingress-UI retirement and version compatibility.

## Agent's Discretion

- Exact native route names, request/response models, and the whitelist constant names (suggested: `/native/adapters`, `/native/adapters/{name}/power`, `/native/scan/start|stop`, `/native/devices`, `/native/devices/pair`, `/native/devices/{address}/connect|disconnect`, `DELETE /native/devices/{address}`, `/native/settings`, `PUT /native/settings/speakers/{address}`; `SAFE_DEVICE_MANAGEMENT_REASONS`).
- Whether the panel's management view lives in `media-panel.tsx` or a new `speaker-management.tsx` component mounted by it.
- Options-flow shape (suggested: choose speaker → edit settings form), provided it calls the same client method as the service/panel.
- Use module-local tests: bridge `py -3.12 -m pytest`, integration unit tests, WSL Ubuntu SIL venv for HA-dependent suites, panel Vitest, and isolated package parity.

## Out of Scope

- Removing or changing the add-on ingress UI or legacy unauthenticated routes (Phase 38).
- Add-on/integration version compatibility reporting (Phase 38, NUX-05).
- Writable Supervisor add-on options (no Supervisor token handling), demo/player-tuning settings, BlueZ agent changes, and new Bluetooth capabilities. The three bridge-managed SystemSettings fields in D-07 are writable from HA.
- Deployment, publishing, GHCR, HA host access, live pairing/hardware/playback acceptance (Phase 39 under explicit authorization).
- Phase 35/36 behavior.

## Existing Implementation References

- Bridge routes and auth: `modules/bridge/backend/bl_haos/api/routes.py` (`require_native_auth`, `SAFE_QUEUE_CONTROL_REASONS`, `/native/speakers`, legacy device/settings/adapter routes)
- Settings models and store: `modules/bridge/backend/bl_haos/config.py` (`SpeakerSettings`, `SystemSettings`, `update_speaker`, `remove_speaker`)
- Bridge tests: `modules/bridge/tests/test_api.py`, `modules/bridge/tests/test_native_transport.py`, `modules/bridge/tests/test_bridge_sil.py`
- Integration client/config: `modules/integration/custom_components/bl_haos/client.py`, `config_flow.py`, `__init__.py`, `strings.json`
- Integration tests: `modules/integration/tests/unit/test_client_commands.py`, `modules/integration/tests/test_ha_integration_sil.py`, `modules/integration/tests/test_package_layout.py`
- Panel: `modules/integration/panel_ui/src/media-panel.tsx` (+ tests), packaged at `modules/integration/custom_components/bl_haos/panel_static/bl-haos-media-panel.js`
- Add-on web UI (parity reference only, not modified): `modules/bridge/web_ui/src/components/*`, `modules/bridge/web_ui/src/api/client.ts`
