# Revision 3A design notes

This file records the decisions that materially affect safety, cost, or whether the board can be assembled. Candidate part numbers are not approvals to order.

## Power path

### Rev3A automatic front end

The proposed Rev3A power architecture removes the manual JP2 selector and the shared
Q1/Q2/D12/D13 gate network. F1 and F2 remain independent per-input fuses. Each fused
input uses a FirstBuild-derived P-channel reverse-protection stage followed by its own
TPS22810DBVR load switch. Rev 3A uses the currently available CJ3407 instead of the
scarce DMP3030SN reference part. Each channel has a 0.022 uF timing capacitor, 1 uF
input capacitor, 0.1 uF output capacitor, and a 100 pF/5.1 k/51 ohm PMOS gate network.
An MMBT3904 with external 10 k resistors makes J1 pin 1 the priority source when both
appliance inputs are valid. This replaces the inconsistent and end-of-life pre-biased
transistor choices found in the reference files with common parts whose values are
explicit in the schematic. MBR0540 output isolation is intended to keep the secondary
source from back-powering the selected path. The common isolated V_INPUT feeds the existing
AP63205 input network directly. USB F3/D10 and buck D11 isolation are unchanged.

There are no user controls or power-selection jumpers. The target layout calls for
diagnostic pads at each fused input, the isolated common node, USB VBUS, +5V and +3V3;
those pads are now present on the PCB, including TP8 through TP14 for the two automatic
input paths and USB VBUS. J2 remains a schematic-only do-not-install header and does
not create a PCB or enclosure feature. J3 is the existing do-not-install Tag-Connect
footprint. JP1 is the inherited signal-mapping solder selector, not a power selector.
Its bare-board copper defaults to pads 1-2 for the FirstBuild-compatible mapping; the
DNP flag means there is no separately assembled part. Cutting that bridge and joining
pads 2-3 is an engineering-only alternate mapping. The design is safe to evaluate only with current-limited sources until
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

Espressif requires the data traces to run together, remain nearly equal in length, see continuous ground beneath them, and present 90 ohms differential impedance within 10 percent. Rev3A uses four copper layers with solid `In1.Cu` and `In2.Cu` ground-reference planes.

This matches the published FirstBuild Gerber archive, which contains only top and
bottom copper layers. In a JLCPCB calculator check on 2026-09-14, five 88.7 mm by
34 mm bare boards were $4 total with two layers and $7 total with four layers before
shipping. A finished two-layer routing trial fragmented its ground fill into 18
disconnected islands. The four-layer revision preserves the same outline and
placement while providing uninterrupted return planes, so the small historical bare-
board premium was accepted. The final assembled quote must confirm the current cost.

The FirstBuild Gerber outline is approximately 59.94 mm by 27.43 mm. Its smaller
carrier uses a Seeed XIAO ESP32-C3 daughterboard, components on both sides, and many
0402/0603 packages. Revision 3A's native ESP32-C3-WROOM-02, larger passives, and
single-sided placement dominate its approximately 88.7 mm by 40.0 mm outline. The
extra height creates a dedicated lower-edge buck-converter corridor without crossing
the USB pair; extra copper layers alone would not create the same size reduction.

The complete connector-to-ESP32 D+ and D- routes are 24.314 mm and 25.357 mm
respectively, for 1.043 mm skew. Both are 0.20 mm wide. Each uses two standard
0.8/0.4 mm through-vias to cross from `F.Cu` to `B.Cu` and back while remaining
referenced to an uninterrupted internal ground plane. These dimensions establish
manufacturing limits, not a controlled-impedance claim: obtain the selected vendor's
four-layer stack-up review before release. The smallest vias elsewhere on the board
are also standard 0.8/0.4 mm through-vias. Two smaller prototype vias on a low-speed
control net were rerouted after they invoked high-precision fabrication charges in
the quote calculator. There are no microvias or via-in-pad features.

Decision order:

1. Keep the connector fan-out at or above the documented 0.20/0.10 mm limits.
2. Keep the paired nets close in length and away from switching nodes and the antenna.
3. Prove USB enumeration, flashing, sustained logging, and reconnect behavior on prototypes.
4. Confirm the fabricator's stack-up and physical USB reliability before release.

Current routed evidence: J4, U7, R28/R29, and the ESP32 are connected end to end.
KiCad 9.0.9 reports no USB short, clearance, or unconnected item and the complete PCB
reports zero DRC errors. Treat successful physical USB testing as a release gate
rather than assuming that a clean DRC proves signal integrity.

## RF and enclosure

The ESP32 module contains the antenna; no separate antenna is needed. U2 is placed
at `(81.6, 17.0)` with its antenna facing the right edge. The module antenna
overhangs the base board and its embedded keepout begins at the 88.7 mm board
edge, following Espressif's preferred module-on-baseboard placement. The
rightmost solder pad retains 0.65 mm edge clearance. The enclosure must leave at
least 15 mm of clear space beyond the antenna edge (`x = 88.7..103.7 mm`,
`y = 3..31 mm`) with no metal, wiring, fasteners, or structural ribs. Final
throughput and Wi-Fi range must be tested in the printed enclosure and next to
the appliance chassis.

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
soldering. J4 specifies SHOU HAN `TYPE-C 16PIN 2MD(073)` (`C2765186`), an
Economic Assembly part with ample quoted stock. Its official drawing matches
the existing KiCad 9 land pattern
`Connector_USB:USB_C_Receptacle_HCTL_HC-TYPE-C-16P-01A`: 0.50 mm contact pitch,
5.78 mm locating-hole spacing, 8.64 mm shell-slot spacing, matching shell-slot
positions, and an 8.94 mm by 7.35 mm body envelope. The earlier HCTL
`HC-TYPE-C-16P-01A` (`C2894897`) has the same land pattern but was not selectable
from JLCPCB's live Economic Assembly inventory. Revalidate the complete USB
cluster against the selected connector drawing after any footprint or routing
change and again in the vendor preview before ordering. Do not substitute
another mechanically similar connector without comparing its official contact,
locating-hole, shell-tab, and body dimensions.

The current schematic exports 42 populated BOM groups covering 90 placed
parts, and every group has an exact LCSC identity. C16/C17 use Samsung
`CL32B226KAJNNNE` (`C309062`), a stocked 22 uF, 25 V, X7R, 1210 capacitor
specified to 125 C. It replaces an unavailable 16 V X8L part and provides more
voltage and temperature margin than the 85 C X5R fallback. Prototype testing
must still check AP63205 load-step response, ripple, and capacitor temperature
at the intended input and load extremes. A matched BOM does not establish the
assembled price; live stock, assembly classification, and setup fees remain
quote-time gates.

### Live sourcing checkpoint

The 2026-09-15 LCSC/JLCPCB catalog review found the regulator, load switches,
ESP32 module, USB protection, USB-C connector, PMOS devices, power diodes, fuses,
inductor, and principal capacitors under their documented catalog identities.
Stock counts are volatile and are not a substitute for the assembly quote.

| Risk | Parts | Quote-time action |
| --- | --- | --- |
| Mechanical single source | J1 EVERCOM `5301-8P8C` (`C3097717`) | Verify live availability, drawing, orientation, and wave-solder charge; do not substitute by appearance. |
| No validated drop-in alternate | U2 ESP32-C3-WROOM-02-N4 (`C2934560`) | Keep the exact part or return the footprint/layout for review. |
| Verified quote substitution | J4 SHOU HAN `TYPE-C 16PIN 2MD(073)` (`C2765186`) | Keep the selected part; the HCTL `HC-TYPE-C-16P-01A` (`C2894897`) is mechanically compatible but was unavailable to Economic Assembly during the live quote. |
| Availability needs confirmation | C11/C13 Samsung `CL21A106KAYNNNE` (`C15850`), F3 Littelfuse `1206L050YR` (`C163512`) | Approve only a same-package, equal-or-better electrical alternate after datasheet review. |
| Lower observed stock | D14-D17 MCC `MBR0540-TP` (`C78744`) | Recheck quantity before assembly submission; do not change diode rating or footprint without review. |
| Exact-part stock observed | U8 `AP63205WU-7` (`C2071056`), U6 `AP2112K-3.3TRG1` (`C51118`), U9/U10 `TPS22810DBVR` (`C205990`), Q3/Q4 `CJ3407` (`C15903`), U7 `USBLC6-2SC6` (`C7519`) | Confirm the quote did not silently substitute parts. |

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
