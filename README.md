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

v0.3.0 renamed the integration domain from `ripple` to `ripple_irrigation` (the old domain collided with Home Assistant's built-in XRP "ripple" integration, which is also why the wrong logo appeared). After updating: remove the old integration entry in Settings → Devices & Services, restart HA, and add **Ripple** again.

## Logo / brand icon

As of Home Assistant **2026.3.0**, custom integrations ship their own brand images — the central [home-assistant/brands](https://github.com/home-assistant/brands) repository no longer accepts custom-integration icons ([announcement](https://developers.home-assistant.io/blog/2026/02/24/brands-proxy-api)). The assets live in [`custom_components/ripple_irrigation/brand/`](custom_components/ripple_irrigation/brand/):

- `icon.png` / `icon@2x.png` — the Ripple droplet mark (256×256 / 512×512, works on light and dark)
- `logo.png` / `logo@2x.png` — the navy Ripple wordmark (for light theme)
- `dark_logo.png` / `dark_logo@2x.png` — the white Ripple wordmark (for dark theme)

Local brand images are auto-detected and take priority over the brands CDN — no PR or manifest change needed. Requires HA 2026.3+; on older versions HA shows a neutral placeholder.
