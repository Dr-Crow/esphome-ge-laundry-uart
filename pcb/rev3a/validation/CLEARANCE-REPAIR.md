# Rev3A intended-clearance routing repair

This isolated candidate starts from frozen `a94c46e7456edd8d267fc0e4bf7b64c01a580e7f`. All 62 expanded routing conflicts are resolved under the original intended **Power 0.25 mm / Switching 0.30 mm** rules. Every assignment, global minimum, custom rule, severity and exclusion remains unchanged. This is a digital routing repair; electrical, fabricator-process and physical qualification remain open.

## Native result and preserved source

KiCad **9.0.9**, with the pinned official libraries, reports **0 ERC errors / 53 warnings** and **0 DRC errors / 5 warnings**, with all severities, all track errors and schematic parity included. There are zero unconnected, parity or excluded findings. Standard aggregation also has zero errors. All warning dictionaries match the frozen source exactly; a command using `--exit-code-violations` still returns nonzero because those warnings remain.

All 111 complete footprint subtrees, 315 pads, 71 PCB nets, outline, mounts and interface/case-critical placements are unchanged. Schematic, project, custom-rule, firmware and case files are byte-identical to the baseline. Both appliance inputs, original automatic PIN1 priority, original PMOS orientation/gate network, TPS22810 switches, PPTCs, AP63205 and USB/module/LED functions remain. No part value, manufacturer, MPN, LCSC identity or pin net changes.

The native BOM still reproduces **93 fitted references, 44 value-specific rows and 40 distinct purchasing tuples**. Native CPL conversion remains byte-identical. The unchanged schematic PDF, assembly drawings and part models retain their existing geometry. Current source/export hashes and UUID deltas are bound in the [routing proof](native-kicad-9.0.9/clearance-repair-proof.json) and [manifest](native-kicad-9.0.9/manifest.json).

## Bounded routing change

The original classification remains historical evidence: 26 pad/track, 22 via/track, nine track/track and five J1 PTH-pad/track entries. These are routing conflicts, not intrinsic package gaps or demonstrated appliance failures.

Local connected-node moves and a few short track segments open the left ALT_PWR/BOOT/USB corridor, PIN1 branch, central V_INPUT/GND corridor and PIN3 branch. Every existing track width and layer remains unchanged. PIN3_EN's former Q4 squeeze-route cannot accommodate the 0.20 mm trace with the intended 0.25 mm clearances. A short B.Cu control detour with two ordinary through-vias preserves the same enabled pins and automatic priority. Its two F.Cu connections and underlying ground-reference/return region were inspected in actual native copper pixels. No footprint moved.

Nine existing vias change from **0.80/0.40 mm to 0.68/0.40 mm**, giving **0.14 mm nominal annuli**: BOOT, LED2, GEA2_RX, GEA2_TX, two D6-A vias, V_INPUT, PIN3_GATE and USB_VBUS_FUSED. The JP1-A via changes to **0.72/0.40 mm**, giving **0.16 mm**. Drill diameters and positions of those ten vias are unchanged. Two new PIN3_EN vias use 0.68/0.40 mm. Their exact UUIDs, nets and coordinates are in the proof.

Native board minima remain 0.05 mm annulus, 0.40 mm via diameter, 0.30 mm drill, 0.20 mm track width, 0.20 mm global clearance and 0.25 mm hole clearance. The [current JLC rigid capability table](https://jlcpcb.com/capabilities/pcb-capabilities) separately gives a via diameter at least 0.10 mm larger than its hole, with 0.15 mm preferred; these diametral differences are 0.28/0.32 mm. The table's PTH component-pad category is more conservative and must not be substituted for its via-specific guidance. Nominal CAD annuli are not finished annuli. Drill registration, plating and etch tolerances, finished annular acceptance, and actual stack-up/process approval remain fabricator gates.

The TP12/D5-A corridor has a measured native clearance of **0.2502 mm**, only **0.2 µm** above its 0.25 mm rule. A stricter 0.26 mm diagnostic rule was used only in a separate measurement copy; the production rules are unchanged. That very small excess is a geometry pass, not a physical tolerance guarantee. The immediate GEA_FullRx neighbor has about 0.2002 mm clearance, so the additional 9.8 µm cannot come from that gap alone. A bounded 20 µm corridor shift introduced 19 conflicts; the refined 12 µm shift produced 0.1897 mm at R21-Pad1/USB_VBUS. A short back-layer bypass also encounters JP1-A, V_INPUT and BOOT. These probes rule out those simple moves, not every possible staggered reroute. The [exact diagnostic and local constraints](native-kicad-9.0.9/tp12-margin-review.json) retain the margin/process gate; no failed-trial change entered production.

## Exports and qualification limits

All four copper layers and the plated drill payload are regenerated. Unchanged paste, mask, silkscreen, outline, non-plated drill and job payloads are preserved after comparison with fresh native exports excluding only creation dates/checksums. The matching ZIP has 14 members. The plated map includes two additional 0.40 mm control vias; no blind/buried, filled-via or bottom-assembly process is added. BOM/CPL bytes are preserved after native reproduction checks.

Actual native outer/inner copper pixels, plated drill-map pixels and populated renders are inspected. These establish layout/export consistency. The original D18/TPS22810 stress mismatch, PMOS orientation/gate-stress review, PIN3 protection/headroom, source-current/thermal limits, USB isolation, enclosure and RF gates remain in [NATIVE-REVIEW.md](NATIVE-REVIEW.md#independent-electrical-gates). No manufacturing approval, appliance compatibility, order, remote publication or physical test follows from zero routing errors.
