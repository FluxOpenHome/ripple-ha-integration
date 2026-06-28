"""Data update coordinator — polls the Ripple server for devices + entities."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import RippleApiClient, RippleAuthError, RippleApiError
from .const import DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class RippleCoordinator(DataUpdateCoordinator):
    """Fetches the account's devices + entities on a timer."""

    def __init__(self, hass: HomeAssistant, client: RippleApiClient) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
        self.client = client

    async def _async_update_data(self) -> dict:
        try:
            devices = await self.client.get_devices()
            entities = await self.client.get_entities()
        except RippleAuthError as err:
            raise ConfigEntryAuthFailed(str(err)) from err
        except RippleApiError as err:
            raise UpdateFailed(str(err)) from err

        return {
            "devices": {str(d.get("id", "")): d for d in devices},
            "entities": {
                e["entity_id"]: e for e in entities if e.get("entity_id")
            },
        }
