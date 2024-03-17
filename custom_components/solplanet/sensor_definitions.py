from asyncio import timeout
from datetime import timedelta
import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import PERCENTAGE, EntityCategory, UnitOfEnergy, UnitOfPower
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN, UPDATE_INTERVAL_SECONDS
from .hub import Hub

_LOGGER = logging.getLogger(__name__)


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
        entity_category=None,
    ) -> None:
        """Initialize sensor base."""
        super().__init__(coordinator)

        if entity_category:
            self._attr_entity_category = entity_category

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
    # _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, name, device_key, data_key, hub, coordinator, **kwargs):
        super().__init__(name, device_key, data_key, hub, coordinator, **kwargs)


class CurrentSensor(Sensor):
    device_class = SensorDeviceClass.CURRENT
    # _attr_unit_of_measurement = "A"
    _attr_native_unit_of_measurement = "A"

    def __init__(self, name, device_key, data_key, hub, coordinator, **kwargs):
        super().__init__(name, device_key, data_key, hub, coordinator, **kwargs)


class PowerSensor(Sensor):
    device_class = SensorDeviceClass.POWER
    _attr_native_unit_of_measurement = UnitOfPower.KILO_WATT

    def __init__(self, name, device_key, data_key, hub, coordinator, **kwargs):
        super().__init__(name, device_key, data_key, hub, coordinator, **kwargs)


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
        **kwargs,
    ):
        super().__init__(name, device_key, data_key, hub, coordinator, **kwargs)
        if state_class:
            self._attr_state_class = state_class


class ChargeSensor(Sensor):
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_device_class = SensorDeviceClass.BATTERY

    def __init__(self, name, device_key, data_key, hub, coordinator, **kwargs):
        super().__init__(name, device_key, data_key, hub, coordinator, **kwargs)
