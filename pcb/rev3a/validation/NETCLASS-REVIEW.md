# Rev3A hierarchical netclass correction

Reviewed public source: `origin/design/rev3a-pr` at
`a5a9fac87cbcb59d337a1fb8d3084ad18867a3e6`.

Seventeen exact netclass patterns omitted the leading slash of the corresponding
hierarchical net. Each corrected pattern now exactly names an existing PCB net;
none assigns a class to a guessed or absent net. Class clearances, routed-width
settings, custom rules, severities and exclusions are unchanged.

Pinned native KiCad 9.0.9 and libraries reproduced the original configuration at
zero ERC errors / 53 warnings and zero DRC errors / seven warnings, with zero
unconnected or schematic-parity findings. That configured pass did not exercise
all intended Power checks. Correct patterns expose 57 Power clearance errors
under standard track aggregation, or 62 using `--all-track-errors`; both retain
seven warnings before the separate silkscreen cleanup. All errors request the
existing 0.25 mm Power clearance. No copper is changed here.

The [pattern list](native-kicad-9.0.9/pattern-corrections.json), original reports
and intended reports in [native-kicad-9.0.9/](native-kicad-9.0.9/) preserve the
actual evidence. Earlier KiCad 9.0.2 courtyard findings must retain their own
version/source/library context; this exact-head 9.0.9 run found no courtyard
violation. The older historical report is not reclassified as erroneous.

Resolve the exposed routing findings under the selected dual-input architecture
before fabrication; do not lower the Power threshold or add automatic waivers.
Neither this rule-assignment correction nor a geometric DRC result settles input
protection, source selection, current/thermal capacity or physical qualification.

The later isolated [routing repair](CLEARANCE-REPAIR.md) resolves all 62 expanded findings under these exact assignments and unchanged thresholds. That repair changes only tracks/vias; this pattern-correction report and its original/intended62-finding evidence remain historical. The current native reports have zero errors and retain 53 ERC/five DRC warnings, with zero unconnected/parity. Process-margin and independent electrical/physical gates remain open.
