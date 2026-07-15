"""Map Ripple server entities -> HA platforms + metadata."""
from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN

# server entity domain -> HA platform
DOMAIN_TO_PLATFORM = {
    "sensor": "sensor",
    "binary_sensor": "binary_sensor",
    "switch": "switch",
    "number": "number",
    "select": "select",
    "text": "text",
    "time": "time",
    "button": "button",
}

# substring in entity_id -> (device_class, unit)
SENSOR_HINTS = {
    "rssi": ("signal_strength", "dBm"),
    "battery": ("battery", "%"),
    "soc": ("battery", "%"),
    "moisture": ("moisture", "%"),
    "percentage": ("moisture", "%"),
    "temperature": ("temperature", "°C"),
    "voltage": ("voltage", "V"),
    "current": ("current", "A"),
    "power": ("power", "W"),
}


def entity_domain(entity_id: str) -> str:
    return entity_id.split(".", 1)[0] if "." in entity_id else ""


def platform_for(entity_id: str) -> str | None:
    return DOMAIN_TO_PLATFORM.get(entity_domain(entity_id))


def sensor_hint(entity_id: str) -> tuple[str | None, str | None]:
    low = entity_id.lower()
    for key, (dclass, unit) in SENSOR_HINTS.items():
        if key in low:
            return dclass, unit
    return None, None


def device_info_for(device: dict) -> DeviceInfo:
    dev_id = str(device.get("id", "")) or "unknown"
    name = device.get("display_name") or device.get("mac_address") or "Ripple Device"
    model = {
        "controller": "keepr Irrigation Controller",
        "remote": "beetl Remote",
        "blue_remote": "beetl Remote",
        "probe": "gophr Moisture Probe",
        "thermo": "frogg Thermo Sensor",
        "lora_probe": "gophr LoRa Probe",
        "lora_gateway": "magpi Gateway",
        "lora_extender": "pidgn Extender",
    }.get(device.get("device_category", ""), "Ripple Device")
    info = DeviceInfo(
        identifiers={(DOMAIN, dev_id)},
        name=name,
        manufacturer="Ripple",
        model=model,
    )
    if device.get("firmware_version"):
        info["sw_version"] = device["firmware_version"]
    return info
