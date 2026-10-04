# Rev3A native source review, October 3, 2026

**The later intended-clearance routing repair now has zero errors.** Native KiCad 9.0.9 retains the same 53 ERC and 5 DRC warnings, with zero unconnected/parity under unchanged rules. No footprint, part identity, pin net, project/custom rule, firmware or case position changes. Via annuli, two new PIN3_EN control vias, and the TP12 physical-margin limit are documented in [CLEARANCE-REPAIR.md](CLEARANCE-REPAIR.md). Electrical/process/physical qualification remains open.

The earlier metadata-review stages below describe frozen `a94c46e7456edd8d267fc0e4bf7b64c01a580e7f` and its predecessors. At that stage no copper changed and62 intended routing findings remained. Historical reports/classification are retained, while the current [routing proof](native-kicad-9.0.9/clearance-repair-proof.json) and manifest bind the repaired source.

## Source and exact native results

Public starting head: `origin/design/rev3a-pr` at
`a5a9fac87cbcb59d337a1fb8d3084ad18867a3e6`. Native executable: KiCad **9.0.9**,
with symbols `ad36cd14bcd1b1cd0484f629ccdd3481366f74f3` and footprints
`2b941bf1d97862be429793b46fd52a5add09a2fc`, both official 9.0.9 libraries.
The [manifest](native-kicad-9.0.9/manifest.json) binds the exact source and assets.

| Stage | ERC errors/warnings | DRC errors/warnings | Unconnected/parity |
| --- | --- | --- | --- |
| Original configured source | 0 / 53 | 0 / 7 | 0 / 0 |
| Correct exact netclass patterns, original silk | 0 / 53 | 62 / 7 | 0 / 0 |
| Frozen a94 source, fabrication-layer silk cleanup | 0 / 53 | 62 / 5 | 0 / 0 |
| Current intended-clearance routing repair | 0 / 53 | 0 / 5 | 0 / 0 |

These DRC totals use `--severity-all --schematic-parity --all-track-errors`.
Without all-track-errors, the recorded intended/current clearance totals are
**57**, while original remains zero. Repeated standard-aggregation runs during
this metadata refresh yielded 56 and 57 errors on the identical source; the
all-track-errors result remains 62 and was the frozen stage's blocking clearance count. Current routing reports have zero errors. Exclusion counts are zero throughout. Existing ignored
rule categories remain as configured; this cleanup changes no severity and adds
no exclusion. `--exit-code-violations` returns 5 for warning-inclusive reports because
reviewed warnings remain; the present routing repair has zero error-level findings. A successful report-generation exit without that flag is not a
DRC pass.

Seventeen patterns missed exact slash-prefixed hierarchical nets, including the
PIN1/PIN3 rails, V_INPUT, USB labels and BUCK_BST. Corrections preserve every class
threshold and custom rule. The original configured pass therefore cannot stand
in for the intended Power check. Details: [NETCLASS-REVIEW.md](NETCLASS-REVIEW.md).
Earlier KiCad 9.0.2 review reported six courtyard findings. On this exact public
head, pinned 9.0.9 reports no courtyard violation; keep the earlier report's own
version/source/library context rather than declaring that historical evidence
wrong. No courtyard geometry was changed in this Rev3A cleanup.

## Clearance findings and warning status

Every one of the 62 expanded findings requests the existing **0.25 mm Power**
clearance. They are geometric rule conflicts, not 62 independently proven
field-failure mechanisms:

- 26 SMD pad/track conflicts. Examples: U10 pad 6 at (60.1375, 26.0500), GND
  route clearance 0.2298 mm; R32 pad 1 at (49.0875, 31.0000), PIN3_GATE_CLAMP
  route clearance 0.2368 mm; R34 beside V_INPUT, clearance 0.2037 mm.
- 22 track/via conflicts. Examples: PIN3_SW_OUT beside a D6-anode via at
  (63.6446, 32.5178), clearance 0.2051 mm; V_INPUT beside the PIN3_GATE via
  at (61.3726, 29.3539), clearance 0.2016 mm.
- Nine track/track conflicts. Examples: GEA2_TX beside V_INPUT near
  (57.5000, 35.9483), clearance 0.2281 mm; BOOT beside ALT_PWR on B.Cu,
  clearance 0.2194 mm.
- Five J1 through-hole-pad/track conflicts. Example: ALT_PWR beside J1 pad 8
  at (16.5100, 21.4450), clearance 0.2017 mm.

There are **zero zone conflicts, intrinsic same-footprint pad/pad conflicts or
cross-footprint pad/pad conflicts** in this reported set. The retained local
J4 locating-hole minimum of 0.18 mm applies to that footprint's hole clearance;
it is unrelated to these copper findings. No narrower applicable copper rule
was identified. [Full classification with UUIDs and locations](native-kicad-9.0.9/clearance-classification.json).

The four unprintable U2 antenna outline/marker graphics were moved from F.SilkS
onto F.Fab with their geometry preserved. This resolves the two board-edge silk
warnings. Five retained footprint/library differences remain at D2, C5, SW2,
TP13 and U2. ERC remains 44 embedded-symbol differences, eight USB off-grid
warnings and one +5V/hidden-VCC alias. They remain visible for review; this
cleanup adds no automatic waiver.

## Part and export consistency

The native schematic export has 112 listed components including an excluded
alternate J3; PCB has 111 footprints. There are exactly **93 fitted top-side
BOM/CPL references, 40 distinct purchasing parts and 44 value-specific BOM
rows**. Four formerly mixed-value groups are split by exact native Value; the
manufacturer part-number header now uses the native field name MPN. Reference
sets, LCSC identifiers, manufacturer/MPN, quantities and footprints are unchanged. All 93 CPL positions,
rotations and sides are unchanged; the final CPL is byte-identical to the public
source package.

The refreshed BOM also restores eight previously blank metadata cells from the
committed schematic: forward/reverse ratings of D10/D11; F3 hold current; L1
rated/saturation current; U6 output current; U8 input-range/output-current fields.
These are metadata reproduction, not new part selections or current design
ratings. Source-derived output-current fields do not establish available appliance
power or thermal capacity.

All four copper Gerbers, paste, mask, board outline, rear silk and both drill
payloads reproduce the old package after excluding creation timestamps. Only
front silk changes. The refreshed matched archive contains 14 files. The later metadata normalization
also aligns three saved plot settings with that existing archive: Protel filename
extensions enabled, no drill-center markers, and solder mask subtracted from
silkscreen. The enhanced manufacturing check reproduces all 13 Gerber/drill
payloads and job metadata while ignoring only creation timestamps. Archive bytes
and circuit geometry are unchanged. Schematic,
assembly, outline and drill-map PDFs, all four layer SVGs, and all four populated
native renders were refreshed from this source. Exact referenced stock STEP
models were fetched from official KiCad packages3D 9.0.9 commit
`a0244fe3442823dbb052ebc4820b4c2951e1742c`; their
[URL/hash receipt](native-kicad-9.0.9/stock-model-provenance.json) records the inputs.
Assembly/outline PDF page boxes are cropped around native vector content with
a 12-point margin for readable review; no geometry is transformed. The existing
assembly reference-label positions remain crowded and need review at high zoom.
Connector/enclosure envelope models remain geometric aids requiring real-part fit
qualification. The 3D pictures are not mechanical approval.

## Independent electrical gates

These remain design-review gates independently of CAD cleanliness:

1. **Transient/rating coordination.** Exact D18 SUNMATE SMF16A is connected from
   PIN1_PROTECTED to ground. Its author-published data specify 16 V standoff,
   17.8–19.7 V breakdown and 26 V clamp at 7.7 A under the stated 10/1000 us pulse
   conditions. [TPS22810](https://www.ti.com/lit/ds/symlink/tps22810.pdf) VIN is
   recommended only to 18 V and absolute maximum 20 V. The SMF16A clamp rating
   alone therefore does not establish protection of U9 at its allowable stress.
   Bound actual waveform, source impedance, overshoot and energy and resolve the
   coordination. This is not a claim that every appliance will produce that pulse.
2. **PMOS orientation and gate stress.** Native source maps Q3/Q4 source pin 2
   to the respective fused input and drain pin 3 to the protected rail. Review
   body-diode direction and reverse-current behavior in every powered/unpowered
   state. Ground-referenced D16/D17 are not by themselves proof that CJ3407 VGS
   remains within its ±20 V maximum; check gate/source waveforms and exact diode
   polarity. The [manufacturer CJ3407 drawing](https://www.jscj-elec.com/pdf/f3fb09e55afae446e8a8f8a35ab44e62.pdf)
   is the reference. No orientation or gate-network edit is made here.
3. **PIN3 path and source selection.** D18 is on PIN1 only; PIN3_PROTECTED/U10
   requires its own justified transient envelope. The existing diode-OR/buck path
   must also support the verified PIN3 supply: a nominal 5 V PIN3 source cannot be
   presumed to make regulated 5 V through a fixed-5 V AP63205 buck plus path drops.
   Preserve both original inputs and automatic behavior while choosing and
   independently reviewing any necessary design change.
4. **Available current and thermal margin.** Measure source current availability
   across appliance operating states, startup/inrush, Wi-Fi load, fuse derating,
   switch/diode drops and enclosed regulator temperature. Component headline
   ratings and a native ERC/DRC pass do not establish this system budget.
5. **Manufacturing and physical qualification.** First resolve intended clearances
   without lowering rules, complete independent pinout/polarity/land-pattern review,
   regenerate the package, then review fabricator previews. Only separately
   authorized current-limited bench qualification can test USB isolation, all eight
   dual-input/USB combinations, both handoff directions, enclosure/antenna behavior
   and eventual appliance compatibility. None of those hardware tests ran here.

No remote PR, publish, purchase, sign-in or appliance test was performed.
