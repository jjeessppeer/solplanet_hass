from .const import DOMAIN


class DeviceBase:
    """Manager for generic device."""

    def __init__(self, device_id: str, name: str) -> None:
        """Initialize manager for generic device."""
        self._id = device_id
        self.name = name
        self._callbacks = set()

    @property
    def device_info(self):
        """Return information to link entities with the correct device."""
        return {
            "identifiers": {(DOMAIN, self._id)},
            "name": self.name,
            "model": "Solplanet",
            "manufacturer": "Solplanet/AISWEI",
        }


class Inverter(DeviceBase):
    """Inverter information class."""

    def __init__(self, inverter_id: str, hub_name: str) -> None:
        """Initialize an inverter device."""
        super().__init__(f"{inverter_id}_inverter", f"{hub_name} Inverter")


class Battery(DeviceBase):
    """Battery information class."""

    def __init__(self, inverter_id: str, hub_name: str) -> None:
        """Initialize a battery device."""
        super().__init__(f"{inverter_id}_battery", f"{hub_name} Battery")


class Meter(DeviceBase):
    """Meter information class."""

    def __init__(self, inverter_id: str, hub_name: str) -> None:
        """Initialize a meter device."""
        super().__init__(f"{inverter_id}_meter", f"{hub_name} Meter")


class Solar(DeviceBase):
    """Solar information class."""

    def __init__(self, inverter_id: str, hub_name: str) -> None:
        """Initialize a meter device."""
        super().__init__(f"{inverter_id}_solar", f"{hub_name} Solar")
