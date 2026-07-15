"""Base entity for Ripple — backed by the coordinator's entity feed."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import RippleCoordinator
from .entity_map import device_info_for, entity_domain


class RippleEntity(CoordinatorEntity[RippleCoordinator]):
    """One HA entity mirroring one server entity_id."""

    _attr_has_entity_name = False

    def __init__(self, coordinator: RippleCoordinator, entity_id: str) -> None:
        super().__init__(coordinator)
        self._eid = entity_id
        self._attr_unique_id = f"ripple_{entity_id}"

    @property
    def _entity(self) -> dict:
        return self.coordinator.data["entities"].get(self._eid, {})

    @property
    def _device(self) -> dict:
        did = str(self._entity.get("device_id", ""))
        return self.coordinator.data["devices"].get(did, {})

    @property
    def name(self) -> str:
        return (
            self._entity.get("friendly_name")
            or self._entity.get("attributes", {}).get("friendly_name")
            or self._eid
        )

    @property
    def available(self) -> bool:
        return self._eid in self.coordinator.data.get("entities", {})

    @property
    def device_info(self):
        return device_info_for(self._device)


def async_setup_ripple_entities(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
    domain: str,
    factory,
) -> None:
    """Create entities for ``domain`` now, and again whenever the server feed
    grows new ones — so a newly-paired device or a new sensor (e.g. a gateway's
    packets/online sensors) shows up without an HA restart. Removal is handled
    by the coordinator pruning the device/entity registry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    known: set[str] = set()

    @callback
    def _discover() -> None:
        fresh = []
        for eid in coordinator.data.get("entities", {}):
            if eid in known or entity_domain(eid) != domain:
                continue
            known.add(eid)
            fresh.append(factory(coordinator, eid))
        if fresh:
            async_add_entities(fresh)

    _discover()
    entry.async_on_unload(coordinator.async_add_listener(_discover))
