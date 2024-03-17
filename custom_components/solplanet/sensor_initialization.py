"""Initializer functions for sensors for each device."""

from .sensor import CurrentSensor, VoltageSensor


def create_meter_sensors(hub, coord):
    entities = [CurrentSensor("Current phase 2", "meter", "current_2", hub, coord)]
    return entities
