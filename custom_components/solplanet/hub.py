"""A demonstration 'hub' that connects several devices."""
from __future__ import annotations

import asyncio
from asyncio import timeout
import contextlib
import random

import requests

from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .devices import Battery, Inverter, Meter, Solar


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
        self.devices["inverter"] = Inverter(inverter_id, self._name)
        self.devices["battery"] = Battery(inverter_id, self._name)
        self.devices["meter"] = Meter(inverter_id, self._name)
        self.devices["solar"] = Solar(inverter_id, self._name)

        self.energy_sum = 0

    @property
    def hub_id(self) -> str:
        """ID for solplanet hub."""
        return self._id

    async def fetch_data(self) -> dict:
        """Fetch data from the inverter API."""

        def req(url):
            return requests.get(url, timeout=10)

        inverter_req = await self._hass.async_add_executor_job(
            req, "http://192.168.1.101:8080/inverter_test.json"
        )
        battery_req = await self._hass.async_add_executor_job(
            req, "http://192.168.1.101:8080/battery_test.json"
        )
        with contextlib.suppress(Exception):
            inverter_info = inverter_req.json()
            battery_info = battery_req.json()

        # TODO: add json validation
        result = {}

        result["battery"] = {
            "energy_in_total": battery_info["ebi"] / 10,
            "energy_out_total": battery_info["ebo"] / 10,
            "current": battery_info["cb"],
            "voltage": battery_info["vb"],
            "power": battery_info["pb"],
            "state_of_charge": battery_info["soc"],
        }

        result["inverter"] = {
            "power_in_solar": 10,
            "power_in_battery": 100,
            "power_in_total": 100,
            "energy_in_solar": 10,
            "energy_in_battery": 100,
            "energy_in_total": 100,
        }

        result["meter"] = {
            "voltage_1": inverter_info["vac"][0],
            "voltage_2": inverter_info["vac"][1],
            "voltage_3": inverter_info["vac"][2],
            "current_1": inverter_info["iac"][0],
            "current_2": inverter_info["iac"][1],
            "current_3": inverter_info["iac"][2],
            "export_power": 10,
            "import_power": 10,
            "export_energy": 10,
            "import_energy": 10,
        }

        result["solar"] = {
            "power_total": 10,
            "power_1": 10,
            "power_2": 10,
            "voltage_1": 10,
            "voltage_2": 10,
            "current_1": 10,
            "current_2": 10,
        }

        return result

    async def test_connection(self) -> bool:
        """Test connectivity to inverter is OK."""
        await asyncio.sleep(1)
        return True
