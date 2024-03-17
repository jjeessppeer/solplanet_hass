"""Platform for sensor integration."""
# This file shows the setup for the sensors associated with the cover.
# They are setup in the same way with the call to the async_setup_entry function
# via HA from the module __init__. Each sensor has a device_class, this tells HA how
# to display it in the UI (for know types). The unit_of_measurement property tells HA
# what the unit is, so it can display the correct range. For predefined types (such as
# battery), the unit_of_measurement should match what's expected.
# import async_timeout
from asyncio import timeout
from datetime import timedelta
import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import PERCENTAGE, UnitOfEnergy, UnitOfPower
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN, UPDATE_INTERVAL_SECONDS
from .hub import Hub

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
    new_entities.append(EnergySensor("Energy In", "meter", "voltage", hub, coord))

    async_add_entities(new_entities)


class Coordinator(DataUpdateCoordinator):
    """Custom coordinator."""

    def __init__(self, hass: HomeAssistant, hub: Hub):
        """Initialize coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="Solplanet",
            update_interval=timedelta(seconds=UPDATE_INTERVAL_SECONDS),
        )
        self.hub = hub

    async def _async_update_data(self):
        async with timeout(10):
            return await self.hub.fetch_data()


class Sensor(CoordinatorEntity, SensorEntity):
    """Base sensor interacting with manager hub."""

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

    # @callback
    # def _handle_coordinator_update(self) -> None:
    #     """Handle updated data from the coordinator."""
    #     self.async_write_ha_state()

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
        if self.coordinator.data[self._device_key][self._data_key] is None:
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
    _attr_native_unit_of_measurement = UnitOfPower.KILO_WATT

    def __init__(self, name, device_key, data_key, hub, coordinator):
        super().__init__(name, device_key, data_key, hub, coordinator)


class EnergySensor(Sensor):
    # _attr_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    _attr_device_class = SensorDeviceClass.POWER
    _attr_state_class = SensorStateClass.TOTAL_INCREASING

    def __init__(
        self,
        name,
        device_key,
        data_key,
        hub,
        coordinator,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ):
        super().__init__(name, device_key, data_key, hub, coordinator)
        if state_class:
            self._attr_state_class = state_class


class ChargeSensor(Sensor):
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_device_class = SensorDeviceClass.BATTERY

    def __init__(self, name, device_key, data_key, hub, coordinator):
        super().__init__(name, device_key, data_key, hub, coordinator)
