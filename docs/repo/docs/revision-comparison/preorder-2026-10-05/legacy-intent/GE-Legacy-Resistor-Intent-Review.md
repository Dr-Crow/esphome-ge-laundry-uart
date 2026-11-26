# GE legacy resistor intent review

Review date: 5 October 2026 UTC. Fixed integrated source: `11826a7f6ba1ed19131ddba46e4d62b06196a8c6`. This is a read-only engineering recommendation before any source or BOM change.

## Recommendation

For a newly reviewed Rev2.0 or Rev2.1 purchasing revision, retain the declared **R18/R21 = 220 kΩ and R22 = 4.7 kΩ**, and explicitly correct purchasing identities to **C104108 / RALEC RTT052203FTP** and **C17673 / UNI-ROYAL 0805W8F4701T5E**. These are the matching identities already used by Rev2.2 and current Rev3A/B/C. Make the adoption a documented purchasing decision, regenerate that revision's paired source/BOM/CPL evidence, and require loaded-interface qualification before release. Do not describe it as a proven recreation of the originally fitted hardware.

Preserve original Rev2.0/2.1 sources, archives and purchasing tables. Their C17539/C17713 identities document a plausible **historically procured 200 kΩ/47 kΩ build**, but the inspected record does not establish that this was a deliberately designed or qualified electrical variant. If reproducing such a physical board is the goal, retain it as a separate historical build with honest electrical values and independent test evidence; do not quietly relabel every revision or replace installed resistors. No source, BOM, footprint, placement, copper or physical part was changed by this review.

## Evidence of intent and its limits

1. At the original Rev2 beta commit [`af1f2c40029ef67c56910fb2c55feac835553525`](https://github.com/mulcmu/esphome-ge-laundry-uart/tree/af1f2c40029ef67c56910fb2c55feac835553525/pcb), the schematic and purchasing BOM both say R18/R21 **220k**, R22 **4K7**, while using C17539 and C17713. This proves the contradiction existed in the original purchasing package; it does not tell us what was fitted.
2. The complete three-resistor network occurs in **12 preserved backup schematic members**, dated 21–28 May 2025. Every one retains those same conflicting labels/codes. Five earlier members use an earlier reference inventory and are not evidence that the final R18 network had a different value. No complete-network backup uses a 200k or 47k electrical label.
3. [`4c6741e78f3ed8fa0120dc4741aaa30917405e29`](https://github.com/mulcmu/esphome-ge-laundry-uart/commit/4c6741e78f3ed8fa0120dc4741aaa30917405e29) carries the conflict through the Rev2.1 modifications. [`1fba9cf944bd46b2e4f8d8331c75f0fc4578f848`](https://github.com/mulcmu/esphome-ge-laundry-uart/commit/1fba9cf944bd46b2e4f8d8331c75f0fc4578f848) copies those identities into formal LCSC fields during KiCad 9 migration. Copying a code into another field is not an electrical-intent decision.
4. At [`bc0d52495bd97ed1504bd0ca0775e47feb01a648`](https://github.com/Dr-Crow/esphome-ge-laundry-uart/commit/bc0d52495bd97ed1504bd0ca0775e47feb01a648), the Rev2.1→Rev2.2 schematic comparison changes only **Description and LCSC** for these three resistors: C17539→C104108 and C17713→C17673. Their values, placement, UUIDs, footprints and population remain the same; the complete wire, junction and no-connect arrays are identical. Its [Rev2.2 README](https://github.com/Dr-Crow/esphome-ge-laundry-uart/blob/bc0d52495bd97ed1504bd0ca0775e47feb01a648/pcb/rev2.2/README.md) identifies the matching 220k/4.7k entries as intended parts. This is direct evidence of the **later revision's intent**, supporting the recommendation; it cannot retroactively prove the original author's intention.
5. Historical reports that boards worked, and reports of Rev2 supervisor boot loops, do not identify measured resistor values or provide a resistor-controlled comparison. No deliberate 200k/47k rationale or measured fitted-value record was found in the bounded source/README/backup record.

The **Rev1 R5 conflict remains a separate decision**. Its exact [`87984047ee029efb83bf9947dc21818fd18e39b3`](https://github.com/mulcmu/esphome-ge-laundry-uart/tree/87984047ee029efb83bf9947dc21818fd18e39b3/pcb) schematic says 4K7 and prose BOM says 47k. It parallels the half-duplex diode section, but Rev1 bias values, architecture and population options differ. That older ambiguity makes an inherited purchasing error plausible; it does not authorize applying this Rev2 recommendation to Rev1.

## Actual numbered nets and diode behavior

Read directly from the fixed native netlists and independently matched to **actual board pad/net membership** in Rev2.0, Rev2.1 and Rev2.2:

| Function | Exact physical terminals |
| --- | --- |
| Half-duplex receive node H | R18.1, R22.2, R23.1, D9.2, U4.1, TP4.1; R18.2 is GND |
| Half-duplex transmit node T | R22.1, R19.1, D9.3, U5.6; R19.2 is +5 V and R19 is 10k |
| Appliance half-duplex path | H → R23 1k → J1.7 (`GEA_HalfDplx`) |
| Full-duplex appliance-transmit receive node | R21.1, R25.1, U4.3, TP6.1; R21.2 is +5 V; R25 1k reaches J1.4 (`GEA_FullTx`) |
| Buffer domains | U4.5 is +5 V; U5.5 is +3V3; both pin 2 terminals are GND |

The [Nexperia BAV99 datasheet](https://assets.nexperia.com/documents/data-sheet/BAV99.pdf), Rev 7, 1 July 2022, p 2, defines **pin 1=A1, pin 2=K2, pin 3=K1/A2**. D9.1 is deliberately unconnected. Therefore the used section conducts from **T (D9.3 anode) toward H (D9.2 cathode)**. With T sunk low and H positive it is reverse-biased, leaving R22 as the resistive sink path. With T released, R19 pulls it toward +5 V and the diode can assist charging H.

The legacy K/A/K pin names and derived net labels are wrong. Inspection of the preserved symbol geometry shows the series-diode graphic and pin locations are already consistent with the manufacturer's numerical topology: pin 1 at the first anode, pin 2 at the second cathode, pin 3 at the series junction. A semantic correction must keep those endpoints and all board pads fixed; it is not a diode pin swap or reversal.

The [Diodes 74LVC2G07 datasheet](https://www.diodes.com/datasheet/download/74LVC2G07.pdf), DS35162 Rev 6-2, pp 2–4, confirms the W6-7 pinout and noninverting open-drain operation: low input sinks output; high input releases it. At U4's nominal 5 V, guaranteed input limits are **VIL≤1.5 V and VIH≥3.5 V**; at U5's 3.3 V, they are **VIL≤0.8 V and VIH≥2.0 V**. Thresholds must follow the actual supply range. U5's released output voltage is set by R19 and the connected bus rather than its 3.3 V supply. The device specifies a maximum input transition rate of 10 ns/V at both supply domains (p 3); input slew needs its own measured check.

## Functional impact

- Changing 200k→220k reduces bias current by 9.09% at fixed voltage (25.0→22.73 µA at 5 V) and increases the isolated RC time constant by 10%. R18 weakly biases H low; R21 weakly biases the full-duplex receive node high. Actual idle/noise margins depend on appliance drivers, external bias and leakage.
- Changing R22 47k→4.7k increases its resistive sink current tenfold at the same voltage difference (21.28→212.77 µA at 1 V). When U5.6≈0 V and D9 is reverse-biased, **R18∥R22 changes from 38.057 kΩ to 4.602 kΩ**, making that local sink 8.27 times stronger and its simple capacitive decay 8.27 times faster for fixed capacitance/loading.
- As an explicitly hypothetical illustration, a 5 V appliance pull-up of 10k through the existing 1k R23 produces H≈3.879 V with 200k/47k versus ≈1.475 V with 220k/4.7k, assuming ideal zero U5 output, no other loading and reverse-biased D9. The corrected nominal case barely meets U4's nominal VIL bound under that example and is not guaranteed with tolerance or output voltage. This demonstrates sensitivity; **10k is not an established appliance pull-up**, and neither number is an observed board voltage.

R22 changes the electrical behavior of a board assembled to the old codes even though the recommended purchasing correction leaves CAD values/netlist unchanged. Treat it as requiring a new loaded-interface result, not merely CSV parity. Released/high-state behavior cannot be justified by a resistor-only divider because diode conduction, driver states, leakage and rail variation matter.

## Recommended part identity rating and fit

| References | Recommended exact catalog identity | Verified primary specification |
| --- | --- | --- |
| R18, R21 | [C104108](https://www.lcsc.com/product-detail/C104108.html), RALEC RTT052203FTP | 220 kΩ ±1%; 0805; 125 mW at 70 °C; ±100 ppm/°C; 150 V maximum working/300 V maximum overload; −55 to +155 °C |
| R22 | [C17673](https://www.lcsc.com/product-detail/C17673.html), UNI-ROYAL 0805W8F4701T5E | 4.7 kΩ ±1%; 0805; 125 mW at 70 °C; ±100 ppm/°C; 150 V maximum working/300 V maximum overload; −55 to +155 °C |

Manufacturer sources: [RALEC RTT IE-SP-010 dated 27 January 2026](https://www.ralec.com/upload/media/product/file/IE-SP-010%20.pdf), pp 1–3, and [UNI-ROYAL SMD-SP-001 V10 dated 28 July 2025](https://www.uni-royal.cn/en/images/userfile/file/1769240915c56505e6d9ab55c7.pdf), ordering/dimension/rating pages. Ordering schemes independently distinguish 2003=200k, 4702=47k and 4701=4.7k for UNI-ROYAL, and 2203=220k for RALEC.

RALEC RTT05 body is 2.00±0.10×1.25±0.10×0.50±0.10 mm. UNI-ROYAL 0805 is 2.00±0.15×1.25(+0.15/−0.10)×0.55±0.10 mm. Both have the same standard 2012/0805 package class as the legacy source; their body tolerances differ. Existing R18/R21/R22 land pads are 1.025×1.4 mm at ±0.9125 mm. This supports leaving the footprint unchanged for a reviewed candidate; it does not prove solder-process or supplier-library acceptance.

Power derates above 70 °C. Continuous applied voltage is also limited by sqrt(P×R), not only the 150 V family maximum: at 125 mW the 4.7k part reaches that power at ≈24.24 V. A hypothetical 5 V continuously across R22 dissipates 5.319 mW; across 220k it dissipates 0.114 mW. These nominal examples do not qualify transient pulse energy or the board's overall power/protection envelope.

Current catalog stock indications and crawl-age limits are retained in the accompanying [catalog source review](catalog/catalog-verification-report.md). A displayed stock count is not a reservation, JLC assembly eligibility or order-time availability. Check the exact identity, stock and supplier pose in an authorized quote before purchase; do not make an unreviewed fallback substitution.

## Other unambiguous legacy corrections

These can be prepared as separately reviewed metadata/population corrections without inventing a component selection:

- Rev2.0 H1/H2 are existing bare mounting holes, not purchased assembly items. Excluding them from BOM/assembly while retaining their board geometry makes the fitted purchasing set 60 instead of the validator's current 62. Preserve H3/H4 as absent-board mechanical placeholders and retain the current DNP service pads, R8 and solder selectors. Rev2.1 already has a 60-reference fitted set; Rev2.2 has 59 because U1 is DNP. Do not carry that U1 omission backward automatically.
- Rev1 H1–H4 and TP1–TP7 are board features, and R1 is explicitly textual DNP. Encode those facts while retaining geometry/nets. Preserve all R17/R77, R8/R88 and R9/R99 alternative footprints and document both population choices; select neither by inference. Optional D6/SW1 remain explicit variants.
- Rev2.0/2.1 U6's historical **C5205181 = Diodes AP2205-33Y-13** can be named with its own datasheet. The [AP2205 manufacturer sheet](https://www.diodes.com/datasheet/download/AP2205.pdf), p 3, gives Y-package pin 1 VIN / pin 2 GND / pin 3 VOUT, matching +5 V/GND/+3V3. Correct the AP2204R library alias/datasheet by preserving pin endpoints; do not select the YR reversed-pin part or copy Rev2.2's TECH PUBLIC identity.
- Correct the C2500 Nexperia diode pin names without altering numerical geometry. Record Diodes 74LVC2G07W6-7 for Rev2 U4/U5 and link its datasheet rather than treating the historical TI link as purchasing evidence. Transfer other verified historical identities only after value/package/pin checks. Preserve original conflicting codes as provenance when an adopted code differs.

D7/D8 and the broader legacy catalog register are handled in a separate audit. This review does not close Rev1 generic passive/module/fuse/value selection, Rev2.0 D8 C2993047 identity, exact jack suffix or supplier orientation.

## Evidence required after adoption

1. Independently prove the intended delta: corrected purchasing metadata and explicitly justified assembly exclusions only; unchanged resistor values, numbered nets, numerical symbol endpoints, copper, footprints, placement, drills, outline, rules and firmware. Preserve original archives and every historical revision.
2. Run pinned KiCad 9.0.9 ERC/DRC and source/export checks on the exact adopted commit. Regenerate paired review BOM/CPL; check exact fitted-reference equality, quantities, DNP, values, manufacturer/MPN/LCSC and supplier package identity. Add a catalog-value check so identical wrong source/BOM fields cannot pass solely through parity.
3. On separate authorized prototypes, identify actual fitted resistor values; measure U4 inputs, U5 sink/output, bus low/high levels, input slew and edges with actual appliance loading and cables across supply/temperature/tolerance bounds. Exercise GEA2 half-duplex transmit/receive, release/turnaround and contention, GEA3 full-duplex receive/transmit, idle, repeated traffic, startup/power cycling and powered-off/backfeed states. Compare nominal source-value and historical-coded builds if either is to be supported. Establish margin against manufacturer thresholds and firmware/protocol timing using measured rail ranges.
4. Obtain supplier diode/IC polarity and zero-angle overlays, connector drill/retention/case fit and solder-process evidence. Independently retain reset-supervisor, regulator thermal/dropout/reverse-feed, input source/fuse/TVS/transient-energy, RF and appliance qualification gates. Neither matching catalog identities nor clean CAD closes them.

## Exact source binding and verification

Current source hashes:

| Source at 11826a7f6ba1ed19131ddba46e4d62b06196a8c6 | Git blob | SHA256 |
| --- | --- | --- |
| pcb/rev2.0/design/OnionStraws.kicad_sch | 7de6fee453a3b6c39e23ea9eefd30626e7804242 | e07d25f2fbaa58c997bd973c13ca19893bb1126050f3a1af5f74108f0d7d4b43 |
| pcb/rev2.1/design/OnionStraws.kicad_sch | 21abd50f942125a4034bc671c11a363279c66487 | ae2e3d79fa1ce635c008c50e324ffd00f8516b461e4540c4f664fbb1f76da6d1 |

Upstream corrective comparison at bc0d52495bd97ed1504bd0ca0775e47feb01a648 uses Rev2.1 blob 6e02076d06b0a212caf1a6172767bbc30622afc5 and Rev2.2 blob 56913e0d6186b10b8d7e86670ca77abb5f18b1ff. Full schematic/PCB/netlist/footprint/library/README/BOM commit, blob and SHA256 records are in [source-hashes.json](evidence/source-hashes.json). Backup archive/member hashes, extracted history, exact upstream diff, populations and numbered terminal maps are retained alongside it.

The reproducible `read-only verifier` (original analytical helper; recorded data/formulas below) passed at 12:52 UTC: 35 fixed-source captures, 6 history stages, 17 backup schematic members, affected-net equality across Rev2.0/2.1/2.2, direct board-pad/native-netlist equality, and purchasing-only resistor deltas in the upstream corrective comparison. The shared checkout remained clean at the exact source commit. This pass did not rerun native CAD checks, order parts, submit files, publish changes or perform physical tests.
