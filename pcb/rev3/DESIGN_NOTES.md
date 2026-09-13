# Revision 3A design notes

This file records the decisions that materially affect safety, cost, or whether the board can be assembled. Candidate part numbers are not approvals to order.

## Power path

Appliance power and USB power enter through separate protected paths:

```text
appliance -> fuse/protection -> 5 V switching regulator -> blocking diode --+
                                                                         +-> board 5 V -> 3.3 V regulator -> ESP32
USB-C VBUS -> resettable fuse -------------------------> blocking diode --+
```

- The AP63205 switching regulator is more efficient than the Revision 2 linear regulator, so it should produce less heat when stepping appliance voltage down to 5 V.
- The AP2112K provides more 3.3 V current margin for ESP32 Wi-Fi peaks than the Revision 2 AP2205.
- The two blocking diodes are intended to stop either source from driving backward into the other source.
- Protection diodes D7 and D8 are currently marked do-not-install because their required voltage and energy ratings are not proven from appliance measurements.
- The resettable-fuse choices remain provisional until boot current, Wi-Fi peaks, fault current, and enclosure temperature are measured.

Prototype testing must measure both input currents and the USB, 5 V, and 3.3 V rails while sources are attached, removed, and applied in either order. No appliance-derived voltage may appear at USB VBUS.

## USB-C

The ESP32-C3 provides native USB Full Speed on GPIO18 and GPIO19. The board adds:

- a USB-C receptacle;
- one 5.1 kohm pull-down on each configuration pin so a normal USB-C host recognizes a device;
- a low-capacitance USB ESD protector;
- one 22 ohm series resistor on each data line; and
- a resettable fuse and blocking diode on USB power.

Espressif requires the data traces to run together, remain nearly equal in length, see continuous ground beneath them, and present 90 ohms differential impedance within 10 percent. Four layers make that geometry easier because the ground plane can sit close below the traces. Two layers are acceptable only when the fabricator approves a practical geometry and the rerouted board preserves a nearly continuous bottom ground plane.

Decision order:

1. Move the USB protection and series parts to create a wider, direct routing corridor.
2. Ask JLCPCB and PCBWay for the actual low-cost two-layer and four-layer stack-ups and controlled-impedance limits.
3. Use the two-layer option only if the approved geometry fits without cutting the ground return or antenna keepout.
4. Otherwise use four layers for the USB-capable prototype; do not guess trace dimensions from an online calculator.

## RF and enclosure

The ESP32 module contains the antenna; no separate antenna is needed. Copper, traces, components, and enclosure hardware must stay out of the module's antenna keepout. Final Wi-Fi range must be tested in the actual printed enclosure and near the appliance chassis.

## Assembly and sourcing

The target is a turnkey assembled board with no customer hand soldering. The manufacturing package must include:

- Gerbers and drill files;
- a BOM with manufacturer, exact manufacturer part number, package, electrical ratings, assembly type, and optional JLC/LCSC number;
- a placement file covering both surface-mount and through-hole parts; and
- a clear top/bottom assembly drawing for connector orientation and do-not-install parts.

JLCPCB is the natural first quote for the existing designs because many parts already carry JLC/LCSC catalog numbers. PCBWay remains a useful comparison, but it needs the vendor-neutral manufacturer fields rather than only JLC/LCSC numbers. Live stock, substitutions, setup fees, through-hole labor, shipping, and quantity determine the real price.

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
