# Board validation and current decisions

[Comparison](README.md) · [Exact source heads](HANDOFF.md) · [Pricing](PRICING.md) · [Finish plan](FINISH-PLAN.md)

Updated October 4, 2026; source and quote snapshot: October 3. The shared Rev3C design with two 40 V-rated TPS1H200A switches is selected. It retains both appliance PIN1/PIN3 inputs, automatic PIN1 priority, the AP63205 buck and C3/C6 header functions. Applicable protection backports to Rev3A/B are authorized next; older revisions remain separate. Selection and digital passes do not qualify a 40 V board, appliance operation, assembly, thermal behavior or enclosure.

## Current native checkpoints

Genuine KiCad **9.0.9**, full severities, expanded track reporting and schematic parity were used. Counts below are source-bound; each row's full local commit is recorded in [HANDOFF.md](HANDOFF.md). No physical test or manufacturing release is claimed.

| Revision / local checkpoint | ERC errors / warnings | DRC errors / warnings | Unconnected / parity | Scope and remaining limits |
| --- | ---: | ---: | ---: | --- |
| Restored Rev1.0 `12f82aa` | 0 / 1 | 0 / 0 | 0 / 0 | One VCC/+5V alias warning retained; generic classic ESP32, external buck, PIN1 only; original archive has no BOM/CPL |
| Restored Rev2.0 `17b41df` | 0 / 4 | 0 / 0 | 0 / 0 | Four alias warnings retained; manual dual input; current export/provenance closeout in progress |
| Rev2.1 `fe69d276` | 0 / 0 | 0 / 0 | 0 / 0 | 60 fitted references; three source-bound pad-center placement conventions need supplier review |
| Rev2.2 `0ee8e021` | 0 / 0 | 0 / 0 | 0 / 0 | 59 fitted references; legacy power/current/thermal and physical gates remain |
| Rev3A `d1769b2` | 0 / 53 | 0 / 5 | 0 / 0 | All 62 intended-rule errors repaired; 93 fitted references; routing process and protection gates remain |
| Rev3B `0b957ba` | 0 / 0 | 0 / 0 | 0 / 0 | 82 fitted references; rated protection backport not yet implemented |
| Selected Rev3C `fafd3ea` / electrical `7bb455f` | 0 / 0 | 0 / 0 | 0 / 0 | 83 matched BOM/CPL references; current-source checks pass; power/physical qualification remains open |

Rev3A's original configured Power patterns missed slash-prefixed nets. Correct intended patterns exposed 62 expanded errors (57 under standard aggregation); the repair retains the 0.25 mm Power clearance and now has zero errors under both modes. TP12's native clearance is **0.2502 mm**, only 0.2 µm above the rule. Nominal 0.14/0.16 mm via annuli also require supplier finished-annulus/process review. These geometry passes are not tolerance guarantees. Its retained 53 ERC and five DRC warnings are explicit, not erased.

The Rev2.1/2.2 C9/C10 courtyard issue is now resolved in their current cleanup sources. Rev2.1's J1/U3/U6 centroid conventions are separately documented and source-bound; native pad-center agreement does not approve supplier placement. Existing original archives remain historical artifacts.

## Historical source and engine boundaries

| Exact original source | ERC errors / warnings | DRC errors / warnings | Unconnected / parity | Classification |
| --- | ---: | ---: | ---: | --- |
| Rev1.0 `8798404` | 3 / 276 | 0 / 51 | 0 / 59 | Electrical pin membership matched; 59 parity findings were generated net-name metadata |
| Rev2.0 `af1f2c4` | 3 / 168 | 1 / 62 | 0 / 6 | Electrical membership matched by source UUID; reference aliases plus two absent DNP mechanical placeholders; one starved GND thermal |

Recovery of original bytes does not establish source-to-CAM geometry parity. Rev1's retained Gerber archive is the original Git blob, with no BOM/CPL inside. Rev2's original archive and standalone CPL differ by six genuine 180° semiconductor rotations; nine diode rotations differ from native placement in both. Possible supplier conventions were not approval evidence. Current exports must be checked against the restored source independently.

Earlier interface/electrical research used KiCad **9.0.2** netlist/geometry extraction. It was not a 9.0.9 ERC/DRC rerun. Six earlier 9.0.2 courtyard findings did not reproduce on the exact public 9.0.9 source; that does not erase the separate intended Power-routing findings repaired on Rev3A. Keep source, engine, libraries, severities and aggregation attached to each result; counts from different runs are not interchangeable.

Rev2's `FullRX5` and `FullTX4` labels use appliance/programmer perspective: `FullRX5 ← ESP GPIO21 TX`, `FullTX4 → ESP GPIO20 RX`. They are not intrinsically miswired or blanket “swapped UART labels.” Current Rev2.1/2.2 service documentation states the ESP perspective explicitly. Their C3 profiles do not match Rev1's classic ESP32 wiring.

## Power and service limits

The selected Rev3C's TPS1H200A switches add margin against the conditional SMF16A 26 V clamp example that exceeds TPS22810's 20 V absolute input rating. The design adds PIN3 TVS and source-referenced nominal 12 V gate clamps, retains reverse-PMOS/OR/priority/buck architecture and uses 33 V PPTCs. Its PMOS, buck, fuses, differentials and pulse energy have separate limits; **40 V switches do not make a 40 V carrier** or prove that GE supplies that pulse. Current limit/retry behavior, source current, low-input loaded startup and thermal bounds remain unqualified.

FirstBuild has two TPS22810 paths, transistor PIN1 priority, OR diodes and an AP2204K-5.0TRG1 linear regulator. Its D101 is reverse across the LDO, not a forward series output loss; no carrier input PTCs appear in its schematic/BOM. Our AP63205 buck adds L1/support parts and forward D11 loss. Neither net naming nor an ideal 5.000 V assumption establishes real module headroom. [Original FirstBuild schematic](https://github.com/geappliances/home-assistant-adapter/blob/4888a7df56e8ce6382ed91e4b95bd5020f1802f6/doc/schematic-v1.0.pdf).

Legacy Rev2.x keeps manual selection and linear regulation. Rev2.2's TECH PUBLIC U6 C19268131 is rated 200 mA; restored Rev2/Rev2.1 instead select C5205181 and retain an AP2205-3.3 value versus AP2204R-3.3 symbol/datasheet ambiguity. Their exact populated-part identity and supply capability require separate review. TVS/PMOS gate/capacitor coordination, zener/fuse/regulator thermal behavior and loaded startup remain gates. Rev1 has only its original PIN1 path and an unidentified external buck. Do not apply a shared-carrier rating or firmware profile to those architectures.

Use one reviewed supply, leave UART VCC disconnected and do not inject a module's 3V3 output. Rev3B/C require disconnecting appliance power before powered USB. Rev3A's separate USB/appliance isolation paths need bench checks. Actual appliance model, loaded voltage/current, transients, hot/cold startup, inrush, Wi-Fi peaks and recovery behavior remain unmeasured.

## Firmware and CI evidence

Eight actual local ESPHome **2026.9.1 config and compile** results use ESP-IDF **5.5.5** and pinned GEA `283ff2b0dfe90a6d14a5417a23176d433be8a5b3`, with factory/OTA/ELF hashes recorded. Shared/classic outputs remain local; the original temporary legacy binaries are no longer present, so only their recorded output hashes remain.

| Profile family | Real builds | Proven UART assignments, TX / RX |
| --- | ---: | --- |
| Legacy C3 GEA2 / GEA3 | 2 | GPIO5 / 10; GPIO21 / 20 |
| Shared XIAO C3/C6 × GEA2/GEA3 | 4 | C3: 5 / 10 and 21 / 20; C6: 21 / 18 and 16 / 17 |
| Rev1 classic ESP32 GEA2 / GEA3 | 2 | GPIO18 / 19 inverted 19,200; GPIO17 / 16 non-inverted 230,400 |

Classic candidate `dde0af3` configures only proved carrier LED GPIO13; its exact purchased 38-pin module remains unknown. GEA2 has eight format plus one unused-function warning; GEA3 has seven format plus one unused-function warning. They include ERD/text decimal conversions, not only logging. Xtensa `int`/`long` have matching 32-bit widths and signedness here, with no evidenced argument displacement/truncation; the printf type-contract defects remain and runtime formatting was not tested. No device was flashed, attached or functionally tested. Shared Matter/Thread appliance firmware is not implemented.

Universal CI source `563f5ba` has seven meaningful regression tests, separate native/source/manufacturing/firmware checks and current-source-bound qualification gates. Its current manifest declares the two legacy profiles; shared/classic successes are separate local build evidence, and their full CI-manifest integration remains to be reviewed. Local test/schema validation passed; pinned KiCad 9.0.9 and ESPHome 2026.9.1 containers are specified. **Fresh container execution and hosted jobs have not run.** The latest integration tree combines selected Rev3C, repaired Rev3A, legacy updates and classic profiles; integration is a source checkpoint, not hosted execution. Missing source, infrastructure failure and stale/untracked evidence remain failures.

## Mechanical and delivery boundary

Legacy case `5e01d79` passes native C3 geometry checks with unchanged CAD; current rated-component heights were not re-derived. It is C3-only, never the default shared enclosure. Exact five-piece common CAD is unavailable and needs restoration, source provenance, calibration, fit and actuator qualification. Module retention, vibration, USB/buttons, antenna/pigtail clearance and RF remain physical gates. Original galleries are historical.

All current review heads are local and unpublished. No new order, PR, upstream publication, hosted run or physical qualification is included. [FINISH-PLAN.md](FINISH-PLAN.md) records what remains and what evidence can close it.
