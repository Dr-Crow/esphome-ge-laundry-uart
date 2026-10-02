# C3/C6 carrier compatibility and Matter options

[Comparison](README.md) · [Project handoff](HANDOFF.md)

Research snapshot: October 2, 2026. No C6 carrier or Matter firmware has been
implemented. A shared carrier is a proposal; the published Rev3C remains
specified for the pre-headered XIAO ESP32-C3.

## Header pattern

The Rev3C carrier and Seeed's official C6 PCB use two seven-pin rows with
2.54 mm pitch and 15.24 mm between row centers. Both modules are nominally
21 × 17.8 mm, with 5 V, ground and 3.3 V in the same side-header positions.
This is a PCB-coordinate check, not confirmation of installed height or fit.

| Physical XIAO pin | Current carrier use | C3 GPIO | C6 GPIO |
| --- | --- | ---: | ---: |
| D0 / D1 / D2 | Three status LEDs | 2 / 3 / 4 | 0 / 1 / 2 |
| D3 | GEA2 transmit | 5 | 21 |
| D4 / D5 | Unconnected | 6 / 7 | 22 / 23 |
| D6 | GEA3 transmit and recovery TX | 21 | 16 |
| D7 | GEA3 receive and recovery RX | 20 | 17 |
| D8 | C3 strapping pull-up | 8 | 19 |
| D9 | C3 BOOT connection | 9, BOOT | 20, ordinary GPIO |
| D10 | GEA2 receive | 10 | 18 |

Sources: [Seeed C3 pin map](https://wiki.seeedstudio.com/XIAO_ESP32C3_Getting_Started/),
[Seeed C6 pin map and PCB download](https://wiki.seeedstudio.com/xiao_esp32c6_getting_started/).
Carrier connections were read from Rev3C source at `38d94d3`.

## Shared-carrier proposal

Most signal differences can be handled by separate C3 and C6 firmware
configurations. A jumper does not make one compiled firmware image run on
both chips. No processor-selector jumper has been implemented or shown to
be necessary for normal operation.

The recovery exception needs explicit handling: C3 brings BOOT to D9;
C6's actual GPIO9 BOOT signal is not on its two seven-pin side headers.
A jumper among those header pins cannot reach C6 BOOT. The inexpensive
proposal is to retain J2 UART/power access, use the C6 module's own BOOT and
RESET buttons, and label or isolate the C3-only J2 BOOT connection as needed.
Review the real ROM UART pins and complete boot sequence before acceptance.

Remaining work: review every pin and startup pull resistor; verify 5 V/3.3 V
power and regulator headroom; preserve the single-source restriction until
a different circuit is verified; adapt USB/button/antenna case access;
compile both configurations; and test actual modules. C6's antenna switch
uses onboard GPIO3 and GPIO14 and needs firmware configuration.

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
