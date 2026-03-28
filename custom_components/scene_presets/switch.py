import logging
from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.restore_state import RestoreEntity
from .const import DOMAIN, NAME

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Scene Presets switch platform."""
    async_add_entities([
        ScenePresetsTurnOnOffLightsSwitch(),
        ScenePresetsDynamicSwitch(),
        ScenePresetsShuffleSwitch(),
        ScenePresetsSmartShuffleSwitch(),
        ScenePresetsCustomBrightnessSwitch(),
        ScenePresetsCustomTransitionSwitch(),
    ])

class ScenePresetsSwitchEntity(RestoreEntity, SwitchEntity):
    """Base class for Scene Presets switch entities."""

    def __init__(self, key, name, icon, default_val):
        self._attr_name = f"{NAME} {name}"
        self._attr_unique_id = f"{DOMAIN}_{key}"
        self._attr_icon = icon
        self._attr_is_on = default_val

    @property
    def is_on(self):
        """Return True if entity is on."""
        return self._attr_is_on

    async def async_added_to_hass(self):
        """Restore last state."""
        await super().async_added_to_hass()
        last_state = await self.async_get_last_state()
        if last_state and last_state.state not in ("unknown", "unavailable"):
            self._attr_is_on = last_state.state == "on"

    async def async_turn_on(self, **kwargs) -> None:
        """Turn the entity on."""
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the entity off."""
        self._attr_is_on = False
        self.async_write_ha_state()


class ScenePresetsTurnOnOffLightsSwitch(ScenePresetsSwitchEntity):
    def __init__(self):
        super().__init__("turn_on_off_lights", "Turn On Off Lights", "mdi:lightbulb-on", True)

class ScenePresetsDynamicSwitch(ScenePresetsSwitchEntity):
    def __init__(self):
        super().__init__("dynamic", "Dynamic", "mdi:motion-play-outline", False)

class ScenePresetsShuffleSwitch(ScenePresetsSwitchEntity):
    def __init__(self):
        super().__init__("shuffle", "Shuffle", "mdi:shuffle", False)

class ScenePresetsSmartShuffleSwitch(ScenePresetsSwitchEntity):
    def __init__(self):
        super().__init__("smart_shuffle", "Smart Shuffle", "mdi:shuffle-variant", False)

class ScenePresetsCustomBrightnessSwitch(ScenePresetsSwitchEntity):
    def __init__(self):
        super().__init__("custom_brightness", "Custom Brightness", "mdi:brightness-auto", False)

class ScenePresetsCustomTransitionSwitch(ScenePresetsSwitchEntity):
    def __init__(self):
        super().__init__("custom_transition", "Custom Transition", "mdi:transition", False)
