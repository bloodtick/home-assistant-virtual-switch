"""Config flow for Virtual Switch."""

from __future__ import annotations

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN


class VirtualSwitchConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):
    """Handle Virtual Switch config flow."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input=None,
    ) -> FlowResult:
        """Set up Virtual Switch."""

        await self.async_set_unique_id(
            DOMAIN
        )

        self._abort_if_unique_id_configured()

        if user_input is not None:
            return self.async_create_entry(
                title="Virtual Switch",
                data={},
            )

        return self.async_show_form(
            step_id="user",
            data_schema=None,
        )
