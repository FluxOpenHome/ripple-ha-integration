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
from homeassistant.helpers import device_registry as dr

from .coordinator import RippleCoordinator
from .entity_map import device_info_for


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    client = RippleApiClient(
        entry.data.get(CONF_SERVER_URL, DEFAULT_SERVER_URL),
        entry.data[CONF_EMAIL],
        entry.data[CONF_PASSWORD],
    )
    coordinator = RippleCoordinator(hass, client)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    # Register EVERY device on the account up front (from /user/api/devices) so
    # they all appear in the UI, the integration card shows a real device count
    # (like other integrations), and each device can be opened — even before its
    # entities load. Entities created by the platforms below then attach via
    # matching identifiers (see device_info_for).
    device_reg = dr.async_get(hass)
    for device in coordinator.data.get("devices", {}).values():
        device_reg.async_get_or_create(
            config_entry_id=entry.entry_id,
            **device_info_for(device),
        )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        coordinator: RippleCoordinator = hass.data[DOMAIN].pop(entry.entry_id)
        await coordinator.client.close()
    return unloaded
