# Rev2 schematic alias normalization candidate

Candidate checkout: `/workspace/shared/ge-oct4-rev2-erc-normalize`

Exact input: `24dd93b0cb633c889765108397380a0e438393fa`

Candidate: `ab7e7341d43cdce956606b80f058802d8eda3c6d`, branch `fix/rev2-power-net-aliases`

Owner commit: `fix(pcb): normalize Rev2 schematic net aliases`; author and committer
`Dr-Crow <9339757+Dr-Crow@users.noreply.github.com>`. Only the schematic and local
symbol library are committed. No integration, publication or hardware action.

## Bounded source delta

- `GLITCHES` local label becomes the already exported canonical `DBG_LED`.
- Remove the two redundant processor-side `RXD`/`TXD` labels, which already sit on
  original wires joined to canonical global `GEA3_TX`/`GEA3_RX` annotations.
- Convert the four connector-side UART local labels to those canonical global
  labels on the same original J2/J3 pin attachment coordinates. Their global
  shape remains the original project's `input` presentation. Native pin functions
  still identify ESP receive/transmit; no physical direction or net changes.
- Present original U4 pin 5 (`VCC`, `power_in`) explicitly on both units. Its body
  contact remains local `(0,2.54)` with a visible 3.175 mm lead ending at
  `(0,5.715)`; remove the hidden flag and mirror this presentation in the local
  `74LVC2G07` symbol. Pin 2 GND remains unchanged. Number, name and electrical type
  are unchanged.
- Retain original `#PWR028`/`#PWR034` UUIDs, reference/value strings and orientations;
  shift each original +5V annotation +5.08 mm x/+6.35 mm y and connect the new
  visible pin endpoint using two short right-angle wires. Shift U4 reference/value
  text -3.81 mm x for readability. Four annotation wires are added, no originals
  altered. Three existing PWR_FLAGs remain byte/metadata identical.

`annotation-delta.json` records every label/annotation UUID and coordinate change.

## Verified native outcome

Genuine KiCad 9.0.9, activated from `/workspace/shared/ge-oct3-tools/activate.sh`:

- All-severity ERC: input 0 errors/4 warnings; candidate 0 errors/0 warnings,
  0 exclusions.
- All-severity/all-track-error DRC with schematic parity: 0 violations,
  0 unconnected items, 0 parity issues.
- Exact 186 unique physical ref/pin/net/name/type memberships, 45 net names and
  codes, complete component/libpart/library exported metadata.
- Exact complete native board metadata: 73 footprints, 222 pads, 712 track/via
  items, 483 board drawings, 905 footprint graphics. Fresh unchanged-board native
  metadata also equals tracked `current-geometry.json` exactly.
- All original schematic routing, no-connect/junction/text/image/sheet objects
  remain exact except the seven recorded label presentations. Original physical
  symbol instance metadata remain exact; only the recorded power/text positions
  and U4 pin5 presentation differ.
- 190 of 192 tracked input files are byte-identical. The preserved inventory is
  `preserved-tracked-sha256.json`: every PCB, project/rule/grid file, local
  footprint, BOM/CPL, historical archive, current CAM, board render and firmware
  file. Historical PCBA ZIP SHA256 remains
  `b9c0b397806d3a719c32faa83c08bac2e80aa1c1d4d27d3e6d6a35cd5381445a`.
- Regenerated all nine current Gerbers and separate PTH/NPTH drills; all 11 payloads
  match retained current CAM after removing generation-date header lines only.
  Retained files and archives are unchanged. `cam-regeneration-parity.json` records
  both raw byte hashes and this narrow metadata normalization.
- Native source-fixture negative controls (temporary design copies only) detect
  changing U4.5 +5V to +3V3 and swapping U2.11/U2.12 canonical UART net attachments.
  Both retain all 186 pins and original pin names/types. Additional comparison-only
  graph and complete-board U4 pad5 controls are also detected.
- Native schematic PDF and full sheet/U4A/U4B/J2-J3/processor crops inspected.
  Explicit VCC number/name, bent leads and original power arrows are clear.
  `visual-inspection.json` binds the final PDF to identical inspected render pixels.

The original manual selector, APX803L/ESP32-C3 processor arrangement, L7805/AP2205
power architecture, every interface, and all physical pad/net memberships remain.
Ratings, legacy U1 boot-loop, module/regulator identity discrepancy, supplier
rotations/procurement, physical powering, qualification and hosted CI gates remain
open. ERC success establishes schematic annotation consistency only.

## Integration replacements and source-binding work needed

The source-only candidate deliberately leaves the older tracked review package
intact. Do not claim that its ERC4 reports or source ZIP describe the candidate.
When integrating, perform these explicit updates:

1. Replace current `pcb/rev2.0/native-review/schematic.pdf` with the inspected
   `after-schematic.pdf`; replace current native `netlist.xml` with fresh integrated
   native export (our `after.net.xml` has exact physical graph/metadata).
2. Refresh `reports/erc.json`, `reports/drc.json`, `reports/native-summary.json`
   against the integrated final source using all severities, all track errors and
   schematic parity. Replace the current warning classification with a source-bound
   annotation-delta record that retains the four baseline warnings as historical
   findings and records their explicit corrections; current warnings/exclusions=0.
3. Update `proof/validate_native.py`'s hardcoded ERC4 alias expectations to exact
   zero; preserve native version, genuine tools, sequential temp-copy validation,
   grid, rules and all parity checks. Add source-specific native negative controls.
4. Amend `proof/verify_cleanup.py` only for this recorded annotation delta. Its
   historical top-level label/wire fingerprint, original symbol-instance exact
   comparison, and exact recovered `74LVC2G07` definition checks currently reject
   these intended changes. Apply exact UUID/coordinate/pin5 exceptions and require
   all other original data, 186 pin memberships/45 partitions and complete board
   metadata to remain exact. Do not replace historical `input-*` fingerprints or
   reset their baselines. Record fresh candidate input hashes separately.
5. Preserve `symbols/source-map.json`'s original-to-local mapping and
   `RESTORED-PROVENANCE.json`'s historical blob evidence. Add explicit presentation
   exception/source-bound delta metadata for `74xGxx:74LVC2G07` ->
   `LegacySymbols:74LVC2G07` pin5; original recovery remains provenance, while the
   candidate definition is no longer byte-exact recovered presentation.
6. Update `design/README.md`, revision `README.md`, `native-review/REVIEW.md`
   and `STANDALONE-REVIEW.md` statements about four retained aliases, hidden U4 VCC,
   all labels/pins unchanged, and documentation-only standalone adjustment. Clarify
   schematic labels now use canonical GEA3 nets while physical board silk, original
   archive markings and endpoint map remain unchanged. Retain the UART VCC caution
   and all electrical/procurement/physical gates.
7. Refresh `reports/source-hashes.json` and `reports/deliverable-hashes.json` with
   final integrated source/report/PDF hashes and source commit. Current native source
   ZIP contains pre-normalization source; preserve its old bytes as a historical
   snapshot and prepare a separately paired refreshed current native source package,
   then update `reports/current-archive-hashes.json`. Preserve current/historical
   CAM archives and payload bytes; their PCB binding stays exact at
   `73cf5b1aec5182b9e162540e9a4b7897b89c961b958dfe228d6fe3530fc8826c`.
8. Refresh carrier-level source/deliverable/CI manifests or evidence matrices that
   point to baseline source `24dd93b0...` or ERC4; bind them to the final integrated
   commit, new schematic/library hashes and exact annotation proof. No PCB/CAM,
   BOM/CPL, placement or firmware source hash should change. Hosted CI still needs
   to run against that final integrated commit.
