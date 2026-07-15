"""Constants for the Ripple integration."""
DOMAIN = "ripple_irrigation"
DEFAULT_SERVER_URL = "https://app.fluxopenhome.com"
CONF_SERVER_URL = "server_url"
CONF_EMAIL = "email"
CONF_PASSWORD = "password"
PLATFORMS = ["sensor", "binary_sensor", "switch", "number", "select", "text", "time", "button"]
DEFAULT_SCAN_INTERVAL = 15  # seconds — how fast HA reflects new server data
