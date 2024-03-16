"""Constants for the AISWEI integration."""

from homeassistant.components.sensor import SensorDeviceClass

DOMAIN = "solplanet"


SENSOR_CONFIGS = {
    "voltage": {
        "device_class": SensorDeviceClass.CURRENT,
        "unit": "V",
        "state_class": None,
    },
    "current": {
        "device_class": SensorDeviceClass.CURRENT,
        "unit": "V",
        "state_class": None,
    },
}

SOLAR_SENSORS = [
    {
        "name": "Current",
        "device_key": "solar",
        "data_key": "current",
        "unit": "A",
        "device_class": SensorDeviceClass.CURRENT,
    },
    {
        "name": "Voltage",
        "device_key": "solar",
        "data_key": "current",
        "unit": "A",
        "device_class": SensorDeviceClass.VOLTAGE,
    },
    {
        "name": "Voltage",
        "device_key": "solar",
        "data_key": "current",
        "unit": "A",
        "device_class": SensorDeviceClass.VOLTAGE,
    },
]

INVERTER_SENSORS = [
    {
        "name": "Current",
        "device_key": "inverter",
        "data_key": "current",
        "unit": "A",
        "device_class": SensorDeviceClass.CURRENT,
    },
    {
        "name": "Voltage",
        "device_key": "inverter",
        "data_key": "voltage",
        "unit": "V",
        "device_class": SensorDeviceClass.VOLTAGE,
    },
]

BATTERY_SENSORS = [
    {
        "name": "Current",
        "device_key": "battery",
        "data_key": "current",
        "unit": "A",
        "device_class": SensorDeviceClass.CURRENT,
    },
    {
        "name": "Voltage",
        "device_key": "battery",
        "data_key": "voltage",
        "unit": "V",
        "device_class": SensorDeviceClass.VOLTAGE,
    },
]
