# XIAO ESP32-C3 v1.3 mechanical model

`XIAO-ESP32-C3-v1.3-envelope.step` is a build123d-generated clearance envelope, not manufacturer CAD. It includes the board envelope, USB-C protrusion, both button envelopes, U.FL connector envelope, and a conservative populated-component height envelope. Do not use it as evidence of physical fit or cosmetic geometry.

## Alignment and source

- Footprint origin: left edge of the 17.8 mm side, with the USB edge at `y=-21 mm`; footprint body is `17.8 x 21.0 mm`. The STEP uses positive Y (`0..21 mm`) because KiCad mirrors the model Y axis relative to footprint coordinates.
- Official Seeed v1.3 KiCad project: <https://files.seeedstudio.com/wiki/XIAO_WiFi/Resources/XIAO_ESP32C3_v1.3_KiCad_260116.zip>.
- Seeed OSHW-XIAO-Series repository was checked for a directly hosted ESP32-C3 STEP; it contains the KiCad footprint library but no ESP32-C3 STEP model.
- Official resource page: <https://wiki.seeedstudio.com/XIAO_ESP32C3_Getting_Started/>. Seeed links the 3D model to GrabCAD; no directly hosted manufacturer CAD was imported here.

The STEP solids use millimetres, with Y mirrored to match KiCad's 3D coordinate convention. The model has been checked over the footprint in KiCad 9. Verify enclosure clearances against a physical module and the selected USB cable, button actuator, U.FL mating plug/cable, and antenna installation before fabrication.
