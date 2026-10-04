# Revision 3A manufacturing review package

The selected rated-protection backport retains the integrated ESP32-C3/AP2112K architecture and both original GE inputs/automatic PIN1 priority. Matched source/export evidence is in [the current manifest](../validation/rated-protection-manifest.json) and [protection review](../RATED-PROTECTION.md). Native consistency is established; this is an unqualified prototype package.

- [Gerber/drill archive](GERBER-GEA-Adapter-Rev3A.zip):14 members, with creation-time-only comparisons preserving unchanged payload bytes.
- [Native BOM](BOM-GEA-Adapter-Rev3A.csv):97 fitted references,49 exact-value/full-footprint groups,42 exact LCSC/manufacturer/MPN purchasing tuples. Every ref is explicit; DNP items are excluded.
- [Supplier CPL](CPL-GEA-Adapter-Rev3A.csv):97 top-side references, paired to the BOM. J1/U2 use source-bound nominal body-centroid corrections; J4 uses its verified centered body datum. Native position export is preserved separately in validation for provenance.

The outline remains88.7×40.0 mm, four layers,1.6 mm. Native plated drills are0.30 mm minimum; newly routed vias have0.7/0.3 or0.8/0.4 mm diameters/drills and0.20 mm radial rings. Existing clearance-repair via rings of0.14/0.16 mm remain explicitly reviewed. No blind/buried/filled vias or controlled-depth drilling are introduced. Tenting, finished annuli, paste/drill/mask registration, underbody fused via and TP12 tolerance are supplier/process gates.

J1 is exact EVERCOM 5301-8P8C; J2 is the populated hanxia 2×3 recovery header; U2 is exact ESP32-C3-WROOM-02-N4. J4 selects exact SHOU HAN TYPE-C 16PIN 2MD(073). Its drawing recommends 0.80 mm PCB; the retained board is 1.60 mm and now uses the exact reviewed forward shell slots/lands at unchanged centres. Its top-mount body seats, while the approximately 1 mm tabs end inside the slots. Assembler-approved solder delivery, joint inspection, retention and finish remain unqualified. The retained approximate STEP must not substitute for the primary review.

Actual supplier-library zero, pin1, rotation, pick/reel orientation, part stock, PCB/PCBA process, stencil/solder acceptance and quote preview must be checked before any assembly acceptance. A native-anchor equality test alone does not validate centroid coordinates. All electrical/transient/loaded5V/LDO/EN/reset/RF/USB/thermal/case gates remain open; no order is authorized by this package.

## Historical quote

The September 19, 2026 frozen 93-placement/40-purchasing-group quote was $149.96 for five assembled boards before shipping/tax: PCB $8.00, PCBA $141.96 including components $50.12 and extended-component fees $74.16. That point-in-time quote does not price this 97-reference repair. The dated current exact-part screen is a selected-parts subtotal, not a complete supplier quote; stock, assembly classes/fees and totals require fresh exact-source confirmation.
