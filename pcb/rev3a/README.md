# Revision 3A PCB

Revision 3A is an unqualified prototype ESP32-C3 adapter for the low-voltage
GEA serial bus used by compatible GE appliances. Its J1 8P8C connector is not
Ethernet. It retains the ESP32-C3-WROOM-02 from Revision 2.x and adds native
USB-C, automatic appliance-power selection, a switching 5 V supply, a stronger
3.3 V rail, separate RESET and BOOT controls, and a permanent recovery header.

> [!WARNING]
> No assembled Rev3A board has completed electrical or appliance testing. Do
> not connect an unqualified board to an appliance. Follow the complete
> [bench bring-up procedure](#prototype-bring-up) and [release gates](#release-and-appliance-connection-gates).

![Revision 3A populated-board render](images/3d-top.png)

## Navigation

- [What changed](#what-changed-from-revision-22)
- [Board map and normal use](#board-map-and-normal-use)
- [Power architecture and design rationale](#power-architecture-and-design-rationale)
- [Engineering and manufacturing status](#engineering-and-manufacturing-status)
- [Prototype bring-up](#prototype-bring-up)
- [Release and appliance-connection gates](#release-and-appliance-connection-gates)
- [Package map](#package-map)

## What changed from Revision 2.2

| Area | Revision 2.2 | Revision 3A |
| --- | --- | --- |
| ESP32 | ESP32-C3-WROOM-02 | Same module and built-in antenna |
| Programming | External programming connection | USB-C native USB plus J2 recovery header |
| Appliance power | One fixed appliance-power pin | Automatic pin 1 / pin 3 selection with pin-1 priority |
| 5 V supply | L7805 linear regulator | AP63205 switching regulator |
| 3.3 V supply | AP2205, 200 mA | AP2112K, up to 600 mA |
| USB and appliance power | Not intended for simultaneous use | Diode-isolated paths, pending prototype verification |
| Board | 88.7 x 30.1 mm, two layers | 88.7 x 40.0 mm, four layers |

## Board map and normal use

The appliance connector is on the left, USB-C is along the lower edge, and the
ESP32 antenna overhangs the right edge. Keep at least 15 mm beyond that edge
clear of metal, wiring, fasteners, and enclosure ribs.

| Marking | Function | Normal use |
| --- | --- | --- |
| `J1` | Appliance 8P8C connector | Power and GEA serial bus only after qualification |
| `J4` | USB-C | Normal flashing, logging, and bench power |
| `J2 RECOVERY` | 2-by-3 recovery header | Backup 3.3 V UART flashing with enclosure open |
| `SW1 RESET` | Reset button | Restart the ESP32-C3 |
| `SW2 BOOT` | Boot-mode button | Hold during reset for ROM downloader |
| `D4` green | Wi-Fi status | Firmware-controlled Wi-Fi-connected indication |
| `D5` red | Diagnostic | User-controlled diagnostic indication |
| `D6` yellow | GEA status | Firmware-controlled appliance-bus indication |

### Normal flashing

Leave J1 disconnected for initial bench work. Connect J4 with a USB-C data
cable and flash over native USB. If automatic download mode does not start,
hold `SW2 BOOT`, tap and release `SW1 RESET`, then release BOOT after the
downloader starts.

### Recovery flashing

J2 is a backup for an unavailable USB data path. Use only a 3.3 V logic
USB-to-UART adapter and female Dupont leads: never use RS-232 or 5 V logic.
The matching enclosure keeps J2 inside the case; remove the lid before attaching
leads and disconnect them before closing the enclosure or connecting J1.

## Power architecture and design rationale

No user jumper is required. Each appliance input has its own resettable fuse,
CJ3407 PMOS reverse-current blocking stage, and TPS22810 controlled load switch.
The switched outputs feed `V_INPUT` through Schottky diodes, while a transistor
network gives pin 1 priority when both inputs are present. USB-C VBUS is fused
and diode-isolated before joining the 5 V rail:

```text
J1 pin 1 -> fuse -> reverse-current block -> load switch -> diode --+
                                                                  +-> V_INPUT -> AP63205 -> +5V
J1 pin 3 -> fuse -> reverse-current block -> load switch -> diode --+

USB-C VBUS -> fuse -> diode -----------------------------------------> +5V
```

Q3/Q4 and the CJ3407 stages are intended to limit reverse current and source-
to-source backfeed. They are not claimed to protect against a physically
reversed connector supply. All source combinations and handoffs require
current-limited bench supplies and an independently checked J1 breakout.

The FirstBuild schematic labels its downstream `V_INPUT` rail as 4.3–15 V.
That is neither a measured Rev3A appliance-input range nor a design guarantee;
the AP63205 cannot regulate 5 V from a 4.3 V input. Minimum appliance voltage,
path drop, regulator headroom, and transient environment must be measured.

### Transient protection

D18 is a populated unidirectional SUNMATE SMF16A TVS (`C399290`) from
`PIN1_PROTECTED` to ground in the SOD-123FL footprint. This follows the single-
TVS position in the published FirstBuild reference design. Population is not
qualification: verify polarity and exact part, measure steady-state maximum and
connection/removal transients, and confirm that D18 neither conducts during
valid operation nor permits an unsafe peak. Do not improvise a surge-generator
test; it requires a separately reviewed fixture and test plan.

### USB, regulators, and layout rationale

The AP63205 replaces the Rev2 linear 5 V stage to reduce heat and improve
efficiency. AP2112K-3.3 replaces the 200 mA AP2205 for more Wi-Fi peak-current
headroom. Regulator temperature, startup, and rail stability remain hardware
tests.

USB-C uses the ESP32-C3 native USB interface with USBLC6-2SC6 ESD protection.
R38 (220 kohm to ground) discharges `USB_VBUS`; no controlled-impedance claim
is made. The four-layer stack was chosen because a two-layer trial fragmented
the ground return and left USB without a defensible continuous reference:

| Layer | Function |
| --- | --- |
| `F.Cu` | Components, local power, and signal routing |
| `In1.Cu` | Continuous ground-reference plane |
| `In2.Cu` | Ground plane with one short D18 signal branch |
| `B.Cu` | Signal routing and short USB/feedback transitions |

The D18 branch uses two standard through-vias and a short `In2.Cu` trace.
Native USB remains referenced to continuous `In1.Cu`. All fitted components are
top-side; routed vias use 0.40 mm drills and the ESP32 thermal pad uses a
0.30 mm minimum plated drill. There are no blind/buried or filled vias,
controlled-depth drilling, via-in-pad requirements, or bottom-side placements.

## Engineering and manufacturing status

- KiCad 9.0.9 ERC: zero errors and 53 reviewed warnings.
- KiCad 9.0.9 DRC: zero errors, zero unconnected items, zero schematic-parity
  findings, and seven reviewed warnings.
- Manufacturing package: 40 purchasing groups and 93 fitted top-side placements.
- Board: four copper layers, 1.6 mm target thickness, 0.20 mm minimum routed
  track, ordinary 0.8/0.4 mm through-vias, and no bottom assembly.
- Key parts include J1 EVERCOM 5301-8P8C (`C3097717`), J2 recovery header
  (`C42391552`), J4 SHOU HAN USB-C (`C2765186`), D18 SMF16A (`C399290`), and
  R38 RALEC 220 kohm (`C104108`).

Supplier stock and assembly classifications change. A quote-time substitution
is unacceptable unless package, pinout, voltage/current ratings, temperature
range, and manufacturer data are reviewed. The September 19, 2026 planning
quote accepted five assembled boards, 40 BOM groups, and 93 placements at
$149.96 before shipping and tax ($29.99 each); refresh it before purchase.

These checks establish file consistency, not electrical safety or appliance
compatibility. The [validation package](validation/README.md) describes the
review artifacts and summarized warning dispositions; source files are
authoritative and generated artifacts must be regenerated after source changes.

## Prototype bring-up

This is a bench test plan, not permission to connect untested hardware. Do not
connect a GE appliance until the unpowered checks, USB checks, all eight
steady-state source combinations, and both dynamic handoff directions pass with
current-limited bench sources.

### Equipment and record

Use one current-limited supply or two isolated channels, a multimeter, an
oscilloscope, a USB-C data cable and ESPHome/`esptool`, magnification, and an
independently checked J1 breakout fixture. Use insulated probes and remove power
before changing connections. Never inject a surge or reversed supply without a
reviewed fixture and test plan.

Record board identifier, PCB revision, assembly supplier/lot, verified J1
fixture pin map, supply channels/current limits, target appliance, firmware
image/commit, inspector, and date.

### Visual and unpowered checks

1. Compare connector orientation, polarized markings, and DNP items with the
   schematic and assembly drawing.
2. Confirm D18 is SMF16A in the documented orientation, R38 is 220 kohm, and no
   part was silently substituted.
3. Inspect for bridges, tombstones, bent connector pins, and antenna debris.
4. With every source disconnected, measure resistance from `+3V3`, `+5V`,
   `V_INPUT`, `USB_VBUS`, `PIN1_PROTECTED`, and `PIN3_PROTECTED` to ground.
5. Stop for a hard short or a result materially different from other boards.

### USB-only test

With J1 disconnected, measure `USB_VBUS`, `+5V`, and `+3V3`; confirm no USB
voltage/current reaches J1 pins 1 or 3. Confirm enumeration, flashing, reset,
and at least ten repeated reconnect/download cycles. Run sustained logging with
Wi-Fi traffic and record disconnects, resets, host warnings, current, and rail
voltage. After USB removal, verify `USB_VBUS` falls below 0.8 V within one
second. This is the prototype R38 acceptance target, not a USB certification.

### Recovery flashing through J2

Viewed from the top with `J2 RECOVERY` below the header:

| Pin | Signal | Connection |
| ---: | --- | --- |
| 1 | `+3V3` | Optional regulated 3.3 V input with every other source disconnected |
| 2 | `GND` | Adapter ground |
| 3 | GPIO9 / `BOOT` | Hold low during download reset |
| 4 | GPIO21 / UART0 TX | Adapter RX |
| 5 | GPIO20 / UART0 RX | Adapter TX |
| 6 | `EN` | Pull low briefly to reset |

Connect ground and crossed UART signals. Power from one approved source; use J2
pin 1 only with every other source disconnected. Hold BOOT low, pulse EN low,
release EN, then release BOOT after the downloader starts. Disconnect all leads
before closing the enclosure or connecting J1.

### Appliance-input tests and eight-state matrix

Use the measured target-appliance voltage, start with a low current limit, and
increase only while observing current, rails, and temperature. Apply power
through J1 so the resettable fuse remains in circuit. Test pin 1 only and pin 3
only, recording `PIN*_FUSED`, `PIN*_PROTECTED`, `PIN*_SW_OUT`, `V_INPUT`, `+5V`,
and `+3V3`; the inactive path must remain unpowered.

With two isolated channels and common fixture ground, start pin 3 then apply pin
1: pin 1 must take priority without pin-3 reverse-current spike. Remove pin 1:
pin 3 must take over without unsafe rail excursion, reset, or reverse current.
Repeat each transition at least ten times while monitoring both source currents.
Do not deliberately reverse or over-voltage an input during first bring-up.

| Test | Pin 1 | Pin 3 | USB | Expected behavior |
| --- | --- | --- | --- | --- |
| 1 | absent | absent | absent | Board remains off |
| 2 | present | absent | absent | Pin 1 powers `V_INPUT` |
| 3 | absent | present | absent | Pin 3 powers `V_INPUT` |
| 4 | present | present | absent | Pin 1 priority; pin 3 isolated |
| 5 | absent | absent | present | USB powers only the board |
| 6 | present | absent | present | Pin 1 and USB coexist without backfeed |
| 7 | absent | present | present | Pin 3 and USB coexist without backfeed |
| 8 | present | present | present | Pin 1 priority; pin 3 and USB isolated |

For rows 6–8, monitor `USB_VBUS` and host current. Remove USB with appliance
power present and verify VBUS decay below 0.8 V in one second; reconnect without
host-directed excursion. Remove appliance power with USB present and confirm
stability.

### D18, stop conditions, and results

Verify D18 stand-off exceeds every valid steady-state condition. Capture
`PIN1_PROTECTED` and `V_INPUT` at application, removal, and handoff; record peak,
pulse duration, ringing, and D18 temperature. Stop if peaks approach stand-off
or clamp regions or the part warms during valid operation.

Remove power immediately for unexpected current limiting, collapsed or excessive
rails, inactive-input drive, appliance voltage on USB VBUS, USB over-current,
repeated resets, rapid heating, discoloration, smoke, or smell. Record results
for unpowered checks, USB/recovery, each source state and handoff, VBUS decay,
D18 transients, rail/temperature stability, enclosed Wi-Fi, appliance-only,
and appliance-plus-USB tests. A second person must review the recorded
measurements before the board is connected to an appliance.

| Item | Measurement or observation | Reviewed | Notes |
| --- | --- | --- | --- |
| Unpowered checks |  |  |  |
| USB-only power and repeated flashing |  |  |  |
| J2 recovery flashing |  |  |  |
| Pin 1 only |  |  |  |
| Pin 3 only |  |  |  |
| Pin 3 to pin 1 handoff |  |  |  |
| Pin 1 removal / pin 3 takeover |  |  |  |
| USB plus appliance sources |  |  |  |
| USB VBUS decay and no-backfeed |  |  |  |
| D18 transient observations |  |  |  |
| Rail stability and temperature |  |  |  |
| Enclosed Wi-Fi performance |  |  |  |
| Appliance-only test |  |  |  |
| Appliance plus USB test |  |  |  |

## Release and appliance-connection gates

Before ordering more than a small prototype batch or connecting an appliance:

1. Complete independent schematic, layout, BOM, and mechanical reviews.
2. Review fabricator board, drill, part-selection, and placement previews.
3. Measure actual appliance supply range and AP63205 headroom.
4. Pass all eight matrix states and both dynamic handoffs without dropout,
   cross-feed, or unsafe heating on at least two boards.
5. Pass USB VBUS decay and appliance-to-USB no-backfeed tests.
6. Qualify D18 against measured steady-state/transient conditions or revise it.
7. Pass USB enumeration/flashing, sustained logging, Wi-Fi load, enclosure fit,
   connector access, and antenna-performance tests on at least two boards.

Keep USB disconnected for the first appliance-only test; test appliance plus USB
only after appliance-only operation passes. Until every physical gate passes,
Rev3A remains prototype hardware.

## Package map

- [`design/`](design/) — editable KiCad source, local footprints, and 3D models
- [`manufacturing/`](manufacturing/) — matched Gerber, BOM, and placement files
- [`validation/`](validation/) — review artifacts, checks, and qualification gates
- [`images/`](images/) — moved layer views and populated-board renders
- [Rev3A enclosure](../../case/rev3a/README.md) — printable case source and exports
