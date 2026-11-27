# GE Appliance Adapter Rev 3L · 65 × 30 mm
**Fully routed engineering prototype for review. Physical verification and factory acceptance are open.** Start with [the editable KiCad project](design/GEA-Adapter-Rev3L.kicad_pro), [top assembly map](evidence/top-assembly-map.svg) and [printed case](case/).
 
The debug LED and both sides of its series circuit are routed. This revision keeps the complete service circuit, including J7 and 18 dedicated probe lands. All 232 reference, pad and net records match Rev 3K. Both eFuses, source priority, data protection, buck and all three indicators remain.

## Size and population

The PCB measures 65 × 30 mm. FirstBuild measures 59.944 × 27.432 mm from its outline Gerber. Area difference is +18.59%. These measurements describe bare PCB outlines, excluding connector overhang and enclosure walls. [FirstBuild source Gerbers](https://github.com/geappliances/home-assistant-adapter/blob/4888a7df56e8ce6382ed91e4b95bd5020f1802f6/doc/pcb/HA%20Adapter%20Gerbers%2011-15-24.zip)

The fitted BOM and placement file agree on 72 components and 32 distinct order codes. All placements are on top. The review Gerbers have 178 top paste objects and zero rear paste. The jack placement uses its manufacturer body datum. Compare the [BOM, CPL and CAM](manufacturing/) with the [layout audit](evidence/layout-audit.json).

## Electrical and layout review

KiCad 9.0.9 reports zero ERC violations, zero DRC violations, zero unconnected items and zero schematic-parity differences with all severities and track errors enabled. Geometry editing used pcbnew 9.0.2. The footprint, solder-mask and copper artwork, drill files, BOM and CPL are review outputs. Board SHA-256 is `9faa8f7f80f640abb621236e157072cc80d1f4c9ef6cfe0db4edfe34dd5f369d`. [ERC](evidence/ERC.json) · [DRC and parity](evidence/routing-DRC.json) · [Top](evidence/rev3l-top.svg) · [Bottom](evidence/rev3l-bottom.svg)

With 35 µm outer copper, the 0.60 A module 5 V feed drop is 30.71 mV at 15.2 µm modeled inner copper and 29.04 mV at 30.48 µm. The J1.8 to J6.6 return drops 4.02 and 2.15 mV respectively on a 0.25 mm grid. The resistance screen includes routed rail segments, return pours and modeled 20 µm via plating. It excludes device/connector losses, transients and temperature rise. The 3.3 kΩ eFuse settings correspond to about 1.01 A nominal input current limit. [Both appliance inputs, buck and 3.3 V branches](evidence/rail-paths.csv) · [Return mesh](evidence/ground-return.csv) · [Model assumptions](../rev3k/evidence/power/README.md)

There are 18 fitted bodies within JLC's 2.5 mm body-to-edge guideline. J1 intentionally extends 0.38 mm beyond the board. Ask the factory to review the actual body envelopes, connector insertion and any edge rails, breakoff and extra tooling price. The minimum drilled-via-to-SMD-land gap screened on either face is 0.2039 mm. Confirm mask registration, hole plating, finished copper and exposed-pad stencil with the factory. Use five fully assembled single-board, lead-free Economic assemblies as the price baseline. [Body distances](evidence/component-body-edge.csv) · [Via clearances](evidence/via-to-land.csv) · [JLC assembly terms](https://jlcpcb.com/help/article/terms-and-conditions-of-jlcpcb-assembly-service)

## Use and validation

Disconnect the appliance cable before connecting USB. The closed case covers the USB port. D11 blocks reverse flow into the buck, but the inserted XIAO connects header 5 V to USB VBUS. The assembly has a shared ground and no verified simultaneous-source protection. Keep any appliance-facing work isolated from host USB and confirm interface voltage and pinout on an isolated test fixture. Do not bypass the input protection.

Verify startup on each input, pin-1 priority and handover, overload/thermal behavior, clamps, GEA2/GEA3 communication and reset-time traffic on both module variants. Confirm XIAO socket height, RF operation, latched RJ45 and both printed lids with physical samples. These checks and a supplier assembly review remain open. There was no powered testing or vendor quote for this revision.

With the case removed, the 2 mm diameter vertical-probe screen clears TP12 buck output and TP16 ground, TP1 module 5 V, TP2 module 3.3 V, TP3 protected input and TP7 ground for both registered module envelopes. TP18 fails this screen. J7 is the series-protected bus monitor. Probe bodies and actual cables need a physical check. [Probe map](evidence/probes.svg) · [Access distances](evidence/probe-clearance.json)

The placement-only files in evidence/unrouted-placement, placement-DRC.json and power-trials.csv are historical. The linked routing-DRC.json, rail-paths.csv and ground-return.csv describe the current board.
