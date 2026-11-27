# Rev 3L printed enclosure study

Use one common base, the lid for the installed XIAO, and the three matching light guides. The 65 × 30 × 1.6 mm PCB registers on two locating posts. The closed enclosure measures 72.2 × 38 × 31.9 mm before the 0.02 mm guide-tip projection. Rev 3K has a 70 × 32 mm PCB and a separate 77.2 × 40 × 31.9 mm case.

The lids have integral printed BOOT and RESET buttons and return springs. The closure uses friction tongues. The USB opening is closed in use. Remove the appliance cable before opening the case to use USB. The enclosure provides no electrical isolation rating.

[Common base](common-base.step) · [C3 lid](closed-usb-lid-c3.step) · [C6 lid](closed-usb-lid-c6.step) · [Geometry checks](case-checks.json)

## Module and optical fit

The C3 design reserves the U.FL plug, a 29.23 mm modeled lead path with a 5 mm minimum modeled bend radius, and a flexible antenna pocket. Check the actual assembly's unbent lead allowance, connector retention and cable bend specification. The C6 design leaves 9.45 mm from the modeled ceramic antenna to the lid. Confirm RF operation in the installed case.

The D4 light guide exits 3.2 mm off its inlet axis to clear the C3 BOOT mechanism. In the solid-model checks, both lids clear the board envelope and all three guides. The captive PCB sleeve has 0.37 mm nominal vertical clearance at 1.6 mm PCB thickness. The friction features intentionally interfere by 0.42 mm³ per assembled lid. Confirm the print's latch force, button rest gaps, return travel, jack latch, light visibility and socket stack before adopting the enclosure. Physical print and populated fits remain open.

STEP and STL pieces use millimetres. Run `python3 generate.py` with build123d 0.10 and the sibling Rev 3K case support directory available to regenerate all solids. The PCB remains an incomplete routing prototype.

