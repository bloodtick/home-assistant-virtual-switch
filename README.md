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
- Supports explicit units for attributes
- Supports Home Assistant templates for transforming attribute values
- Updates when source entities change
- Updates when entities referenced by templates change
- Does not poll
- Links the virtual switch to the source entity's existing HA device
- Supports multiple virtual switches

## Installation with HACS

1. Open HACS.
2. Go to **Integrations**.
3. Add a custom repository.
4. Use this repository:

   `https://github.com/bloodtick/home-assistant-virtual-switch`

5. Select **Integration** as the repository type.
6. Install **Virtual Switch**.
7. Restart Home Assistant.
8. Go to **Settings > Devices & services**.
9. Add **Virtual Switch**.

Virtual switch definitions are configured in YAML.

## Example Configuration

```yaml
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
```

This creates a virtual switch whose state follows:

```text
switch.master_bedroom_fan
```

Turning the virtual switch on or off sends the same command to:

```text
switch.master_bedroom_fan
```

The resulting switch can expose attributes such as:

```text
power: 13
power_unit: W
voltage: 121
voltage_unit: V
```

## Options

### name

Friendly name for the virtual switch.

```yaml
name: "Master Bedroom Switch Fan"
```

### unique_id

Unique Home Assistant identifier.

```yaml
unique_id: master_bedroom_switch_fan
```

### state_entity

Entity used to determine whether the virtual switch is on or off.

```yaml
state_entity: switch.master_bedroom_fan
```

The virtual switch is also associated with the Home Assistant device belonging
to this entity.

### command_entity

Entity that receives on and off commands.

```yaml
command_entity: switch.master_bedroom_fan
```

If omitted, `state_entity` is used.

### Icons

Different icons can be used for the on and off states.

```yaml
on_icon: mdi:fan
off_icon: mdi:fan-off
```

Home Assistant templates can also be used for icons.

## Attributes

Attributes allow information from other Home Assistant entities to be exposed
as attributes of the virtual switch.

### Copy an Entity State

```yaml
attributes:
  power:
    entity: sensor.master_bedroom_fan_power
```

This produces:

```text
power: 13
```

### Copy the Unit of Measurement

Use `copy_unit: true` to copy the source entity's unit.

```yaml
attributes:
  power:
    entity: sensor.master_bedroom_fan_power
    copy_unit: true
```

This produces:

```text
power: 13
power_unit: W
```

### Copy a Specific Attribute

Instead of copying the entity state, a specific attribute can be copied.

```yaml
attributes:
  current_mode:
    entity: climate.living_room
    attribute: hvac_action
```

### Transform a Value with value_template

Starting with version 1.0.1, attribute values can be transformed using a
Home Assistant template.

The source value is available inside the template as `value`.

For example, convert UPS runtime from seconds to minutes:

```yaml
attributes:
  battery_runtime_min:
    entity: sensor.ups_battery_runtime
    value_template: >
      {{ (value | float(0) / 60) | round(1) }}
    unit: "min"
```

If the source entity reports:

```text
2580
```

the virtual switch will expose:

```text
battery_runtime_min: 43.0
battery_runtime_min_unit: min
```

### Template Variables

The following variables are available inside `value_template`:

| Variable | Description |
| --- | --- |
| `value` | State or selected attribute from the source entity |
| `entity` | Entity ID of the source entity |
| `state` | Full Home Assistant State object for the source entity |

Normal Home Assistant template functions such as `states()` and
`state_attr()` are also available.

For example:

```yaml
attributes:
  rounded_power:
    entity: sensor.device_power
    value_template: >
      {{ value | float(0) | round(1) }}
    unit: "W"
```

### Explicit Unit

Use `unit` to assign an explicit unit to an attribute.

```yaml
attributes:
  runtime:
    entity: sensor.ups_battery_runtime
    value_template: >
      {{ (value | float(0) / 60) | round(1) }}
    unit: "min"
```

An explicit `unit` takes precedence over `copy_unit`.

### Unit Handling

If an explicit unit is configured:

```yaml
unit: "min"
```

that unit is used.

Otherwise:

```yaml
copy_unit: true
```

copies the source entity's `unit_of_measurement`.

The resulting unit is exposed as:

```text
<attribute_name>_unit
```

For example:

```text
power_unit: W
battery_runtime_min_unit: min
```

## UPS Example

The following example creates a virtual UPS power switch with power, voltage,
battery charge, raw battery runtime, converted battery runtime, and UPS status.

```yaml
virtual_switch:
  switches:
    master_bedroom_ups_power_switch:
      name: "UPS Power"
      unique_id: master_bedroom_ups_power_switch

      state_entity: switch.hubitat_ups_mb_switch
      command_entity: switch.hubitat_ups_mb_switch

      on_icon: mdi:power
      off_icon: mdi:power

      attributes:
        power:
          entity: sensor.hubitat_ups_mb_switch_power
          copy_unit: true

        voltage:
          entity: sensor.hubitat_ups_mb_switch_voltage
          copy_unit: true

        battery:
          entity: sensor.ups_battery_charge
          copy_unit: true

        battery_runtime:
          entity: sensor.ups_battery_runtime
          copy_unit: true

        battery_runtime_min:
          entity: sensor.ups_battery_runtime
          value_template: >
            {{ (value | float(0) / 60) | round(1) }}
          unit: "min"

        status:
          entity: sensor.ups_status

        status_data:
          entity: sensor.ups_status_data
```

A resulting switch could expose:

```text
power: 37
power_unit: W

voltage: 121
voltage_unit: V

battery: 100
battery_unit: %

battery_runtime: 2580
battery_runtime_unit: s

battery_runtime_min: 43.0
battery_runtime_min_unit: min

status: OL
status_data: Online
```

## Other value_template Examples

### Watts to Kilowatts

```yaml
attributes:
  power_kw:
    entity: sensor.house_power
    value_template: >
      {{ (value | float(0) / 1000) | round(2) }}
    unit: "kW"
```

### Celsius to Fahrenheit

```yaml
attributes:
  temperature_f:
    entity: sensor.device_temperature
    value_template: >
      {{ ((value | float(0) * 9 / 5) + 32) | round(1) }}
    unit: "°F"
```

### Convert a Numeric Value to Text

```yaml
attributes:
  load_status:
    entity: sensor.device_power
    value_template: >
      {% if value | float(0) > 10 %}
        Active
      {% else %}
        Standby
      {% endif %}
```

### Reference Another Home Assistant Entity

Templates can also use normal Home Assistant template functions.

```yaml
attributes:
  room_status:
    entity: sensor.device_power
    value_template: >
      {% if is_state('binary_sensor.room_occupied', 'on') %}
        Occupied
      {% else %}
        Empty
      {% endif %}
```

The virtual switch will update when entities referenced by the template change.

## Multiple Virtual Switches

```yaml
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
```

## Attribute Configuration Reference

Each attribute supports:

| Option | Required | Description |
| --- | --- | --- |
| `entity` | Yes | Source Home Assistant entity |
| `attribute` | No | Copy a specific source attribute instead of the entity state |
| `copy_unit` | No | Copy the source entity's unit of measurement |
| `unit_attribute` | No | Source attribute containing the unit. Defaults to `unit_of_measurement` |
| `value_template` | No | Home Assistant template used to transform the source value |
| `unit` | No | Explicit unit for the resulting attribute |

## Version 1.0.1

Added:

- `value_template` support for virtual switch attributes
- Explicit `unit` support
- Template variables for `value`, `entity`, and `state`
- Tracking of entities referenced by attribute templates
- Explicit units take precedence over `copy_unit`

Existing configurations remain compatible.

## License

MIT
