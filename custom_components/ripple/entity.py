"""Base entity for Ripple — backed by the coordinator's entity feed."""
from __future__ import annotations

from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import RippleCoordinator
from .entity_map import device_info_for


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
