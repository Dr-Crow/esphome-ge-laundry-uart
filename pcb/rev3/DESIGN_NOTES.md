# Revision 3A design notes

This file records the decisions that materially affect safety, cost, or whether the board can be assembled. Candidate part numbers are not approvals to order.

## Power path

### Rev3A automatic front end

The final Rev3A power architecture removes the manual JP2 selector and the shared
Q1/Q2/D12/D13 gate network. F1 and F2 remain independent per-input fuses. Each fused
input uses a FirstBuild-derived P-channel reverse-protection stage followed by its own
TPS22810DBVR load switch. Rev 3A uses the currently available CJ3407 instead of the
scarce DMP3030SN reference part. Each channel has a 0.022 uF timing capacitor, 1 uF
input capacitor, 0.1 uF output capacitor, and a 100 pF/5.1 k/51 ohm PMOS gate network.
An MMBT3904 with external 10 k resistors makes J1 pin 1 the priority source when both
appliance inputs are valid. This replaces the inconsistent and end-of-life pre-biased
transistor choices found in the reference files with common parts whose values are
explicit in the schematic. MBR0540 output isolation prevents the secondary source
from back-powering the selected path. The common isolated V_INPUT feeds the existing
AP63205 input network directly. USB F3/D10 and buck D11 isolation are unchanged.

There are no user controls or power-selection jumpers. The target layout calls for
diagnostic pads at each fused input, the isolated common node, USB VBUS, +5V and +3V3;
those pads are now present on the PCB, including TP8 through TP14 for the two automatic
input paths and USB VBUS. J2 remains a schematic-only do-not-install header and does
not create a PCB or enclosure feature. J3 is the existing do-not-install Tag-Connect
footprint. The design is safe to evaluate only with current-limited sources until
reverse current, switch timing, and thermal behavior are measured.

The source headroom gate is explicit: AP63205 is retained for prototype work, but a
4.3 V minimum source cannot be regulated to 5 V. The measured appliance minimum must
exceed the regulator's required headroom after the PMOS, load-switch and diode drops.

Appliance power and USB power enter through separate protected paths:

```text
appliance -> fuse/protection -> 5 V switching regulator -> blocking diode --+
                                                                         +-> board 5 V -> 3.3 V regulator -> ESP32
USB-C VBUS -> resettable fuse -------------------------> blocking diode --+
```

- The AP63205 switching regulator is more efficient than the Revision 2 linear regulator, so it should produce less heat when stepping appliance voltage down to 5 V.
- The AP2112K provides more 3.3 V current margin for ESP32 Wi-Fi peaks than the Revision 2 AP2205.
- The two blocking diodes are intended to stop either source from driving backward into the other source.
- The optional TVS footprint D8 remains do-not-install because its required voltage and energy ratings are not proven from appliance measurements. The old D7/manual-selector path is removed.
- The resettable-fuse choices remain provisional until boot current, Wi-Fi peaks, fault current, and enclosure temperature are measured.

Prototype testing must measure both input currents and the USB, 5 V, and 3.3 V rails while sources are attached, removed, and applied in either order. No appliance-derived voltage may appear at USB VBUS.

## USB-C

The ESP32-C3 provides native USB Full Speed on GPIO18 and GPIO19. The board adds:

- a USB-C receptacle;
- one 5.1 kohm pull-down on each configuration pin so a normal USB-C host recognizes a device;
- a low-capacitance USB ESD protector;
- one 22 ohm series resistor on each data line; and
- a resettable fuse and blocking diode on USB power.

Espressif requires the data traces to run together, remain nearly equal in length, see continuous ground beneath them, and present 90 ohms differential impedance within 10 percent. Rev 3A remains a two-layer design to control cost. It is acceptable only when the fabricator supports a practical geometry and the routed board preserves a nearly continuous bottom ground plane.

This matches the published FirstBuild Gerber archive, which contains only top and
bottom copper layers. In a JLCPCB calculator check on 2026-09-14, five 88.7 mm by
34 mm bare boards were $4 total with two layers and $7 total with four layers before
shipping. Four layers are therefore not prohibitively expensive, but they do not
remove the top-side area required by the connectors, ESP32 antenna keepout, and power
components. Two layers remain the default; four layers are a fallback only if the
finished USB and ground layout cannot meet the release gates.

The FirstBuild Gerber outline is approximately 59.94 mm by 27.43 mm. Its smaller
carrier uses a Seeed XIAO ESP32-C3 daughterboard, components on both sides, and many
0402/0603 packages. Revision 3A's native ESP32-C3-WROOM-02, larger passives, and
single-sided placement dominate its approximately 88.7 mm by 40.0 mm outline. The
extra height creates a dedicated lower-edge buck-converter corridor without crossing
the USB pair; extra copper layers alone would not create the same size reduction.

For the nominal JLCPCB 1.6 mm two-layer calculator stack-up, the layout starting
geometry is 17 mil (0.432 mm) top-layer traces, an 8 mil (0.203 mm) gap between the
pair, and 8 mil clearance to top-layer ground copper. JLCPCB's calculator reports
approximately 90.37 ohms differential for that geometry. The normal two-layer
service is not advertised as controlled-impedance/TDR certified, so the board and
documentation must call this a calculated target. Keep the pair on the top layer,
use no vias, preserve uninterrupted bottom ground, target no more than 1 mm pair
skew, and keep it away from the switching nodes and antenna.

Decision order:

1. Place the USB protection and series parts to create a short, direct routing corridor.
2. Apply a KiCad differential-pair rule for the documented 17/8/8 mil geometry.
3. Use the two-layer layout only if the pair fits without cutting the ground return or antenna keepout.
4. If it does not fit, revise the two-layer placement and return for review; do not silently change the layer count.

Current routed evidence: the ESP32-to-series-resistor section is entirely on
`F.Cu`, uses the 0.432 mm USBData width, and measures 5.225 mm for D- and
6.025 mm for D+ (0.800 mm skew). KiCad 9.0.9 reports no short, clearance,
courtyard, via-count, or pair-skew violation for this section. The two remaining
USB sections are still unrouted and must meet the same release gates before the
board can be fabricated.

## RF and enclosure

The ESP32 module contains the antenna; no separate antenna is needed. Copper, traces, components, and enclosure hardware must stay out of the module's antenna keepout. Final Wi-Fi range must be tested in the actual printed enclosure and near the appliance chassis.

## Assembly and sourcing

The target is a turnkey assembled board with no customer hand soldering. The manufacturing package must include:

- Gerbers and drill files;
- a BOM with manufacturer, exact manufacturer part number, package, electrical ratings, assembly type, and optional JLC/LCSC number;
- a placement file covering both surface-mount and through-hole parts; and
- a clear top/bottom assembly drawing for connector orientation and do-not-install parts.

JLCPCB is the natural first quote for the existing designs because many parts already carry JLC/LCSC catalog numbers. PCBWay remains a useful comparison, but it needs the vendor-neutral manufacturer fields rather than only JLC/LCSC numbers. Live stock, substitutions, setup fees, through-hole labor, shipping, and quantity determine the real price.

Current sourcing review has corrected two catalog mismatches: C9 now specifies FH
`1206B106K500NT` (`C303950`), a 10 uF, 50 V, X7R capacitor in the placed
1206 footprint, and C10 specifies FH `0603B104M500NT` (`C286510`), a
100 nF, 50 V, X7R capacitor in the placed 0603 footprint. J1 consistently
specifies the low-cost EVERCOM `5301-8P8C` (`C3097717`) and requires wave
soldering. J4 now specifies HCTL `HC-TYPE-C-16P-01A` (`C2894897`). Its
official drawing matches the existing GCT-family footprint's contact order,
0.5 mm pitch, locating holes, and four shell-tab centers. It was selected
because the exact GCT part was unavailable and the HCTL part was in stock at
the time of review. Do not substitute another mechanically similar USB
connector without comparing the official pad and shell-tab drawing.

The current schematic exports 43 populated BOM groups covering 90 placed
parts. Seven groups still lack an LCSC identifier, so this is not yet a matched
assembly BOM and no assembled-price claim should be made from it.

## Release gates

- Complete routing with no unintended open connections or shorts.
- KiCad ERC and DRC pass using reviewed project-level exclusions only.
- USB geometry is approved by the selected fabricator.
- Exact footprints match manufacturer drawings, especially the appliance connector and USB-C connector.
- Power loss, temperature rise, reverse current, and transient behavior pass on at least two prototypes.
- The vendor preview shows every fitted part, including the through-hole appliance connector, with correct orientation.
- The assembled-board and enclosure quote supports the goal of staying below the former $39.99 FirstBuild retail price at a practical batch size.

## Primary references

- [Espressif ESP32-C3 hardware design guidelines](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c3/pcb-layout-design.html)
- [ESP32-C3-WROOM-02 datasheet](https://documentation.espressif.com/esp32-c3-wroom-02_datasheet_en.html)
- [AP63205 regulator datasheet](https://www.diodes.com/datasheet/download/AP63200-AP63201-AP63203-AP63205.pdf)
- [AP2112 regulator datasheet](https://www.diodes.com/assets/Datasheets/AP2112.pdf)
- [JLCPCB placement-file requirements](https://jlcpcb.com/help/article/pick-place-file-for-pcb-assembly)
