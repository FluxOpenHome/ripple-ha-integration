"""Data update coordinator — polls the Ripple server for devices + entities."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import RippleApiClient, RippleAuthError, RippleApiError
from .const import DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class RippleCoordinator(DataUpdateCoordinator):
    """Fetches the account's devices + entities on a timer."""

    def __init__(
        self, hass: HomeAssistant, entry: ConfigEntry, client: RippleApiClient
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
        self.entry = entry
        self.client = client

    async def _async_update_data(self) -> dict:
        try:
            devices = await self.client.get_devices()
            entities = await self.client.get_entities()
        except RippleAuthError as err:
            raise ConfigEntryAuthFailed(str(err)) from err
        except RippleApiError as err:
            raise UpdateFailed(str(err)) from err

        data = {
            "devices": {str(d.get("id", "")): d for d in devices},
            "entities": {
                e["entity_id"]: e for e in entities if e.get("entity_id")
            },
        }
        # Remove devices/entities that no longer exist on the server (e.g. the
        # user deleted them in the portal) so they don't linger in HA forever.
        self._prune(data["devices"].keys(), data["entities"].keys())
        return data

    def _prune(self, current_device_ids, current_entity_ids) -> None:
        dev_ids = set(current_device_ids)
        ent_keys = set(current_entity_ids)

        dev_reg = dr.async_get(self.hass)
        ent_reg = er.async_get(self.hass)

        # 1) Drop registry entities whose source entity_id is gone from the feed.
        #    unique_id is "ripple_<server_entity_id>" (see entity.py).
        for entry in er.async_entries_for_config_entry(ent_reg, self.entry.entry_id):
            src = entry.unique_id[len("ripple_"):] if entry.unique_id.startswith("ripple_") else None
            if src is not None and src not in ent_keys:
                ent_reg.async_remove(entry.entity_id)

        # 2) Drop registry devices that are no longer in the server device list.
        for device in dr.async_entries_for_config_entry(dev_reg, self.entry.entry_id):
            ids = {ident[1] for ident in device.identifiers if ident[0] == DOMAIN}
            if ids and not (ids & dev_ids):
                dev_reg.async_remove_device(device.id)
