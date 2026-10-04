# Rev3B mechanical models

`XIAO-ESP32-C3-v1.3-envelope.step` is a build123d-generated clearance envelope, not manufacturer CAD. It includes the board envelope, USB-C protrusion, both button envelopes, U.FL connector envelope, and a conservative populated-component height envelope. Do not use it as evidence of physical fit or cosmetic geometry.

## XIAO ESP32-C3 alignment and source

- Footprint origin: left edge of the 17.8 mm side, with the USB edge at `y=-21 mm`; footprint body is `17.8 x 21.0 mm`. The STEP uses positive Y (`0..21 mm`) because KiCad mirrors the model Y axis relative to footprint coordinates.
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

`1812L075-33DR-max-envelope.step` and `TPS1H200A-DGN0008K-max-envelope.step` are transferred unchanged from selected C source fafd3ea. They are approximate maximum solids derived from the Littelfuse/TI package drawings cited in [RATED-PROTECTION.md](../../RATED-PROTECTION.md), not authenticated supplier CAD or physical/thermal qualification. Current native model resolution is recorded in [current-3d-model-resolution.json](../../validation/current-3d-model-resolution.json). The soldered C3 model and original case/interface boundaries remain.
