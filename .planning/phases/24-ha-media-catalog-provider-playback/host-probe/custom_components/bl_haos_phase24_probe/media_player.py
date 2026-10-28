from homeassistant.components.media_player import (
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
)

ENTITY_NAME = "BL-HAOS Phase24 Probe Sink"
ENTITY_UNIQUE_ID = "bl_haos_phase24_probe_sink"


async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([ProbeMediaPlayer()])


class ProbeMediaPlayer(MediaPlayerEntity):
    _attr_name = ENTITY_NAME
    _attr_unique_id = ENTITY_UNIQUE_ID
    _attr_should_poll = False
    _attr_state = MediaPlayerState.IDLE
    _attr_supported_features = MediaPlayerEntityFeature.PLAY_MEDIA

    def __init__(self):
        self._call_count = 0
        self._last_media_type = None

    @property
    def extra_state_attributes(self):
        return {
            "probe_sink": True,
            "call_count": self._call_count,
            "last_media_type": self._last_media_type,
        }

    async def async_play_media(self, media_type, media_id, **kwargs):
        self._call_count += 1
        self._last_media_type = "music" if media_type == "music" else "other"
        self.async_write_ha_state()