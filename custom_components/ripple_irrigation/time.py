"""Ripple time entities (schedule start times exposed as time pickers)."""
from __future__ import annotations

from datetime import time as dt_time

from homeassistant.components.time import TimeEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import RippleEntity, async_setup_ripple_entities


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    async_setup_ripple_entities(hass, entry, async_add_entities, "time", RippleTime)


class RippleTime(RippleEntity, TimeEntity):
    @property
    def native_value(self) -> dt_time | None:
        raw = str(self._entity.get("state") or "")
        try:
            hh, mm = raw.split(":")[:2]
            return dt_time(int(hh), int(mm))
        except (ValueError, TypeError):
            return None

    async def async_set_value(self, value: dt_time) -> None:
        await self.coordinator.client.set_entity(self._eid, value.strftime("%H:%M"))
        await self.coordinator.async_request_refresh()
