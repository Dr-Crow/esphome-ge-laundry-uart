# Onion Straws revision 2.2 manufacturing candidate

This directory contains the matched files needed to quote a small revision 2.2 prototype batch. Revision 2.2 is not a proven hardware release until physical boards pass bring-up testing.

## What changed

- `U1` is an optional voltage-monitor chip intended to reset the ESP32 when its supply is too low. It caused repeated boot loops on existing Rev 2 boards, so Rev 2.2 leaves it uninstalled. Its small footprint remains on the board for rework, but the factory BOM and placement data exclude it. R3 still keeps the ESP32 enabled. Neither board button is wired as a reset button; reset requires a power cycle or an external reset connection.
- The rear silkscreen identifies the board as revision 2.2.
- The appliance-facing connector labels now use the adapter/ESP perspective:
  - pin 5, `Full TX`: adapter/ESP TX to appliance RX;
  - pin 4, `Full RX`: appliance TX to adapter/ESP RX.
- `Q1` is one of two identical power-control transistors. Its supplier catalog field was blank, while `Q2` already identified the correct part. Rev 2.2 gives both the same LCSC catalog number so JLCPCB can source the part automatically. This is purchasing metadata only and does not change the circuit.
- `J1` retains the original low-cost EVERCOM `5301-8P8C` (`C3097717`). Its eight signal holes now use the manufacturer's recommended 0.90 mm diameter; the connector position and two 3.20 mm locating holes are unchanged. Confirm the connector orientation and drill pattern in the vendor preview and prototype batch before production use.
- `JP1` and `JP2` are existing three-pad solder selectors on the bottom of the board. `JP1` selects the FirstBuild-compatible signal mapping. `JP2` selects the normal or alternate appliance power input. Both default to pads 1-2 because that copper bridge is part of the manufactured board; changing one requires cutting that bridge and soldering pads 2-3.

The older files under `pcb/gerber5/` and `pcb/jlcpcb/` describe revision 2.1 and are intentionally unchanged. Do not combine those files with this package.

## Debug and programming access

Rev 2.2 preserves two service interfaces, both excluded from factory assembly:

- `J2` is a row of six 2.54 mm through-holes carrying, from square pin 1 to pin 6, 3.3 V, ground, boot, board transmit, board receive, and enable. Revision 2.2 leaves these holes unpopulated. A header may be soldered into them later, or a custom pogo fixture may contact them.
- `J3` carries the same six signals on a flat, bottom-side Tag-Connect `TC2030-IDC-NL` pattern. It has copper contacts and three alignment holes but no connector component, so it adds no BOM or assembly cost. A compatible cable or reusable pogo clip can make a no-solder connection.

Neither interface is USB. Connecting a Mac requires a 3.3 V USB-to-UART adapter plus the matching cable or fixture; do not connect 5 V logic to these signals. The current Rev 2 enclosure covers both service areas and is unchanged in this revision.

## Production files

- `production/GERBER-OnionStraws-rev2.2.zip`: two-layer Gerbers, plated and non-plated drill files, and the Gerber job file.
- `production/BOM-OnionStraws-rev2.2.csv`: KiCad-generated assembly BOM with DNP parts excluded.
- `production/CPL-OnionStraws-rev2.2.csv`: top-side placement data for the installed parts, including through-hole J1. U1 and the unpopulated J2 header are excluded.

## Before ordering

1. Upload only the revision 2.2 ZIP, BOM, and CPL together. For a no-hand-solder board, request turnkey mixed assembly so the assembler installs both the SMT parts and through-hole J1. Confirm the fabrication preview shows a 2-layer, 1.6 mm board with the expected 88.7 mm by 30.1 mm outline and drill map.
2. In the parts review, confirm all 59 designators are recognized, U1 and J2 are absent, and no substitute has been accepted without review. A September 2026 five-board quote matched 23 of 24 BOM groups, but U4/U5 were unavailable and only four units of U6 (`AP2205-33Y-13`, `C5205181`) were in stock. The inherited Rev 2.1 supplier fields also matched R22's `4K7` value to a 47 kΩ part and R18/R21's `220k` value to a 200 kΩ part. Do not order until those resistor values are confirmed against the intended circuit and every unavailable part is restocked or an exact electrical and pin-compatible substitute is qualified.
3. In the assembly preview, confirm J1 is the EVERCOM `5301-8P8C` (`C3097717`), is installed with its socket opening facing out from the short board edge, and its pins and two locating posts align with the drill preview. Also confirm the pin 5/pin 4 labels are legible. If J1 is missing or the vendor will not assemble it, stop before checkout; that quote would require hand soldering.
4. Confirm whether the target appliance supplies power on connector pin 1 or pin 3. Rev 2.2 defaults to the existing pin-1 power path through `JP2` pads 1-2. A pin-3 appliance requires the documented solder-selector rework; do not connect an unknown appliance until its pinout and supply voltage are confirmed.
5. Order a small prototype batch first. Because the standard BOM includes the ESP32 module, use a current-limited bench supply for first power. Inspect orientation, shorts, and solder joints, then verify the 5 V and 3.3 V rails before allowing a normal Wi-Fi workload.
6. Power the adapter from one source at a time during first bring-up. Do not connect appliance power and USB simultaneously until their rail interaction is measured.
7. Start with passive, receive-only logging. Do not transmit control writes until the appliance model and protocol generation have been confirmed.
8. Verify stable repeated boots without U1 before treating revision 2.2 as a production release.

KiCad 9.0.9 checks found no new electrical or layout finding classes compared with revision 2.1, and the Gerber ZIP passes an integrity check. Existing revision 2.1 ERC/DRC findings and physical prototype validation remain outstanding.
