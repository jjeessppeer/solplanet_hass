"""A demonstration 'hub' that connects several devices."""
from __future__ import annotations

# In a real implementation, this would be in an external library that's on PyPI.
# The PyPI package needs to be included in the `requirements` section of manifest.json
# See https://developers.home-assistant.io/docs/creating_integration_manifest
# for more information.
# This dummy hub always returns 3 rollers.
import asyncio
from collections.abc import Callable
import random

from homeassistant.core import HomeAssistant

from .const import DOMAIN


class Hub:
    """Solplanet manager hub."""

    manufacturer = "Solplanet/AISWEI"

    def __init__(self, hass: HomeAssistant, host: str, inverter_id: str) -> None:
        """Init hub."""
        self._host = host
        self._inverter_id = inverter_id
        self._hass = hass
        self._name = inverter_id
        self._id = inverter_id.lower()
        self.online = True

        self.devices = {}
        self.devices["inverter"] = Inverter(inverter_id, self._name, self)
        self.devices["battery"] = Battery(inverter_id, self._name, self)

        self.energy_sum = 0

    @property
    def hub_id(self) -> str:
        """ID for solplanet hub."""
        return self._id

    async def fetch_data(self) -> dict:
        """Fetch data from the inverter API."""
        self.energy_sum += 3
        self.energy_sum %= 1000
        print(self.energy_sum)
        return {
            "inverter": {
                "power_in_solar": 100,
                "power_in_battery": 100,
                "current_in": 100,
                "power_in": 100,
                "total_energy_in": 100,
                "solar_power_in": 100,
                "battery_power_in": 100,
                "current": random.randint(0, 100),
                "voltage": random.randint(0, 100),
            },
            "battery": {
                "energy_in_total": self.energy_sum,
                "energy_out_total": self.energy_sum,
                "current": random.randint(0, 100),
                "voltage": random.randint(0, 100),
                "power": random.randint(0, 100),
                "state_of_charge": random.randint(0, 100),
            },
            "solar_all": {"voltage": 100, "current": 100, "power": 100},
            "solar_1": {"voltage": 100, "current": 100, "power": 100},
        }

    async def test_connection(self) -> bool:
        """Test connectivity to inverter is OK."""
        await asyncio.sleep(1)
        return True


class DeviceBase:
    def __init__(self, device_id: str, name: str, hub: Hub):
        self._id = device_id
        self.name = name
        self.hub = hub
        self._callbacks = set()

    @property
    def device_info(self):
        """Return information to link entities with the correct device."""
        return {
            "identifiers": {(DOMAIN, self._id)},
            "name": self.name,
            "model": "Solplanet",
            "manufacturer": self.hub.manufacturer,
        }


class Inverter(DeviceBase):
    """Inverter information class."""

    def __init__(self, inverter_id: str, hub_name: str, hub: Hub) -> None:
        """Initialize an inverter device."""
        super().__init__(f"{inverter_id}_inverter", f"{hub_name} Inverter", hub)


class Battery(DeviceBase):
    """Battery information class."""

    def __init__(self, inverter_id: str, hub_name: str, hub: Hub) -> None:
        """Initialize a battery device."""
        super().__init__(f"{inverter_id}_battery", f"{hub_name} Battery", hub)
