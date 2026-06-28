"""Config flow — log in with a Ripple account."""
from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .api import RippleApiClient, RippleAuthError
from .const import (
    CONF_EMAIL,
    CONF_PASSWORD,
    CONF_SERVER_URL,
    DEFAULT_SERVER_URL,
    DOMAIN,
)


class RippleConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the Ripple account login."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        errors: dict[str, str] = {}

        if user_input is not None:
            client = RippleApiClient(
                user_input.get(CONF_SERVER_URL, DEFAULT_SERVER_URL),
                user_input[CONF_EMAIL],
                user_input[CONF_PASSWORD],
            )
            try:
                customer_id = await client.login()
            except RippleAuthError:
                errors["base"] = "invalid_auth"
            except Exception:  # noqa: BLE001 — surface as cannot_connect
                errors["base"] = "cannot_connect"
            else:
                await self.async_set_unique_id(customer_id or user_input[CONF_EMAIL])
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=user_input[CONF_EMAIL], data=user_input
                )
            finally:
                await client.close()

        schema = vol.Schema(
            {
                vol.Required(CONF_EMAIL): str,
                vol.Required(CONF_PASSWORD): str,
                vol.Optional(CONF_SERVER_URL, default=DEFAULT_SERVER_URL): str,
            }
        )
        return self.async_show_form(
            step_id="user", data_schema=schema, errors=errors
        )
