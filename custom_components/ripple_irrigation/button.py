"""Ripple buttons (quick run, stop all, check-in, ...)."""
from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import RippleEntity, async_setup_ripple_entities


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    async_setup_ripple_entities(hass, entry, async_add_entities, "button", RippleButton)


class RippleButton(RippleEntity, ButtonEntity):
    async def async_press(self) -> None:
        await self.coordinator.client.set_entity(self._eid, "press")
        await self.coordinator.async_request_refresh()
