"""Constants for the Ripple integration."""
DOMAIN = "ripple"
# TODO(rebrand): Ripple production domain. Defaults to the current server.
DEFAULT_SERVER_URL = "https://app.fluxopenhome.com"
CONF_SERVER_URL = "server_url"
CONF_EMAIL = "email"
CONF_PASSWORD = "password"
PLATFORMS = ["sensor", "binary_sensor", "switch", "number"]
DEFAULT_SCAN_INTERVAL = 60  # seconds
