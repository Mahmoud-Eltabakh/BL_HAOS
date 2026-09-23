# Phase 15 Research

## Existing Constraints

- The integration uses `BLHAOSClient.async_initialize()` to validate `/api/native/identity`, load `/api/native/speakers`, and start `/ws/native` listening.
- `_async_refresh_snapshot()` already removes absent addresses from `client.speakers` and notifies listeners, but `media_player.async_setup_entry()` currently interprets every listener callback as add-or-update and has no removal path.
- `modules/integration/tests/test_package_layout.py` is static-only; there is no Home Assistant runtime fixture or integration SIL dependency today.
- The repository root `pytest.ini` discovers `modules/integration/tests` and `tests/integration/requirements-test.txt` supplies the shared container test dependencies.

## Selected Test Harness

Use `pytest-homeassistant-custom-component` with Home Assistant's `hass` fixture, custom-component enablement, config-entry setup/unload helpers, and mocked aiohttp transport. Keep bridge responses deterministic by loading checked-in JSON fixtures rather than relying on a live endpoint.

## Package Legitimacy Audit

| Package | Registry URL | Use | Status |
|---|---|---|---|
| `pytest-homeassistant-custom-component` | https://pypi.org/project/pytest-homeassistant-custom-component/ | Test-only Home Assistant core/custom integration fixture support | VERIFIED |

The selected package is a named PyPI project with the expected purpose. No unverified package should be added by this phase.

## Risks To Cover

- A snapshot can remove a cached speaker while the platform's local entity map still retains the entity.
- Config-entry unload must stop the client's websocket task and release listeners.
- Invalid bridge identity or endpoint responses must leave setup retryable rather than creating entities.
- Snapshot fixtures must preserve the bridge's authoritative shape and address normalization rules.
