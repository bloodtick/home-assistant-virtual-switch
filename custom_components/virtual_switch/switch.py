"""Switch platform for Virtual Switch."""

from __future__ import annotations

from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device import async_entity_id_to_device
from homeassistant.helpers.entity_platform import (
    AddConfigEntryEntitiesCallback,
)
from homeassistant.helpers.event import (
    async_track_state_change_event,
)

from .const import (
    DOMAIN,
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


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Virtual Switch entities."""

    switches = (
        hass.data
        .get(DOMAIN, {})
        .get(CONF_SWITCHES, {})
    )

    entities = [
        VirtualSwitch(
            hass=hass,
            switch_id=switch_id,
            config=switch_config,
        )
        for switch_id, switch_config
        in switches.items()
    ]

    async_add_entities(
        entities
    )


class VirtualSwitch(SwitchEntity):
    """Virtual switch backed by Home Assistant entities."""

    _attr_should_poll = False
    _attr_has_entity_name = False

    def __init__(
        self,
        hass: HomeAssistant,
        switch_id: str,
        config: dict[str, Any],
    ) -> None:
        """Initialize Virtual Switch."""

        self._hass = hass
        self._switch_id = switch_id

        self._state_entity = config[
            CONF_STATE_ENTITY
        ]

        self._command_entity = config.get(
            CONF_COMMAND_ENTITY,
            self._state_entity,
        )

        self._attributes_config = config.get(
            CONF_ATTRIBUTES,
            {},
        )

        self._on_icon = config[
            CONF_ON_ICON
        ]

        self._off_icon = config[
            CONF_OFF_ICON
        ]

        self._attr_name = config[
            CONF_NAME
        ]

        self._attr_unique_id = config[
            CONF_UNIQUE_ID
        ]

        #
        # Link this helper entity to the existing
        # device that owns state_entity.
        #
        self.device_entry = async_entity_id_to_device(
            hass,
            self._state_entity,
        )

    @property
    def is_on(self) -> bool:
        """Return current state."""

        return self._hass.states.is_state(
            self._state_entity,
            "on",
        )

    @property
    def available(self) -> bool:
        """Return source availability."""

        state = self._hass.states.get(
            self._state_entity
        )

        return (
            state is not None
            and state.state
            not in (
                "unavailable",
                "unknown",
            )
        )

    @property
    def icon(self) -> str:
        """Return dynamic icon."""

        return (
            self._on_icon
            if self.is_on
            else self._off_icon
        )

    @property
    def extra_state_attributes(
        self,
    ) -> dict[str, Any]:
        """Return configured attributes."""

        result: dict[str, Any] = {}

        for (
            output_name,
            attribute_config,
        ) in self._attributes_config.items():

            source_entity = attribute_config[
                CONF_ENTITY
            ]

            source_attribute = (
                attribute_config.get(
                    CONF_ATTRIBUTE
                )
            )

            source_state = (
                self._hass.states.get(
                    source_entity
                )
            )

            if source_state is None:
                result[
                    output_name
                ] = None

                continue

            if source_attribute:
                result[
                    output_name
                ] = source_state.attributes.get(
                    source_attribute
                )

            else:
                result[
                    output_name
                ] = source_state.state

            if attribute_config.get(
                CONF_COPY_UNIT
            ):
                unit_attribute = (
                    attribute_config.get(
                        CONF_UNIT_ATTRIBUTE,
                        "unit_of_measurement",
                    )
                )

                result[
                    f"{output_name}_unit"
                ] = source_state.attributes.get(
                    unit_attribute
                )

        return result

    async def async_turn_on(
        self,
        **kwargs: Any,
    ) -> None:
        """Turn command entity on."""

        await self._hass.services.async_call(
            "homeassistant",
            "turn_on",
            {
                "entity_id":
                    self._command_entity
            },
            blocking=True,
        )

    async def async_turn_off(
        self,
        **kwargs: Any,
    ) -> None:
        """Turn command entity off."""

        await self._hass.services.async_call(
            "homeassistant",
            "turn_off",
            {
                "entity_id":
                    self._command_entity
            },
            blocking=True,
        )

    async def async_added_to_hass(
        self,
    ) -> None:
        """Subscribe to source changes."""

        tracked_entities = {
            self._state_entity,
            self._command_entity,
        }

        for attribute_config in (
            self._attributes_config.values()
        ):
            tracked_entities.add(
                attribute_config[
                    CONF_ENTITY
                ]
            )

        @callback
        def _source_changed(
            event,
        ) -> None:
            self.async_write_ha_state()

        self.async_on_remove(
            async_track_state_change_event(
                self._hass,
                list(
                    tracked_entities
                ),
                _source_changed,
            )
        )
