# Seeed XIAO PCB derived assets

Copyright Seeed Studio. The XIAO_ESP32C3_v1.3_vendor_pcb_visual_reference.step
and XIAO_ESP32C6_v1.0_vendor_pcb_visual_reference.step files are adaptations of
Seeed's officially published KiCad projects. The companion manufacturer
schematic title blocks explicitly identify Creative Commons Attribution
ShareAlike 4.0 (CCBY-SA4.0).

License: https://creativecommons.org/licenses/by-sa/4.0/
Legal code: https://creativecommons.org/licenses/by-sa/4.0/legalcode

Official sources:

- C3 v1.3, title block 2026-01-15: https://files.seeedstudio.com/wiki/XIAO_WiFi/Resources/XIAO_ESP32C3_v1.3_KiCad_260116.zip
- C6 v1.0, title block 2026-01-14: https://files.seeedstudio.com/wiki/SeeedStudio-XIAO-ESP32C6/XIAO_ESP32_C6_v1.0_SCH%26PCB_260114.zip

Changes in this adaptation: native KiCad 9.0.9 STEP export with a 14-pin-grid
datum, board/copper geometry, and selected generic package component models.
Unresolved components, shields, buttons, antenna parts and male headers are
omitted. Thin mask/silk export faces were omitted to retain valid STEP solids.
The C3 UBF31-0171 USB receptacle is represented by a generic GCT package model;
this is not exact manufacturer USB-shell geometry. See the per-reference
provenance and accuracy report. These are partial reference previews, not
manufacturer assembly CAD or mechanical qualification.

Component geometry is Copyright KiCad and its 3D-library contributors,
CC BY-SA 4.0 with the KiCad library exception. The pinned source commit is
a0244fe3442823dbb052ebc4820b4c2951e1742c (9.0.9).
See KICAD-LIBRARY-LICENSE.md and the component model source notices recorded
in the provenance receipt.

No affiliation or endorsement by Seeed or KiCad is asserted. These assets are
provided without warranties under their respective licenses. The repository's
MIT license does not replace the licenses for these third-party-derived assets.
