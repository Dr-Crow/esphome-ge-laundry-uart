# Shared Rev3C firmware

These unchanged recovered profiles support the common XIAO ESP32-C3/C6 side-header functions on the restored dual appliance-input Rev3C review candidate. Restoring PIN1/PIN3 and automatic PIN1 priority does not qualify power circuitry or an appliance model. Read [power qualification](../../pcb/rev3c/POWER-QUALIFICATION.md) before connecting hardware.

| Profile | Module | Protocol | Module TX / RX GPIO |
| --- | --- | --- | --- |
| [c3-gea2.yaml](c3-gea2.yaml) | XIAO ESP32-C3 | GEA2, inverted, 19,200 baud | 5 / 10 |
| [c3-gea3.yaml](c3-gea3.yaml) | XIAO ESP32-C3 | GEA3, non-inverted, 230,400 baud | 21 / 20 |
| [c6-gea2.yaml](c6-gea2.yaml) | XIAO ESP32-C6 | GEA2, inverted, 19,200 baud | 21 / 18 |
| [c6-gea3.yaml](c6-gea3.yaml) | XIAO ESP32-C6 | GEA3, non-inverted, 230,400 baud | 16 / 17 |

## Pinned sources and build evidence

Use ESPHome **2026.9.1** with ESP-IDF **5.5.5**. GEA is pinned to commit `283ff2b0dfe90a6d14a5417a23176d433be8a5b3`. The four profiles and four package YAML files remain unchanged during dual-input restoration. All four configurations and real factory/OTA/ELF builds were already checked with these pinned tools, using dummy secrets and no network or appliance connection; this restoration does not require rebuilding unchanged sources.

Copy a profile and its `packages` directory together, then supply `wifi_ssid`, `wifi_password` and `esp_home_ota_pw` in your own ignored `secrets.yaml`. Build success verifies firmware generation, not GPIO electrical behavior, power headroom, bus acceptance or hardware qualification.

Choose protocol, destinations and ERDs for the exact appliance. GEA2 destination `0x24` and Door/Cycle Complete entities are examples, not a verified refrigerator profile. GEA3 uses destination `0xC0`. These are ESPHome Wi-Fi profiles; Matter/Thread is not implemented.

## Carrier mapping and JP1

GEA2 TX/RX use D3/D10; keep `JP1`'s default 1–2 bridge for these profiles. Alternate 2–3 changes TX and reaches C3 BOOT. C6 D9 is GPIO20, not C6 BOOT. GEA3 TX/RX use D6/D7. Shared schematic names refer to appliance direction: `GEA3_RX` is module TX, while `GEA3_TX` is module RX.

- **D4 green:** Wi-Fi connected, C3 GPIO3 / C6 GPIO1
- **D5 red:** manual light, off at startup, C3 GPIO2 / C6 GPIO0
- **D6 yellow:** GEA component bus-connected state, C3 GPIO4 / C6 GPIO2

Yellow indicates connection rather than blinking for each packet. C3 GPIO2 is a strapping pin; its carrier pull-up matters before application startup. Existing pulls and all 14 socket functions remain part of the recovered interface.

## RF selection and service

C6 GPIO3 low enables RF. GPIO14 low selects ceramic/internal; `c6_external_antenna: true` selects external. Attach the correct external antenna before enabling that option. The [local antenna exclusion](../../pcb/rev3c/ANTENNA-REVIEW.md) addresses copper overlap; RF with the socketed module, antenna and final case remains unqualified.

Use each module's BOOT/RESET buttons and native USB for recovery. The shared carrier omits J2/D19. C3/C6 buttons and U.FL connectors require different case geometry; the historical C3-specific case is not a default shared enclosure. Mating height, retention, USB/button access and RF need physical checks.

Disconnect the appliance cable before powered USB, and remove USB before appliance use. Both reviewed modules tie side-header VBUS directly to USB VBUS; carrier diodes do not isolate a USB host. Use module 3V3 only as its output. Do not attach a battery or drive underside power pads within the reviewed budget. PIN1/PIN3 from one appliance are internally selected inputs, not permission for simultaneous appliance/USB sources.

`logger.baud_rate: 0` suppresses application UART logs. Both chips can still emit ROM boot messages on D6 before application setup, reaching existing GEA3 TX even with a GEA2 profile selected. No appliance corruption or field failure is established by this finding. Hardware TX containment is a separately reviewed option and is not implemented here; these sources do not promise silence during reset, download or brownout.
