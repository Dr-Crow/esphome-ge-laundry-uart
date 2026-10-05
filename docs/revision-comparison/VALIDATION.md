# Board validation and current decisions

## Current integration recheck

The new `integration/ge-restored-final-2026-10-04` branch combines the complete genuine final per-revision, firmware, CI and comparison histories. It includes the selected Rev3C stencil correction `b87d3e8`. It is a newly identified integration; the earlier `f85ba98` integration's omitted ancestor/tree remains unavailable.

Fresh local checks on October 4 after source restoration use the exact KiCad 9.0.9 image, official pinned libraries and matching Python/pcbnew runtime. All seven full-severity ERC/all-track DRC checks and all seven intended-rule audits pass with zero errors, warnings, open connections or schematic-parity issues. Source/CAM parity passes all seven. Full BOM/CPL manufacturing checks pass Rev2.1/2.2/3A/3B/3C; Rev1/Rev2's missing current supplier inputs stay explicit failures. Twenty-eight regression tests pass, including rejection of source-matched drill-marker stencils and deleted legacy Power-net memberships.

The current [CI review receipt](../../ci/validation/INTEGRATED-CI-REVIEW.json) binds all 380 CAD dependencies, current configuration/test hashes and eight profile/include inventories. CircleCI schema validation accepted the exact current configuration on October 4 using CLI 1.0.51932; its [separate receipt](../../ci/validation/INTEGRATED-CIRCLECI-SCHEMA.json) records the hashes. All 21 power/source/physical release gates remain blocked. Fresh firmware config/compile and hosted jobs have not run in this integration. Older compilation and integration reports below retain their historical source boundaries; their binaries are not freshly verified.

Rev3C's [stencil review](../../pcb/rev3c/STENCIL-REVIEW.md) removes 26 unintended openings from each paste layer; existing SMT geometry and BOM/CPL are preserved. Rev2.1/2.2/3A/3B already use drillshape 0, and independent fresh native paste/CAM audits pass. Unplaced source-paste apertures remain for Rev2.2 U1 and Rev3A/3B/3C D8 and require assembler review. Rev3C’s October 5 quote now matches the corrected ZIP: USD 134.64 for five or 168.92 for ten assembled carriers; placement/stencil/process qualification remains open.

## Prior engineering checkpoints

[Comparison](README.md) · [Exact source heads](HANDOFF.md) · [Pricing](PRICING.md) · [Finish plan](FINISH-PLAN.md)

Updated October 4, 2026 at 06:58 UTC; strict seven-revision native checks and exact source-bound quote snapshots. The shared Rev3C design with two 40 V-rated TPS1H200A switches is selected. It retains both appliance PIN1/PIN3 inputs, automatic PIN1 priority, the AP63205 buck and C3/C6 header functions. The Rev3B rated-protection backport has passed independent digital review; Rev3A rated protection, exact connector lands and zero-warning schematic normalization are independently reviewed and staged; all seven revisions now have zero native findings. Older revisions remain separate. Selection and digital passes do not qualify a 40 V board, appliance operation, assembly, thermal behavior or enclosure.

## Current native checkpoints

Genuine KiCad **9.0.9**, full severities, expanded track reporting and schematic parity were used. Counts below are source-bound; each row's full local commit is recorded in [HANDOFF.md](HANDOFF.md). No physical test or manufacturing release is claimed.

| Revision / local checkpoint | ERC errors / warnings | DRC errors / warnings | Unconnected / parity | Scope and remaining limits |
| --- | ---: | ---: | ---: | --- |
| Rev1.0 `53a4b3d` | 0 / 0 | 0 / 0 | 0 / 0 | Explicit faithful VCC presentation; 166 physical tuples unchanged; native/current CAM passes; original BOM/CPL and actual module/buck identity missing |
| Rev2.0 `5c8afe4` | 0 / 0 | 0 / 0 | 0 / 0 | Canonical UART/LED and explicit VCC presentation; 186 physical tuples unchanged; current CAM passes; historical supplier rotations/part identity remain unqualified |
| Rev2.1 `3d98559` / source `fe69d276` | 0 / 0 | 0 / 0 | 0 / 0 | 60 refs; three source-bound pad-center conventions; source-specific legacy power/placement gates remain |
| Rev2.2 `b00c96f` / source `0ee8e021` | 0 / 0 | 0 / 0 | 0 / 0 | 59 refs; native cleanup/manufacturing passes; regulator/current/protection/thermal gates remain |
| Rated Rev3A `615863d` | 0 / 0 | 0 / 0 | 0 / 0 | 97 refs; body J1/J4/U2 datums, recommended J4 shell slots/lands, explicit EN capacitor; source/body-CPL/CAM and 14 pixel views independently reviewed |
| Rated Rev3B `ce2979b` | 0 / 0 | 0 / 0 | 0 / 0 | 85 refs; typed J1/U2 datums; native-registered partial C3 model; exact module stock/process and physical gates open |
| Selected Rev3C `5542734` / quote `b53cfca` | 0 / 0 | 0 / 0 | 0 / 0 | 83 refs; typed J1 datum; source-preserving C3/C6 module/SoC previews; complete current quotes; qualification open |

The combined source at `dbcfef6` passed fresh strict native checks for all seven revisions. Later documentation checkpoint `f85ba98` changes only the CI README and review summary; current native/firmware/manifest inputs remain byte-identical. No severity, rule, grid or exclusion waiver was used. All 25 validator tests pass. Five modern source-bound manufacturing checks pass; Rev1/Rev2 CAM also matches, while supplier BOM/CPL absence remains explicit red. Their intended-netclass audits remain red because no reviewed policy is declared. All 21 power/source/physical readiness gates remain blocked.

Rev3A's provenance remains separate: `d1769b2` repaired all 62 intended Power errors under unchanged 0.25 mm clearance with 53 ERC and 5 DRC warnings; rated freeze `d2bde08` reached 0 ERC errors/9 warnings and 0 DRC findings. Schematic-only normalization resolves those nine while preserving all 301 physical ref/pin/net/function/type tuples and 72 nets; meaningful native controls reject changed supply/UART memberships. USB endpoints use the existing 25 mil grid and VCC is connected explicitly with its datasheet name. No PCB or power topology is changed by that presentation cleanup.

A's reviewed J4 exact SHOU HAN C2765186 footprint now matches forward shell drills 0.60×1.40mm and lands 1.00×1.80mm. Top-mount seating is possible on 1.6 mm; the approximately 1 mm legs remain recessed and no shell paste apertures are defined. Assembler-approved solder delivery, inspection and retention remain gates. TP12 is 0.250201 mm from D5A, only 0.000201 mm above the Power rule; finished annulus/stencil and return-path/fill effects also need process/physical qualification. Direct native Gerber ZIP viewing hit OS error11 after a bounded retry; exact 14-member CAM reproduction and actual source schematic/copper/drill/3D pixels passed.

Current B/C placement uses separately typed nominal manufacturer/module-body points: J1(8.645,−16.995) mm on B/C; B U2(87.89,−12.90) mm. A J1 is (8.645,−17.000) mm; its U2 integrated module and J4 have source-specific proofs. Native rotations/sides and unrelated rows are retained; stale corner origins fail controls. These are documented conventions, not approval of supplier private library zero, actual body/pad/pin1 alignment or process. Supplier previews did not render; the J1 public library iframe was blocked by Chromium. No restriction bypass was used.

A's native 49-row BOM is serialized as 97 one-reference supplier rows with all fields/parts equivalent; exact reimport clears the unselected-parts warning. Current A quotes include its integrated C3; B's exact C3 module shortage prevents a full quote. Historical archives and earlier raw source proofs retain their explicit old hashes. Current native counts do not make legacy boards safe fallbacks.

## Historical source and engine boundaries

| Exact original source | ERC errors / warnings | DRC errors / warnings | Unconnected / parity | Classification |
| --- | ---: | ---: | ---: | --- |
| Rev1.0 `8798404` | 3 / 276 | 0 / 51 | 0 / 59 | Electrical pin membership matched; 59 parity findings were generated net-name metadata |
| Rev2.0 `af1f2c4` | 3 / 168 | 1 / 62 | 0 / 6 | Electrical membership matched by source UUID; reference aliases plus two absent DNP mechanical placeholders; one starved GND thermal |

Recovery of original bytes does not establish source-to-CAM geometry parity. Rev1's retained Gerber archive is the original Git blob, with no BOM/CPL inside. Rev2's original archive and standalone CPL differ by six genuine 180° semiconductor rotations; nine diode rotations differ from native placement in both. Possible supplier conventions were not approval evidence. Both final historical packages now have independent-review closeout and regenerated source-bound current CAM, kept separate from the preserved originals. Rev1's missing original BOM/CPL remains a procurement gate; Rev2's supplier rotations remain unqualified.

Earlier interface/electrical research used KiCad **9.0.2** netlist/geometry extraction. It was not a 9.0.9 ERC/DRC rerun. Six earlier 9.0.2 courtyard findings did not reproduce on the exact public 9.0.9 source; that does not erase the separate intended Power-routing findings repaired on Rev3A. Keep source, engine, libraries, severities and aggregation attached to each result; counts from different runs are not interchangeable.

Rev2's `FullRX5` and `FullTX4` labels use appliance/programmer perspective: `FullRX5 ← ESP GPIO21 TX`, `FullTX4 → ESP GPIO20 RX`. They are not intrinsically miswired or blanket “swapped UART labels.” Current Rev2.1/2.2 service documentation states the ESP perspective explicitly. Their C3 profiles do not match Rev1's classic ESP32 wiring.

## Power and service limits

The selected Rev3C's TPS1H200A switches add margin against the conditional SMF16A 26 V clamp example that exceeds TPS22810's 20 V absolute input rating. The design adds PIN3 TVS and source-referenced nominal 12 V gate clamps, retains reverse-PMOS/OR/priority/buck architecture and uses 33 V PPTCs. Its PMOS, buck, fuses, differentials and pulse energy have separate limits; **40 V switches do not make a 40 V carrier** or prove that GE supplies that pulse. Current limit/retry behavior, source current, low-input loaded startup and thermal bounds remain unqualified.

FirstBuild has two TPS22810 paths, transistor PIN1 priority, OR diodes and an AP2204K-5.0TRG1 linear regulator. Its D101 is reverse across the LDO, not a forward series output loss; no carrier input PTCs appear in its schematic/BOM. Our AP63205 buck adds L1/support parts and forward D11 loss. Neither net naming nor an ideal 5.000 V assumption establishes real module headroom. [Original FirstBuild schematic](https://github.com/geappliances/home-assistant-adapter/blob/4888a7df56e8ce6382ed91e4b95bd5020f1802f6/doc/schematic-v1.0.pdf).

Legacy Rev2.x keeps manual selection and linear regulation. Rev2.2's TECH PUBLIC U6 C19268131 is rated 200 mA; restored Rev2/Rev2.1 instead select C5205181 and retain an AP2205-3.3 value versus AP2204R-3.3 symbol/datasheet ambiguity. Their exact populated-part identity and supply capability require separate review. TVS/PMOS gate/capacitor coordination, zener/fuse/regulator thermal behavior and loaded startup remain gates. Rev1 has only its original PIN1 path and an unidentified external buck. Do not apply a shared-carrier rating or firmware profile to those architectures.

Use one reviewed supply, leave UART VCC disconnected and do not inject a module's 3V3 output. Rev3B/C require disconnecting appliance power before powered USB. Rev3A's separate USB/appliance isolation paths need bench checks. Actual appliance model, loaded voltage/current, transients, hot/cold startup, inrush, Wi-Fi peaks and recovery behavior remain unmeasured.

## Firmware and CI evidence

Eight historical local ESPHome **2026.9.1 config and compile** results use ESP-IDF **5.5.5** and pinned GEA `283ff2b0dfe90a6d14a5417a23176d433be8a5b3`, with factory/OTA/ELF hashes recorded. The earlier temporary output binaries are not included in the restored package; their recorded output hashes remain historical evidence and have not been freshly verified.

| Profile family | Real builds | Proven UART assignments, TX / RX |
| --- | ---: | --- |
| Legacy C3 GEA2 / GEA3 | 2 | GPIO5 / 10; GPIO21 / 20 |
| Shared XIAO C3/C6 × GEA2/GEA3 | 4 | C3: 5 / 10 and 21 / 20; C6: 21 / 18 and 16 / 17 |
| Rev1 classic ESP32 GEA2 / GEA3 | 2 | GPIO18 / 19 inverted 19,200; GPIO17 / 16 non-inverted 230,400 |

Classic candidate `dde0af3` configures only proved carrier LED GPIO13; its exact purchased 38-pin module remains unknown. GEA2 has eight format plus one unused-function warning; GEA3 has seven format plus one unused-function warning. They include ERD/text decimal conversions, not only logging. Xtensa `int`/`long` have matching 32-bit widths and signedness here, with no evidenced argument displacement/truncation; the printf type-contract defects remain and runtime formatting was not tested. No device was flashed, attached or functionally tested. Shared Matter/Thread appliance firmware is not implemented.

Universal CI candidate `0d3358a` has 25 meaningful boundary tests, canonical local dependency closure, separate native/source/manufacturing/firmware/intended-rule checks and source-bound release gates. Its standalone current-main manifest declares the two legacy profiles. Complete-source checkpoint `7df3567` declares all eight legacy/shared/classic profiles, verifies 356 CAD dependencies including 16 STEP assets and has independent review closeout. That prior combined checkpoint included all seven warning-free native sources, 380 local design dependencies/28 STEP assets, typed A/B/C body datums and current supplier serialization/model receipts. All 25 tests passed after integration; all eight real build inputs remain matched. The final CircleCI config including the validator-tests job passed the official CLI schema service at 05:31 UTC. Fresh containers and hosted jobs have not run.  Missing source, infrastructure failure and stale/untracked evidence remain failures.

## Mechanical and delivery boundary

Legacy case `5e01d79` passes native C3 geometry checks with unchanged CAD; current rated-component heights were not re-derived. It is C3-only, never the default shared enclosure. Exact five-piece common CAD is unavailable and needs restoration, source provenance, calibration, fit and actuator qualification. Module retention, vibration, USB/buttons, antenna/pigtail clearance and RF remain physical gates. Original galleries are historical. Current C3/C6 previews now use official Seeed PCB geometry, licensed package models, dimension-checked 5 ×5 mm SoC bodies/pin 1 poses and separately reviewed RJ45/socket drawings. Carrier electrical/CAM/firmware bytes were preserved by model-only changes. Complete revision-matched assembly models, button/U.FL identities, seating and case fit remain unresolved; detailed-looking partial models do not close those gates.

All current review heads are local and unpublished. No new order, PR, upstream publication, hosted run or physical qualification is included. [FINISH-PLAN.md](FINISH-PLAN.md) records what remains and what evidence can close it.
