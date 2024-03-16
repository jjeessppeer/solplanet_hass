"""Platform for sensor integration."""
# This file shows the setup for the sensors associated with the cover.
# They are setup in the same way with the call to the async_setup_entry function
# via HA from the module __init__. Each sensor has a device_class, this tells HA how
# to display it in the UI (for know types). The unit_of_measurement property tells HA
# what the unit is, so it can display the correct range. For predefined types (such as
# battery), the unit_of_measurement should match what's expected.
from datetime import timedelta
import logging
import random

import async_timeout

from homeassistant.components.light import LightEntity
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN, INVERTER_SENSORS, BATTERY_SENSORS
from homeassistant.components.sensor.const import SensorStateClass
from .hub import Hub
from homeassistant.const import UnitOfEnergy, UnitOfPower

_LOGGER = logging.getLogger(__name__)


# See cover.py for more details.
# Note how both entities for each roller sensor (battry and illuminance) are added at
# the same time to the same list. This way only a single async_add_devices call is
# required.
async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add sensors for passed config_entry in HA."""
    hub = hass.data[DOMAIN][config_entry.entry_id]

    coord = Coordinator(hass, hub)
    await coord.async_config_entry_first_refresh()

    def create_sensor_entity():
        return Sensor()

    new_entities = []
    # for s in INVERTER_SENSORS + BATTERY_SENSORS:
    #     new_entities.append(create_sensor_entity(s, hub, coordinator))
    if hub.devices["inverter"] is not None:
        new_entities.append(VoltageSensor("Voltage", "inverter", "voltage", hub, coord))
        new_entities.append(CurrentSensor("Current", "inverter", "current", hub, coord))
    if hub.devices["battery"] is not None:
        new_entities.append(VoltageSensor("Voltage", "battery", "voltage", hub, coord))
        new_entities.append(CurrentSensor("Current", "battery", "current", hub, coord))
        new_entities.append(
            EnergySensor("Energy3", "battery", "energy_total", hub, coord)
        )

    async_add_entities(new_entities)


def create_sensor_entity(sensor_config, hub, coordinator):
    """Create a sensor entity from configuration."""
    return Sensor(
        sensor_config["name"],
        sensor_config["device_key"],
        sensor_config["data_key"],
        sensor_config["unit"],
        sensor_config["device_class"],
        hub,
        coordinator,
    )


class Coordinator(DataUpdateCoordinator):
    """Custom coordinator."""

    def __init__(self, hass: HomeAssistant, hub: Hub):
        """Initialize coordinator."""
        super().__init__(
            hass, _LOGGER, name="Solplanet", update_interval=timedelta(seconds=1)
        )
        self.hub = hub

    async def _async_update_data(self):
        async with async_timeout.timeout(10):
            return await self.hub.fetch_data()


class Sensor(CoordinatorEntity, SensorEntity):
    def __init__(
        self,
        name: str,
        device_key,
        data_key,
        hub: Hub,
        coordinator: Coordinator,
    ):
        super().__init__(coordinator)

        self._attr_unique_id = f"{hub._id}_{device_key.lower()}_{name.lower()}"
        self._attr_name = f"{hub.devices[device_key].name} {name}"

        self._device_key = device_key
        self._data_key = data_key

        self._hub = hub

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    @property
    def device_info(self):
        """Return information to link this entity with the correct device."""
        return self._hub.devices[self._device_key].device_info

    @property
    def available(self) -> bool:
        """Return True if roller and hub is available."""
        if self._device_key not in self.coordinator.data:
            return False
        if self._data_key not in self.coordinator.data[self._device_key]:
            return False
        return True

    @property
    def state(self) -> float:
        """Return the state of the sensor."""
        return self.coordinator.data[self._device_key][self._data_key]


class VoltageSensor(Sensor):
    device_class = SensorDeviceClass.VOLTAGE
    # _attr_unit_of_measurement = "V"
    _attr_native_unit_of_measurement = "V"

    def __init__(self, name, device_key, data_key, hub, coordinator):
        super().__init__(name, device_key, data_key, hub, coordinator)


class CurrentSensor(Sensor):
    device_class = SensorDeviceClass.CURRENT
    # _attr_unit_of_measurement = "A"
    _attr_native_unit_of_measurement = "A"

    def __init__(self, name, device_key, data_key, hub, coordinator):
        super().__init__(name, device_key, data_key, hub, coordinator)


class PowerSensor(Sensor):
    device_class = SensorDeviceClass.POWER
    _attr_unit_of_measurement = UnitOfPower.KILO_WATT

    def __init__(self, name, device_key, data_key, hub, coordinator):
        super().__init__(name, device_key, data_key, hub, coordinator)


class EnergySensor(Sensor):
    _attr_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    _attr_device_class = SensorDeviceClass.POWER
    _attr_state_class = SensorStateClass.TOTAL_INCREASING

    def __init__(self, name, device_key, data_key, hub, coordinator):
        super().__init__(name, device_key, data_key, hub, coordinator)
