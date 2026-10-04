# Selected Rev3C prototype: shared XIAO C3/C6 carrier

The selected development design uses two **TPS1H200A 40 V-rated switches**, 33 V resettable input fuses, and coordinated review of both GE power branches. It preserves PIN1 and PIN3 inputs, automatic PIN1 priority, the AP63205 buck and all C3/C6 side-header functions. C3 is the first implementation focus; C6 firmware and mechanical flexibility remain. Selection does not qualify the appliance supply, surge energy, loaded startup, thermal behavior or enclosure.

The switch change adds voltage margin against the conditional 26 V SMF16A clamp example that exceeds the former TPS22810’s 20 V absolute input limit. It does not give the entire carrier a 40 V rating or prove that a GE appliance produces that pulse. Read the [rated-input review](RATED-SWITCH-OPTION.md) and [qualification gates](POWER-QUALIFICATION.md).

[PCB revision index](../README.md) · [Gate repair](GATE-PROTECTION.md) · [Power qualification](POWER-QUALIFICATION.md) · [Antenna review](ANTENNA-REVIEW.md) · [Shared firmware](../../firmware/shared-rev3c/README.md)

## Preserved hardware

- Original 99 × 40 mm outline, four copper layers and 1.6 mm board thickness
- Mounting datums at (4.5, 33) and (94, 35) mm
- Factory-populated `J5`/`J6` HCTL PM254-1-07-Z-8.5 female 1×7 sockets and all 14 side-header functions
- GEA2/GEA3 interfaces, LEDs, pull-ups and `JP1`'s default 1–2 bridge
- Both original input branches, corrected reverse-FET/gate networks, selected rated load switches, diode isolation, common AP63205 buck and automatic PIN1 priority

The shared-source omissions are `J2` and `D19`; neither GE power input is removed. The local C6 antenna change adds an all-layer copper exclusion at x77.0–80.9, y11.8–19.2 mm and minimal reroutes of `GEA2_RX`, `GEA2_MCU_TX` and `BOOT_SEL`. The selected rated-switch design preserves the original selection and conversion topology. See the [antenna review](ANTENNA-REVIEW.md) for geometry and limits.

The [KiCad project](design/GEA-Adapter-Rev3C.kicad_pro), [schematic](design/GEA-Adapter-Rev3C.kicad_sch) and [PCB](design/GEA-Adapter-Rev3C.kicad_pcb) are editable review sources. Restoration starts from public Rev3C commit `38d94d3dc7c41692e3c41710ec33b9f6e0c38b3e` and recovered shared schematic blob `2799d9e3f023144f684d708297805eed4f355355`.

## Module and firmware selection

The side-header functions match the [XIAO ESP32-C3](https://wiki.seeedstudio.com/XIAO_ESP32C3_Getting_Started/) and [XIAO ESP32-C6](https://wiki.seeedstudio.com/xiao_esp32c6_getting_started/) references. The module is supplied separately from the assembled carrier. Use a module with all 14 header pins installed, and verify its actual revision, header mating depth and retention before use. This interface review does not establish compatibility with other XIAO models.

The [four shared firmware profiles](../../firmware/shared-rev3c/README.md) cover C3/C6 and GEA2/GEA3. Their GPIO numbers differ by module; the recovered eight YAML sources are unchanged. Keep `JP1` at 1–2 for these GEA2 profiles. The alternate 2–3 position changes TX and reaches C3 BOOT; the corresponding C6 D9 pin is GPIO20, not C6 BOOT.

Insert or remove the module only with all power disconnected. Seat all 14 pins without reversal or row offset; the sockets are unkeyed. Match the module USB connector to the carrier's right edge and orientation mark. Recovery uses the module's own BOOT/RESET buttons and native USB. There is no populated carrier recovery header or auxiliary 5 V recovery input.

## Power and qualification

PIN1 and PIN3 from one appliance are two internally selected input branches. Disconnect the appliance cable before attaching powered USB, and remove USB before appliance use. Both reviewed modules connect side-header VBUS directly to USB receptacle VBUS; carrier diodes do not isolate a connected USB host. Keep UART VCC disconnected. Use module 3V3 only as its output. Do not attach a battery within the reviewed load budget.

The corrected reverse-FET/source-referenced gate networks remain. The rated switches address the old switch/clamp rating mismatch in a bounded positive-pulse comparison, and PIN3 gains its matching TVS. Whole-chain transient/energy/differential limits, source current, current-limit/retry effects, thermal behavior and both modules' nominal5 V loaded startup remain open in [POWER-QUALIFICATION.md](POWER-QUALIFICATION.md). Automatic priority detects PIN1 presence rather than useful output power. No universal appliance compatibility is established.

## Review package and cost

Native KiCad 9.0.9 full-severity [ERC](validation/native-kicad-9.0.9-erc.json) and all-track/[parity DRC](validation/native-kicad-9.0.9-drc.json) report 0 violations,0 unconnected items and0 parity differences. The current [rated-switch proof](validation/rated-switch-proof.json) verifies 100 schematic/PCB items,233 pin nets,205 unchanged nonreplacement pin nets, original core functions/outline/mounts/sockets/firmware and0.0 mm² filled copper in the antenna exclusion on all four layers. The historical restoration/gate proofs describe their frozen checkpoints, not the current rated design's full delta.

The regenerated [BOM](manufacturing/BOM-GEA-Adapter-Rev3C.csv) and [CPL](manufacturing/CPL-GEA-Adapter-Rev3C.csv) each contain 83 matching fitted references,80−C22/C23+R38/R39/R40/R41/D20. The module is supplied separately; DNI D8 stays excluded. The native [Gerber/drill ZIP](manufacturing/GERBER-GEA-Adapter-Rev3C.zip) contains 14 members. [Schematic](validation/schematic.pdf), [PTH](validation/pth-drill-map.pdf) and [NPTH](validation/npth-drill-map.pdf) review PDFs are refreshed.

Current copper views: [front](images/rev3c-copper-f-cu.svg), [inner ground](images/rev3c-copper-in1-cu.svg), [inner routing](images/rev3c-copper-in2-cu.svg), [bottom](images/rev3c-copper-b-cu.svg). Current native partial previews: [C3 top](images/rev3c-render-top.png), [bottom](images/rev3c-render-bottom.png), [C3 oblique](images/rev3c-render-oblique.png), [C6 alternative](images/rev3c-render-c6-oblique.png). The [component model accuracy checkpoint](MODEL-ACCURACY.md) explains the revision-specific official PCB-derived C3/C6 geometry, generic USB/package substitutions, omitted module parts, drawing-based RJ45/socket detail and provisional installed height. Complete manufacturer assembly CAD was not verified; shield/buttons/antenna/male headers are omitted; a separately registered nominal U.FL reference is included and switch/PPTC maximum envelopes remain. Actual pixels were inspected. The [electrical preservation receipt](validation/component-model-electrical-preservation.json) proves that this model lane leaves all electrical source, manufacturing files and firmware unchanged.

Complete exact-part JLCPCB quotes checked on October 3, 2026 are **$134.64 for five assembled carriers** and **$168.91 for ten**, before shipping, tax and separately supplied XIAO modules. The source-corrected 80-part baseline was $130.39/$160.37 under the same settings, making the selected design about **$0.85 more per carrier**. All 83 references, including RJ45 and sockets, matched; these are price/availability checks rather than placement or manufacturing approval.

Use the illustrated [JLCPCB quote and ordering guide](ORDERING.md) for the matching Gerber/BOM/CPL trio, exact file hashes, observed settings and review steps. Never mix the selected 83-reference files with the historical baseline. D16/D17 use reviewed MCC BZT52C12-TP/C668891; R40/R41 use the exact 100 kΩ resistor under stocked C149504. The [clamp comparison](RATED-SWITCH-OPTION.md#reviewed-gate-clamp-sourcing-correction) retains MCC’s impedance, temperature and transient limits. CPL and factory ZIP bytes remain those checked for source `7bb455f`.

The selected switches add approximately 86 mV of illustrative path loss at 364 mA and change startup/current-fault behavior. Neither the quote nor a native pass closes the loaded 5 V, current, thermal or transient gates. No order or physical test has been performed.

## Enclosure

No Rev3C enclosure is included as the default for this shared candidate. The original C3-specific Rev3C case was not copied into it and is not a shared C3/C6 or C6 case. Physical socket height, retention, vibration, USB access, both modules' BOOT/RESET access, antenna/pigtail clearance and RF performance in a final enclosure remain untested.

The [placement-datum review](validation/PLACEMENT-DATUM-REVIEW.md) corrects J1’s CPL body centre without changing CAD, BOM or rotation. Earlier quote hashes remain historical; actual supplier-library pose/process approval is still required.
