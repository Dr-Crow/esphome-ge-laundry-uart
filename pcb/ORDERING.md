# Ordering a PCB assembly

This guide describes the common process for ordering a small assembled prototype batch from JLCPCB or a similar service. Always read the selected revision's README first: its component availability, connector orientation, appliance-power behavior, and test status may differ.

[Back to the project overview](../README.md) · [PCB revision index](README.md)

## Choose the revision

New builds should use [Rev 2.2](rev2.2/README.md). A revision's `manufacturing/` directory is one matched package:

- the Gerber ZIP describes the board layers, outline, silkscreen, and holes;
- the BOM identifies the parts to install;
- the CPL identifies each installed part's position, side, and rotation.

Never mix one revision's Gerbers with another revision's BOM or CPL.

## Request the quote

1. Upload the Gerber ZIP to the PCB quote page.
2. Confirm the detected board outline, layer count, thickness, quantity, and drill preview against the revision README.
3. Enable PCB assembly and upload the matching BOM and CPL.
4. For a board that does not require hand soldering, select the assembly option that includes both surface-mount and through-hole parts.
5. Review every substitution. Do not accept a different electrical value, package, pinout, or connector footprint only because the website suggests it.

## Review the previews

Before checkout, confirm:

- the board orientation and dimensions are correct;
- holes and slots appear in the fabrication preview;
- connectors face the intended board edge;
- polarized parts have the expected orientation;
- the assembly side and component rotations look correct;
- all required designators are recognized;
- intentionally uninstalled parts are absent from the assembly list; and
- the quoted assembly service installs every connector that you do not plan to solder yourself.

Save screenshots or a PDF of the fabrication, parts, and assembly previews with the order record. A vendor preview is a required human check; it is not replaced by KiCad ERC/DRC or repository validation.

## Order and bring up prototypes

Order a small prototype batch before committing to a larger run. When the boards arrive:

1. Compare the board and component orientations with the saved previews.
2. Inspect for solder bridges, damaged parts, and reversed polarized components.
3. Use a current-limited bench supply for first power when practical.
4. Verify the expected power rails before starting a normal ESP32 Wi-Fi workload.
5. Test programming and serial communication before connecting to an appliance.
6. Begin appliance testing with passive receive-only logging, then expand testing only after the appliance model and protocol are confirmed.

Record the assembler, order date, approved substitutions, and observed test results. Component prices and inventory change frequently, so treat old quotes as estimates rather than current pricing.
