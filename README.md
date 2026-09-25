# Virtual Switch for Home Assistant

Virtual Switch is a custom Home Assistant helper that creates virtual switch entities backed by existing Home Assistant entities.

It is useful when you want to combine the state, control, and attributes of existing Home Assistant entities into a single logical switch.

For example, a virtual switch can use one entity for its on/off state, another for commands, and expose power, voltage, battery level, runtime, or other entity data as attributes.

## Features

- Creates standard Home Assistant switch entities
- Uses another entity as the switch state
- Sends on/off commands to a configurable entity
- Supports separate state and command entities
- Supports different on/off icons
- Exposes states from other entities as attributes
- Copies specific attributes from other entities
- Supports Home Assistant templates for transforming attribute values
- Supports explicit units of measurement
- Can automatically copy units of measurement from source entities
- Updates when source entities or template dependencies change
- Does not poll
- Links the virtual switch to the source entity's existing Home Assistant device
- Supports multiple virtual switches

## Installation with HACS

1. Open HACS.
2. Go to Integrations.
3. Add a custom repository.
4. Use this repository:

   `https://github.com/bloodtick/home-assistant-virtual-switch`

5. Select **Integration** as the repository type.
6. Install **Virtual Switch**.
7. Restart Home Assistant.
8. Go to **Settings > Devices & services**.
9. Add **Virtual Switch**.

Virtual switch definitions are configured in YAML.

## Basic Configuration

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

Turning the virtual switch on or off sends the command to:

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

## Configuration Options

### `name`

Friendly name for the virtual switch.

```yaml
name: "Master Bedroom Switch Fan"
```

### `unique_id`

Unique Home Assistant identifier for the virtual switch.

```yaml
unique_id: master_bedroom_switch_fan
```

### `state_entity`

Entity used to determine whether the virtual switch is on or off.

```yaml
state_entity: switch.master_bedroom_fan
```

The virtual switch is also associated with the Home Assistant device belonging to this entity when a device is available.

### `command_entity`

Entity that receives the on and off commands.

```yaml
command_entity: switch.master_bedroom_fan
```

If omitted, `state_entity` is used.

### Icons

Different icons can be displayed for the on and off states.

```yaml
on_icon: mdi:fan
off_icon: mdi:fan-off
```

## Attributes

Virtual Switch can expose data from other Home Assistant entities as attributes of the switch.

### Copy an entity state

```yaml
attributes:
  power:
    entity: sensor.master_bedroom_fan_power
```

This creates a `power` attribute using the state of the source entity.

### Copy the unit of measurement

```yaml
attributes:
  power:
    entity: sensor.master_bedroom_fan_power
    copy_unit: true
```

If the source entity reports watts, the resulting attributes could be:

```text
power: 13
power_unit: W
```

### Copy a specific source attribute

Instead of using the source entity's state, you can copy one of its attributes.

```yaml
attributes:
  current_mode:
    entity: climate.living_room
    attribute: hvac_action
```

## Attribute Templates

Attribute values can be transformed using Home Assistant templates.

The source value is available inside the template as:

```text
value
```

The source entity ID is available as:

```text
entity
```

The complete Home Assistant State object is available as:

```text
state
```

### Example: Convert seconds to minutes

```yaml
attributes:
  battery_runtime_min:
    entity: sensor.ups_battery_runtime
    value_template: >
      {{ (value | float(0) / 60) | round(1) }}
    unit: "min"
```

If the source sensor reports:

```text
3600
```

the virtual switch will expose:

```text
battery_runtime_min: 60.0
battery_runtime_min_unit: min
```

### Example: Convert watts to kilowatts

```yaml
attributes:
  power_kw:
    entity: sensor.house_power
    value_template: >
      {{ (value | float(0) / 1000) | round(2) }}
    unit: "kW"
```

### Example: Convert Celsius to Fahrenheit

```yaml
attributes:
  temperature_f:
    entity: sensor.room_temperature
    value_template: >
      {{ ((value | float(0)) * 9 / 5 + 32) | round(1) }}
    unit: "°F"
```

### Example: Convert a numeric value to text

```yaml
attributes:
  load_status:
    entity: sensor.device_power
    value_template: >
      {% if value | float(0) > 100 %}
        High
      {% elif value | float(0) > 10 %}
        Normal
      {% else %}
        Idle
      {% endif %}
```

Templates can also reference other Home Assistant entities using normal Home Assistant template functions.

```yaml
attributes:
  system_status:
    entity: sensor.device_power
    value_template: >
      {% if is_state('binary_sensor.system_online', 'on') %}
        Online - {{ value }} W
      {% else %}
        Offline
      {% endif %}
```

Virtual Switch tracks entities referenced by templates so the virtual switch updates when those dependencies change.

## Units

There are two ways to add units to an attribute.

### Copy the source unit

```yaml
copy_unit: true
```

### Specify a unit explicitly

```yaml
unit: "min"
```

If both are specified, the explicit `unit` value takes precedence.

For example:

```yaml
attributes:
  battery_runtime_min:
    entity: sensor.ups_battery_runtime
    copy_unit: true
    value_template: >
      {{ (value | float(0) / 60) | round(1) }}
    unit: "min"
```

The resulting unit will be `min`, regardless of the source sensor's unit.

## UPS Example

A virtual UPS power switch can combine switch control with power and battery telemetry:

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

This allows one logical switch entity to provide:

```text
State
Power
Voltage
Battery charge
Battery runtime
Battery runtime in minutes
UPS status
UPS status data
```

while still controlling the original UPS switch.

## Multiple Virtual Switches

Multiple switches can be defined under the same integration.

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

| Option | Description |
|---|---|
| `entity` | Source Home Assistant entity |
| `attribute` | Optional attribute to read instead of the entity state |
| `copy_unit` | Copy the source entity's unit of measurement |
| `unit` | Explicit unit to expose for the virtual attribute |
| `value_template` | Home Assistant template used to transform the source value |
| `unit_attribute` | Optional source attribute containing the unit |

## Updating

When updating Virtual Switch through HACS:

1. Install or redownload the latest release.
2. Restart Home Assistant.

Python changes to custom integrations require a Home Assistant restart before they take effect.

## License

MIT
