"""Ripple numbers (run durations, thresholds, sleep duration, ...)."""
from __future__ import annotations

from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import RippleEntity, async_setup_ripple_entities


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    async_setup_ripple_entities(hass, entry, async_add_entities, "number", RippleNumber)


class RippleNumber(RippleEntity, NumberEntity):
    @property
    def native_value(self) -> float | None:
        try:
            return float(self._entity.get("state"))
        except (TypeError, ValueError):
            return None

    async def async_set_native_value(self, value: float) -> None:
        await self.coordinator.client.set_entity(self._eid, value)
        await self.coordinator.async_request_refresh()
