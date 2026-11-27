# XIAO firmware for Rev 3K, 3L, 3M and the shared Rev 3C carrier

Read the revision printed on the carrier and the C3 or C6 marking on the removable XIAO. Use the matching row below and select the protocol documented for the exact appliance. **Unplug the appliance cable before attaching USB.** For a first flash, remove the XIAO from the carrier and use the module’s native USB port. The compact carriers are engineering prototypes with open electrical, enclosure and factory checks.

## Choose a profile

The TX and RX numbers below are GPIO numbers from the module’s perspective. The checked-in defaults work with the factory routing on all three compact designs.

| XIAO | Appliance protocol | Profile | Module TX / RX | UART |
| --- | --- | --- | --- | --- |
| ESP32-C3 | GEA2 | [c3-gea2.yaml](c3-gea2.yaml) | GPIO5 / GPIO10 | 19,200 baud, inverted |
| ESP32-C3 | GEA3 | [c3-gea3.yaml](c3-gea3.yaml) | GPIO21 / GPIO20 | 230,400 baud, non-inverted |
| ESP32-C6 | GEA2 | [c6-gea2.yaml](c6-gea2.yaml) | GPIO21 / GPIO18 | 19,200 baud, inverted |
| ESP32-C6 | GEA3 | [c6-gea3.yaml](c6-gea3.yaml) | GPIO16 / GPIO17 | 230,400 baud, non-inverted |

Copy the profile and its [packages directory](packages/) together. Supply `wifi_ssid`, `wifi_password` and `esp_home_ota_pw` in an ignored `secrets.yaml` next to the profile. GEA2 uses D3/D10 and GEA3 uses D6/D7 on the XIAO by default. The schematic names refer to the appliance direction. `GEA3_RX` carries module TX and `GEA3_TX` carries module RX.

The example GEA2 destination is `0x24` with Door and Cycle Complete entities. GEA3 uses `0xC0`. Confirm destination and ERDs for the target model. These ESPHome profiles use Wi-Fi. [GEA2 settings](packages/gea2.yaml) · [GEA3 settings](packages/gea3.yaml)

## Selectors and reset behavior

| Carrier | Default TX routes | Options |
| --- | --- | --- |
| [3K](../../pcb/rev3k/README.md) and [3L](../../pcb/rev3l-placement/README.md) | JP1 1–2 selects D3 for GEA2. JP2 1–2 selects D6 for GEA3. | Most users can leave these as built. Engineering rework on JP2 can move GEA3 TX to D4 to keep UART0 ROM boot text off that line. Change the matching profile’s `gea_tx_gpio` to GPIO6 for C3 or GPIO22 for C6. JP1’s alternative D9 reaches the C3 BOOT strap or C6 GPIO20. Leave JP1 at default for the listed profiles. |
| [3M](../../pcb/rev3m/README.md) | D3 and D6 are fixed in copper. | No JP1 or JP2. Keep the default GPIO settings. Both JP3 and JP4 service links remain. Opening JP4 disconnects outbound GEA3 drive, including normal transmissions. |

The JP2 comments in the GEA3 profiles apply only to boards fitted with that selector. Selection changes are made unpowered by opening the default bridge and verifying continuity before bridging the alternative. A profile change alone cannot move the physical route. For earlier Rev 3C, follow its [carrier documentation](../../pcb/rev3c/README.md).

`logger.baud_rate: 0` silences application UART logs. With default routing, ROM messages can still reach the GEA3 transmit circuit during reset, download or brownout, even when GEA2 firmware is loaded. Check the connector during these transitions for each XIAO.

## What the service connections tell you

On 3K and 3L, J7 is a 3.3 V listen-only tap. Pin 1 is local ground. Pin 2 is module-side GEA2 receive, pin 3 is module-side GEA3 receive and pin 4 is module-side GEA3 transmit. Each signal has a 1 kΩ series resistor. Use an isolated receiver on a qualified bench fixture and leave its TX and power leads disconnected. A clean J7.4 trace confirms the module’s UART output upstream of U5. Check the cable waveform separately at J1.5. The 3M omits J7 and all dedicated probe lands. [3L pad map](../../pcb/rev3l-placement/evidence/debug-pad-map.csv) · [3M service lands](../../pcb/rev3m/evidence/existing-service-lands.csv)

For GEA3 fixture qualification, compare the following traces with the actual UART supply, load and cable. Record valid frames and CRC errors alongside the measurements.

- **Appliance to module, J1.4.** U4 requires a guaranteed high of 0.7 × its supply in the 4.5–5.5 V operating range. At a 5.0 V U4 supply, a 3.3 V push-pull high falls below the 3.5 V guarantee. Measure at U4 pin 3 with the intended source. [Diodes 74LVC2G07 datasheet, page 3](https://www.diodes.com/datasheet/download/74LVC2G07.pdf#page=3)
- **Module to appliance, J1.5.** U5 drives open drain through JP4 and R24 (1 kΩ), with a 10 kΩ pull-up at R20. At 230,400 baud the nominal mid-bit is 2.17 µs. As an example, 200 pF at J1.5 with no remote pull-up takes about 2.65 µs to rise from zero to 70%. Check the representative receiver’s threshold and cable loading before changing R20. Opening JP4 leaves the connector-side pull-up in circuit. [3M schematic](../../pcb/rev3m/design/GEA-Adapter-Rev3M.kicad_sch)
- **Carrier unpowered.** JP3 opens the buck feed. U11’s upper steering diodes still connect the appliance data lines to the downstream +5 V rail. On a current-limited isolated fixture, measure rail rise and signal current with the carrier supply off. The module header and USB port share power/ground paths that require separate C3 and C6 backfeed testing. Leave protective parts in circuit. [ProTek SRV05-4](https://protekdevices.com/products/series-details/?id=5150)

## Status indicators and RF

| LED reference | Indication | C3 / C6 GPIO |
| --- | --- | --- |
| D4 green | Wi-Fi connected | GPIO3 / GPIO1 |
| D5 red | User-controlled, initialized off | GPIO2 / GPIO0 |
| D6 yellow | GEA bus-connected state, checked once per second | GPIO4 / GPIO2 |

D4 through D6 here are LED component references. C3 GPIO2 is a strap with a carrier pull-up. C6 GPIO3 low enables RF. GPIO14 low selects the ceramic antenna. Set `c6_external_antenna: true` only with the appropriate external antenna attached. Verify the module’s mating height, antenna clearance, button access and RF performance with the matching lid. Use module 3V3 only as its output. [Shared RF settings](packages/c6-rf.yaml) · [Original Rev 3C power qualification](../../pcb/rev3c/POWER-QUALIFICATION.md)

## Build provenance

The shared profiles pin ESP-IDF **5.5.5** and GEA **`95cf5a6fa4b006b25533a4ce7a95cad749a740d4`**. Repository CI pins ESPHome **2026.9.1**. The GEA update commit reports successful configuration of all four shared profiles and successful compilation of all eight repository profiles. Earlier build evidence at GEA `283ff2b` predates this update. This documentation review checked the four YAML inputs and the upstream diagnostic getters. For fresh configuration, compile and binary-hash receipts, run the repository’s `python3 ci/validate.py firmware` in its pinned ESPHome environment. Appliance behavior and electrical margins require bench evidence. [GEA update and reported builds](https://github.com/Dr-Crow/esphome-ge-laundry-uart/commit/d611c4c4d93f71b63aa0e8d5e62a29f8d715a107) · [Pinned GEA sources](https://github.com/mguaylam/esphome-gea/tree/95cf5a6fa4b006b25533a4ce7a95cad749a740d4) · [Repository CI](../../.circleci/config.yml)
