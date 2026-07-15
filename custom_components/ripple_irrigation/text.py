"""Ripple text inputs (schedule start times as HH:MM, names, ...)."""
from __future__ import annotations

from homeassistant.components.text import TextEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import RippleEntity, async_setup_ripple_entities


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    async_setup_ripple_entities(hass, entry, async_add_entities, "text", RippleText)


class RippleText(RippleEntity, TextEntity):
    @property
    def native_value(self) -> str | None:
        state = self._entity.get("state")
        return str(state) if state is not None else None

    async def async_set_value(self, value: str) -> None:
        await self.coordinator.client.set_entity(self._eid, value)
        await self.coordinator.async_request_refresh()
