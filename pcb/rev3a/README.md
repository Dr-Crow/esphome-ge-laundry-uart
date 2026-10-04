# Revision 3A PCB

The current branch backports the selected rated protection circuit and adds the
recommended CHIP_EN capacitor to the integrated Rev3A architecture. See
[RATED-PROTECTION.md](RATED-PROTECTION.md) and
[POWER-QUALIFICATION.md](POWER-QUALIFICATION.md). **Native source checks and refreshed exports are paired in the
[current source manifest](validation/rated-protection-manifest.json); electrical,
supplier/process and physical qualification gates remain open.**

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
| Appliance power | Manual JP2 selection of pin 1 / pin 3 | Automatic pin 1 / pin 3 selection with pin-1 priority |
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
| `J2 RECOVERY` | 2-by-3 recovery header | Backup UART flashing with 3.3 V logic and enclosure open |
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
Leave adapter VCC and J2 pin 1 disconnected; never inject the regulator-output
`+3V3` rail. Power the board from one reviewed input after its qualification
procedure.
The matching enclosure keeps J2 inside the case; remove the lid before attaching
leads and disconnect them before closing the enclosure or connecting J1.

## Power architecture and design rationale

No user jumper is required. Each appliance input has its own resettable fuse,
CJ3407 PMOS reverse-current blocking stage, and TPS1H200A controlled high-side switch.
The switched outputs feed `V_INPUT` through Schottky diodes, while a transistor
network gives pin 1 priority when both inputs are present. USB-C VBUS is fused
and diode-isolated before joining the 5 V rail:

```text
J1 pin 1 -> fuse -> reverse-current block -> load switch -> diode --+
                                                                    +-> V_INPUT
J1 pin 3 -> fuse -> reverse-current block -> load switch -> diode --+
```

`V_INPUT` then feeds the buck regulator, and USB joins the same `+5V` rail
through its own diode:

```text
V_INPUT -> AP63205 -> BUCK_5V -> D11 --+
                                       +-> +5V
USB-C VBUS -> fuse -> D10 -------------+
```

`+5V` is a nominal name, not a guaranteed level. Whichever source is active,
the rail sits below that source by the forward drop of its isolation diode
(`D11` for the appliance/AP63205 path, `D10` for USB), and that drop depends on
load current and temperature. No specific voltage range is claimed here; it
has not been measured.

Q3/Q4 and the CJ3407 stages are intended to limit reverse current and source-
to-source backfeed. They are not claimed to protect against a physically
reversed connector supply. All source combinations and handoffs require
current-limited bench supplies and an independently checked J1 breakout.

The FirstBuild schematic labels its downstream `V_INPUT` rail as 4.3–15 V.
That is neither a measured Rev3A appliance-input range nor a design guarantee;
the AP63205 cannot regulate 5 V from a 4.3 V input. Minimum appliance voltage,
path drop, regulator headroom, and transient environment must be measured.

### Transient protection

D18 and D19 are populated unidirectional SUNMATE SMF16A TVS parts (`C399290`)
from `PIN1_PROTECTED` and `PIN3_PROTECTED` to ground. Both are upstream of the
switch current limits. The reviewed protection backport uses 33 V Littelfuse
PPTCs, corrected PMOS source/drain connections, source-referenced nominal 12 V
MCC gate clamps, and 40 V TPS1H200A switches. It retains the original source
priority and all downstream regulators.

The SMF16A 26 V clamp is specified for one stated pulse/current/temperature
condition. It does not establish an appliance transient envelope or a 40 V
rating for the carrier. PMOS differential voltage, low-current/hot gate stress,
PPTC fault voltage, converter limits and transient energy remain separate gates.
Validate both protected nodes under reviewed fixtures and conditions; no
physical transient tests have run. See the complete
[protection limits](RATED-PROTECTION.md#source-referenced-gate-and-whole-chain-bounds).

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
| `In1.Cu` | Ground reference with documented retry-control slot and via antipads |
| `In2.Cu` | Ground plane with local power/control routing |
| `B.Cu` | Signal routing and short USB/feedback transitions |

The D18 branch uses two standard through-vias and a short `In2.Cu` trace.
Native USB retains its original signal routing. Actual reference-plane refill and
return-path changes are documented in the current protection review and require
physical qualification. All fitted components are top-side; new routed vias use
0.30/0.40 mm drills and the ESP32 thermal pad uses a
0.30 mm minimum plated drill. There are no blind/buried or filled vias,
controlled-depth drilling, via-in-pad requirements, or bottom-side placements.

## Engineering and manufacturing status

- The current schematic has zero KiCad 9.0.9 ERC errors or warnings. The
  [schematic-only ERC cleanup](validation/erc-normalization/README.md) moves eight
  USB symbols and attached markers onto the unchanged 25 mil connection grid,
  and explicitly wires the unchanged U4 VCC pins to +5V. All 301 current pin
  memberships remain identical. The earlier namespace recovery removed 44
  symbol-mismatch warnings. Existing rated-protection reports/manifests and
  package schematic PDF still describe the pre-cleanup snapshot pending refresh.
- Full native all-severity/all-track/parity DRC has zero errors, warnings and
  unconnected items. Exact frozen embedded footprint recovery clears five library
  mismatch warnings without pad, model, graphic, placement or attribute changes.
- Matched native BOM has 97 fitted references, 49 exact-value/full-footprint rows
  and 42 purchasing tuples. The supplier CPL applies explicit J1/U2 body-centroid
  transforms; actual supplier zero, rotation and assembly-process acceptance remain open.
- Original global rules, Power 0.25 mm and Switching 0.30 mm remain. The TI
  0.20 mm exception applies only to adjacent pads within the same U9 or U10
  footprint. All tracks and vias retain their normal rules.
- The earlier [clearance repair](validation/CLEARANCE-REPAIR.md) describes the
  frozen `d1769b25` base. Its 53 ERC/five DRC warning counts and 93-part package
  are historical evidence, not current backport counts or exports.

Native checks establish digital source consistency. Loaded nominal 5 V margin,
current/inrush/retry, integrated LDO temperature, EN/reset-adapter behavior,
source/transient coordination, manufacturing process, physical fit and appliance
qualification remain open. The new source does not inherit the September quote
or a manufacturing approval.

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
2. Confirm D18/D19 are SMF16A in the documented orientations, R38 is 220 kohm, and no
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

| Pin | Position | Signal | Connection |
| ---: | --- | --- | --- |
| 1 | Upper left | `+3V3` | Regulator-output rail: leave disconnected; do not inject power |
| 2 | Middle left | `GND` | Adapter ground |
| 3 | Upper right | GPIO9 / `BOOT` | Hold low during download reset |
| 4 | Lower right | GPIO20 / UART0 RXD | Adapter TX |
| 5 | Middle right | GPIO21 / UART0 TXD | Adapter RX |
| 6 | Lower left | `EN` | Pull low briefly to reset |

Connect ground and crossed 3.3 V logic UART signals. Leave adapter VCC/J2 pin 1
disconnected and never inject `+3V3`. Power from one reviewed input after its
qualified power procedure. Hold BOOT low, pull EN low long enough for C26 to
discharge and satisfy the reset-low timing, then release EN. Keep BOOT held
through the delayed EN rise until the downloader starts. Actual adapter
pulse/sink behavior must pass the [reset qualification](POWER-QUALIFICATION.md).
Disconnect all leads before closing the enclosure or connecting J1.

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
6. Qualify both SMF16A paths, source-referenced CJ3407 gate clamps, PPTC/TPS/converter
   coordination, current/inrush/retry, both loaded nominal 5 V paths, integrated
   AP2112K thermal behavior and EN/reset programming against measured conditions.
   See [the architecture-specific gates](POWER-QUALIFICATION.md).
7. Retain the repaired intended clearances, review the TP12/process margin and
   finished via annuli with the fabricator, and recheck the matched exports after
   any further source change.
8. Pass USB enumeration/flashing, sustained logging, Wi-Fi load, enclosure fit,
   connector access, and antenna-performance tests on at least two boards.

Keep USB disconnected for the first appliance-only test; test appliance plus USB
only after appliance-only operation passes. Until every physical gate passes,
Rev3A remains prototype hardware.

## Package map

- [`design/`](design/) — editable KiCad source, local footprints, and 3D models
- [`manufacturing/`](manufacturing/) — matched Gerber, BOM, and placement files
- [`validation/`](validation/) — review artifacts, checks, and qualification gates
- [`images/`](images/) — moved layer views and populated-board renders
- [Historical Rev3A enclosure guide](https://github.com/Dr-Crow/esphome-ge-laundry-uart/blob/a5a9fac87cbcb59d337a1fb8d3084ad18867a3e6/case/rev3a/README.md) — pinned historical source; enclosure CAD is outside this upstream board package. Revised protection parts, approximate models and component heights require separate fit review.
