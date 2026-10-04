# Rev3A J4 exact-part body datum and pin-1 review

Body-origin and pin-1 screening passes. No J4 placement-origin shift or rotation correction is indicated. This is not full exact-part manufacturing qualification.

The reviewed primary part is SHOU HAN TYPE-C 16PIN 2MD(073), LCSC C2765186. Manufacturer-authored supplier PDF page 1, drawing Rev A, sheet 1 of 1, units mm, was retrieved read-only from https://atta.szlcsc.com/upload/public/pdf/source/20250421/4251387FDD0B70FDBB4F5FD36EE975AA.pdf. Local PDF SHA256: 39110c4af62ba9309f87e6405ce58368b479fcf233e9166d54fc6ffae5b366ba. Exact page pixels are SHOU-HAN-C2765186-page1.png, with enlarged land/pin and side-view crops alongside.

## Datum findings

- Supplier body is 8.94 x 7.35 mm. Side view places front edge 2.60 mm beyond the forward shell-lug center.
- Native forward lug y=+1.075 mm therefore gives front y=+3.675 and rear y=-3.675 mm. Native Fab x=+/-4.47, y=+/-3.675 matches the body centered at native anchor (72,36.325), rotation 0.
- Native opening/front edge is board y=40.0 mm, coincident with Edge.Cuts. Shell centers x=+/-4.32, rear y=-3.105, forward y=+1.075; locator holes x=+/-2.89,y=-2.605 match the drawing coordinate relationships.
- Existing manufacturing CPL (72,-36.325), rotation 0, is the body center under y=-board-y. It is not a pad bounding-box or rear contact-row center.

## Pin-1 transform

Primary top-view drawing labels the left rear land A1/B12, both GND. Native A1 and B12 are coincident at local (-3.2,-3.745), board (68.8,32.58). CPL vector is (-3.2,+3.745), absolute (68.8,-32.58). Native Fab pin-1 mark aligns with that rear-left pair. All 12 physical land positions representing the 16 named contacts follow the drawing order. No mirror or 180-degree correction is indicated.

## Namespace and qualification limits

The native footprint namespace remains Connector_USB:USB_C_Receptacle_HCTL_HC-TYPE-C-16P-01A. Its stock HCTL description and 5 A claim must not be treated as SHOU HAN identity/rating evidence. Native BOM/properties select exact SHOU HAN C2765186; supplier source names that exact part.

The primary recommended layout says PCB thickness 0.80 mm; Rev3A board is 1.60 mm. It recommends forward shell holes 0.60 x 1.40 with pad height 1.80 mm; native HCTL-derived holes are 0.60 x 1.20 with pad height 1.60 mm. Native signal lands are 1.30 mm tall; drawing callout is 1.17 mm, but its adjacent 5.32-4.17 dimensions imply 1.15 mm. These pre-existing differences require exact-part manufacturing/fit qualification and were not changed. They do not support moving the body-origin datum.

The source has no pick-and-place origin/tape orientation specification, so assembler proprietary placement transform remains unverified. Local model filename says SHOU HAN 16PIN but STEP FILE_NAME says USB-C-SMD_TYPE-C-6PIN-2MD-073.step; that model was not primary geometry/pin-map evidence here.

## Snapshot evidence

Native tool: pinned KiCad 9.0.9. Supplied active PCB SHA 796cad8c... had advanced before the review. Own current snapshot SHA256 is 5e41644ab8741f0d9f9dfb3734e223b5dda0f7d2ca1abe33400a74b6356135fa. Frozen PCB SHA256 is 2f4a2cb171c99e112ccd92e08608380abe10f9f071ba5a99e14f68fa9a8548aa. The full embedded J4 blocks are identical after ignoring only global numeric net-ID renumbering; normalized J4 SHA256 is db5e0d23b52a2f00c4a727380c22a265750c2889233b4820538138e8f7eb7057.

Detailed typed facts and native pad/Fab observations are in J4-BODY-DATUM-REVIEW.json and native-J4-geometry.json. All writes are in this review scratch directory; active/frozen sources and original quote browser were untouched.

## Actual-tab and seating follow-up

The printed actual shell-tab dimensions do not authenticate a nominal insertion or top-contact failure:

- Forward tab is 0.8 mm, rear tab 1.1 mm. The title block applies +/-0.15 mm to one-decimal dimensions. Forward maximum printed width is 0.95 mm versus native nominal slot length 1.20 mm, leaving 0.25 mm total clearance in that direction before finished-hole/registration effects. Rear maximum width 1.25 mm is below native rear slot length 1.70 mm. This is not a full worst-case fit stack.
- Rear view prints 1.00 mm projection from the contact/seating-level line, with general two-decimal tolerance +/-0.10 mm. If that line is interpreted as PCB-top seating plane, lugs terminate 0.50...0.70 mm short of the bottom on a 1.60 mm board, while protruding 0.10...0.30 mm through a 0.80 mm board. The drawing does not explicitly label the line as PCB top or state a minimum protrusion. Short lugs within through holes do not by themselves prevent insertion or top-side seating.
- Bottom view prints 0.30 mm solder-tail projection beyond the rear body line. Native signal pads extend 0.72 mm beyond that body line and 0.58 mm inward, so there is no demonstrated nominal longitudinal pad miss under the reviewed body datum.

Exact solder-fill/wetting process, finished-hole tolerance, full positional stack, narrow-direction tab thickness, coplanarity, and retention criteria remain unverified. Confirming exact-part fit/reflow at native 1.20 mm forward slots and 1.60 mm board is a conditional qualification recommendation, not an authenticated incompatibility. No further footprint/source variants were created. Additional enlarged primary-source pixels: drawing-tab-seating-detail.png, drawing-bottom-view-detail.png, drawing-tolerance-detail.png.
