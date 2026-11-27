# GE Appliance Adapter Rev 3M · 59.944 × 27.432 mm

[Silkscreen review and scannable underside preview](evidence/silkscreen/README.md)
**Fully routed engineering prototype for review. Physical verification and factory acceptance are open.** Start with [the editable KiCad project](design/GEA-Adapter-Rev3M.kicad_pro), [top assembly map](evidence/top-assembly-map.svg) and [printed case](case/).
 
This revision omits TP1–TP18, the J7 bus monitor and its R48–R50 series resistors, and the unpopulated C30 and D8 footprints. The D3 and D6 default signal paths are fixed in copper. The two engineering selectors JP1/JP2 are omitted. Both input eFuses, source priority, transient clamps, onboard pull-ups, JP3 and JP4 service links, all three indicators, RJ45 and both module sockets remain. Use 3L for a first bring-up that needs easy probing.

## Size and population

The PCB measures 59.944 × 27.432 mm. FirstBuild measures 59.944 × 27.432 mm from its outline Gerber. Area difference is +0.00%. These measurements describe bare PCB outlines, excluding connector overhang and enclosure walls. [FirstBuild source Gerbers](https://github.com/geappliances/home-assistant-adapter/blob/4888a7df56e8ce6382ed91e4b95bd5020f1802f6/doc/pcb/HA%20Adapter%20Gerbers%2011-15-24.zip)

The fitted BOM and placement file agree on 68 components and 30 distinct order codes. All placements are on top. The review Gerbers have 168 top paste objects and zero rear paste. The jack placement uses its manufacturer body datum. Compare the [BOM, CPL and CAM](manufacturing/) with the [layout audit](evidence/layout-audit.json).

Removing four fitted references saves four placements per board and the monitor header and resistors as line items where unique. The bare pads and DNP parts had no fitted cost. There is no new vendor quote. A smaller outline may leave a five-board fabrication tier unchanged. The actual fee difference depends on SKU classifications, order quantity, handling and tooling.

## Electrical and layout review

KiCad 9.0.9 reports zero ERC violations, zero DRC violations, zero unconnected items and zero schematic-parity differences with all severities and track errors enabled. Geometry editing used pcbnew 9.0.2. The footprint, solder-mask and copper artwork, drill files, BOM and CPL are review outputs. Board SHA-256 is `c120337846df5238d40800c6ef0afda243c2a517b15f14e9aa9d5a918e84aa07`. [ERC](evidence/ERC.json) · [DRC and parity](evidence/routing-DRC.json) · [Top](evidence/rev3m-top.svg) · [Bottom](evidence/rev3m-bottom.svg)

With 35 µm outer copper, the 0.60 A module 5 V feed drop is 33.74 mV at 15.2 µm modeled inner copper and 29.62 mV at 30.48 µm. The J1.8 to J6.6 return drops 4.48 and 2.44 mV respectively on a 0.25 mm grid. The resistance screen includes routed rail segments, return pours and modeled 20 µm via plating. It excludes device/connector losses, transients and temperature rise. The 3.3 kΩ eFuse settings correspond to about 1.01 A nominal input current limit. [Both appliance inputs, buck and 3.3 V branches](evidence/rail-paths.csv) · [Return mesh](evidence/ground-return.csv) · [Model assumptions](../rev3k/evidence/power/README.md)

There are 24 fitted bodies within JLC's 2.5 mm body-to-edge guideline. J1 intentionally extends 0.38 mm beyond the board. Ask the factory to review the actual body envelopes, connector insertion and any edge rails, breakoff and extra tooling price. The minimum drilled-via-to-SMD-land gap screened on either face is 0.2250 mm. Confirm mask registration, hole plating, finished copper and exposed-pad stencil with the factory. Use five fully assembled single-board, lead-free Economic assemblies as the price baseline. [Body distances](evidence/component-body-edge.csv) · [Via clearances](evidence/via-to-land.csv) · [JLC assembly terms](https://jlcpcb.com/help/article/terms-and-conditions-of-jlcpcb-assembly-service)

## Use and validation

Disconnect the appliance cable before connecting USB. The closed case covers the USB port. D11 blocks reverse flow into the buck, but the inserted XIAO connects header 5 V to USB VBUS. The assembly has a shared ground and no verified simultaneous-source protection. Keep any appliance-facing work isolated from host USB and confirm interface voltage and pinout on an isolated test fixture. Do not bypass the input protection.

Verify startup on each input, pin-1 priority and handover, overload/thermal behavior, clamps, GEA2/GEA3 communication and reset-time traffic on both module variants. Confirm XIAO socket height, RF operation, latched RJ45 and both printed lids with physical samples. These checks and a supplier assembly review remain open. There was no powered testing or vendor quote for this revision.

## Bring-up access and layout tradeoffs

With the case removed, D11 pad 2 exposes the pre-diode buck output to a fine top-side tip. JP3 pad 2 exposes module 5 V. The underside socket solder tails J6.7, J6.5 and J6.6 provide 5 V, 3.3 V and ground respectively. The nominal exposed tip diameters are 0.65 mm at D11 and 1.77 mm at JP3. Use an isolated fixture and inspect the populated joints before probing. The coordinates are given in the board's top-view frame. [Existing service lands](evidence/existing-service-lands.csv)

R1 was rotated on its original footprint. The C15 bootstrap capacitor moved to clear J1. Its connections stay on the top layer. The total switch-net trace length changes from 6.868 mm on 3L to 6.989 mm on 3M, and the bootstrap trace from 2.060 to 2.273 mm. Check the AP63205 switching waveform and load response on an isolated fixture. A new ground stitch ties the bottom-layer copper at the module ground pin into the return. The modeled 0.60 A module feed and return on the thinner stack are 33.74 and 4.48 mV, compared with 30.71 and 4.02 mV on 3L. These results support further prototype evaluation of the four-layer build with 1 oz outer and 0.5 oz inner copper. They do not qualify its temperature rise or RF performance.

J7 (C492403) and R48/R49/R50 (C21190) are the only references using those two order codes in the 3L BOM. The reductions are four fitted parts per board, two distinct order codes and twenty plated-header solder joints across five boards. RJ45 and the XIAO sockets still need through-hole assembly. No feeder-fee or total dollar saving has been confirmed for 3M. The board uses 15.67% less PCB area than 3L. The enclosure is a separate printed part and includes space for the module buttons, antenna and connector.
