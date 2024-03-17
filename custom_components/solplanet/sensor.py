"""Platform for sensor integration."""

from .const import DOMAIN
from .sensor_definitions import Coordinator
from .sensor_initialization import (
    create_battery_sensors,
    create_meter_sensors,
    create_solar_sensors,
)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add sensors for passed config_entry in HA."""
    hub = hass.data[DOMAIN][config_entry.entry_id]

    coord = Coordinator(hass, hub)
    await coord.async_config_entry_first_refresh()

    new_entities = []

    new_entities += create_meter_sensors(hub, coord)
    new_entities += create_solar_sensors(hub, coord)
    new_entities += create_battery_sensors(hub, coord)

    async_add_entities(new_entities)
