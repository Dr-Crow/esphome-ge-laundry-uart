# C3/C6 carrier compatibility and Matter options

[Comparison](README.md) · [Validation and decisions](VALIDATION.md) · [Project handoff](HANDOFF.md)

Hardware/firmware update: October 3, 2026. Four shared C3/C6 × GEA2/GEA3
ESPHome profiles were recovered exactly and freshly compiled, including C6
antenna-switch configuration. The public Rev3C baseline remains C3-specific.
The PIN1-only carrier experiment is rejected. Useful shared-interface findings
may inform a replacement retaining both appliance inputs and automatic selection.
No physical module/case/RF qualification or Matter implementation is claimed.
The optional Matter research below retains its October 2 scope and is not a
new platform-support verification.

## Header and recovery findings

Both side-header patterns have 2.54 mm pitch and 15.24 mm between rows.
Modules are nominally 21 × 17.8 mm, with side 5 V, GND and 3V3 positions
aligned. Coordinate agreement does not prove installed height or fit.

| Physical XIAO pin | Carrier use | C3 GPIO | C6 GPIO |
| --- | --- | ---: | ---: |
| D0 / D1 / D2 | Red diagnostic / green Wi-Fi / yellow GEA-connected LEDs | 2 / 3 / 4 | 0 / 1 / 2 |
| D3 | GEA2 TX | 5 | 21 |
| D4 / D5 | Unconnected | 6 / 7 | 22 / 23 |
| D6 | GEA3 TX | 21 | 16 |
| D7 | GEA3 RX | 20 | 17 |
| D8 | Existing pull-up | 8 | 19 |
| D9 | Existing C3 BOOT connection | 9, BOOT | 20, ordinary GPIO |
| D10 | GEA2 RX | 10 | 18 |

Sources: [Seeed C3](https://wiki.seeedstudio.com/XIAO_ESP32C3_Getting_Started/),
[Seeed C6](https://wiki.seeedstudio.com/xiao_esp32c6_getting_started/).
All 14 shared header functions and firmware assignments were independently
compared with exact recovered sources and official module CAD. The red LED
is manual and starts off; yellow reports bus connection, not packet activity.

C6 BOOT is not on its two side-header rows. The recovered shared schematic
removes legacy J2/D19 and uses each module's USB, BOOT and RESET controls.
Different firmware images are required for C3 and C6; a jumper cannot convert
one build into the other. Both ROMs can emit UART text onto GEA3 TX before
application logging stops. Appliance response is untested; optional TX
containment is not implemented.

## Firmware and remaining hardware gates

All four profiles passed config checks and real local builds with ESPHome
2026.9.1, ESP-IDF 5.5.5 and GEA commit
`283ff2b0dfe90a6d14a5417a23176d433be8a5b3`. C6 GPIO3 enables its antenna
switch; GPIO14 selects internal or optional external antenna. GEA2 destination
and ERD examples are not a verified refrigerator configuration.

The reviewed all-layer carrier copper exclusion improves the C6 ceramic antenna
area without qualifying RF. The legacy case is C3-only; no common C3/C6 case
has completed calibration, fit or physical testing. Purchased module revisions,
5 V/3V3 headroom, demand, retention, USB/buttons, thermal and RF remain gates.
Use one external source at a time: side VBUS connects directly to module USB.
Leave UART VCC disconnected and never inject the module's 3V3 output.

## Thread, ESPHome and Matter

Thread supplies an IPv6 mesh network. A border router carries that network
to the LAN. Matter defines device functions, commands and attributes for a
controller/app to use. A Thread router example is not appliance firmware.

ESPHome over Wi-Fi is the current firmware path. Supported C6 configurations
can use [ESPHome OpenThread](https://esphome.io/components/openthread/) for
the network transport while retaining ESPHome's Home Assistant API.
That does not automatically expose Matter device types.

Native Matter would require an application mapping actual GE protocol
features into Matter endpoints, using an SDK such as
[Espressif esp-matter](https://docs.espressif.com/projects/esp-matter/en/latest/esp32c3/introduction.html).
Existing C3 hardware can run Matter over Wi-Fi; C6 adds native Thread radio
support. Reuse protocol logic where practical, then measure flash/RAM and
OTA partition requirements on the actual build. Neither adequacy nor
inadequacy of the modules' 4 MB flash has been established for this application.

## Appliance features and platform support

Matter defines refrigerators/freezers from version 1.2 and ovens from 1.3.
Capabilities depend on implemented optional features and the underlying
appliance; these are not guarantees for every GE model.

| Appliance | Features the standard can represent |
| --- | --- |
| Oven | Separate cavities, supported cooking modes, temperature targets, operating/preheat/cooling status and target-temperature indications |
| Fridge/freezer | Separate compartments, temperature setpoints or cooling levels, optional measured temperatures, supported modes and door-left-open alarms |

Sources: [CSA Matter 1.2](https://csa-iot.org/newsroom/matter-1-2-arrives-with-nine-new-device-types-improvements-across-the-board/),
[CSA Matter 1.3](https://csa-iot.org/newsroom/matter-1-3-specification-released/),
[temperature-controlled cabinet definition](https://github.com/project-chip/connectedhomeip/blob/master/data_model/1.4/device_types/TemperatureControlledCabinet.xml),
[temperature control definition](https://github.com/project-chip/connectedhomeip/blob/master/data_model/1.4/clusters/TemperatureControl.xml),
[refrigerator alarm definition](https://github.com/project-chip/connectedhomeip/blob/master/data_model/1.4/clusters/RefrigeratorAlarm.xml).

Apple Home's [published Matter list](https://support.apple.com/en-us/102135)
does not list ovens or refrigerators. Google's
[published Matter list](https://developers.home.google.com/matter/supported-devices)
does not officially support those types, although it lists washers and
dishwashers. Google separately supports
[ovens](https://developers.home.google.com/cloud-to-cloud/guides/oven) and
[refrigerators](https://developers.home.google.com/cloud-to-cloud/guides/refrigerator)
through cloud integrations. Cloud support does not establish native Matter
support. No physical platform interoperability tests were performed here.

Future app support may expose already-implemented endpoints without changing
the PCB, but firmware updates and testing may still be needed. Actual usable
features are the intersection of GE protocol access, our implementation,
Matter's feature model and the platform's user interface. Preserve appliance
safety restrictions. Do not promise all-platform support or invent remote
commands the appliance does not provide.

## DIY pairing and certification

Personal development can use test credentials. Home Assistant documents
test/beta-device pairing with an uncertified-accessory warning. Apple
documents an Add Anyway path for development accessories. Google's
documented development route requires a matching Developer Console
integration and a developer or field-trial account. Supported device types
and features still determine usefulness after pairing.

Sources: [Home Assistant Matter](https://www.home-assistant.io/integrations/matter/),
[Apple development/OTA guide](https://developer.apple.com/accessories/Apple-Matter-OTA-User-Guide.pdf),
[Google pairing restrictions](https://developers.home.google.com/matter/integration/pair).

Official product certification is separate from developer status and DIY
pairing. A module or SDK's certification does not certify the complete
adapter. Apple directs distributed/sold Matter accessories through CSA
certification, and Google requires certification for its normal consumer
route. Review current program requirements before making distribution or
branding claims: [Apple accessory requirements](https://developer.apple.com/apple-home/),
[Espressif certification guide](https://docs.espressif.com/projects/esp-matter/en/latest/esp32h2/certification.html).

The recommended sequence is a reliable ESPHome adapter first, then a small
Matter proof of concept for one known appliance and named target platform.
Start with useful status readings, confirm app behavior, and add commands
only where GE supports them. Matter is optional and should not delay the
existing hardware revisions.
