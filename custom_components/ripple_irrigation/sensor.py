"""Ripple sensors (read-only readings: moisture, battery, RSSI, ...)."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import RippleEntity, async_setup_ripple_entities
from .entity_map import sensor_hint


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    async_setup_ripple_entities(hass, entry, async_add_entities, "sensor", RippleSensor)


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
