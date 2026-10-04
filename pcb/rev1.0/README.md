# PCB Rev 1.0

Rev 1.0 is the historical one-input carrier for a generic 38-pin classic ESP32 development board and an external buck module. It added resistor positions for inverted GEA2 serial signaling. Current C3 firmware profiles do not match this board's UART pins.

[Editable source](design/) has been restored from exact public commit `87984047ee029efb83bf9947dc21818fd18e39b3` and cleaned with project-local source definitions and explicit external-supply ERC modelling. The original pin/net groups, parts, routes, positions, outline and holes are retained. Only connector silk outside the board has a physical geometry edit. Genuine KiCad 9.0.9 reports zero ERC errors/warnings after explicit faithful VCC presentation, and zero DRC/parity/unconnected findings.

Read the [native source review](validation/NATIVE-REVIEW.md), [schematic](validation/schematic.pdf), [board views](validation/views/), and [source/export proof](validation/native-kicad-9.0.9/preservation-proof.json). The [current review CAM](review-manufacturing/) is separate from the byte-preserved [original Gerber archive](manufacturing/GERBER-OnionStraws-rev1.0.zip). No supplier BOM or CPL was present in the original package; none has been invented.

This historical source cleanup does not establish electrical/appliance qualification or manufacturing readiness. Original supply, protection, supervisor, buck-module, thermal and physical gates remain open. Classic ESP32 firmware is handled separately.

[Back to the PCB revision index](../README.md)

[Standalone candidate scope and release boundaries](STANDALONE-REVIEW.md).

## Current schematic presentation

[Schematic normalization](validation/erc-normalization/integration-updates.json) resolves the former alias warnings with explicit faithful power presentation. Native KiCad 9.0.9 now reports zero errors/warnings/unconnected/parity. Original physical architecture, PCB/CAM, firmware and pin memberships remain; power/module/procurement/assembly/physical gates are still open. Earlier source/independent receipts are frozen historical evidence.
