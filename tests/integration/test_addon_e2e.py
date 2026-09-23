import os
import pytest
import requests
from playwright.sync_api import Page, expect

HA_URL = os.getenv("HA_URL", "http://localhost:8123")
# Assuming the add-on exposes its API on port 8099 mapped to host or via ingress
ADDON_URL = os.getenv("ADDON_URL", "http://localhost:8099")

def test_ha_is_running():
    """Verify that the Home Assistant instance is up and running."""
    response = requests.get(f"{HA_URL}/manifest.json")
    assert response.status_code == 200

def test_addon_api_unauthorized():
    """
    Regression test for CR-01: Native control endpoints have no authentication.
    Attempts to hit the playback endpoint without credentials.
    """
    try:
        response = requests.post(f"{ADDON_URL}/api/v1/commands/play", json={"entity_id": "media_player.test_speaker"}, timeout=5)
        # Should be blocked, we expect 401 Unauthorized or 403 Forbidden
        assert response.status_code in [401, 403], f"Expected unauthorized, but got {response.status_code}"
    except requests.exceptions.ConnectionError:
        # If the add-on isn't exposing 8099 directly but only via ingress, this test might need adjustment
        # to hit the ingress URL instead.
        pytest.skip("Add-on API not exposed on 8099, skipping direct unauth test.")

def test_addon_ingress_ui(page: Page):
    """
    Load Home Assistant, verifying Playwright can reach the frontend.
    Deep UI testing (login, ingress navigation) can be expanded here.
    """
    page.goto(HA_URL)
    # Depending on HAOS setup, it might redirect to /onboarding
    expect(page).to_have_title("Home Assistant")
