import logging
from homeassistant.components.number import NumberEntity
from homeassistant.helpers.restore_state import RestoreEntity
from .const import DOMAIN, NAME

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Scene Presets number platform."""
    async_add_entities([
        ScenePresetsCustomBrightnessNumber(),
        ScenePresetsCustomTransitionNumber(),
        ScenePresetsDynamicTransitionNumber(),
        ScenePresetsDynamicIntervalNumber(),
    ])

class ScenePresetsNumberEntity(RestoreEntity, NumberEntity):
    """Base class for Scene Presets number entities."""
    
    def __init__(self, key, name, icon, min_val, max_val, step, default_val, unit=None):
        self._attr_name = f"{NAME} {name}"
        self._attr_unique_id = f"{DOMAIN}_{key}"
        self._attr_icon = icon
        self._attr_native_min_value = min_val
        self._attr_native_max_value = max_val
        self._attr_native_step = step
        self._attr_native_value = default_val
        self._attr_native_unit_of_measurement = unit

    async def async_added_to_hass(self):
        """Restore last state."""
        await super().async_added_to_hass()
        last_state = await self.async_get_last_state()
        if last_state and last_state.state not in ("unknown", "unavailable"):
            try:
                self._attr_native_value = float(last_state.state)
            except ValueError:
                pass

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        self._attr_native_value = value
        self.async_write_ha_state()

class ScenePresetsCustomBrightnessNumber(ScenePresetsNumberEntity):
    def __init__(self):
        super().__init__(
            "custom_brightness_value", "Custom Brightness Value", "mdi:brightness-6", 
            0, 255, 1, 128
        )

class ScenePresetsCustomTransitionNumber(ScenePresetsNumberEntity):
    def __init__(self):
        super().__init__(
            "custom_transition_value", "Custom Transition", "mdi:transition", 
            0, 300, 1, 60, "s"
        )

class ScenePresetsDynamicTransitionNumber(ScenePresetsNumberEntity):
    def __init__(self):
        super().__init__(
            "dynamic_transition_value", "Dynamic Transition", "mdi:transition-masked", 
            0, 300, 1, 45, "s"
        )

class ScenePresetsDynamicIntervalNumber(ScenePresetsNumberEntity):
    def __init__(self):
        super().__init__(
            "dynamic_interval_value", "Dynamic Interval", "mdi:timer-sand", 
            0, 300, 1, 60, "s"
        )
