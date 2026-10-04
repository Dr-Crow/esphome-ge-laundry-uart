# Rev3A schematic ERC normalization

This isolated cleanup starts from `60ccb434ea4bb9c9e0cde7bbac36a15220b23a0e`.
The input identifies electrical freeze
`d2bde08da836b493f76de03d330aa0489e2c3419`; that imported freeze is provenance,
not a second circuit being modified here.

Genuine pinned KiCad **9.0.9** reproduces **0 ERC errors / 0 warnings**, and both
standard and all-track, all-severity DRC with schematic parity reproduce
**0 errors / 0 warnings / 0 unconnected / 0 parity findings**. All checks include
exclusions; none exist. The pre-edit native ERC has exactly eight off-grid USB
symbol warnings and one hidden VCC/+5V naming warning. No rule, grid, severity,
exclusion, component selection or circuit topology changes.

## Changes and electrical proof

- Translate J4, U7, R26/R27, F3, R28/R29 and D10 onto the existing **25 mil /
  0.635 mm** connection grid. Their 35 pin endpoints, rotations and directions
  remain faithful to their original definitions. All 27 attached local labels and
  two no-connect markers follow the exact translations. None of these USB
  endpoints has an attached wire or junction; every original wire and junction
  is unchanged.
- Expose only U4's common **pin 5 VCC** in the cached schematic and matching local
  symbol library. Preserve its name, number, power-input type, position, direction,
  zero length and every other definition property, including hidden GND. Move
  the two existing +5V symbols 3.175 mm outward without changing their identities
  or rotations, and connect them to the original VCC endpoints with two explicit
  wires. Shift U4's reference/value text 3.81 mm left for readable clearance.
  No pin is renamed to a net name.
- Before/after native XML netlists have identical **301 unique
  (reference, pin, net, pinfunction, electrical-type) tuples**, all 72 net names
  and codes, and all component and netlist library metadata. U4 pin 5 remains
  `+5V`, pinfunction `VCC`, type `power_in`; pin 2 remains GND. A comparison-only
  negative fixture changes U4 pin 5 to +3V3 while preserving the 301-node count;
  the comparator detects exactly the missing +5V tuple and added +3V3 tuple.

[PROOF.json](PROOF.json) binds source hashes for all 25 closure files, report and
artifact hashes, the native command results, and preservation checks.
[pin-preservation.json](pin-preservation.json), the full native netlists,
[coordinate-remap.json](coordinate-remap.json) and [verify.py](verify.py) retain
reviewable evidence. The verification script compares this isolated cleanup with
its exact input commit; later unrelated integration changes require their own
source-bound validation.

Actual pixels of the fresh native [schematic PDF](schematic.pdf) were inspected
at full-page scale and in the [USB crop](usb-group.png) and
[U4A](u4a.png)/[U4B](u4b.png) close-ups. The exposed VCC names, pin 5 numbers,
wires and +5V symbols are legible without overlap. The USB labels and no-connect
markers remain attached to the intended endpoints.

## Byte preservation and integration refresh

Only the schematic, its matching LegacySymbols definition/source map, and two
status documents differ among the 172 pre-existing tracked files. The other 167
are byte-identical, including the actual PCB, project/custom rules, every BOM,
CPL and CAM archive, all footprints/models, firmware and case files. The fitted
97-reference package and its prior manufacturing comparison are unchanged.
This is a schematic presentation cleanup; no hardware test or supplier action
was performed.

This separate proof/PDF is current for the cleanup. The prior
`rated-protection-manifest.json`, rated-protection native reports and package
schematic PDF retain their pre-cleanup bytes and must be refreshed by the
integrator before claiming one fully refreshed release package:

1. Replace the package schematic PDF with a fresh native export of the integrated
   source and recheck its pixels. Other board-derived pictures/assembly PDFs have
   unchanged PCB inputs.
2. Rerun native ERC and both DRC variants on the integrated source. Refresh their
   source hashes, report hashes/dates and ERC counts/classes in the manifest;
   all 25 closure hashes must match the integrated source. The changed closure
   files in this cleanup are the schematic and LegacySymbols library only.
3. Refresh source-bound proof/manifest links and any manufacturing-comparison
   metadata that binds the schematic SHA. Regenerate/check BOM/CPL/CAM under the
   existing export workflow and confirm the retained purchasing/placement tuples
   and normalized CAM payloads. Their current bytes were preserved here.
4. Run the integrated candidate's genuine strict ERC/DRC gates without a warning
   waiver or baseline allowance. Physical, ratings, process and appliance gates
   remain as documented in the main Rev3A review.

## Reproduce the native checks

Activate `/workspace/shared/ge-oct3-tools/activate.sh`, then from the repo root:

```sh
kicad-cli version
kicad-cli sch export netlist --format kicadxml -o pcb/rev3a/validation/erc-normalization/after.net.xml pcb/rev3a/design/GEA-Adapter-Rev3A.kicad_sch
kicad-cli sch erc --format json --severity-all --exit-code-violations -o pcb/rev3a/validation/erc-normalization/after-erc.json pcb/rev3a/design/GEA-Adapter-Rev3A.kicad_sch
kicad-cli pcb drc --format json --severity-all --schematic-parity --exit-code-violations -o pcb/rev3a/validation/erc-normalization/after-drc-standard.json pcb/rev3a/design/GEA-Adapter-Rev3A.kicad_pcb
kicad-cli pcb drc --format json --severity-all --all-track-errors --schematic-parity --exit-code-violations -o pcb/rev3a/validation/erc-normalization/after-drc.json pcb/rev3a/design/GEA-Adapter-Rev3A.kicad_pcb
python pcb/rev3a/validation/erc-normalization/verify.py
```

Fresh native report/export timestamps will change their file hashes; refresh the
proof artifact hashes after regenerating them. Reports retain native date/time
formatting rather than rewriting it. Baseline exports were captured before any
source edit; their hashes and all 172 original tracked hashes are retained.
