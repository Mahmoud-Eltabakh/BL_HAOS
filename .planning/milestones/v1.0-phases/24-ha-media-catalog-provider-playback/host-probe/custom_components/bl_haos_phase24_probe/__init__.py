from pathlib import Path

from homeassistant.components import frontend, panel_custom
from homeassistant.components.http import StaticPathConfig
from homeassistant.const import Platform

DOMAIN = "bl_haos_phase24_probe"
PANEL_PATH = "bl-haos-phase24-probe"
PROBE_URL = "/bl_haos_phase24_probe/probe.js"
PLATFORMS = [Platform.MEDIA_PLAYER]


async def async_setup_entry(hass, entry):
    if not hass.data.get(DOMAIN):
        await hass.http.async_register_static_paths(
            [StaticPathConfig(PROBE_URL, str(Path(__file__).with_name("probe.js")), False)]
        )
        hass.data[DOMAIN] = True
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    await panel_custom.async_register_panel(
        hass,
        frontend_url_path=PANEL_PATH,
        webcomponent_name=PANEL_PATH,
        module_url=PROBE_URL,
        sidebar_title="Phase24 Probe",
        sidebar_icon="mdi:test-tube",
        require_admin=True,
    )
    return True


async def async_unload_entry(hass, entry):
    if not await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        return False
    frontend.async_remove_panel(hass, PANEL_PATH)
    return True