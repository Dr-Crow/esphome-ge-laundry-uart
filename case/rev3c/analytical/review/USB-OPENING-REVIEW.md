# Separate Rev 3C USB aperture study

**A 16×10 mm rounded opening improves the wall aperture, but is unadopted. It does not establish a usable 14×8 mm plug-body corridor through the assembled lid.** All button and closure supports remain intact. Original case sources, prior analytical outputs and the board are preserved.

## Dimensions and explicitly assumed gauges

| Parameter | Frozen baseline | Separate candidate |
|---|---:|---:|
| Opening width along Y |14.8 mm |16.0 mm |
| Opening height along Z |9.0 mm |10.0 mm |
| Corner radius |2.2 mm |2.2 mm |
| Y center |12.9175 mm |12.9175 mm |
| Fixed Z center |20.7 mm |20.7 mm |
| Optional per-assembly Z |20.7+stack−11.65 |20.7+stack−11.65 |
| Cut X interval |98–110 mm |98–110 mm |

The 14×8 and 12×6 mm gauges are synthetic rectangular bodies. They are centered atY12.9175 and **Z=carrier top 5.25+installed module-bottom stack+3.55**. The 3.55 mm term is the midpoint of the prior provisional USB screen from module underside+1.6 to+5.5; it is not a measured USB mating axis or actual plug profile. Installed stacks sampled are 11.0/11.325/11.65 mm.

A wall-only gauge occupiesX103–110 mm. The stronger full-body corridor starts at the prior conservative USB screen's maximumX: **C3 X 100.003 mm; C6 X 100.0143 mm**, ending atX110. These source/proxy planes are not authenticated manufacturer mating faces. The apparent body-start plane changes with a real cable's metal shank, overmold step, body rounding and actual connector mating datum.

## Bounded results

The 16×10 opening with its per-assembly center passes the 14×8 rounded-aperture profile across all three sampled stacks. At the unchanged fixed Z20.7 center it can still clip bottom corners at the 11.0 mm stack. The opening's rectangular bounding box alone is insufficient: at low stack the gauge sits 0.90 mm below the fixed center, and its corner radius distance exceeds 2.2 mm. The shifted center leaves a constant 0.25 mm vertical offset under this assumed gauge axis.

Complete lid tests separately check material that is added after the opening cut. At 11.0 mm, the 14×8 full-body corridor intersects the C3 corner closure datum by 0.02286 mm³. For C6 it intersects closure/button collar/support material by 5.63856 mm³. This is why a clear aperture profile cannot be called a complete plug fit. Supports were not trimmed to force a pass. Endpoint and 12×6 corridor results are in the receipts.

All four module/antenna variants are checked at both candidate center endpoints. The base, current module/button footprints, light-guide paths, closure datums and antenna features retain their source geometry. Newly widened apertures are valid single-solid lid candidates. At a common center the old 14.8×9 rounded cut is contained by the new 16×10 cut, so the aperture-only operation adds no lid material. Current component screens are checked separately.

At maximum centerZ20.7, aperture top isZ25.7: **2.8 mm below roof undersideZ28.5**, and 4.8 mm below roof topZ30.5. At the low shifted centerZ20.05, the lower edgeZ15.05 is **6.9 mm above the base tongue topZ8.15**. These are nominal structural webs, not strength or printed-tolerance qualification. Changes are 0.6 mm each side and 0.5 mm vertically relative to the old opening at the same center. There is no roof/button-slot intersection, and the shared base is unchanged.

### Whole-body corridor results with the shifted 16×10 opening

| Module | Installed stack |12×6 corridor intersection |14×8 corridor intersection | Wall-only intersection |
|---|---:|---:|---:|---:|
| C3 |11.00 mm |0 |0.022860 mm³ |0 |
| C3 |11.65 mm |0 |0 |0 |
| C6 |11.00 mm |0.465531 mm³ |5.638561 mm³ |0 |
| C6 |11.65 mm |1.474181 mm³ |8.423551 mm³ |0 |

For C6 at low stack, the 14×8 collision separates into the corner datum 0.022860 mm³, BOOT stop/collar/support 2.813968 mm³ and RESET stop/collar/support 2.801733 mm³. At high stack the datum clears, while those button structures account for 4.220951/4.202600 mm³. Moving cap/shaft/foot envelopes do not intersect this gauge. The 12×6 original-aperture pass remains a wall/profile result; it did not prove a full overmold corridor.

The fixed-center 16×10 opening at the low stack still clips the actual wall by 0.249560 mm³. Its shifted version clears the wall at both endpoints. Eight full lid configurations (four variants at two shifted centers) are valid single solids; all eight current component-screen checks have zero intersections. Base and other source/data files compare byte-identical.

## Source and stopping point

`candidate/enclosure.py` adds functional USB_OPENING_WIDTH/HEIGHT/RADIUS settings and a `usb_opening=(16,10,2.2)` configuration tuple. `usb-opening-source.patch` is the exact diff against the frozen source copy. Other candidate source/data files are unchanged. The candidate remains a separate study; prior published/frozen geometry is not replaced.

The remaining required input is an actual cable envelope or fit measurement: connector mating plane/axis, metal-shank length and size, overmold front position, body/corner and strain-relief dimensions. This study stops at that input. It makes no all-plug, full-insertion, shank-depth, printer-fit or strength claim.

`CASE-ANALYSIS-CORRECTED-WORDING.md` additionally corrects the earlier report:0.15/0.11 mm conditional contact depression does not prove electrical make. Fitted C3 make/travel and C6 switch identity/make remain UNKNOWN. Original sealed artifacts and historical numerical screening receipts are preserved.
