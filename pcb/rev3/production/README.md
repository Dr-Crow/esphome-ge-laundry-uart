# Rev3A quote package

This directory is a quote and prototype artifact, not production authorization.
Upload the matching Gerber ZIP, BOM, and CPL as one revisioned set.

- `GERBER-GEA-Adapter-Rev3A.zip`
- `BOM-GEA-Adapter-Rev3A.csv`
- `CPL-GEA-Adapter-Rev3A.csv`

- The Gerber ZIP defines copper, solder mask, silkscreen, board outline, and
  plated/non-plated drills.
- The BOM maps fitted references to exact parts and quantities.
- The CPL supplies fitted-part coordinates, side, and rotation using JLCPCB's
  documented `Designator`, `Mid X`, `Mid Y`, `Rotation`, and `Layer` headers.

J1 is the appliance-facing, through-hole EVERCOM `5301-8P8C` connector. A turnkey
quote must include it and show the correct orientation and through-hole assembly
method. DNP service/test items are intentionally excluded from BOM and CPL.

The PCB is 88.7 mm by 40.0 mm with four copper layers. The Gerber set must contain
`F.Cu`, `In1.Cu`, `In2.Cu`, and `B.Cu`; both inner layers are solid GND planes.

Do not order or connect a board to an appliance until the owner reviews the vendor
board, drill, parts, and placement previews. After fabrication, the current-limited
checks in [BRINGUP.md](../BRINGUP.md) must prove USB operation, all eight power-source
states, reverse-current isolation, regulator headroom, rail stability, temperature,
transient behavior, enclosure fit, and installed Wi-Fi performance.
