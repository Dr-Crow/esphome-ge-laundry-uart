# Rev 1.0 standalone source-review candidate

This focused candidate is based on public main `bc0d52495bd97ed1504bd0ca0775e47feb01a648` and carries only `pcb/rev1.0/` from reviewed source `3bb5f854f35c7d263d3c55392ac68ffac3995b25`, plus its PCB index update. It is a local review unit. No push, PR publication, order, powered bench test, appliance test or hosted validation is established.

## Release status

This historical board retains one appliance pin-1 power input and an external buck module. Appliance pin 3 remains unconnected. The purchased ESP32/buck module identity, protection coordination and all electrical/thermal/physical qualification remain open.

Every source/current/transient, component stress, regulator reverse-feed/thermal, supplier placement, physical connector/module/enclosure and appliance qualification gate remains open. Clean native rules and export pairing do not approve fabrication, power, appliance use or a fallback board. The inherited top-level overview, ordering guide and other revision rows describe older public-base material; their recommendations are not release evidence for this candidate.

## Service interface and power boundary

Rev 1.0 retains its generic 38-pin classic ESP32 development-board interface. GEA2 TX/RX remain GPIO18/GPIO19; GEA3 TX/RX remain GPIO17/GPIO16. Its J1 is the external buck-module interface, not a qualified programmer-power input.

Programmer UART VCC leads must remain disconnected. Direct 3.3 V injection onto a regulator-output rail is not a qualified power method. UART direction is stated from the identified endpoint perspective; check each endpoint's native pin function. This review supplies no approved powering or bring-up recipe.

## Firmware review

Firmware is a separate universal pinned legacy/classic review unit. This PCB candidate retains public-base firmware bytes, whose external component revisions are unpinned. Those inherited configurations must not be described as the exact inputs to earlier successful builds. Rev 1.0 requires the separate classic ESP32 pin profiles; C3 profiles do not apply.

## Preserved review evidence

All native CAD, local libraries, manufacturing exports, original archives, retained machine-readable proofs and rendered review assets are copied byte-for-byte from the stated reviewed source, except the explicitly superseding Rev 2.1 dependency attestation below. Documentation only is adjusted for standalone navigation and review boundaries. Original archives remain distinct from current review CAM. Physical and hosted proof remain pending.

[PCB revision index](../README.md).

## Current schematic presentation

[Schematic normalization](validation/erc-normalization/integration-updates.json) resolves the former alias warnings with explicit faithful power presentation. Native KiCad 9.0.9 now reports zero errors/warnings/unconnected/parity. Original physical architecture, PCB/CAM, firmware and pin memberships remain; power/module/procurement/assembly/physical gates are still open. Earlier source/independent receipts are frozen historical evidence.
