"""Real-network E2E scenarios against a live BL-HAOS bridge container.

Unlike the SIL suites (test_bridge_sil.py, test_ha_integration_sil.py) which
mock the HTTP/WebSocket transport, these tests drive an actually-running
bridge container (in demo mode) over real HTTP, and — for the integration
checks — a real in-process Home Assistant core talking real aiohttp to that
container. This is the closest simulation of a real environment achievable
without physical Bluetooth hardware.

Scope note: the demo runtime (modules/bridge/backend/bl_haos/demo.py) only
implements a fixed single demo speaker and does not implement pairing/scan/
adapter-power. Those remain covered by the SIL suites' mocked BluetoothManager.
When a new demo scenario or native endpoint is added, extend this file --
see .github/skills/update-e2e-tests/SKILL.md.
"""

from __future__ import annotations

import os
import time

import httpx
import pytest
from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.bl_haos.const import CONF_ENDPOINT, CONF_TOKEN, DOMAIN

# socket_enabled opts back into real sockets: pytest-homeassistant-custom-component
# blocks raw sockets by default so tests don't accidentally hit the network, but
# these tests intentionally talk to a real, live bridge container.
pytestmark = pytest.mark.usefixtures("enable_custom_integrations", "socket_enabled")

BRIDGE_URL = os.environ.get("BRIDGE_URL", "http://localhost:8099").rstrip("/")
TOKEN = os.environ.get("BLHAOS_NATIVE_TOKEN", "e2e-test-token")
SCENARIO = os.environ.get("BLHAOS_DEMO_SCENARIO", "healthy")
DEMO_ADDRESS = "aa:bb:cc:11:22:33"
AUTH_HEADERS = {"Authorization": f"Bearer {TOKEN}"}


@pytest.fixture(autouse=True)
def wait_for_bridge(socket_enabled):
    """Block until the live container answers /api/health, or fail fast.

    Depends explicitly on socket_enabled (rather than relying on scope
    ordering) so real sockets are guaranteed enabled before this fixture's
    own network call runs -- a module-scoped autouse fixture would otherwise
    execute before the function-scoped socket_enabled fixture and get
    blocked by pytest-socket.
    """
    deadline = time.monotonic() + 60
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        try:
            response = httpx.get(f"{BRIDGE_URL}/api/health", timeout=3)
            if response.status_code == 200:
                return
        except httpx.HTTPError as error:
            last_error = error
        time.sleep(1)
    pytest.fail(f"Bridge at {BRIDGE_URL} never became healthy: {last_error}")


# ---------------------------------------------------------------------------
# Connect device
# ---------------------------------------------------------------------------

def test_connect_device_adapter_and_speaker_are_visible():
    adapters = httpx.get(f"{BRIDGE_URL}/api/adapters", timeout=5).json()
    assert any(adapter["interface"] == "hci0" for adapter in adapters)

    devices = httpx.get(f"{BRIDGE_URL}/api/devices", timeout=5).json()
    assert any(device["address"] == DEMO_ADDRESS for device in devices)


# ---------------------------------------------------------------------------
# Connect integration (real Home Assistant core, real network, no mocks)
# ---------------------------------------------------------------------------

async def test_connect_integration_creates_media_player_entity(hass):
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_ENDPOINT: BRIDGE_URL, CONF_TOKEN: TOKEN},
        title="BL-HAOS Bluetooth Audio",
        unique_id="bl_haos_native_bridge",
    )
    entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    entities = [state for state in hass.states.async_all("media_player")]
    assert any(state.name == "Demo Speaker" for state in entities)

    demo_state = next(state for state in entities if state.name == "Demo Speaker")
    if SCENARIO == "healthy":
        assert demo_state.state != "unavailable"
    else:
        assert demo_state.state == "unavailable"

    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()


async def test_connect_integration_rejects_wrong_token(hass):
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_ENDPOINT: BRIDGE_URL, CONF_TOKEN: "not-the-real-token"},
        title="BL-HAOS Bluetooth Audio",
        unique_id="bl_haos_wrong_token",
    )
    entry.add_to_hass(hass)

    assert not await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    assert entry.state is config_entries.ConfigEntryState.SETUP_RETRY


# ---------------------------------------------------------------------------
# Play music
# ---------------------------------------------------------------------------

@pytest.mark.skipif(SCENARIO != "healthy", reason="demo speaker is only connected in the healthy scenario")
def test_play_music_round_trips_through_native_command():
    response = httpx.post(
        f"{BRIDGE_URL}/api/native/speakers/{DEMO_ADDRESS}/command",
        headers=AUTH_HEADERS,
        json={"version": 1, "operation": "play_media", "url": "http://example.local/stream.mp3", "media_type": "music"},
        timeout=5,
    )
    assert response.status_code == 200
    assert response.json()["address"] == DEMO_ADDRESS

    volume_response = httpx.post(
        f"{BRIDGE_URL}/api/native/speakers/{DEMO_ADDRESS}/command",
        headers=AUTH_HEADERS,
        json={"version": 1, "operation": "set_volume", "volume": 0.5},
        timeout=5,
    )
    assert volume_response.status_code == 200

    pause_response = httpx.post(
        f"{BRIDGE_URL}/api/native/speakers/{DEMO_ADDRESS}/command",
        headers=AUTH_HEADERS,
        json={"version": 1, "operation": "pause"},
        timeout=5,
    )
    assert pause_response.status_code == 200


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_edge_case_missing_token_is_rejected():
    response = httpx.get(f"{BRIDGE_URL}/api/native/identity", timeout=5)
    assert response.status_code == 401


def test_edge_case_wrong_token_is_rejected():
    response = httpx.get(
        f"{BRIDGE_URL}/api/native/identity", headers={"Authorization": "Bearer wrong"}, timeout=5
    )
    assert response.status_code == 401


def test_edge_case_invalid_address_format_is_rejected():
    response = httpx.post(
        f"{BRIDGE_URL}/api/native/speakers/not-a-mac/command",
        headers=AUTH_HEADERS,
        json={"version": 1, "operation": "play"},
        timeout=5,
    )
    assert response.status_code == 422


def test_edge_case_set_volume_without_volume_is_rejected():
    response = httpx.post(
        f"{BRIDGE_URL}/api/native/speakers/{DEMO_ADDRESS}/command",
        headers=AUTH_HEADERS,
        json={"version": 1, "operation": "set_volume"},
        timeout=5,
    )
    assert response.status_code == 422


@pytest.mark.skipif(SCENARIO == "healthy", reason="demo speaker is connected in the healthy scenario")
def test_edge_case_command_on_disconnected_speaker_is_rejected():
    response = httpx.post(
        f"{BRIDGE_URL}/api/native/speakers/{DEMO_ADDRESS}/command",
        headers=AUTH_HEADERS,
        json={"version": 1, "operation": "play"},
        timeout=5,
    )
    assert response.status_code in (404, 409)


# ---------------------------------------------------------------------------
# Recovery
# ---------------------------------------------------------------------------

def test_recovery_contract_is_available():
    response = httpx.get(f"{BRIDGE_URL}/api/recovery", headers=AUTH_HEADERS, timeout=5)
    assert response.status_code == 200
    payload = response.json()
    assert payload["contract_version"] == 1
    assert "guidance" in payload


def test_recovery_refresh_diagnostics_action_succeeds():
    response = httpx.post(
        f"{BRIDGE_URL}/api/recovery/actions",
        headers=AUTH_HEADERS,
        json={"action_id": "refresh_diagnostics"},
        timeout=5,
    )
    assert response.status_code == 200
    assert "diagnostics" in response.json()


def test_recovery_rejects_unsupported_action():
    response = httpx.post(
        f"{BRIDGE_URL}/api/recovery/actions",
        headers=AUTH_HEADERS,
        json={"action_id": "not_a_real_action"},
        timeout=5,
    )
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# All implemented features: health, diagnostics, support bundle redaction
# ---------------------------------------------------------------------------

def test_health_and_diagnostics_are_reachable():
    for path in ("/api/health", "/api/diagnostics", "/api/diagnostics/native"):
        response = httpx.get(f"{BRIDGE_URL}{path}", timeout=5)
        assert response.status_code == 200, path


def test_support_bundle_never_leaks_secrets():
    response = httpx.get(f"{BRIDGE_URL}/api/support/bundle", timeout=5)
    assert response.status_code == 200
    body = response.text
    assert TOKEN not in body
