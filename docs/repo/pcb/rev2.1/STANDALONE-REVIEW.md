# Rev 2.1 standalone source-review candidate

This focused candidate is based on public main `bc0d52495bd97ed1504bd0ca0775e47feb01a648` and carries only `pcb/rev2.1/` from reviewed source `fe69d276e0031a752d600d55066d5f59a2018143`, plus its PCB index update. It is a local review unit. No push, PR publication, order, powered bench test, appliance test or hosted validation is established.

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

## Complete Rev 2.1 centroid attestation

[placement-origin-review.json](validation/placement-origin-review.json) is copied byte-for-byte from `7df3567e2785f3937ca9884a226c557eda3318e0`. Its SHA-256 is `1ac8ac51e72b080097d3a80d5c06ede7a7365d137ff103855d10d569b63c37e1` and it binds all 80 native source/library dependencies. CAD, libraries, anchor geometry, three centroid records, BOM, CPL and CAM bytes are unchanged. J1/U3/U6 exactly use native pad-bounding-box centers; other fitted references use native anchors. Supplier package/model/process alignment remains unqualified.

The retained assembly-centroid-offsets.json records the previous attestation hash as historical metadata. That old evidence hash is superseded by the complete attestation linked above; it is not the current proof hash. The preservation and export records remain untouched.

[PCB revision index](../README.md).
