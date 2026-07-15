"""Ripple selects (zone modes, probe roles, crop profiles, ...)."""
from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import RippleEntity, async_setup_ripple_entities


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    async_setup_ripple_entities(hass, entry, async_add_entities, "select", RippleSelect)


class RippleSelect(RippleEntity, SelectEntity):
    @property
    def options(self) -> list[str]:
        opts = self._entity.get("attributes", {}).get("options")
        return [str(o) for o in opts] if isinstance(opts, list) else []

    @property
    def current_option(self) -> str | None:
        state = self._entity.get("state")
        return str(state) if state is not None else None

    async def async_select_option(self, option: str) -> None:
        await self.coordinator.client.set_entity(self._eid, option)
        await self.coordinator.async_request_refresh()
