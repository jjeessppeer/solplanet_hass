"""Platform for sensor integration."""

from homeassistant.const import EntityCategory

from .const import DOMAIN
from .sensor_definitions import (
    ChargeSensor,
    Coordinator,
    CurrentSensor,
    EnergySensor,
    PowerSensor,
    VoltageSensor,
)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add sensors for passed config_entry in HA."""
    hub = hass.data[DOMAIN][config_entry.entry_id]

    coord = Coordinator(hass, hub)
    await coord.async_config_entry_first_refresh()

    new_entities = []
    # for s in INVERTER_SENSORS + BATTERY_SENSORS:
    #     new_entities.append(create_sensor_entity(s, hub, coordinator))
    if hub.devices["inverter"] is not None:
        new_entities.append(VoltageSensor("Voltage", "inverter", "voltage", hub, coord))
        new_entities.append(CurrentSensor("Current", "inverter", "current", hub, coord))

    if hub.devices["battery"] is not None:
        new_entities.append(EnergySensor("Energy In", "battery", "voltage", hub, coord))
        new_entities.append(
            EnergySensor("Energy Out", "battery", "voltage", hub, coord)
        )
        new_entities.append(VoltageSensor("Voltage", "battery", "voltage", hub, coord))
        new_entities.append(CurrentSensor("Current", "battery", "current", hub, coord))
        new_entities.append(PowerSensor("Power", "battery", "power", hub, coord))
        new_entities.append(
            ChargeSensor("State of Charge", "battery", "state_of_charge", hub, coord)
        )

    # Meter sensors
    new_entities.append(
        PowerSensor("Export power", "meter", "export_power", hub, coord)
    )
    new_entities.append(
        PowerSensor("Import power", "meter", "import_power", hub, coord)
    )
    new_entities.append(
        VoltageSensor(
            "Voltage phase 1",
            "meter",
            "voltage_1",
            hub,
            coord,
            entity_category=EntityCategory.DIAGNOSTIC,
        )
    )
    new_entities.append(
        VoltageSensor(
            "Voltage phase 2",
            "meter",
            "voltage_2",
            hub,
            coord,
            entity_category=EntityCategory.DIAGNOSTIC,
        )
    )
    new_entities.append(
        VoltageSensor(
            "Voltage phase 3",
            "meter",
            "voltage_3",
            hub,
            coord,
            entity_category=EntityCategory.DIAGNOSTIC,
        )
    )
    new_entities.append(
        CurrentSensor(
            "Current phase 1",
            "meter",
            "current_1",
            hub,
            coord,
            entity_category=EntityCategory.DIAGNOSTIC,
        )
    )
    new_entities.append(
        CurrentSensor("Current phase 2", "meter", "current_2", hub, coord)
    )
    new_entities.append(
        CurrentSensor("Current phase 3", "meter", "current_3", hub, coord)
    )

    async_add_entities(new_entities)
