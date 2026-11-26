# Rev 3E bring-up pads — local review receipt

Base: `51290d40f108aecdcfc82cfb931b62a74badd511` (`work/rev3c-first-fit`).
This is a bench-prototype review candidate, not an order-ready fabrication release.

- Added six unpopulated probe footprints, eight short traces, and one FLT escape via; existing routing, outline, footprint locations, and every existing net except the two formerly unconnected FLT pins are unchanged. Native schematic netlist comparison confirmed all other original pin-to-net memberships. Refilling the original copper zones changes their generated polygon cache, not the zone definitions.
- TP13 AUXOFF1 front (51.80, 16.20 mm); TP14 PIN3_OV back (49.4025, 21.10); TP15 plated GND_MUX accessible on both sides (52.00, 25.60); TP16 GND_ESD front beside U11 ground (22.50, 12.60); TP17 PIN1_FLT_N front (56.05, 16.25); TP18 PIN3_FLT_N back (56.20, 21.12). Coordinates are in KiCad board view.
- KiCad 9.0.2 native full-severity ERC: 0. Native DRC with all-track errors and schematic parity: 0 electrical/layout violations, 0 unconnected items, and 0 parity errors; the same 62 library-footprint-mismatch warnings on the same footprints as the unmodified base in this installation. No new warnings or overrides.
- Regenerated native Gerber and split-drill archive, tested ZIP integrity. BOM and CPL are byte-identical to the base (69 assembled references); the six copper pads add no placed parts. C30 remains unpopulated. The added plated ground probe is a PCB fabrication feature, not an assembly step.
- Repository preflights pin KiCad 9.0.9, so the hardware, rules and manufacturing validators stopped at the version check here. The Python suite ran 38 tests: 35 passed and three hit that same KiCad version check. Run pinned native/CI again before fabricating. No bench tests or fab preview/quote performed.
