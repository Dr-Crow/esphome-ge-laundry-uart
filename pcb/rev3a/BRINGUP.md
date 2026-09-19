# Revision 3A prototype bring-up

This procedure is for the first assembled Rev3A boards. It is a bench test plan,
not permission to connect untested hardware to an appliance.

Do not connect a GE appliance until the unpowered checks, USB checks, all eight
steady-state power combinations, and both dynamic handoff directions pass with
current-limited bench sources.

## Equipment

- one current-limited bench supply, or two isolated channels for dual-input tests;
- digital multimeter with resistance, voltage, and current modes;
- oscilloscope with appropriate probes for startup and handoff observations;
- USB-C data cable and a computer with ESPHome or `esptool`;
- magnification and good lighting; and
- an independently checked J1 breakout fixture.

Use insulated probes and remove power before changing connections. Do not inject a
surge or reversed supply without a separately reviewed fixture and test plan.

## Record the board

| Field | Result |
| --- | --- |
| Board identifier | |
| PCB revision | Revision 3A |
| Assembly supplier and lot | |
| J1 breakout fixture and verified pin map | |
| Supply channels and current limits | |
| Target appliance model | |
| Firmware image and commit | |
| Inspector and date | |

## Visual and unpowered checks

1. Compare connector orientation, polarized-part markings, and DNP items with the
   schematic and assembly drawing.
2. Confirm D18 is an SMF16A in the documented orientation, R38 is 220 kohm, and no
   part has been silently substituted.
3. Look for solder bridges, tombstoned parts, bent connector pins, or debris near
   the ESP32 antenna.
4. With every source disconnected, record resistance from `+3V3`, `+5V`,
   `V_INPUT`, `USB_VBUS`, `PIN1_PROTECTED`, and `PIN3_PROTECTED` to ground.
5. Stop for a hard short or a result materially different from the other boards.

## USB-only test

1. Leave J1 disconnected and connect USB-C through a current-monitored source where
   practical.
2. Measure `USB_VBUS`, `+5V`, and `+3V3`.
3. Confirm no USB-derived voltage or current reaches J1 pins 1 or 3.
4. Confirm USB enumeration, flash firmware, reset, and repeat at least ten times.
5. Run sustained logging while generating Wi-Fi traffic. Record disconnects,
   resets, host warnings, current, and rail voltage.
6. Disconnect USB and confirm `USB_VBUS` falls below 0.8 V within one second. This
   is the Rev3A prototype acceptance target for the R38 discharge path, not a claim
   of USB certification.

## Recovery flashing through J2

J2 is a top-side 2-by-3 header. Open the enclosure and use a reputable 3.3 V logic
USB-to-UART adapter with female Dupont leads. Never use RS-232 or 5 V UART logic.

Viewed from the top with `J2 RECOVERY` below the header:

| J2 pin | Signal | Connection |
| ---: | --- | --- |
| 1 | `+3V3` | Optional regulated 3.3 V input with every other source disconnected |
| 2 | `GND` | Adapter ground |
| 3 | GPIO9 / `BOOT` | Hold low during reset for download mode |
| 4 | GPIO21 / UART0 TX | Adapter RX |
| 5 | GPIO20 / UART0 RX | Adapter TX |
| 6 | `EN` | Pull low briefly to reset |

Connect ground and crossed UART signals. Power the board from one approved source;
use J2 pin 1 only with every other source disconnected. Hold BOOT low, pulse EN low,
release EN, then release BOOT after the downloader starts. Disconnect all recovery
leads before closing the enclosure or connecting J1.

## Appliance-input bench tests

Use the measured supply voltage for the target appliance family. Start with a low
current limit and increase it only while observing current, rail voltage, and
temperature. Apply power through J1 so the resettable fuse remains in circuit.

### Pin 1 only

Apply power to J1 pin 1. Record `PIN1_FUSED`, `PIN1_PROTECTED`, `PIN1_SW_OUT`,
`V_INPUT`, `+5V`, and `+3V3`. Confirm the pin-3 path remains unpowered and the
board boots normally.

### Pin 3 only

Repeat through J1 pin 3. Confirm the pin-1 path remains unpowered.

### Both inputs and dynamic handoff

Use two isolated channels with a common ground at the fixture.

1. Start with pin 3 active, then apply pin 1. Confirm pin 1 takes priority, `V_INPUT`
   remains within the recorded operating band, and no reverse-current spike appears
   at pin 3.
2. With both inputs present, remove pin 1. Confirm pin 3 takes over without an
   unsafe rail excursion, reset, or reverse-current spike.
3. Repeat each transition at least ten times while monitoring `V_INPUT`, `+5V`, and
   both source currents with the oscilloscope/current measurement setup.

Do not deliberately reverse or over-voltage an input during first bring-up.

## Eight-state power matrix

Record startup, steady-state current, rail voltage, temperature, and any backfeed
for every row.

| Test | Pin 1 | Pin 3 | USB | Expected behavior | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | absent | absent | absent | Board remains off | |
| 2 | present | absent | absent | Pin 1 powers `V_INPUT` | |
| 3 | absent | present | absent | Pin 3 powers `V_INPUT` | |
| 4 | present | present | absent | Pin 1 has priority; pin 3 is isolated | |
| 5 | absent | absent | present | USB powers only the board | |
| 6 | present | absent | present | Pin 1 and USB coexist without backfeed | |
| 7 | absent | present | present | Pin 3 and USB coexist without backfeed | |
| 8 | present | present | present | Pin 1 priority; pin 3 and USB remain isolated | |

For rows 6-8, monitor `USB_VBUS` and the USB-source current. Disconnect USB while
appliance power remains present and confirm VBUS falls below 0.8 V within one second.
Reconnect USB and confirm VBUS returns to the host-supplied value without a voltage
or current excursion toward the host. Disconnect appliance power while USB remains
present and confirm the board stays stable.

## D18 and input-transient qualification

Before an appliance connection, verify from the exact manufacturer data that D18's
stand-off voltage exceeds every valid steady-state condition. During current-limited
fixture testing, capture `PIN1_PROTECTED` and `V_INPUT` at power application,
removal, and dynamic handoff. Record peak voltage, pulse duration, ringing, and D18
temperature.

Do not claim surge immunity from these observations alone. If recorded peaks
approach the TVS stand-off or clamp region, or if the part warms during valid
operation, stop and review the protection design before proceeding.

## Appliance-connection gate

Proceed only after:

- all eight matrix rows and both dynamic handoff directions pass on two boards;
- no unintended voltage or reverse current is measured at an inactive input;
- USB VBUS decay and appliance-to-host no-backfeed checks pass;
- the measured appliance voltage leaves sufficient AP63205 headroom;
- D18's selection is consistent with the measured input and transient envelope;
- `+5V` and `+3V3` remain stable under flashing, logging, and Wi-Fi load; and
- a second person has reviewed the measurements.

Keep USB disconnected for the first appliance-only test. Test appliance plus USB
only after appliance-only operation passes.

## Stop conditions

Remove power immediately if a supply enters current limiting unexpectedly, a rail
collapses or exceeds its intended value, either appliance input is driven by another
source, appliance voltage appears on disconnected USB VBUS, USB reports over-current,
the ESP32 resets repeatedly, or any part rapidly heats, discolors, smokes, or smells.

## Results summary

| Item | Measurement or observation | Reviewed | Notes |
| --- | --- | --- | --- |
| Unpowered checks | | | |
| USB-only power and repeated flashing | | | |
| J2 recovery flashing | | | |
| Pin 1 only | | | |
| Pin 3 only | | | |
| Pin 3 to pin 1 handoff | | | |
| Pin 1 removal / pin 3 takeover | | | |
| USB plus appliance sources | | | |
| USB VBUS decay and no-backfeed | | | |
| D18 transient observations | | | |
| Rail stability and temperature | | | |
| Enclosed Wi-Fi performance | | | |
| Appliance-only test | | | |
| Appliance plus USB test | | | |
