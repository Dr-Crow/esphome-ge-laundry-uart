# Independent Rev3B rated-protection review

Reviewed 2026-10-04 UTC. Read-only source review and scratch-only native checks. The implementation is electrically consistent with the selected Rev3C prototype and passes independent native integrity and manufacturing checks. No functional compromise was detected. This does not establish loaded appliance operation or physical qualification.

There is one preservation caveat: the retained track/via objects and zone definitions are unchanged outside the bounded work, but regenerated F.Cu ground fill is not identical everywhere outside the track-edit bounds. Do not describe the entire filled-copper delta as confined to those bounds or all unrelated filled copper as byte/geometrically identical.

## Source binding

- Backport checkout: `/workspace/shared/ge-oct3-rev3b-rated-protection`, clean owner commit `5742253a1c95fb51b91638f57c5ae9ecab88c385`.
- Frozen original: `/workspace/shared/ge-oct3-rev3b-cleanup`, clean commit `0b957ba996e7e7a86f8776c9289b6cfb634421ee`.
- Selected C source: `/workspace/shared/ge-oct3-rev3c-rated-switch`, clean commit `fafd3eab5a8a8465697e1557bb075d88f85be9d9`. The diff from electrical/source selection `7bb455fbc85c748f3125ed091a54375de69fbbcc` changes documentation, images and manifest only; no CAD, BOM, CPL or manufacturing changes occur between these commits.

SHA-256 of the reviewed actual files:

| File | SHA-256 |
|---|---|
| Schematic | `40c0f743f5cebbd27e9727a00276291257fd84f8dc47263d075e2e0abd38f0f1` |
| PCB | `a21a84afde3d430d0749b10b0d20312ef122954420cca0baf46ab7304feca598` |
| Project | `abea7adbb5a1ee515cd443d6735b7c1808d31d0cef98924e77ab61f694fccbc9` |
| Local rule file | `e554982cc3654d5baaed9eba564ed0a7ba4cc0e81e7c80c31a68d5b17f545454` |
| BOM | `23ec68c57f4a09124a1bc0cb251dbc1fe21fd55b554e9ad74ef809fdc4cdb186` |
| CPL | `249a8eb1b786cb5daa3c51e738dc966a5e30b0369af028afb94bc2639c58823b` |
| Factory ZIP | `8f0b11b89f4b1ca77e4e1f128bae8ff0698d54773f41c1063af04e52fea97639` |

All 53 current manifest entries independently match actual SHA-256 and byte counts. Reports and independently regenerated outputs are in this directory. No worktree was edited, committed, published, ordered, physically tested or sent to another service.

## Circuit review from fresh native netlists and PCB pads

I exported fresh original, B-backport and selected-C KiCad XML netlists, parsed the original/current native board files independently, and compared their actual pin nets and component identities. The selected protection references have no net or exact-SKU discrepancy against C. Native PCB pad nets also match the independently exported current schematic, including explicit NCs.

Both original branches remain: J1.1/VDC → F2 → Q3 → U9 → D14 → V_INPUT, and J1.3/ALT_PWR → F1 → Q4 → U10 → D15 → V_INPUT. J1 data-pin assignments, D14/D15 diode OR, AP63205 U8 and D11 buck-output isolation remain unchanged.

Q3/Q4 retain CJ3407. Pin 2/source is the respective protected node; pin 3/drain is the respective fused input. D16/D17 pin 1/cathode is at that source and pin 2/anode at gate-bias. They are exact MCC BZT52C12-TP/C668891, not an inherited Nexperia electrical specification. R31/R32 remain 5.1 kΩ from gate-bias to GND, C18/C19 remain 100 pF between protected source and gate-bias, and R33/R34 remain 51 Ω between bias and actual gate. No source-to-gate pull-up was added.

F1/F2 are exact Littelfuse 1812L075/33DR/C151170. Native pads measure 1.78 × 3.15 mm at ±2.615 mm: 3.45 mm inner gap, matching the primary land drawing. Their centers move from x44 to x45.5; branch source nets remain correct.

U9/U10 are exact TPS1H200AQDGNRQ1/C2653785. Actual native pin map is IN1, DIAG_EN2, FAULT3, CL4, DELAY5, GND6, OUT7, VS8 and EP9. DIAG_EN, GND and EP are GND. FAULT3 is explicitly NC. U9 IN1 and VS8 both follow PIN1_PROTECTED. U10 VS8 is PIN3_PROTECTED; IN1 remains the original PIN3_EN network. Q5/R35/R36/R37 retain their original values, pin nets and native footprints: PIN1_PROTECTED drives Q5 through R35, R37 pulls its base down, and R36 pulls PIN3_EN toward its own PIN3_PROTECTED source. This retains PIN1-presence priority, including inhibition by weak/faulting PIN1; it adds no fault-aware fallback.

R38/R39 are exact 0603WAF3301T5E/C22978, 3.3 kΩ ±1%, CL to GND. R40/R41 are exact 0805W8F1003T5E/C149504, 100 kΩ ±1%, each branch's own VS to DELAY. C22/C23 are removed. D20 is exact SUNMATE SMF16A/C399290 from PIN3_PROTECTED to GND, matching D18 polarity and upstream position.

The TI primary Rev E pp4/6/7/13/28/29 support the pin map, 100 kΩ stand-alone retry connection, nominal 2000/3300 = 0.606061 A and conditional 0.510051–0.704010 A arithmetic. The latter requires VS−OUT ≥2.5 V and stated conditions; it is not a guaranteed normal-operation current ceiling or OEM source allowance. Continued-limit retry is 35–45 ms ON /0.8–1.2 s OFF, specified by design rather than production tested, with thermal interaction remaining relevant.

## Original preservation and rules

Fresh extraction reproduces 100 →103 schematic items, 99 →102 native footprints and 245 →257 pin nets. Exactly 23 original pin nets change, all on the authorized protection/removal set; 222 remain unchanged. Only six original component value/footprint/SKU records change: D16/D17, F1/F2 and U9/U10. Added references are D20/R38/R39/R40/R41; removed references are C22/C23.

The 17 original native footprint changes are C18/C19/C21/C24/C25, D16/D17, F1/F2, Q3/Q4, R31/R32/R33/R34, U9/U10. All other footprint contents, transforms, pad geometry, nets and models remain identical after mapping native net numbers to names. This includes the soldered exact Seeed 113991054/C18212168 XIAO ESP32-C3 U2 and all 22 pads; J1/J2/JP1, LEDs, mounts and recovery interfaces are preserved. Board graphics/99 ×40 mm outline are identical; entire case and firmware trees match byte-for-byte. No C6 compatibility or regulator/module replacement appears.

PCB setup and the entire project file are byte/structurally identical to frozen B. Global minimum clearance stays 0.20 mm; Power/ Switching clearances remain 0.25/0.30 mm. Their netclass assignments, routing defaults and other settings remain. The only added rule content is two clearance rules requiring A.Type and B.Type to be Pad and both objects to belong to the same U9 or same U10 footprint. Thus the 0.20 mm exception cannot match tracks, vias, other parts, or a pad pair split between U9 and U10. No excluded violations or broad waiver was added.

Native U9/U10 leads are 1.4 ×0.45 mm, 0.65 mm pitch and 4.4 mm row spacing, with intrinsic 0.20 mm adjacent gaps. EP copper is 2 ×3 mm with separate 1.57 ×1.89 mm mask/paste aperture, matching TI's 0.125 mm stencil example. Under-paste vias are omitted. Final process, ≥85% EP solder coverage, contamination/insulation and thermal qualification remain open.

## Copper and filled-zone caveat

109 original track/via/arc objects are removed and 163 are added. All 621 retained objects are geometrically and electrically identical after net-name normalization. The track-object edits occupy x39.9125–77.0/y2.0–33.0099 mm. No direct module signal-net or named GE connector signal-net routing changes were found. Small local clearance detours include +3V3 and Net-(D9-K2): the former changes three F.Cu 0.5 mm segments into a 0.3 mm route with two vias and B.Cu detour; the latter changes four F.Cu segments into six segments plus two vias using In2.Cu. Net-(D9-K2) is an intermediate half-duplex receive/clamp net connected to U4.1, so an unrestricted statement that every GE signal-path copper object is unchanged would also be too strong. Their original pin nets are unchanged. These detours should not be hidden by saying that every unrelated routed copper object remains original.

All four GND-zone UUIDs, outlines and fill parameters are identical. Native polygon Boolean comparison nevertheless finds real local/refill ground changes. F.Cu symmetric difference is about 358.269 mm² (233.259 removed/125.011 added); B.Cu/In1.Cu/In2.Cu differences are about 86.875/29.284/48.339 mm². Non-F.Cu differences outside x39–77 are only sub-0.000004 mm² coordinate/Boolean residues.

F.Cu refill propagation extends beyond track-edit bounds: 1.618 mm² lies left of x39, and 24.990 mm² of original ground fill is removed right of x77, reaching x85.467. Nothing substantial changes past x85.5 or below y37.3. Both source definitions and the retained tracks/pads in those adjacent regions remain unchanged. A forced independent original-board refill reproduced the original-versus-current result, so this caveat is not dismissed as an unverified stale-original-fill explanation.

The embedded U2 U.FL connector/external antenna launch keepout remains exactly x77.39–80.184/y10.858–14.922 mm; Boolean fill difference inside it is zero on every copper layer. No RF/physical measurement is inferred. If the required acceptance condition literally means every filled ground region outside the authorized track rectangle must stay geometrically frozen, that condition is not fully demonstrated by this backport. The narrower retained-object/zone-definition preservation statement does pass.

## Independent native and manufacturing results

Using the pinned native KiCad 9.0.9 CLI:

- All-severity ERC: zero errors, warnings and exclusions.
- All-severity/all-track DRC with schematic parity: zero violations, unconnected items and parity differences.
- Fresh native position export: 85 references, identical to the 85 CPL rows and independently derived fitted schematic/BOM set, with no duplicates. Every CPL coordinate, rotation and side matches native output.
- Every BOM value, footprint, LCSC, MPN, manufacturer and quantity matches current schematic fields. DNP/test/mount/JP1/debug references are excluded as intended.
- All 14 stored factory ZIP members match the owner's actual recorded hashes. Independent native regeneration of 11 Gerbers, two separate Excellon drills and the job file is identical after removing only generation timestamps. No aperture, geometry, drill, net attribute, job configuration or other export content differs.
- All 86 attached model references resolve to existing bytes; TI/PPTC models transfer unchanged as approximate drawing envelopes, with no authenticated vendor-CAD or physical-fit claim.

Actual schematic, top render, four-copper contact sheet and TI land pixels were inspected. The explicit prototype warnings and soldered-C3 module geometry are visible. These views establish review visibility, not stencil/thermal/module seating proof.

## Power qualification review

`POWER-QUALIFICATION.md` agrees with the focused primary-backed `/workspace/shared/ge-oct3-research/backport-power-review/REPORT.md`. I also rendered and inspected actual Seeed v1.3 sheet3/3: VUSB enters module F1 marked 6 V/500 mA, then D1 MSK4005, then TLV75733PDBVR; C1/C3 are 2.2 µF each and C23 is 2.2 µF. The installed module identity, its internal diode/fuse and carrier D11 losses remain gates; no AP2112/WROOM budget or 700 mA annotation is promoted to a B supply guarantee.

The documented mixed-condition nominal5 V screen reaches 3.787 V before remaining buck/module/PCB losses. Against the TLV's 1 A/≤85°C 425 mV dropout screening row it leaves only 62 mV, or29 mV with the 1% reserve; no guaranteed 364 mA interpolation is asserted. Loaded PIN1-only and PIN3-only cold starts, RF bursts, actual5V/3V3, ≥50 µs stabilization/reset behavior and completion within retry attempts remain open. The conditional extra4.915 mA active-supply comparison correctly flows before VS through fuse/PMOS, not through the OUT limiting channel; the 2.394 mV arithmetic is qualified by unmatched test conditions.

The original nominal5/7.5/9/13.6 V intended examples remain. No OEM voltage/current/transient envelope, source budget or narrowed specification is invented. PMOS30 V/20 V limits, charged reverse steps, 32 V buck operation, 33 V PPTC differential voltage, upstream TVS energy, MCC low-current/hot/Miller clamp, D14/D15 duty/thermal gates, enclosed module thermal behavior and mutually exclusive USB/appliance/recovery supply remain explicit. Native CAD integrity does not close any of these gates.

## Assessment

No blocker was found in selected circuit topology, exact component identity, native pad mapping, automatic presence priority, source-bound assembly files, local rule scope, module/interface preservation or native ERC/DRC. Accept only as an unqualified prototype implementation, with the filled-ground preservation caveat above stated accurately. No physical electrical, appliance, thermal, RF, environmental, stencil, procurement or order-readiness qualification has been performed.
