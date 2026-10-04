# Rev3B mechanical models

The placed U2 preview now uses `XIAO_ESP32C3_v1.3_vendor_pcb_visual_reference.step`, copied byte-for-byte from the verified Rev3C visual asset. It is derived from the official Seeed v1.3 PCB with generic package models and a nominal, dimension-checked ESP32-C3FH4 QFN32. It is a partial visual reference, not complete manufacturer assembly CAD. See [MODEL-ACCURACY.md](../../MODEL-ACCURACY.md), [Seeed attribution/license](XIAO-ASSET-LICENSE.md) and [KiCad library license](KICAD-LIBRARY-LICENSE.md).

The former `XIAO-ESP32-C3-v1.3-envelope.step` remains as a historical build123d clearance envelope, and the unchanged footprint-library model still names it. The placed PCB U2 association overrides it with the verified partial asset. Its assumed button/U.FL/component envelopes are not used as cosmetic or physical-fit evidence.

## XIAO ESP32-C3 alignment and source

- Unchanged footprint origin: left edge of the 17.8 mm side, with the USB edge at `y=-21 mm`; nominal F.Fab body is `17.8 x 21.0 mm`. That description applies to the historical origin-based envelope, not the new drilled-grid-centered asset.
- The placed partial asset has local model offset `(8.9175,10.5,0)` mm, rotation `(0,0,-90)` degrees and 100% XYZ scale. Native U2 is `(77.39,4)` mm at -90 degrees. The installed asset grid datum is `(87.89,12.9175)` mm; its USB faces the right carrier edge. The retained zero Z is an unmeasured nominal solder-seating assumption, not the Rev3C 11 mm socket stack.
- Official Seeed v1.3 KiCad project: <https://files.seeedstudio.com/wiki/XIAO_WiFi/Resources/XIAO_ESP32C3_v1.3_KiCad_260116.zip>.
- Seeed OSHW-XIAO-Series repository was checked for a directly hosted ESP32-C3 STEP; it contains the KiCad footprint library but no ESP32-C3 STEP model.
- Official resource page: <https://wiki.seeedstudio.com/XIAO_ESP32C3_Getting_Started/>. Seeed links the 3D model to GrabCAD; no directly hosted manufacturer CAD was imported here.

The STEP solids use millimetres, with Y mirrored to match KiCad's 3D coordinate convention. The model has been checked over the footprint in KiCad 9. Verify enclosure clearances against a physical module and the selected USB cable, button actuator, U.FL mating plug/cable, and antenna installation before fabrication.

## J2 recovery header model

`J2-hanxia-HX-PZ-2.54-02-03-S-drawing.step` is a drawing-based nominal model
for Hanxia HX PZ-2.54-02-03-S-PB3.2, LCSC C42391552. The public product listing
is [JLCPCB C42391552](https://jlcpcb.com/partdetail/hanxia-HX_PZ_2_54_02_03_S_PB32/C42391552).
The model uses zero XYZ offset and zero model rotation: two 0.64 mm post
columns at x +/-1.27 mm and three rows at y -2.54/0/+2.54 mm, a nominal
5.00 x 7.42 mm body, 7.50 mm foot envelope, and 9.20 mm nominal height
(9.60 mm stacked pre-assembly maximum). It is a simplified drawing model,
not manufacturer-authenticated CAD or a physical-fit guarantee; retain
assembly/case margin and verify against the actual part.

## Rated-protection approximate package envelopes

`1812L075-33DR-max-envelope.step` and `TPS1H200A-DGN0008K-max-envelope.step` are transferred unchanged from selected C source fafd3ea. They are approximate maximum solids derived from the Littelfuse/TI package drawings cited in [RATED-PROTECTION.md](../../RATED-PROTECTION.md), not authenticated supplier CAD or physical/thermal qualification. The frozen rated-protection model-resolution record is retained in [current-3d-model-resolution.json](../../validation/current-3d-model-resolution.json); this visual lane has its own current [preservation/registration receipt](../../validation/verified-c3-model-preservation.json). The soldered C3 association is updated only in the placed PCB model node; original case/interface boundaries remain.
