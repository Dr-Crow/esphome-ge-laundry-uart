# Rev3C mechanical models

`Socket_1x07_P2.54mm_HCTL_PM254.step` is a millimetre STEP body envelope for
HCTL PM254-1-07-Z-8.5 (18.18 x 2.5 x 8.5 mm), positioned relative to pad 1.
It is based on the public manufacturer drawing and omits tails; it is not
manufacturer-supplied CAD.

`XIAO-ESP32-C3-Rev3C-installed-envelope.step` is a graphics-only,
build123d-generated envelope for the user-installed pre-headered Seeed module.
It includes the official module board outline, USB-C shell, BOOT/RESET switch
envelopes, U.FL location, a conservative complete-module height envelope, and
provisional 2.5 mm male-header spacers. The model is excluded from factory BOM
and position outputs. It is not evidence of physical fit or cosmetic geometry.

## XIAO ESP32-C3 alignment and source

- The module feature locations follow the official Seeed v1.3 KiCad project:
  <https://files.seeedstudio.com/wiki/XIAO_WiFi/Resources/XIAO_ESP32C3_v1.3_KiCad_260116.zip>.
- The public pin map and module information are at
  <https://wiki.seeedstudio.com/XIAO_ESP32C3_Getting_Started/>.
- The envelope uses the verified Rev3C socket transform and mirrored STEP Y
  coordinates for KiCad. The module bottom is shown 11 mm above the carrier
  PCB top (8.5 mm socket body plus provisional 2.5 mm male spacer). Verify
  mating engagement, USB cable, buttons, U.FL plug, and antenna clearance on
  the actual parts before fabrication.

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
