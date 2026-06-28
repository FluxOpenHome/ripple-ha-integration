"""Ripple binary sensors (online, awake, ...)."""
from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import RippleEntity
from .entity_map import entity_domain


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        RippleBinarySensor(coordinator, eid)
        for eid in coordinator.data["entities"]
        if entity_domain(eid) == "binary_sensor"
    )


class RippleBinarySensor(RippleEntity, BinarySensorEntity):
    @property
    def is_on(self) -> bool:
        return str(self._entity.get("state", "")).lower() in ("on", "true", "1", "open")
