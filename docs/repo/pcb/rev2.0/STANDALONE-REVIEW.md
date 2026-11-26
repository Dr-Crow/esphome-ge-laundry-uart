# Rev 2.0 standalone source-review candidate

This focused candidate is based on public main `bc0d52495bd97ed1504bd0ca0775e47feb01a648` and carries only `pcb/rev2.0/` from reviewed source `17b41df540f792d20f0bc29dd736ecf97449f623`, plus its PCB index update. It is a local review unit. No push, PR publication, order, powered bench test, appliance test or hosted validation is established.

## Release status

The two original appliance input paths and manual JP2 selector remain. This source does not implement automatic selection/isolation between appliance pin 1 and pin 3. Historical parts and ratings remain; no 40 V protection backport or module/regulator substitution is introduced. U1 remains a known boot-loop concern in Rev 2.0/2.1 and stays DNP in Rev 2.2.

Every source/current/transient, component stress, regulator reverse-feed/thermal, supplier placement, physical connector/module/enclosure and appliance qualification gate remains open. Clean native rules and export pairing do not approve fabrication, power, appliance use or a fallback board. The inherited top-level overview, ordering guide and other revision rows describe older public-base material; their recommendations are not release evidence for this candidate.

## Service interface and power boundary

The native pin functions establish ESP RX at GPIO20, J2.4 and J3.5, and ESP TX at GPIO21, J2.5 and J3.3. J1.5 is adapter TX to appliance RX; J1.4 is appliance TX to adapter RX. Rev 2.0 retains appliance/programmer-perspective text: J2 RX is printed at the ESP TX path and J2 TX at the ESP RX path. Rev 2.1/2.2 source silk uses the adapter/ESP perspective. Physical boards and original archives must be interpreted using their own unchanged markings.

Programmer UART VCC leads must remain disconnected. Direct 3.3 V injection onto a regulator-output rail is not a qualified power method. UART direction is stated from the identified endpoint perspective; check each endpoint's native pin function. This review supplies no approved powering or bring-up recipe.

## Firmware review

Firmware is a separate universal pinned legacy/classic review unit. This PCB candidate retains public-base firmware bytes, whose external component revisions are unpinned. Those inherited configurations must not be described as the exact inputs to earlier successful builds. Rev 1.0 requires the separate classic ESP32 pin profiles; C3 profiles do not apply.

## Preserved review evidence

All native CAD, local libraries, manufacturing exports, original archives, retained machine-readable proofs and rendered review assets are copied byte-for-byte from the stated reviewed source, except the explicitly superseding Rev 2.1 dependency attestation below. Documentation only is adjusted for standalone navigation and review boundaries. Original archives remain distinct from current review CAM. Physical and hosted proof remain pending.

[PCB revision index](../README.md).

## Current schematic presentation

[Schematic normalization](validation/erc-normalization/DELTA-AND-INTEGRATION.md) resolves the four former aliases with canonical faithful UART/LED labels and explicit VCC presentation. Native KiCad 9.0.9 has zero errors/warnings/unconnected/parity. All 186 physical memberships/45 nets, PCB/CAM, firmware and architecture remain. Frozen earlier source/independent receipts are historical; ratings, module identity, assembly/placement/procurement and physical gates remain open.
