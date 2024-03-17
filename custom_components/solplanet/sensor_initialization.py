"""Initializer functions for sensors for each device."""

from homeassistant.const import EntityCategory

from .sensor_definitions import (
    ChargeSensor,
    CurrentSensor,
    EnergySensor,
    PowerSensor,
    VoltageSensor,
)


def create_battery_sensors(hub, coord):
    """Return sensors for battery device."""
    entities = [
        EnergySensor("Energy In", "battery", "voltage", hub, coord),
        EnergySensor("Energy Out", "battery", "voltage", hub, coord),
        PowerSensor("Power", "battery", "power", hub, coord),
        ChargeSensor("State of charge", "battery", "power", hub, coord),
        VoltageSensor(
            "Voltage",
            "battery",
            "voltage",
            hub,
            coord,
            entity_category=EntityCategory.DIAGNOSTIC,
        ),
        CurrentSensor(
            "Current",
            "battery",
            "current",
            hub,
            coord,
            entity_category=EntityCategory.DIAGNOSTIC,
        ),
    ]
    return entities


def create_meter_sensors(hub, coord):
    """Return sensors for meter device."""
    entities = [
        PowerSensor("Power export", "meter", "export_power", hub, coord),
        PowerSensor("Power import", "meter", "import_power", hub, coord),
        PowerSensor("Power consumed", "meter", "consumed_power", hub, coord),
        EnergySensor("Energy export", "meter", "export_energy", hub, coord),
        EnergySensor("Energy import", "meter", "import_energy", hub, coord),
        EnergySensor("Energy consumed", "meter", "consumed_energy", hub, coord),
        VoltageSensor(
            "Voltage phase 1",
            "meter",
            "voltage_1",
            hub,
            coord,
            entity_category=EntityCategory.DIAGNOSTIC,
        ),
        VoltageSensor(
            "Voltage phase 2",
            "meter",
            "voltage_2",
            hub,
            coord,
            entity_category=EntityCategory.DIAGNOSTIC,
        ),
        VoltageSensor(
            "Voltage phase 3",
            "meter",
            "voltage_3",
            hub,
            coord,
            entity_category=EntityCategory.DIAGNOSTIC,
        ),
        CurrentSensor(
            "Current phase 1",
            "meter",
            "current_1",
            hub,
            coord,
            entity_category=EntityCategory.DIAGNOSTIC,
        ),
        CurrentSensor(
            "Current phase 2",
            "meter",
            "current_2",
            hub,
            coord,
            entity_category=EntityCategory.DIAGNOSTIC,
        ),
        CurrentSensor(
            "Current phase 3",
            "meter",
            "current_3",
            hub,
            coord,
            entity_category=EntityCategory.DIAGNOSTIC,
        ),
    ]
    return entities


def create_solar_sensors(hub, coord):
    """Return sensors for solar device."""
    entities = [
        PowerSensor("Power out", "solar", "power_total", hub, coord),
        PowerSensor(
            "Power out circuit 1",
            "solar",
            "power_1",
            hub,
            coord,
            entity_category=EntityCategory.DIAGNOSTIC,
        ),
        PowerSensor(
            "Power out circuit 2",
            "solar",
            "power_2",
            hub,
            coord,
            entity_category=EntityCategory.DIAGNOSTIC,
        ),
        EnergySensor("Energy out", "solar", "energy_total", hub, coord),
        EnergySensor(
            "Energy out circuit 1",
            "solar",
            "energy_1",
            hub,
            coord,
            entity_category=EntityCategory.DIAGNOSTIC,
        ),
        EnergySensor(
            "Energy out circuit 2",
            "solar",
            "energy_2",
            hub,
            coord,
            entity_category=EntityCategory.DIAGNOSTIC,
        ),
        VoltageSensor(
            "Voltage circuit 1",
            "solar",
            "voltage_1",
            hub,
            coord,
            entity_category=EntityCategory.DIAGNOSTIC,
        ),
        VoltageSensor(
            "Voltage circuit 2",
            "solar",
            "voltage_2",
            hub,
            coord,
            entity_category=EntityCategory.DIAGNOSTIC,
        ),
        CurrentSensor(
            "Current circuit 1",
            "solar",
            "current_1",
            hub,
            coord,
            entity_category=EntityCategory.DIAGNOSTIC,
        ),
        CurrentSensor(
            "Current circuit 2",
            "solar",
            "current_2",
            hub,
            coord,
            entity_category=EntityCategory.DIAGNOSTIC,
        ),
    ]
    return entities
