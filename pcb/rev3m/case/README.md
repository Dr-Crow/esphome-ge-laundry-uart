# Rev 3M printed enclosure

The PCB measures 59.944 × 27.432 × 1.6 mm. Its enclosure measures 67.144 × 35.432 × 31.9 mm when closed, plus 0.02 mm at the light-guide tips. Use the common base, the lid marked for the module, and the three clear printed guides. Both lids have integral printed BOOT/RESET buttons, springs and friction closure. The closed lid covers USB. Unplug the appliance cable before opening it to connect USB.

[Editable generator](generate.py) · [Common base](common-base.step) · [C3 lid](closed-usb-lid-c3.step) · [C6 lid](closed-usb-lid-c6.step) · [Solid-model checks](case-checks.json)

The two posts follow the routed hole centers. Each guide is registered to its LED. The C3 layout reserves a U.FL plug and a 28.31 mm cable path, with a 5 mm modeled bend radius and a 40 × 20 mm flexible-antenna pocket. The C6 ceramic antenna has 9.45 mm modeled lid clearance. The case uses an 11 mm module stack assumption. CAD checks report zero nominal intersection between the PCB envelope and each case half, and between each lid and its guides. The friction closures intentionally engage by 0.42 mm³ per lid.

Dry-fit both module variants and the actual cable, socket headers, printed buttons, antenna and latched plug. Check retention, travel, light visibility and RF behavior. No physical sample has been tested. STEP and STL are in millimetres. To regenerate, run Python with build123d 0.10 and retain the sibling `pcb/rev3k/case/support` and `pcb/rev3e/design/models` directories.
