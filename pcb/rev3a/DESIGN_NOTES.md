# Revision 3A design notes

This document records the major Rev3A design choices and the checks still needed
before the hardware can be treated as qualified.

## Scope

Rev3A keeps the ESP32-C3-WROOM-02 module used by Revision 2.x. It is an evolution
of the existing board, not a XIAO carrier or a firmware redesign.

## Automatic dual-input power

The power front end follows the published FirstBuild architecture closely:
independent pin-1 and pin-3 inputs, per-input fusing, PMOS reverse-current
blocking, TPS22810 load switches, pin-1 priority control, and Schottky ORing into
`V_INPUT`.

Q3 and Q4 are described as reverse-current or backfeed blocking devices. Rev3A
does not claim protection against a physically reversed connector supply. The
first prototypes must use current-limited sources and an independently checked
J1 breakout fixture.

The FirstBuild schematic's 4.3-15 V label is attached to its downstream `V_INPUT`
rail. It is not evidence that every appliance supplies that range and is not a
Rev3A input specification. The AP63205 cannot regulate 5 V from a 4.3 V input;
minimum input voltage and total path loss are physical measurements, not firmware
assumptions.

## Transient protection

D18 is a populated SMF16A unidirectional TVS from `PIN1_PROTECTED` to ground.
This mirrors the single-TVS position used on the pin-1 branch of the FirstBuild
reference design. The selected part is rated for 16 V stand-off and uses a
SOD-123FL footprint.

Population is not qualification. Before appliance use, confirm polarity and exact
part, measure the appliance's steady-state maximum and connection/removal
transients, and verify that D18 neither conducts during valid operation nor allows
an unsafe peak. Any surge-generator test requires a separately reviewed fixture
and test plan; do not improvise an over-voltage test on an assembled board.

## Regulators

The AP63205 switching regulator replaces the Rev2 linear 5 V stage to reduce heat
and improve efficiency. The AP2112K-3.3 replaces the 200 mA Rev2 3.3 V regulator
and provides more headroom for Wi-Fi current peaks. Regulator temperature, startup,
and rail stability remain prototype tests.

## USB-C and recovery

USB-C connects to the ESP32-C3 native USB interface through USBLC6-2SC6 ESD
protection. R38, 220 kohm from `USB_VBUS` to ground, provides a defined discharge
path when the cable is removed. J2 exposes 3.3 V, ground, BOOT, UART TX/RX, and EN
for recovery if native USB cannot be used.

The USB data routes use 0.20 mm tracks and two ordinary 0.8/0.4 mm through-vias
per signal. No controlled-impedance claim is made. Enumeration, flashing,
reconnect, sustained logging, and Wi-Fi-load tests are required on hardware.

## Layer stack and layout

Rev3A uses four copper layers because a two-layer trial fragmented the ground
return and left the USB pair without a defensible continuous reference. The board
remains 88.7 x 40.0 mm; four layers were selected for return-current integrity,
not to shrink the outline.

| Layer | Function |
| --- | --- |
| `F.Cu` | Components, local power, and signal routing |
| `In1.Cu` | Continuous ground-reference plane |
| `In2.Cu` | Ground plane with one short D18 signal branch |
| `B.Cu` | Signal routing and short USB/feedback transitions |

The D18 branch uses two standard through-vias and a short `In2.Cu` trace. It does
not require blind vias or a special fabrication process. Native USB remains
referenced to the continuous `In1.Cu` plane.

All fitted components are on the top side. The minimum plated drill is 0.30 mm in
the ESP32 thermal pad; routed vias use 0.40 mm drills. There are no blind/buried
vias, filled vias, via-in-pad requirements, or bottom-side placements.

## Sourcing and assembly

The matched package contains 44 purchasing groups and 93 placements. D18 uses
SUNMATE SMF16A (`C399290`); R38 shares the existing RALEC 220 kohm part
(`C104108`). J1 is the through-hole EVERCOM 5301-8P8C (`C3097717`), J2 is the
top-side 2-by-3 recovery header (`C42391552`), and J4 is the SHOU HAN USB-C
receptacle (`C2765186`).

Supplier stock and assembly classifications change. A quote-time substitution is
not acceptable unless package, pinout, voltage/current ratings, temperature range,
and manufacturer data are reviewed.

## Remaining gates

- independent schematic, PCB, BOM, and enclosure review;
- vendor board, drill, part-selection, and placement preview review;
- real assembled-board quote from the final 44-group / 93-placement package;
- appliance-voltage and regulator-headroom measurements;
- dynamic pin-1/pin-3 handoff and reverse-current measurements;
- USB VBUS decay and no-backfeed measurements;
- D18 steady-state and transient qualification;
- USB, Wi-Fi, thermal, and enclosure testing on at least two prototypes.

The [validation checklist](validation/REVIEW_CHECKLIST.md) and
[bring-up procedure](BRINGUP.md) track these items.
