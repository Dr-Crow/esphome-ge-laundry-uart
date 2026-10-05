# Named cable corridor screen

The [StarTech USB2CC2M manufacturer drawing](https://sgcdn.startech.com/005329/media/sets/USB2CC2M/Diagram/USB2CC2M_Diagram.PDF) gives maximum overmold dimensions of 12.2 × 6.5 × 22.7 mm. The new `review_usb_corridor.py` checks that rectangular maximum at **explicitly supplied** shoulder X and axis Y/Z. It never derives the native mating face from the substitute GCT STEP model.

The following tests use **hypothetical coordinates**, a 0.25 mm geometric reserve and the current internal-antenna lid. The axis is the earlier proxy-based `5.25 + stack + 3.55` sensitivity, not a manufacturer or measured native USB datum. Positive volume is overlap of the expanded rectangular screen; unmeasured body corners may reduce real overlap. A zero result is conditional clearance for these parameters, not complete cable fit.

| Case | X100 shoulder | X101 shoulder | X102 / X104 shoulders |
| --- | ---: | ---: | ---: |
| C3, 11.65 mm stack, 1.6 mm switch reference | 0 | 0 | 0 |
| C6, 10.35 mm stack, 0.45 mm switch reference | 0.545394 mm³ | 0.081958 mm³ | 0 |
| C6, 11.65 mm stack, 0.65 mm switch reference | 5.272140 mm³ | 0.792261 mm³ | 0 |

All base intersections are zero. The source-hashed [C3 upper](c3-upper.json), [C6 lower](c6-lower.json) and [C6 upper](c6-upper.json) receipts preserve every input and result. They establish that actual shoulder/axis position matters; **they do not select a cable or justify trimming a button support from an assumed position**.

Run the tool with the recorded pinned CAD environment and explicit module, antenna, installed stack, independent BOOT/RESET heights and stops, axis Y/Z, repeated shoulder X values, datum description and output path. Use `--help` for the argument names. The switch stops remain review parameters; no profile supplies safe overtravel. `review_dimensions.py` exposes named conditional C3 family-A/B and C6 Jinbeili/Alps height references without changing the fitted default.

The native UBF31-0171 mating face, axis and insertion depth remain unresolved. The tool excludes metal-shank mating, finger access, actual strain-relief section/bend, cable retention, print shrinkage and tolerances. These are distinct checks. Disconnect appliance RJ45 before powered USB.
