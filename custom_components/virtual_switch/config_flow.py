"""Config flow for Virtual Switch."""

from __future__ import annotations

from typing import Any

from homeassistant import config_entries

from .const import DOMAIN


class VirtualSwitchConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Virtual Switch."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Handle the initial step."""

        # Only one Virtual Switch integration entry is needed.
        if self._async_current_entries():
            return self.async_abort(reason="already_configured")

        return self.async_create_entry(
            title="Virtual Switch",
            data={},
        )
