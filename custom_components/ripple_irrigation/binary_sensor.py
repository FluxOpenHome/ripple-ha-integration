"""Ripple binary sensors (online, awake, ...)."""
from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import RippleEntity, async_setup_ripple_entities


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    async_setup_ripple_entities(hass, entry, async_add_entities, "binary_sensor", RippleBinarySensor)


class RippleBinarySensor(RippleEntity, BinarySensorEntity):
    @property
    def is_on(self) -> bool:
        return str(self._entity.get("state", "")).lower() in ("on", "true", "1", "open")
