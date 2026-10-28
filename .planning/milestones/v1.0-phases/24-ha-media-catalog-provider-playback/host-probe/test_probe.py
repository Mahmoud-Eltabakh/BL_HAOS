import shutil
from importlib.metadata import version
from pathlib import Path
from unittest.mock import AsyncMock, patch

import custom_components
import pytest
from homeassistant.components import frontend, panel_custom
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import SOURCE_USER
from homeassistant.helpers import entity_registry
from homeassistant.setup import async_setup_component

DOMAIN = "bl_haos_phase24_probe"
PANEL_PATH = "bl-haos-phase24-probe"
PROBE_URL = "/bl_haos_phase24_probe/probe.js"

pytestmark = pytest.mark.usefixtures("enable_custom_integrations")


async def test_probe_flow_registration_service_and_removal(hass, monkeypatch, tmp_path):
    assert version("homeassistant") == "2026.10.3"
    hass.config.config_dir = str(tmp_path)
    source = Path(__file__).parent / "custom_components" / DOMAIN
    target = Path(hass.config.path("custom_components", DOMAIN))
    shutil.copytree(source, target)
    monkeypatch.setattr(
        custom_components, "__path__", [str(target.parent), *custom_components.__path__]
    )
    assert await async_setup_component(hass, "http", {})
    with (
        patch.object(type(hass.http), "async_register_static_paths", autospec=True) as register,
        patch.object(panel_custom, "async_register_panel", wraps=panel_custom.async_register_panel) as panel,
        patch.object(frontend, "async_remove_panel", wraps=frontend.async_remove_panel) as remove,
    ):
        frontend_repo = Path(hass.config.path("probe_frontend"))
        (frontend_repo / "hass_frontend").mkdir(parents=True)
        assert await async_setup_component(
            hass, "frontend", {"frontend": {"development_repo": str(frontend_repo)}}
        )
        result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": SOURCE_USER})
        assert result["type"] == "create_entry"
        entry = result["result"]
        await hass.async_block_till_done()
        assert entry.data == {}
        assert entry.unique_id == DOMAIN
        probe_paths = [
            static_path
            for call in register.call_args_list
            for static_path in call.args[1]
            if static_path.url_path == PROBE_URL
        ]
        assert len(probe_paths) == 1
        assert probe_paths[0] == StaticPathConfig(PROBE_URL, str(target / "probe.js"), False)
        panel.assert_awaited_once_with(
            hass,
            frontend_url_path=PANEL_PATH,
            webcomponent_name=PANEL_PATH,
            module_url=PROBE_URL,
            sidebar_title="Phase24 Probe",
            sidebar_icon="mdi:test-tube",
            require_admin=True,
        )
        assert PANEL_PATH in hass.data[frontend.DATA_PANELS]
        registry = entity_registry.async_get(hass)
        entity_id = registry.async_get_entity_id("media_player", DOMAIN, "bl_haos_phase24_probe_sink")
        assert entity_id is not None
        state = hass.states.get(entity_id)
        assert state.name == "BL-HAOS Phase24 Probe Sink"
        assert state.attributes["call_count"] == 0
        with patch("homeassistant.components.media_source.async_resolve_media", new_callable=AsyncMock) as resolve:
            await hass.services.async_call(
                "media_player", "play_media",
                {"entity_id": entity_id, "media_content_id": "media-source://bl_haos_phase24_probe/nonplaying-sentinel", "media_content_type": "music"},
                blocking=True,
            )
            resolve.assert_not_called()
        state = hass.states.get(entity_id)
        assert state.state == "idle"
        assert state.attributes["call_count"] == 1
        assert state.attributes["last_media_type"] == "music"
        assert "media-source://" not in str(state.attributes)
        duplicate = await hass.config_entries.flow.async_init(DOMAIN, context={"source": SOURCE_USER})
        assert duplicate["type"] == "abort"
        assert duplicate["reason"] == "already_configured"
        assert await hass.config_entries.async_remove(entry.entry_id)
        await hass.async_block_till_done()
        remove.assert_called_once_with(hass, PANEL_PATH)
        assert hass.states.get(entity_id) is None
        assert registry.async_get(entity_id) is None
        assert PANEL_PATH not in hass.data[frontend.DATA_PANELS]