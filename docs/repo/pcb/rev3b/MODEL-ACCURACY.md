# Rev3B verified C3 visual reference

The placed U2 preview uses the unchanged, licensed
`XIAO_ESP32C3_v1.3_vendor_pcb_visual_reference.step` from the verified Rev3C
visual lane. It represents the official Seeed C3 v1.3 PCB and copper with
selected generic components, including the dimension-checked nominal
ESP32-C3FH4 QFN32. It is a partial visual reference, not a complete manufacturer
assembly or a physical-fit guarantee. C6 is not supported by this soldered-C3
carrier and no C6 geometry is associated here.

The exact selected Rev3B electrical source is
`1db7a80f38a05c0c85023c01df63db22d81281c4`. Only the placed U2 3D model node
changes in its PCB. The entire non-model token stream is identical: outline,
F.Fab body, pads, nets, tracks, vias, zones, properties and placements. All 43
protected files, including schematics, footprints, project/rules, BOM/CPL/CAM,
firmware and enclosure files, remain byte-identical. Existing manufacturing
datum proofs are retained as historical evidence and are not regenerated or
reinterpreted by this visual lane. Both appliance-input and priority requirements
remain unchanged and still need the qualification in the electrical reports.

## Source and license

The [official Seeed v1.3 archive](https://files.seeedstudio.com/wiki/XIAO_WiFi/Resources/XIAO_ESP32C3_v1.3_KiCad_260116.zip)
has SHA-256 `477bc61cec652eaeefa887cb1f97abb1514e8a61ea9659240b88be7213c3b6ff`.
The unchanged primary PCB has SHA-256
`a761393935ff261a58fee3e3d7ecfb65152eaba8620de64ff7758fb0c043d1db`;
its companion schematic title block names CCBY-SA4.0 and v1.3, 2026-01-15.
The reused STEP has SHA-256
`8ba2b9fd52c2a292f9fb0f3c2214738c83b830287490eef49d0962ddfbd56c80`.
See [Seeed attribution/license](design/models/XIAO-ASSET-LICENSE.md),
[KiCad library license](design/models/KICAD-LIBRARY-LICENSE.md), and the
[C3 source receipt](validation/xiao-c3-model-source.json). The repository MIT
license does not replace these asset licenses.

The unmodified KiCad QFN32 asset is retained under `design/models/xiao-packages/`.
Its 5 × 5 × 0.85 mm body, 0.5 mm pin pitch, 3.7 mm exposed pad and source pin-1
orientation were checked against the primary Espressif package drawing in the
[retained source package receipt](validation/xiao-soc-package-source.json).
Its appearance, dot and height are generic nominal geometry, not a measured
production module. Other component licenses and source notices are retained
in the C3 source receipt.

## Native transform and separate datums

KiCad board coordinates have X right and Y down. The STEP has X right, Y up
and Z above the board. The official source's 14 drilled-pin-grid center is
`(148.4376,105.0036)` mm. Its centered STEP datum registers to carrier
`(87.89,12.9175)` mm using source-to-carrier translation
`(-60.5476,-92.0861)` mm. USB0 is then `(92.589,12.9175)` mm and faces right.

Placed U2 remains at native `(77.39,4)` mm and footprint rotation −90°.
The new association uses model offset `(8.9175,10.5,0)` mm, model Z rotation
**−90°**, and `(1,1,1)` scale. Native KiCad 9.0.9 rendering/export checks determine
the model-angle sign; treating the footprint and model rotations as a simple
same-sign sum would reverse the module. Every existing model retains 100% scale.

Three distinct datums must not be confused:

| Reference | Carrier KiCad coordinates, mm | Meaning |
| --- | --- | --- |
| Unchanged nominal F.Fab body | X 77.39..98.39; Y 4..21.8; center `(87.89,12.90)` | Typed 21 × 17.8 mm nominal body used by the existing manufacturing datum proof |
| Official drilled-pin grid | Center `(87.89,12.9175)` | Export datum for this partial visual asset |
| Official substrate solid | X 77.476..98.431; Y 4.0275..21.8075; center `(87.9535,12.9175)` | 20.955 × 17.78 mm actual source CAD substrate; excludes copper, pads and every component/USB solid |

In the CPL's X-right/Y-up coordinates the official CAD substrate center is
`(87.9535,-12.9175)` mm, versus the unchanged typed nominal-body datum
`(87.89,-12.90)`. The difference is `(+0.0635,-0.0175)` mm, about 0.0659 mm.
This is a sub-0.1 mm CAD-versus-nominal difference, not evidence that the
existing typed nominal-body datum is wrong. It changes no CPL coordinate or
supplier-origin claim. Supplier assembly origin remains unqualified.

The compound's total bounds include USB and copper and must not be used as
the module-body datum. J1/J2 pads 1–7 in the official source establish the
14 drilled-pin grid; those vendor DNP header designators are source datums,
not fitted male-header parts or Rev3B carrier J1/J2. Extra source edge castellations,
test points, underside contacts and component positions are excluded from the
drilled-grid average. Carrier U2 still has all its 22 original solder lands.
Drilled pins register to carrier X 80.27..95.51 at 2.54 mm pitch and Y
5.2975/20.5375; the SMD land rows remain Y 4.835/21.0. Their 0.4625 mm Y
differences are recorded per pin. Registration does not qualify solder overlap,
underside-pad fit or clearance.

The previous zero model Z is retained as an **unmeasured nominal** soldered-module
seating assumption. No Rev3C 11 mm socket/header stack is copied. The module
substrate bottom is Z 0 in its source STEP; thin copper extends down to Z −0.04 mm.
This association is not a measured solder stand-off or collision-free installation.

## Scope and evidence

The partial model contains the nominal verified SoC and a generic GCT USB shell,
while the actual source USB value is UBF31-0171. RF shield, BOOT/RESET switches,
U.FL connector, unresolved charger/regulator/crystal geometry, external antenna
and cable remain omitted. No guessed button or semiconductor body has been
added. An omission is not zero-height clearance evidence. The old assumed envelope
is retained only for historical comparisons and the unchanged footprint-library
association; the placed U2 PCB node uses the partial reference.

The [preservation/registration receipt](validation/verified-c3-model-preservation.json)
binds PCB tokens, protected source bytes, asset and license hashes, all 14 primary
pin coordinates and all 86 resolved native model associations at 100% scale.
The [installed native STEP geometry check](validation/verified-c3-installed-geometry.json)
independently compares every source-model solid at the actual assembled transform
and finds all 14 native pin-hole centers. Its exported source-substrate bottom
is Z 1.595 mm with the zero model offset; that is a native nominal-stackup coordinate,
not measured solder seating. The diagnostic STEP is temporary and is not a new
manufacturing artifact.
[Top](images/rev3b-render-top.png), [bottom](images/rev3b-render-bottom.png) and
[oblique](images/rev3b-render-oblique.png) are native KiCad 9.0.9 previews;
[matched-camera baseline views](images/model-comparison/before-oblique.png)
retain the previous envelope for comparison. The
[render receipt](validation/verified-c3-render-receipt.json) records exact source
and image hashes and pixel inspection. No electrical, RF, thermal, appliance,
enclosure, physical mating or manufacturing qualification is claimed.
