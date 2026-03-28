import logging
from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN, NAME
from . import dynamic_scene_manager
from .file_utils import PRESET_DATA

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Scene Presets sensor platform."""
    async_add_entities([ScenePresetsDynamicSceneSensor()])

class ScenePresetsDynamicSceneSensor(SensorEntity):
    """Representation of a Scene Presets dynamic scene sensor."""

    def __init__(self):
        """Initialize the sensor."""
        self._attr_name = f"{NAME} Dynamic Scene"
        self._attr_unique_id = f"{DOMAIN}_dynamic_scene"
        self._attr_icon = "mdi:play-circle-outline"
        self._state = ""

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self._state

    async def async_added_to_hass(self):
        """Run when entity about to be added to hass."""
        dynamic_scene_manager.add_update_callback(self._handle_dynamic_scenes_update)
        self._handle_dynamic_scenes_update()

    async def async_will_remove_from_hass(self):
        """Clean up when entity is removed."""
        dynamic_scene_manager.remove_update_callback(self._handle_dynamic_scenes_update)

    def _handle_dynamic_scenes_update(self):
        """Handle updates to dynamic scenes."""
        scenes = dynamic_scene_manager.get_all()
        if not scenes:
            self._state = ""
        else:
            names = []
            for scene in scenes:
                preset_id = scene.parameters.get("preset_id", "Unknown")
                preset_name = preset_id
                
                # Resolve the UUID to a human-readable name
                for preset in PRESET_DATA.get("presets", []):
                    if preset.get("id") == preset_id:
                        preset_name = preset.get("name", preset_id)
                        break
                        
                names.append(preset_name)
                
            self._state = ", ".join(names)
            
        self.async_schedule_update_ha_state()
