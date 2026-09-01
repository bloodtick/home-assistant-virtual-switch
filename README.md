# Virtual Switch for Home Assistant

Virtual Switch is a custom Home Assistant integration that creates virtual
switch entities backed by existing Home Assistant entities.

It is useful when you want a simplified switch while preserving the source
entity's state, commands, device relationship, and selected attributes.

## Features

- Creates standard Home Assistant switch entities
- Uses another entity as the switch state
- Sends on/off commands to a configurable entity
- Supports separate state and command entities
- Supports different on/off icons
- Copies states from other entities as attributes
- Copies specific attributes from other entities
- Can copy units of measurement
- Updates when source entities change
- Does not poll
- Links the virtual switch to the source entity's existing HA device
- Supports multiple virtual switches

## Installation with HACS

1. Open HACS.
2. Go to Integrations.
3. Add a custom repository.
4. Use this repository:

   https://github.com/bloodtick/home-assistant-virtual-switch

5. Select Integration as the repository type.
6. Install Virtual Switch.
7. Restart Home Assistant.
8. Go to Settings > Devices & services.
9. Add Virtual Switch.

Virtual switch definitions are configured in YAML.

## Example Configuration

    virtual_switch:
      switches:
        master_bedroom_switch_fan:
          name: "Master Bedroom Switch Fan"
          unique_id: master_bedroom_switch_fan

          state_entity: switch.master_bedroom_fan
          command_entity: switch.master_bedroom_fan

          on_icon: mdi:fan
          off_icon: mdi:fan-off

          attributes:
            power:
              entity: sensor.master_bedroom_fan_power
              copy_unit: true

            voltage:
              entity: sensor.master_bedroom_fan_voltage
              copy_unit: true

This creates a virtual switch whose state follows:

    switch.master_bedroom_fan

Turning the virtual switch on or off sends the same command to:

    switch.master_bedroom_fan

The resulting switch can expose attributes such as:

    power: 13
    power_unit: W
    voltage: 121
    voltage_unit: V

## Options

### name

Friendly name for the virtual switch.

    name: "Master Bedroom Switch Fan"

### unique_id

Unique Home Assistant identifier.

    unique_id: master_bedroom_switch_fan

### state_entity

Entity used to determine whether the virtual switch is on or off.

    state_entity: switch.master_bedroom_fan

The virtual switch is also associated with the HA device belonging to this
entity.

### command_entity

Entity that receives on and off commands.

    command_entity: switch.master_bedroom_fan

If omitted, state_entity is used.

### Icons

    on_icon: mdi:fan
    off_icon: mdi:fan-off

### Attributes

Copy another entity's state:

    attributes:
      power:
        entity: sensor.master_bedroom_fan_power

Copy its unit too:

    attributes:
      power:
        entity: sensor.master_bedroom_fan_power
        copy_unit: true

Copy a specific attribute instead:

    attributes:
      current_mode:
        entity: climate.living_room
        attribute: hvac_action

## Multiple Virtual Switches

    virtual_switch:
      switches:
        bedroom_fan:
          name: "Bedroom Fan"
          unique_id: bedroom_fan
          state_entity: switch.bedroom_fan

        office_fan:
          name: "Office Fan"
          unique_id: office_fan
          state_entity: switch.office_fan

## License

MIT
