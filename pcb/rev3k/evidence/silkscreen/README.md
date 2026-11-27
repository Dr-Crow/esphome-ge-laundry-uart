# Rev 3K silkscreen review

[Component side](top.png) · [Physical underside](bottom.png) · [Native and optical checks](validation.json)

The QR between the two XIAO socket rows opens the public [project repository](https://github.com/Dr-Crow/esphome-ge-laundry-uart). View it from the underside with the board out of the enclosure. The code is version 4 with medium error correction, 33 × 33 modules at 0.31 mm each. Four clear modules on every side are part of the 12.71 mm white field. Dark modules are the underlying solder mask. Use white legend on a dark mask and reserve this area from factory order marks or stickers.

The component side marks the XIAO USB end before the module is inserted. The underside identifies the appliance port, the module's 5 V, ground and 3.3 V socket joints, and the green Wi-Fi, red user-controlled and yellow bus-status LEDs. The disconnect-before-USB warning and prototype ID remain visible. The two sides are shown as each is viewed physically. Existing diagnostic and selector markings are retained where fitted.

KiCad 9.0.9 ERC, all-track DRC and schematic parity passed. The exported top and bottom strokes are at least 0.15 mm. The artwork check decoded the full underside Gerber composite, a half-scale image, a blurred image and a rotated image using ZXing. It compared every QR module and the surrounding quiet zone to the encoded matrix and checked the bottom mask for openings. Four copper layers, both mask and paste layers, outline and both drill programs match the prior review after removing generator/date and project-title metadata. The BOM, CPL and case geometry are unchanged. Verify a phone scan of an actual printed board before accepting production. All electrical and mechanical prototype gates still apply.

[Silkscreen printing guidance](https://jlcpcb.com/blog/pcb-silkscreen) · [QR quiet-zone specification](https://www.qrcode.com/en/howto/code.html)
