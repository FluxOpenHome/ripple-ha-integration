"""Ripple sensors (read-only readings: moisture, battery, RSSI, ...)."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import RippleEntity
from .entity_map import entity_domain, sensor_hint


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        RippleSensor(coordinator, eid)
        for eid in coordinator.data["entities"]
        if entity_domain(eid) == "sensor"
    )


class RippleSensor(RippleEntity, SensorEntity):
    @property
    def native_value(self):
        return self._entity.get("state")

    @property
    def device_class(self):
        return sensor_hint(self._eid)[0]

    @property
    def native_unit_of_measurement(self):
        return sensor_hint(self._eid)[1]
