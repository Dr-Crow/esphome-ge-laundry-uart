# ESPHome reference configurations

These YAML files are starting points for the maintained [ESPHome GEA external component](https://github.com/mguaylam/esphome-gea). They are reference configurations, not complete appliance profiles.

[Back to the project overview](../README.md) · [Recommended PCB Rev 2.2](../pcb/rev2.2/README.md) · [Revision history](../pcb/README.md)

| Configuration | Serial setup | Typical use |
| --- | --- | --- |
| [`gea2.yaml`](gea2.yaml) | GPIO5 TX and GPIO10 RX, inverted, 19,200 baud | Rev 2.x reference for GEA2 appliances. |
| [`gea3.yaml`](gea3.yaml) | GPIO21 TX and GPIO20 RX, non-inverted, 230,400 baud | Rev 2.x reference for GEA3 appliances. Confirm pins against the selected board before flashing. |

Both examples expect these ESPHome secrets:

```yaml
wifi_ssid: "..."
wifi_password: "..."
esp_home_ota_pw: "..."
```

Copy the appropriate example into your ESPHome configuration, change its device name and appliance entities, and confirm the UART pins and protocol settings against the selected PCB revision. A successful YAML compile does not prove electrical compatibility with an appliance.
