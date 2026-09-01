"""Virtual Switch integration."""

from __future__ import annotations

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .const import (
    DOMAIN,
    PLATFORMS,
    CONF_SWITCHES,
    CONF_NAME,
    CONF_UNIQUE_ID,
    CONF_STATE_ENTITY,
    CONF_COMMAND_ENTITY,
    CONF_ON_ICON,
    CONF_OFF_ICON,
    CONF_ATTRIBUTES,
    CONF_ENTITY,
    CONF_ATTRIBUTE,
    CONF_COPY_UNIT,
    CONF_UNIT_ATTRIBUTE,
)


ATTRIBUTE_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ENTITY): cv.entity_id,

        vol.Optional(
            CONF_ATTRIBUTE
        ): cv.string,

        vol.Optional(
            CONF_COPY_UNIT,
            default=False
        ): cv.boolean,

        vol.Optional(
            CONF_UNIT_ATTRIBUTE,
            default="unit_of_measurement"
        ): cv.string,
    }
)


SWITCH_SCHEMA = vol.Schema(
    {
        vol.Required(
            CONF_NAME
        ): cv.string,

        vol.Required(
            CONF_UNIQUE_ID
        ): cv.string,

        vol.Required(
            CONF_STATE_ENTITY
        ): cv.entity_id,

        vol.Optional(
            CONF_COMMAND_ENTITY
        ): cv.entity_id,

        vol.Optional(
            CONF_ON_ICON,
            default="mdi:toggle-switch"
        ): cv.template,

        vol.Optional(
            CONF_OFF_ICON,
            default="mdi:toggle-switch-off"
        ): cv.template,

        vol.Optional(
            CONF_ATTRIBUTES,
            default={}
        ): {
            cv.string: ATTRIBUTE_SCHEMA
        },
    }
)


CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(
                    CONF_SWITCHES
                ): {
                    cv.slug: SWITCH_SCHEMA
                }
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(
    hass: HomeAssistant,
    config: ConfigType,
) -> bool:
    """Store YAML configuration for the config entry."""

    if DOMAIN in config:
        hass.data.setdefault(
            DOMAIN,
            {}
        )

        hass.data[DOMAIN][
            CONF_SWITCHES
        ] = config[DOMAIN].get(
            CONF_SWITCHES,
            {}
        )

    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up Virtual Switch config entry."""

    await hass.config_entries.async_forward_entry_setups(
        entry,
        PLATFORMS,
    )

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Unload Virtual Switch."""

    return await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS,
    )
