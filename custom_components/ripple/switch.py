"""Ripple switches (schedule enable, day toggles, zone enables, ...)."""
from __future__ import annotations

from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import RippleEntity, async_setup_ripple_entities


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    async_setup_ripple_entities(hass, entry, async_add_entities, "switch", RippleSwitch)


class RippleSwitch(RippleEntity, SwitchEntity):
    @property
    def is_on(self) -> bool:
        return str(self._entity.get("state", "")).lower() == "on"

    async def async_turn_on(self, **kwargs: Any) -> None:
        await self.coordinator.client.set_entity(self._eid, "on")
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self.coordinator.client.set_entity(self._eid, "off")
        await self.coordinator.async_request_refresh()
