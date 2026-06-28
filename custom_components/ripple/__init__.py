"""The Ripple integration — native HA control of cloud Ripple devices."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .api import RippleApiClient
from .const import (
    CONF_EMAIL,
    CONF_PASSWORD,
    CONF_SERVER_URL,
    DEFAULT_SERVER_URL,
    DOMAIN,
    PLATFORMS,
)
from .coordinator import RippleCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    client = RippleApiClient(
        entry.data.get(CONF_SERVER_URL, DEFAULT_SERVER_URL),
        entry.data[CONF_EMAIL],
        entry.data[CONF_PASSWORD],
    )
    coordinator = RippleCoordinator(hass, entry, client)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        coordinator: RippleCoordinator = hass.data[DOMAIN].pop(entry.entry_id)
        await coordinator.client.close()
    return unloaded
