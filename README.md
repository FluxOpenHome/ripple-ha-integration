<img src="https://raw.githubusercontent.com/FluxOpenHome/ripple-ha-integration/main/custom_components/ripple_irrigation/brand/logo%402x.png" alt="Ripple" height="72">

# Ripple — Home Assistant Integration

Log in with your **Ripple** account and get **native, controllable Home Assistant entities** for all your devices — zones, schedules, weather, moisture, and the LoRa network (magpi gateways, pidgn extenders, gophr probes). No add-on or MQTT broker required.

## Install (HACS)

1. HACS → Integrations → ⋮ → Custom repositories → add `https://github.com/FluxOpenHome/ripple-ha-integration` (type: Integration).
2. Install **Ripple**, restart HA.
3. Settings → Devices & Services → **Add Integration** → **Ripple** → log in with your Ripple account.

## What you get

- Native entities grouped per device: `sensor` (moisture/battery/RSSI/…), `binary_sensor` (online/awake), `switch` (schedule/zone enables), `number` (durations/thresholds), `select` (modes/roles), `text` & `time` (schedule start times), `button` (quick actions).
- New devices and entities appear automatically between polls; removed ones are pruned — no HA restart needed.
- Control flows back through the Ripple cloud to the device. Manual zone starts always fire.

## Upgrading from ≤ 0.2.0

v0.3.0 renamed the integration domain from `ripple` to `ripple_irrigation`. After updating: remove the old integration entry in Settings → Devices & Services, restart HA, and add **Ripple** again.
