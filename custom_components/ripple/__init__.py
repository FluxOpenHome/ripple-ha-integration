"""The Ripple integration — native HA control of cloud Ripple devices."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import device_registry as dr, entity_registry as er

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

    @callback
    def _reconcile_registries() -> None:
        """Register every current device, and PRUNE devices/entities that were
        deleted on the server so they stop showing in HA."""
        dev_reg = dr.async_get(hass)
        ent_reg = er.async_get(hass)
        devices = coordinator.data.get("devices", {})
        current_ids = set(devices.keys())

        # add / refresh — gives the card a real device count + each opens
        for device in devices.values():
            dev_reg.async_get_or_create(
                config_entry_id=entry.entry_id, **device_info_for(device)
            )
        # remove devices no longer on the account (drops their entities too)
        for dev_entry in dr.async_entries_for_config_entry(dev_reg, entry.entry_id):
            ident = next((i[1] for i in dev_entry.identifiers if i[0] == DOMAIN), None)
            if ident is not None and ident not in current_ids:
                dev_reg.async_remove_device(dev_entry.id)
        # remove stray entities whose server entity_id vanished (device kept)
        current_eids = set(coordinator.data.get("entities", {}).keys())
        for ent in er.async_entries_for_config_entry(ent_reg, entry.entry_id):
            if ent.unique_id.startswith("ripple_") and ent.unique_id[len("ripple_"):] not in current_eids:
                ent_reg.async_remove(ent.entity_id)

    _reconcile_registries()
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Keep HA in sync with the portal: when the account's device set changes
    # (a device added or deleted via the user portal), reload so new devices +
    # their entities appear and deleted ones are removed. Add/remove is rare, so
    # a brief reload here is fine.
    known_devices = set(coordinator.data.get("devices", {}).keys())

    @callback
    def _resync_on_device_change() -> None:
        nonlocal known_devices
        if not coordinator.last_update_success:
            return
        current = set(coordinator.data.get("devices", {}).keys())
        if current != known_devices:
            known_devices = current
            hass.async_create_task(hass.config_entries.async_reload(entry.entry_id))

    entry.async_on_unload(coordinator.async_add_listener(_resync_on_device_change))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        coordinator: RippleCoordinator = hass.data[DOMAIN].pop(entry.entry_id)
        await coordinator.client.close()
    return unloaded
