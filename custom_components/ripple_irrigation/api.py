"""Ripple cloud API client (HA side).

Authenticates against the Ripple management server with the user's account and
fetches their devices + entities. Owns a private aiohttp session so the
portal_session cookie stays isolated to this integration. Control writes go to
/user/api/entities/{id}/set, which the server relays to the device.
"""
from __future__ import annotations

from typing import Any

import aiohttp


class RippleAuthError(Exception):
    """Credentials missing or rejected."""


class RippleApiError(Exception):
    """Network / server error."""


class RippleApiClient:
    def __init__(self, server_url: str, email: str, password: str) -> None:
        self._base = (server_url or "").rstrip("/")
        self._email = email
        self._password = password
        # Private session with its own cookie jar (holds portal_session).
        self._session = aiohttp.ClientSession()
        self._authed = False

    async def close(self) -> None:
        await self._session.close()

    async def login(self) -> str:
        """Authenticate; returns customer_id. Cookie persists in the session."""
        if not self._email or not self._password:
            raise RippleAuthError("Missing account email/password")
        try:
            async with self._session.post(
                f"{self._base}/user/auth/login",
                json={"email": self._email, "password": self._password},
            ) as resp:
                if resp.status == 401:
                    raise RippleAuthError("Invalid email or password")
                if resp.status == 403:
                    raise RippleAuthError("Account is disabled")
                resp.raise_for_status()
                self._authed = True
                data = await resp.json()
                return str(data.get("customer_id", ""))
        except aiohttp.ClientError as err:
            raise RippleApiError(str(err)) from err

    async def _get(self, path: str) -> Any:
        if not self._authed:
            await self.login()
        try:
            async with self._session.get(f"{self._base}{path}") as resp:
                if resp.status in (401, 403):
                    self._authed = False
                    await self.login()
                    async with self._session.get(f"{self._base}{path}") as resp2:
                        resp2.raise_for_status()
                        return await resp2.json()
                resp.raise_for_status()
                return await resp.json()
        except aiohttp.ClientError as err:
            raise RippleApiError(str(err)) from err

    async def get_bundle(self) -> tuple[list[dict], list[dict]]:
        """One-request consolidated feed: (devices, entities).

        Falls back to the two legacy endpoints if the server predates
        /user/api/ha/entities."""
        if not self._authed:
            await self.login()
        try:
            async with self._session.get(f"{self._base}/user/api/ha/entities") as resp:
                if resp.status == 404:
                    return await self.get_devices(), await self.get_entities()
                if resp.status in (401, 403):
                    self._authed = False
                    await self.login()
                    return await self.get_bundle()
                resp.raise_for_status()
                data = await resp.json()
                return data.get("devices", []) or [], data.get("entities", []) or []
        except aiohttp.ClientError as err:
            raise RippleApiError(str(err)) from err

    async def get_devices(self) -> list[dict]:
        data = await self._get("/user/api/devices")
        if isinstance(data, dict):
            return data.get("devices", []) or []
        return data or []

    async def get_entities(self) -> list[dict]:
        data = await self._get("/user/api/entities")
        return data if isinstance(data, list) else []

    async def set_entity(self, entity_id: str, value: Any) -> bool:
        """Relay a control command: HA -> server -> device."""
        if not self._authed:
            await self.login()
        try:
            async with self._session.post(
                f"{self._base}/user/api/entities/{entity_id}/set",
                json={"value": value},
            ) as resp:
                resp.raise_for_status()
                return True
        except aiohttp.ClientError as err:
            raise RippleApiError(str(err)) from err
