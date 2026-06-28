# Ripple — Home Assistant Integration

Log in with your **Ripple** account and get **native, controllable Home Assistant
entities** for all your devices — zones, schedules, weather, moisture, and the
LoRa gateways / extenders / Gophr probes. No add-on or MQTT broker required.

## Install (HACS)
1. HACS → Integrations → ⋮ → Custom repositories → add
   `https://github.com/FluxOpenHome/ripple-ha-integration` (type: Integration).
2. Install **Ripple**, restart HA.
3. Settings → Devices & Services → **Add Integration → Ripple** → log in.

## What you get
- Native entities grouped per device: `sensor` (moisture/battery/RSSI/…),
  `binary_sensor` (online/awake), `switch` (schedule/zone enables),
  `number` (durations/thresholds).
- Control flows back through the Ripple server to the device.

## Status / TODO
- [ ] Visual branding (name shown as "Ripple"; icon/brand assets pending)
- [ ] Production domain (`DEFAULT_SERVER_URL` placeholder → Ripple domain)
- [ ] Additional platforms: `select`, `time`, `button`, `text`
- [ ] Server-side consolidated feed (`/user/api/ha/entities`) for full coverage
- [ ] Dynamic add/remove of entities between polls

> ⚠️ Rebrand in progress — code complete enough to install + log in; needs a
> live HA + Ripple account to validate end-to-end.
