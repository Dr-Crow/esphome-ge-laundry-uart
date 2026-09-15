# Revision 3A prototype bring-up

This procedure is for the first assembled Revision 3A boards. It is a bench test
plan, not permission to connect an untested board to an appliance.

Status: drafted procedure for a future populated prototype. Do not assemble, order,
or connect an appliance until routing, schematic/PCB parity, ERC/DRC, footprint, and
vendor-preview gates pass.

Do not connect a GE appliance until the unpowered checks, USB checks, and all eight
power-source combinations pass with current-limited bench sources.

## Equipment

- current-limited bench supply, or two isolated channels for the dual-input tests;
- digital multimeter with resistance and DC-voltage modes;
- USB-C data cable and a computer with ESPHome or `esptool` installed;
- magnification and good lighting; and
- an approved RJ45 breakout fixture for applying power to J1 pins 1 and 3.

Use insulated probes. Remove power before changing connections. Do not apply power
directly to an after-fuse test pad when validating the complete input path; use the
J1 breakout so the corresponding fuse remains in circuit.

## Required labelled test pads

The release PCB should expose top-side pads for:

- `GND`;
- `PIN1_FUSED` and `PIN3_FUSED`;
- `PIN1_PROTECTED` and `PIN3_PROTECTED`;
- `PIN1_SW_OUT` and `PIN3_SW_OUT`;
- `V_INPUT`;
- `USB_VBUS`;
- `+5V`; and
- `+3V3`.

At minimum, the two fused inputs, `V_INPUT`, `USB_VBUS`, `+5V`, `+3V3`, and a
nearby ground pad are release requirements. The remaining pads make voltage-drop,
priority, and reverse-current failures much easier to isolate.

## Record the board

| Field | Result |
| --- | --- |
| Board identifier | |
| PCB revision | Revision 3A |
| ESP32 module marking | |
| Assembly supplier and lot | |
| RJ45 breakout fixture and revision | |
| Fixture pin map | |
| Supply channel identifiers and limits | |
| Target appliance model | |
| Firmware image and commit | |
| Inspector and date | |

## Visual and unpowered checks

1. Compare connector orientation, component markings, and do-not-install parts with
   the assembly drawing.
2. Look for solder bridges, missing or rotated diodes, tombstoned parts, and damage.
3. Confirm the ESP32 antenna area has no added metal or assembly debris.
4. With every source disconnected, record resistance from `+3V3`, `+5V`,
   `V_INPUT`, and `USB_VBUS` to `GND`, and between `PIN1_FUSED` and
   `PIN3_FUSED`.
5. Stop for a hard short or a reading materially different from the other boards in
   the batch.

Fixed resistance limits are intentionally deferred: capacitors and semiconductor
junctions make a single ohmic limit unreliable. Establish limits from reviewed
measurements on the first known-good boards.

## USB-only test

1. Leave J1 disconnected and attach USB-C through a current-monitored source where
   practical.
2. Measure `USB_VBUS`, `+5V`, and `+3V3` relative to `GND`.
3. Confirm no USB-derived voltage reaches J1 pins 1 or 3, `PIN1_FUSED`, or
   `PIN3_FUSED`.
4. Confirm the ESP32-C3 enumerates, flash the approved firmware, reset it, and repeat
   the enumeration and boot test.
5. Record idle and Wi-Fi-active current and rail voltage.

## Recovery flashing when USB is unavailable

J3 is a top-side Tag-Connect recovery footprint and does not require a connector to
be installed on every board. Open the enclosure to reach it; the current case has
no external service opening. Use a TC2030-compatible cable or pogo fixture and a
3.3 V USB-to-UART adapter. Never use 5 V UART or RS-232 signalling.

| J3 pin | Board signal | Recovery connection |
| ---: | --- | --- |
| 1 | `EN` | Pull low briefly, then release, to reset |
| 2 | `+3V3` | Optional regulated 3.3 V input with all other sources disconnected |
| 3 | ESP32 GPIO21 / UART0 TX | USB-to-UART adapter RX |
| 4 | `GND` | USB-to-UART adapter ground |
| 5 | ESP32 GPIO20 / UART0 RX | USB-to-UART adapter TX |
| 6 | ESP32 GPIO9 / `BOOT` | Hold low while resetting to enter download mode |

R1 holds GPIO8 high for valid ESP32-C3 download mode. With appliance power and USB
disconnected, connect the adapter ground and crossed UART signals. Power the board
from one approved source; use J3 pin 2 only when supplying a current-limited,
regulated 3.3 V rail directly. For the normal button sequence, hold SW2 (`BOOT`),
tap and release SW1 (`RESET`), then release SW2 after the ROM downloader starts. A
pogo fixture can instead hold J3 pin 6 low while pulsing J3 pin 1 low. Flash with
`esptool` over the adapter's serial port. Stop if the 3.3 V rail, regulator, ESP32,
or UART pads are physically damaged; a recovery connector cannot bypass those
failures.

## USB and Wi-Fi reliability

1. Repeat USB enumeration, flashing, reset, and reconnect at least ten times with
   appliance power absent.
2. Run sustained serial logging while the ESP32 transmits Wi-Fi traffic; record any
   USB disconnect, packet error, reset, or host warning.
3. Install the board in the intended enclosure with at least 15 mm of clear space
   beyond the overhanging antenna edge. Keep metal, wiring, fasteners, and enclosure
   ribs out of that volume.
4. Measure Wi-Fi throughput and usable range both away from the appliance and in the
   final mounting position next to the appliance chassis. Compare at least two boards.

Do not approve the four-layer USB/RF layout if USB errors appear under Wi-Fi load or
if the installed enclosure materially degrades range or connection stability.

Stop for unexpected current limiting, a host over-current warning, rapid heating,
or any voltage driven toward an appliance pin.

## Appliance-input bench tests

Set each isolated, current-limited channel to the measured supply voltage for the
target appliance family. Do not assume all GE appliances provide the same voltage.
Start with the lowest practical current limit and increase it only while monitoring
current, rail voltage, and temperature. Normal limits remain characterization data
until prototypes have been measured.

### Pin 1 only

1. Apply the bench source through the RJ45 fixture to J1 pin 1 and `GND`.
2. Leave J1 pin 3 and USB disconnected.
3. Measure `PIN1_FUSED`, `PIN1_PROTECTED`, `PIN1_SW_OUT`, `V_INPUT`, `+5V`,
   and `+3V3`.
4. Confirm the pin 3 path remains unpowered and the board boots normally.

### Pin 3 only

Repeat the procedure through J1 pin 3. Confirm the pin 1 path remains unpowered.

### Both appliance inputs

Use two isolated supply channels with a common ground at the fixture. Apply both
approved input voltages. A passing result requires measured pin-1 priority, no reverse
voltage or current into pin 3, stable board rails, and no unsafe temperature rise as
each input is removed in turn.

Do not deliberately reverse or over-voltage an input during first bring-up. Those
tests require a separately reviewed fixture and limit.

## Eight-state power matrix

“Present” means an approved current-limited source at the characterized input
voltage. Record startup, steady-state current, rail voltage, temperature, and any
backfeed for every row.

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

For rows 6–8, measure `USB_VBUS` while appliance power is present. No
appliance-derived voltage may appear on USB VBUS. Measure both fused appliance inputs
while the other sources are present to detect unintended reverse current.

## Appliance-connection gate

Proceed to the first appliance only after:

- all eight matrix rows have recorded results;
- no unintended backfeed has been observed;
- `+5V` and `+3V3` remain stable under USB flashing and Wi-Fi load;
- USB enumeration and flashing are repeatable;
- the measured appliance voltage leaves sufficient AP63205 regulator headroom;
- component temperatures remain within reviewed limits; and
- a second person has reviewed the measurements.

Keep USB disconnected for the first appliance-only test. Connect USB while the
appliance is attached only after appliance-only operation passes.

## Stop conditions

Remove power immediately if a supply unexpectedly enters current limiting, a rail
collapses or rises above its intended value, either input is driven by another
source, appliance voltage appears on USB VBUS, USB reports over-current, the board
resets repeatedly, or any part becomes rapidly hot, discoloured, or produces smoke
or odor. Record and inspect a failure before trying it again.

## Results summary

| Item | Measurement or observation | Reviewed | Notes |
| --- | --- | --- | --- |
| Unpowered resistance checks | | | |
| USB-only power and current | | | |
| USB enumeration and flashing | | | |
| Pin 1 only | | | |
| Pin 3 only | | | |
| Both appliance inputs | | | |
| USB plus pin 1 | | | |
| USB plus pin 3 | | | |
| USB plus both inputs | | | |
| Reverse-current checks | | | |
| Rail stability under Wi-Fi load | | | |
| USB reliability under Wi-Fi traffic | | | |
| Enclosed Wi-Fi throughput and range | | | |
| Temperature observations | | | |
| Appliance-only test | | | |
| Appliance plus USB test | | | |
