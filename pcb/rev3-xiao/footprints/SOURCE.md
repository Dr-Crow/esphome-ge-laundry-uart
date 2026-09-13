# Seeed XIAO ESP32-C3 rev1.3 footprint source

The footprint in `GEA_XIAO.pretty` is a project-local derivative of Seeed Studio's official `XIAO-ESP32-C3-SMD.kicad_mod`. It is assigned to `U2` in the Rev3B2 power-fixture schematic; the separate placement PCB embeds a board-only mechanical copy and does not claim electrical completeness.

## Pinned sources

- Seeed Studio OPL KiCad Library commit `b0035c51eb0348bb3e165fdb2f2765fa3d1d17bd`, file `Seeed Studio XIAO Series Library/XIAO-ESP32-C3-SMD.kicad_mod`: <https://github.com/Seeed-Studio/OPL_Kicad_Library/blob/b0035c51eb0348bb3e165fdb2f2765fa3d1d17bd/Seeed%20Studio%20XIAO%20Series%20Library/XIAO-ESP32-C3-SMD.kicad_mod>
- Seeed's downloadable XIAO Series footprint archive: <https://files.seeedstudio.com/wiki/XIAO-KiCad-Library/New_XIAO_Series_Footprints.zip>
  - Retrieved footprint SHA-256: `f850def2f4829bd58a1a7f1773277de398930232a521d6a9607d8550aded3784`
  - The retrieved footprint is byte-identical to the file at the pinned OPL commit.
- Seeed XIAO ESP32-C3 rev1.3 KiCad project dated 2026-01-16: <https://files.seeedstudio.com/wiki/XIAO_WiFi/Resources/XIAO_ESP32C3_v1.3_KiCad_260116.zip>
  - Retrieved archive SHA-256: `477bc61cec652eaeefa887cb1f97abb1514e8a61ea9659240b88be7213c3b6ff`
- Seeed XIAO ESP32-C3 resource page and pin map: <https://wiki.seeedstudio.com/XIAO_ESP32C3_Getting_Started/>

## Pad mapping

The project-local footprint preserves Seeed's 22 pad numbers and land geometry. Pads 21 and 22 are the underside battery pads needed by the Rev3B2 experiment.

| Pad | Seeed signal | Pad | Seeed signal |
| ---: | --- | ---: | --- |
| 1 | D0 | 12 | 3V3_OUT |
| 2 | D1 | 13 | GND |
| 3 | D2 | 14 | VBUS |
| 4 | D3 | 15 | D3 / MTDI |
| 5 | D4 | 16 | D5 / MTDO |
| 6 | D5 | 17 | EN |
| 7 | D6 | 18 | GND |
| 8 | D7 | 19 | D2 / MTMS |
| 9 | D8 | 20 | D4 / MTCK |
| 10 | D9 / BOOT | 21 | VBAT |
| 11 | D10 | 22 | GND |

## Project-local changes

- The official pad positions, pad sizes, pad shapes, solder-mask margin, body outline, and USB connector bounds are preserved.
- The fabrication layer labels the USB-C protrusion and the U.FL connector courtyard.
- The front courtyard includes the USB-C protrusion instead of stopping at the module PCB edge.
- The official vertical side-silkscreen lines are omitted because they cross the exposed side-pad solder-mask openings when the footprint is instantiated.
- A KiCad 9 rule area blocks carrier tracks, vias, pads, and copper pours on both copper layers directly below the U.FL connector courtyard. Its `6.858..10.922 mm` by `-2.794..0 mm` bounds are transformed from the U.FL courtyard in Seeed's official rev1.3 PCB source.

The ESP32-C3 board uses a separate FPC antenna connected at U.FL. Seeed does not prescribe a fixed carrier-relative location or keepout for that external radiator. The footprint therefore does not invent one. The enclosure/layout stage must place the FPC antenna and define its clearance using the selected antenna manufacturer's installation guidance.

## License scope

Seeed distributes the OPL library under CC BY-SA 4.0. The attribution and license notice in `LICENSE.md` apply to the derived footprint and this source note only; they do not change the repository's license.
