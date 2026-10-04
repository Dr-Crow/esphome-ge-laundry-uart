# Seeed XIAO ESP32-C3 v1.3 footprint source

`XIAO-ESP32-C3-v1.3-SMD.kicad_mod` is a project-local derivative of Seeed Studio's official OPL footprint. The 22-pad land pattern, pad geometry, underside contacts, and mask/paste layers are retained; project-local additions are the assembly courtyard, USB labeling, and a U.FL carrier copper keepout.

Sources:

- Seeed OSHW-XIAO-Series library: <https://github.com/Seeed-Studio/OSHW-XIAO-Series/tree/main/Seeed%20Studio%20XIAO%20Series%20Library>
- Pinned OPL source commit: <https://github.com/Seeed-Studio/OPL_Kicad_Library/tree/b0035c51eb0348bb3e165fdb2f2765fa3d1d17bd>
- Official v1.3 KiCad project: <https://files.seeedstudio.com/wiki/XIAO_WiFi/Resources/XIAO_ESP32C3_v1.3_KiCad_260116.zip>
- Official resource and pin map page: <https://wiki.seeedstudio.com/XIAO_ESP32C3_Getting_Started/>

See `LICENSE.md` for the limited CC BY-SA attribution notice. This file documents package geometry only; it does not bind the footprint to a schematic reference, placement board, or electrical experiment.

## Assembly courtyard review (3 October 2026)

The previous courtyard followed the 17.8 mm module body and omitted the outer side lands. The retained Seeed lands span `x=-0.54..18.375 mm`; the reviewed rectangular courtyard is `x=-0.79..18.63 mm`, `y=-23.05..0.25 mm`. It includes at least 0.25 mm around the land/body envelope and 0.5 mm beyond the nominal USB shell front at `y=-22.547 mm`, following [KiCad courtyard conventions](https://klc.kicad.org/footprint/f5/f5.3/). This is a carrier assembly envelope; USB cable approach and module installation still need physical verification. The same courtyard is applied to placed U2 without changing pads, copper, keepout, placement, or connectivity.

## Rated-protection vendor lands

`GEA_Rev3B.pretty/Fuse_Littelfuse_1812L_Recommended` and `TPS1H200A_DGN0008K_TI_RevE` are identical vendor-land definitions transferred from selected C source fafd3ea. The Littelfuse1812L sheet specifies1.78 ×3.15 mm pads/3.45 mm gap; TI TPS1H200A-Q1 RevE May2026 DGN0008K-C01 pp28–29 specifies1.4 ×0.45 mm leads/0.65 mm pitch/4.4 mm row spacing and mask-defined1.57 ×1.89 mm EP on2 ×3 mm copper. See [the report](../../RATED-PROTECTION.md) for primary URLs, exact pins, stencil and local-rule limits. No socket or C6 footprint is introduced.
