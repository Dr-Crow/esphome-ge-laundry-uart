# Rev3C component model accuracy checkpoint

This isolated visual review replaces the featureless C3 module block with a
revision-specific PCB-derived reference and adds visible connector openings and
tails. The pre-model electrical source is `47c2fdc5047077b492509b3fbe73c1698958bda4`, including the metadata-only DELAY-pin correction. The matched-camera old-model render uses `409dc01`; its PCB geometry and manufacturing files are identical to that later electrical source.
**Complete, revision-matched manufacturer assembly STEP files were not available
for the selected XIAO modules, EVERCOM jack or HCTL sockets.** The new previews
are partial models for review; their detail must not be interpreted as enclosure,
mating, RF or manufacturing qualification.

The source is the selected 99 × 40 mm, four-layer carrier. C3 remains the first
module; C6 has its own geometry and alternative render. The eight shared firmware
YAML files, schematic, symbols, footprints, copper and manufacturing package are
preserved. No electrical part substitution is proposed here.

## What each visible model represents

| Part | Identity read from the selected source | Model used in this checkpoint | Accuracy limit |
| --- | --- | --- | --- |
| XIAO C3 | Separately installed Seeed XIAO ESP32C3; canonical reference v1.3 | Native KiCad export of official v1.3 PCB and copper with generic package models | Partial assembly; no authenticated complete module STEP |
| XIAO C6 | Separate Seeed XIAO ESP32C6 mechanical variant; reference v1.0 | Native KiCad export of official v1.0 PCB and copper with generic package models | Alternative preview; C3 geometry is never reused as C6 geometry |
| Module SoCs | C3 U4 ESP32-C3FH4; C6 U4 ESP32-C6FH4 | Exact named KiCad QFN-32-1EP 5 × 5 mm, 0.5 mm pitch, 3.7 × 3.7 mm EP model | Verified nominal package dimensions and pin-1 orientation; generic colors/index dot, no chip text or actual production-height claim |
| Module U.FL | Seeed C3 ANT0/C6 ANT2 value U.FL-R-SMT-1 | Separate licensed KiCad named-part Hirose model, dimensions checked against official drawing | Nominal geometry; fitted manufacturer/plating/packaging and mated cable remain unverified |
| J1 | EVERCOM 5301-8P8C, **C3097717** | Locally authored detailed drawing model, Rev A 2025-09-23 | Dimensioned body and signal tails; undimensioned opening and springs are illustrative; locating-post solids omitted |
| J5 and J6 | HCTL PM254-1-07-Z-8.5, C2897370 | Locally authored detailed drawing model, official family drawing Rev A, N = 7 | Dimensioned body and tails; receiving recess widths/depths are illustrative |
| U9 and U10 | TI TPS1H200AQDGNRQ1, C2653785 | Inherited DGN0008K maximum envelope | Simplified maximum body and rectangular leads; no exact vendor CAD imported |
| F1 and F2 | Littelfuse 1812L075/33DR, C151170 | Inherited maximum envelope | Simplified maximum body; terminal shape/marking omitted |
| L1 | Panasonic ETQP3M4R7KVP, C412309 | Official KiCad PCC-M0530M package model | Correct package family, generic appearance; manufacturer STEP was found but redistribution permission was not established |
| Other small fitted parts | Selected schematic/BOM identities | Inherited official KiCad 9.0.9 generic package models | Package visualization; no supplier-specific cosmetics or exact production height claim |

The selected J1 part is C3097717. C22074 is not the J1 field in this source.
J2 and D19 remain absent. The module and its male headers remain outside the
83-reference carrier factory BOM/CPL.

## Official sources and redistribution

The [Seeed C3 wiki](https://wiki.seeedstudio.com/XIAO_ESP32C3_Getting_Started/)
links the [official v1.3 KiCad archive](https://files.seeedstudio.com/wiki/XIAO_WiFi/Resources/XIAO_ESP32C3_v1.3_KiCad_260116.zip).
Its schematic title block is dated 2026-01-15 and explicitly carries CCBY-SA4.0.
The [Seeed C6 wiki](https://wiki.seeedstudio.com/xiao_esp32c6_getting_started/)
links the [official v1.0 archive](https://files.seeedstudio.com/wiki/SeeedStudio-XIAO-ESP32C6/XIAO_ESP32_C6_v1.0_SCH%26PCB_260114.zip),
dated 2026-01-14 and also marked CCBY-SA4.0. Neither archive contains STEP files.
The PCB-derived STEP assets retain Seeed attribution and the
[CC BY-SA 4.0 license](https://creativecommons.org/licenses/by-sa/4.0/).
The added component geometry comes from the
[official KiCad 3D library](https://gitlab.com/kicad/libraries/kicad-packages3D)
at 9.0.9, commit `a0244fe3442823dbb052ebc4820b4c2951e1742c`, under CC BY-SA 4.0
with the KiCad library exception. Asset hashes and per-reference provenance are
in the [module receipt](validation/xiao-model-provenance.json).

The exact C6 reference also uses **U1 SGM6029CYG/TR for its main +3V3 rail**:
U1 VIN/EN are on internal +5V, its SW pin feeds L1, and L1's output/VOS net is
+3V3, shared by module side pin 12 and the MCU supplies. **U3 SGM40567-4.2XG/TR
is the separate VBAT charger**, with VIN on VBUS. The current `260114` archive
SHA-256 is `cea2ed66da575e4a1dd6c7a9acd60583ed4a9adbf6b1d2952851c1e4199c05fc`;
its title block is V1.0, 2026-01-14. The retained final power-headroom review
already uses this buck reference. The [source identity receipt](validation/c6-source-supply-identity.json)
records exact schematic/PCB/PDF hashes and pin/net evidence. Equal V1.0 labels
do not establish equivalence across archive dates or identify the installed
module; this visual reference does not qualify electrical headroom.

The wiki-linked [C3 GrabCAD model](https://grabcad.com/library/seeed-studio-xiao-esp32-c3-1)
is Maurice Pannard's February 2023 reconstruction, predating v1.3; its author
warns about chip, USB-C and U.FL accuracy. The corresponding C6 community model
from November 2024 warns about buttons, U.FL and ceramic antenna positions and
omits some components. These models were not downloaded or imported as exact
manufacturer CAD. No per-asset redistribution license was established.

The [Hirose U.FL product](https://www.hirose.com/product/p/CL0331-0472-2-01)
and official family catalog verify that (01), (60) and (80) indicate packing,
with one receptacle geometry. The published connector envelope is
3.1 × 3.0 × 1.25 mm nominal; the 1.25 mm height tolerance is ±0.2 mm. The
separate KiCad named-part STEP matches the nominal envelope and is registered
to the Seeed signal/ground pads. The manufacturer STEP's accompanying terms
explicitly prohibit redistribution/modification without written permission,
so that vendor file is not included. The licensable KiCad asset is a nominal
reference, not a tolerance maximum or proof of the actual module's supplier.
C6's description mentions a gold connector, while the named Hirose reference
uses silver shell plating; colors and actual fitted part identity remain open.
See the [service component receipt](validation/service-component-provenance.json).

C3 BOOT0/RST0 both have value **TD-1183SN-A3N-D1R**. Seeed's symbol describes
**DEALON (德艺隆) TD-1183SA / 311020740**, a family-level identity. The
manufacturer-authored TD-1183S family drawing shows 3.0 × 2.5 mm bodies and
1.5/1.7 mm height options, but the exact A3N-D1R suffix was not mapped to an
option. Exact switch height, actuator profile and revision remain unresolved;
no guessed button solids were drawn or imported.

### Verified SoC package additions

Both official Seeed sources name U4 as a bare FH4 SoC: **ESP32-C3FH4** and
**ESP32-C6FH4**, respectively. The [C3 datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-c3_datasheet_en.pdf)
v2.4 Figure 7-1 and the [C6 datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-c6_datasheet_en.pdf)
v1.5 Figure 7-2 establish the same QFN32 package: 5.00 ±0.05 mm square body,
0.85 mm nominal height (0.80–0.90 mm), 0.50 mm pitch, 3.70 ±0.05 mm square
exposed pad, 0.25 mm nominal terminal width and 0.40 mm nominal terminal length.
The licensable unmodified KiCad 9.0.9 asset
`QFN-32-1EP_5x5mm_P0.5mm_EP3.7x3.7mm.step` independently measures
5 × 5 × 0.85 mm. Its 32 bottom contact faces and chamfered 3.7 mm exposed pad
also match those nominal dimensions. The older failed 3.5 mm EP download is
historical evidence and is not used. The source file and its license notices
are retained under `design/models/xiao-packages/`.

The [official Espressif library](https://github.com/espressif/kicad-libraries/tree/dd76561812ab300351234ba6e0ec1295641796f0)
was checked at the recorded commit, including its CC BY-SA 4.0 library-exception
terms. It provides module STEP files, but no bare FH4 SoC STEP. No module CAD is
substituted for a chip. The imported geometry is the named KiCad package, with
generic colors and a pin-1 dot; no manufacturer logo, part text or batch marking
has been added. This is nominal geometry, not a tolerance-maximum envelope.

C3's Seeed footprint has local pad 1 at `(-1.75,+2.45)` mm and footprint
orientation −90°. Its model Z rotation is **−90°** to align the stock package
pin-1 corner. C6 local pad 1 is `(-2.45,-1.75)` mm with 0° footprint/model
rotation. Isolated native STEP exports verify the pin-1 dot centers at
`(-2.5223,-0.4876,2.445)` mm for C3 and `(-3.4627,-1.0314,2.445)` mm for C6,
relative to each module's unchanged 14-pin-grid export origin. The stock marker
radius/appearance are generic. The exported package seating plane is
Z = 1.595 mm and top Z = 2.445 mm. These are native export coordinates, not
a measured solder stand-off or an adjustment to the provisional 11 mm stack.

The [package receipt](validation/xiao-soc-package-provenance.json) records the
source archive/datasheet/model hashes, contact geometry, transforms, isolated
exports and valid regenerated full compounds. The previous derivative boards
are augmented only with U4 model nodes; their complete non-model token streams
compare equal. The [producer](validation/augment_xiao_soc_models.py) checks the
pinned input hashes and regenerates both distinct module STEP assets without
refilling or editing source copper. Counts are now 41 included models for C3
and 47 for C6. An [independent export comparison](validation/xiao-soc-export-geometry-preservation.json)
matches the bounding box, volume, surface area and center of mass of every
previous solid: all 1,082 C3 and 906 C6 solids are retained, with exactly one
verified SoC solid added to each compound. The
[protected-file receipt](validation/xiao-soc-electrical-preservation.json)
also proves all 43 electrical, manufacturing and firmware files byte-identical.
The carrier PCB, its 3D associations and the accepted connector
body-datum manufacturing exports are byte-identical to the preceding checkpoint.

The same pass bounded the remaining prominent semiconductor omissions.
**C3 U2 TLV75733PDBVR** is TI DBV0005A/SOT-23-5. Its
[primary package drawing](https://www.ti.com/lit/ds/symlink/tlv757p.pdf) permits
1.45 mm maximum height, but the available immutable KiCad SOT-23-5 asset is
1.55 mm high. It is not attached, resized or buried into the PCB. C3 U1's PCB
value is empty; the schematic retains a PMIC-XC6802MR symbol and an earlier
history note says ETA4054, so a fitted charger suffix/height is not inferred.
C6 U1 [SGM6029CYG/TR](https://www.sg-micro.com/product/SGM6029) uses
WLCSP-0.74 × 1.09-6B, and U3
[SGM40567-4.2XG/TR](https://www.sg-micro.com/rect/assets/e95e555a-a8a2-4761-b86a-6554dff2d8ed/SGM40567.pdf)
uses WLCSP-0.92 × 1.16-6B. Available named KiCad six-ball models have different
body dimensions. These parts remain omitted pending compatible licensed geometry.

The [HCTL official PM254 family product](https://www.hctldz.com/product-5-8/550.html)
has an empty 3D download list. Its [Rev A drawing](https://www.hctldz.com/static/upload/2026/01/28/202601285507.pdf)
provides the body and tail dimensions used by the self-authored fallback.
The EVERCOM official product search supplies a
[5301-880XXX Rev A drawing](https://chinarj45.com/uploads/20260211/99f6f1d1acfb5da691ec9e117bc8ba1c.pdf),
not STEP. These PDFs are cited as dimensional references and are not redistributed
in the repository. The connector generator and generated fallback STEP assets
are covered by the repository MIT license; they do not reproduce supplier CAD.

Panasonic supplies actual STEP for ETQP3M4R7KVP, but its
[terms](https://industrial.panasonic.com/ww/terms-of-use) reserve copying and
modification except permitted use. The downloadable manufacturer asset is not
bundled in this checkpoint. TI's current product page sends package CAD requests
to Ultra Librarian; no authenticated, openly redistributable exact DGN0008K STEP
was obtained in this pass.

## Datums and transforms

Carrier KiCad coordinates use the outline's upper-left `(0, 0)` datum, X right
and Y down; the outline corners are `(0,0)`, `(99,0)`, `(99,40)`, `(0,40)` mm.
Imported STEP coordinates use X right, Y up, Z above the carrier.
All model scales are `(1,1,1)`; there is no hidden nonuniform resize.

The shared 14-pin grid center is carrier `(87.89,12.9175)` mm. Both official
module PCBs align to the same pin centers. C3 D0/pin 1 is carrier
`(95.51,5.2975)`; D7 is `(80.27,20.5375)`; VBUS is `(95.51,20.5375)`.
The USB connector faces the carrier's right edge. The centered module STEP is
attached to J5 with XY offset `(-7.62,-7.62)` mm and zero XYZ rotation.
The [module receipt](validation/xiao-model-provenance.json) records the full
14-pin comparison, native export origin and C3/C6 feature coordinates.

The installed Z uses the existing **unverified** 11 mm module-bottom assumption:
8.5 mm socket body plus a provisional 2.5 mm male-header spacer. Bare module
PCB-derived assets contain no fitted male headers. Their exported substrate-bottom
datum is Z = 0 mm and its top is Z = 1.51 mm; component placement uses the source's
nominal 1.6 mm PCB thickness. Native export separates outer copper/mask from the
substrate. The model offset is Z = 11 mm. These native export datums are recorded
in the receipt. No measured engagement, protruding male-pin length, retention or
preheadered module SKU is inferred. An omitted shield/connector/button is not
zero-height geometry and must not be used to approve clearance.

The separate U.FL reference follows C3 ANT0 at carrier `(78.873,12.9175)` mm,
rotation 180°, or C6 ANT2 at `(78.8825,8.6215)` mm, rotation 180°. Its raw model
is body-centered, with zero local offset in the Seeed footprint. The stock
KiCad footprint's +0.475 mm X model offset must **not** be copied: that stock
footprint uses a different origin. Relative to J5 the C3 offset is
`(-16.637,-7.62,12.6)` mm; the C6 transient preview uses
`(-16.6275,-3.324,12.6)` mm. Z = 12.6 mm follows the same provisional module
bottom 11 + nominal PCB 1.6 assumption. The STEP body is nominal 1.25 mm high, not
the 1.45 mm maximum from the published tolerance. No fitted plug/cable geometry or
measured mating depth is represented.

J5 origin is `(95.51,5.2975)`, orientation 0°; its pin centers run left in 2.54 mm
steps. J6 origin is `(80.27,20.5375)`, orientation 180°. Each socket's local
body is 18.18 × 2.50 × 8.50 mm and its nominal tails extend 3.20 mm below the
carrier-top datum. The local receiving mouth and recess dimensions are only
visual detail, not mating dimensions.

J1 origin is pin 1 at `(13.97,12.55)`, footprint rotation −90°. Its STEP has zero
model offset/rotation and follows the latest drawing body of
15.20 × 18.05 × 11.45 mm. The opening faces the short left board edge and the
dimensioned body face projects to carrier X = −0.38 mm. The inherited previous
model placed its face at X = 0 mm. The drawing's locating-post pitch is 11.50 mm;
the unchanged footprint is 11.43 mm, a 0.07 mm total difference, or 0.035 mm per
post about the shared center. This discrepancy remains for physical/supplier
verification; the model change does not repair or qualify the footprint. Post
solids are omitted because the 3.20 mm recommended drill is not a measured barb
diameter or post profile; no insertion-depth geometry is invented.

## Render comparison and evidence

The old [oblique preview](images/model-comparison/before-oblique.png) used a
featureless grey module block. The new [C3 oblique preview](images/rev3c-render-oblique.png)
shows the official PCB-derived partial reference. The
[top](images/rev3c-render-top.png), [bottom](images/rev3c-render-bottom.png) and
[C6 alternative](images/rev3c-render-c6-oblique.png) provide the other viewpoints.
Native KiCad 9.0.9 renders were inspected as actual pixels. Missing module
components, the generic USB shell and the provisional Z remain visible accuracy
limits, even where a detailed render looks plausible.

The [electrical preservation receipt](validation/component-model-electrical-preservation.json)
compares the complete PCB token stream after removing only 3D model nodes.
Every non-model token matches the selected candidate: pads, nets, tracks, vias,
filled zones, outline, placement and all properties. The schematic, symbol and
footprint libraries, project/rule files, manufacturing files and firmware compare
byte-for-byte. The original source manifests describe their historical electrical
checkpoints; the new [model receipt](validation/component-model-provenance.json)
describes this visual lane.

These previews support feedback about which geometry still needs a verified
supplier asset. They do not close physical mating/USB/button access, enclosure,
RF, electrical, thermal or appliance qualification gates.

## Reuse and other module references

The same C3 v1.3 **bare PCB-derived asset** can be reused for soldered Rev3B
as a visual reference, with a different assembly transform. Rev3B U2 is at
`(77.39,4)` mm, rotation −90°; its shared module-grid datum is again
`(87.89,12.9175)` mm. A centered-asset association would use local XY offset
`(8.9175,10.5)` mm and model Z rotation 90° to preserve USB-right orientation.
SMD seating/solder stand-off Z is unmeasured and must not inherit the Rev3C
11 mm socket stack. Rev3B SMD land rows lie at Y 4.835/21.0 mm, while drilled
module pin centers lie at Y 5.2975/20.5375 mm; equal datum does not prove solder
land overlap or physical assembly fit. No Rev3B source/model/CAM change is
made in this lane.

Rev3A uses **ESP32-C3-WROOM-02-N4**, not XIAO. Its current reference is the
licensed official KiCad ESP32-C3-WROOM-02 model. That model was independently
imported and visually inspected: it has a shaped RF shield, the PCB meander
antenna trace and castellated terminals, 30 valid solids and nominal
18 × 20 × 3.2 mm geometry. Espressif's official 20210906 STEP contains a more
detailed assembly with 179 valid solids and CAD height 3.29929 mm; both values
are within the published 3.2 ±0.15 mm height range. The KiCad stock model is
nominal reference geometry, not a tolerance maximum or a measured production
revision. See the [official datasheet physical dimensions](https://documentation.espressif.com/esp32-c3-wroom-02_datasheet_en.html)
and [manufacturer model source](https://www.espressif.com/en/products/modules/esp32-c3).
No Rev3A source/model/routing/CAM change or manufacturer CAD redistribution is
made here.
