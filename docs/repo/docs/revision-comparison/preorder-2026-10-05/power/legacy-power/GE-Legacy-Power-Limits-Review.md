# GE Rev1.0 / Rev2.0 / Rev2.1 / Rev2.2 power and protection limits

Reviewed 5 October 2026 UTC. Source is bound to **bf581ac1804bab982c78b9e2f6a6292d695e49cc**, with the four native schematic and PCB bytes still identical at the later integration HEAD observed during this pass. This is read-only circuit/source and manufacturer-data research. It supplies no powered test, appliance qualification, production approval, part substitution or source edit.

## Conclusions that can be made now

1. **Rev2.0/2.1 and Rev2.2 each have an unsupported rated C3 supply capability.** Their exact U6 selections are distinct 200 mA parts. The WROOM manufacturer specifies external supply capability of at least 500 mA. Its characterized Wi-Fi TX peaks are also above 200 mA. A short-circuit current-limit figure, extra bypass capacitance, clean CAD, or a report that a historical board worked does not establish the missing rated capability.
2. **The legacy protection chain has no demonstrated gate/capacitor/fault-energy coordination.** Q1's gate is grounded and both MOSFET sources share p2. Their ±20 V gate rating is not protected by a source-referenced clamp. D7's conditional 32.4 V clamp is above that gate rating and C9's 25 V rating. The actual voltage at p2/p3 depends on the source, current, parasitics and switching state; this report does not assert that any GE appliance produces a 32.4 V event.
3. **Rev1 remains identity-limited.** Its external buck and generic 38-pin development board are unqualified identities. The original purchasing prose specifies a 0.2 A/1210 fuse; the schematic links a different 0.3 A/1812 fuse family. Generic capacitor values have no established voltage ratings. Rev2 ratings cannot be copied onto Rev1.

The smallest justified action is to preserve these historical revisions and label the Rev2.x rated C3 supply deficiency explicitly. If a powered candidate is wanted, create a separately reviewed BOM/circuit candidate with **verified continuous 3.3 V supply capability supporting the module's≥500 mA provision plus separately allocated carrier current**, exact pin/package identity, adequate dropout and thermal margin, and compatible upstream source, fuse, PMOS and 5 V regulator capacity. Do not silently install a different regulator or inherit the TECH PUBLIC identity into Rev2.0/2.1. No such candidate was created in this review.

## Numbered topology, checked against actual PCB pads

Fresh KiCad **9.0.2 netlist exports for extraction only** were read and compared with native PCB pad membership at the fixed commit. All connected pad comparisons agree: 157 Rev1.0 and 192 each Rev2.0/2.1/2.2. These counts exclude unconnected pads and are not population/BOM counts. Prior firmware-review netlists have the same numerical net memberships. This is not another 9.0.9 ERC/DRC pass.

| Function | Rev2.0 / Rev2.1 / Rev2.2 actual terminals |
|---|---|
| PIN1 source | J1.1 / VDC → F2.1; F2.2 → JP2.1 |
| PIN3 source | J1.3 / ALT_PWR → F1.1; F1.2 → JP2.3 |
| Manually selected input p1 | JP2.2, D7.2, Q1.3, TP3.1; D7.1 is GND |
| Common MOSFET source p2 | Q1.2, Q2.2, C8.1, R8.2 |
| Q1 gate | Q1.1 is directly GND |
| Q2 gate | Q2.1, C8.2, R8.1, R9.2; R9.1 is GND; R9=1 MΩ, C8=1 µF, R8=DNP |
| Protected/regulator input p3 | Q2.3, U3.1, C9.1, C10.2; C9.2/C10.1 are GND |
| 5 V rail | U3.3, U6.1, D8.1, C11.1, U4.5 and other loads; D8.2 is GND |
| 3.3 V rail | U6.3, U2.1, U5.5, J2.1, J3.2, C13.1, C2.1 and bypass/bias loads |
| Regulator grounds | U3.2 and U6.2 are GND |

JP2 is a manual selector. There is no automatic source priority or independent input isolation before its common terminal. Bridging both throws would connect the two input supplies through their fuses; it is not a reviewed population/use option. D7 is on the common selected-input node, so its rated pulse data does not establish protection of the unselected source or the source-side fuse terminals.

Rev1's path is J2.1 / VDC → F1.2 → F1.1 / p1 → Q1.3; Q1.2/Q2.2 share p2, Q1.1 is GND, and Q2.1 has C4=1 µF to p2 plus R2=1 MΩ to GND with R1 DNP. Q2.3/p3 reaches external-buck J1.3 and C5.1. The buck interface is J1.1=+5V, J1.2=GND, J1.3=protected input, J1.4=no connect. U3.19 is the devboard's 5VIN, and U3.1 provides the carrier +3V3 net. Appliance J2.3 is unconnected. A connector net label does not identify the buck's rated input, dropout, current, regulation, efficiency, reverse-feed or thermal behavior.

## Exact U6 parts and radio demand

| Item | Rev2.0 / Rev2.1 | Rev2.2 |
|---|---|---|
| Purchasing identity | C5205181 = **Diodes AP2205-33Y-13** | C19268131 = **TECH PUBLIC TPAP2205-33Y** |
| Primary document | [Diodes DS41592 Rev 4-2, December 2023](https://www.diodes.com/assets/Datasheets/AP2205.pdf), pp 1–5 | [Exact C19268131 manufacturer-authored five-page sheet](https://atta.szlcsc.com/upload/public/pdf/source/20231201/421357A3C66CA1DC6983E93125C75712.pdf), pp 1–5; hosted by supplier |
| Operating output current | 200 mA for VOUT>1.8 V | 200 mA stated on p 1; load-regulation characterization ends at 0.2 A |
| Output current beyond that rating | 250 mA is an absolute stress rating; IOUT(MAX) minimum 200/typical 250 mA is specified at VIN−VOUT=1 V and VOUT=98% nominal | ILIM minimum 200/**typical 500**, with no maximum shown, is measured at **VOUT = 0**; it is not 500 mA regulated output capability |
| Supply input | 2.3–24 V operating; 36 V absolute | 2–30 V operating; −0.3…32 V absolute |
| Dropout | At100 mA:320 mV typical/460 mV maximum; at 150 mA:360/500 mV. No200 mA dropout limit is tabulated | 3.3 V version:420 mV **typical only** at 100 mA. The 350 mV headline applies to5 V output. No200 mA dropout bound is shown |
| Junction range | −40…125 °C operating;150 °C absolute | −40…125 °C operating;150 °C absolute; ambient−40…85 °C stated |
| SOT89 thermal reference | θJA129 °C/W, measured on two-layer FR4 with 1.5×1.5 cm thermal sink pad in free air | θJA120 °C/W references Note 2, which is absent from the supplied five pages; board/reference conditions remain unresolved |
| Pin evidence | Y: 1 = VIN / 2 = GND / 3 = VOUT. **YR reverses pins1 and3** and is a different choice | The p 2 SOT89 drawing labels 1 = VIN / 2 = GND / 3 = VOUT; the adjacent table instead says **5 VOUT**. The discrepancy is visibly present in the original PDF and needs supplier/manufacturer resolution before release |
| Reverse-feed evidence | Description claims reverse current protection; the sheet does not supply a full guaranteed external-output-power use envelope | Absolute **VOUT−VIN is −32…+0.3 V**. Applying3.3 V externally while VIN is0 V is outside that stated limit |

The historical AP2204R alias/datasheet is not a substitute for either exact sheet. Manufacturer identity, pin endpoints and ratings must remain tied to the purchasing code. The Diodes and TECH PUBLIC PDFs have different authors, limits, tests and protections even though both selected packages are SOT89.

[Espressif ESP32-C3-WROOM-02/02U v1.7](https://www.espressif.com/sites/default/files/documentation/esp32-c3-wroom-02_datasheet_en.pdf), §6.2 pp 22–23, requires 3.0–3.6 V and external supply current capability **≥0.5 A**. §6.4 reports Wi-Fi TX peaks345 mA (802.11b1Mbps/20.5dBm),285 mA (g54Mbps/18dBm) and280 mA (nMCS7). Those are characterized peaks at 3.3 V/25 °C, with TX measured at 100% duty cycle. They are **not a guaranteed worst-case maximum over all firmware, temperature, process and peripherals**. RX82/84 mA uses disabled peripherals and idle CPU. These figures establish why a sleep-current number or radio average cannot clear the rated deficit.

Carrier +3V3 also supplies buffer, bias, LEDs in their selected states and supervisor where populated. Nominal listed rail capacitance is 11.3 µF: C13=10 µF, C2=1 µF and C4/C6/C14=0.1 µF each. An ideal constant 200 mA source versus 345 mA load would discharge11.3 µF from 3.3 to 3.0 V in **23.4 µs**. This example assumes nominal effective capacitance, zero ESR, no other loads and no supply-loop dynamics; tolerance, DC bias, aging, temperature and ESR reduce the usable margin. It does not establish actual burst duration or provide a substitute for≥500 mA supply capability.

J2.1 and J3.2 directly join U6's output rail; no isolation device appears between them. The existing service rule to leave programmer VCC disconnected is reinforced by the TECH PUBLIC differential limit. This report supplies no approved alternative power recipe. The Diodes description's reverse-protection wording does not qualify driving its output externally in all states.

## L7805 voltage and thermal margin

All Rev2.x U3 codes are C86206, **ST L7805ABD2T-TR**, not an unidentified7805. The [ST L78 DS0422 Rev 38, February 2025](https://www.st.com/resource/en/datasheet/l78.pdf), pp 3–6 and ordering table, supports the D2PAK pin mapping and AB identity. At5 mA–1 A and **7.5–18 V input**, output 4.8–5.2 V is specified across−40…125 °C junction. At25 °C it is 4.9–5.1 V under the stated test conditions. The 35 V input figure is an absolute rating; it is not a35 V regulated-board rating. Dropout2 V is **typical at 1 A/25 °C**, with no maximum listed. The sheet explicitly notes minimum5 mA regulation load.

Therefore a manufacturer-bounded input-band check starts at **U3 pin1/p3≥7.5 V**, not merely5+2 V from a typical dropout figure. Source minimum must additionally cover fuse, MOSFET and wiring drops. For the Diodes second stage, a properly regulated minimum4.8 V first stage gives 1.5 V nominal headroom to 3.3 V, but that does not repair U6's current rating, qualify200 mA dropout, or account for startup/supply collapse. TECH PUBLIC gives no maximum dropout guarantee.

The actual p3 voltage and sustained5 V load are unknown. At an **illustrative p3=12 V and I5=200 mA**, U3 dissipates(12−5)×0.2=**1.4 W**, plus input-voltage×ground-current loss. ST's D2PAK thermal table gives62.5 °C/W junction-to-ambient and3 °C/W junction-to-case; actual board copper, mounting and enclosed airflow are not measured. Using62.5 °C/W only as a reference gives87.5 °C rise before ground current. At25 °C ambient that is112.5 °C; at 50 °C it is137.5 °C. At12 V, ST's6 mA maximum quiescent-current entry would add72 mW if that bound applies to the particular operating condition, plus any load-related ground-current change.

| Assumed p3 | Ideal I5 thermal ceiling at 25 °C ambient | At50 °C | At85 °C |
|---|---:|---:|---:|
|7.5 V|640 mA|480 mA|256 mA|
|9 V|400 mA|300 mA|160 mA|
|12 V|229 mA|171 mA|91 mA|
|18 V|123 mA|92 mA|49 mA|

These are calculated from(125−TA)/(62.5×(p3−5)), exclude ground-current losses, and assume the datasheet thermal reference matches the carrier. They are **illustrative ceilings, not guaranteed usable carrier currents**. Upstream regulation/fuse/current limits, ancillary loads and actual cooling can reduce them. Thermal shutdown is fault protection; operation at shutdown is not a thermal qualification.

At 5→3.3 V and 200 mA, ideal U6 dissipation is 340 mW. The Diodes 129 °C/W reference gives 43.9 °C rise; the TECH PUBLIC 120 °C/W value gives 40.8 °C. At85 °C ambient, corresponding ideal junction estimates 128.9/125.8 °C already exceed their125 °C operating limit before ground-current loss. Ideal current ceilings at 85 °C are 182/196 mA respectively. These calculations cannot establish the actual carrier's θJA, particularly because the TECH PUBLIC reference note is missing.

## PMOS, TVS, capacitors and slow gate control

Q1/Q2 select C10493 in Rev2.x, **Vishay SI2309CDS-T1-GE3**. Rev1's value/prose name the same Si2309CDS family, but its schematic URL is an unrelated Si2393DS document and must not establish ratings. The [correct Vishay Si2309CDS sheet](https://www.vishay.com/docs/68980/si2309cd.pdf), document 68980 Rev A, 27 October 2008 with current disclaimer, pp 1–2, gives−60 V VDS and **±20 V VGS absolute**,1 = G / 2 = S / 3 = D. Maximum RDS(on) is 345 mΩ at−10 V and 450 mΩ at−4.5 V, measured at 25 °C under pulsed conditions. At0.2 A, two 450 mΩ devices give a 180 mV/36 mW ideal pair example; that is not a guaranteed hot/startup resistance. Drain-current and package-power headline ratings carry thermal/time conditions and cannot be assigned directly to the populated board.

Q1's grounded gate means VGS=−p2. With the gate resistor fitted and capacitor settled, Q2 also approaches VGS=−p2. The 1 MΩ/1 µF source-gate network yields a nominal **1 s RC** under a stiff source-step assumption; it changes startup slew but does not clamp the final gate voltage or set a guaranteed inrush current. Gate thresholds are not full-enhancement guarantees. Neither R8/R1 DNP nor the capacitor supplies a source-referenced voltage clamp.

D7=C309871 is **Brightking SMAJ20CA/TR13** in Rev2.x; the original Rev1 prose names SMAJ20CA/TR13 while its schematic is generic. A [manufacturer-authored Brightking SMAJ family sheet,21 July 2014](https://files.rct.ru/pdf/diode/201112231713448321.pdf), hosted by a distributor, gives20 V stand-off,22.2–24.5 V breakdown at 1 mA and maximum32.4 V clamp at 12.3 A for the specified10/1000 µs pulse. Its400 W pulse rating is at 25 °C, with mounting/derating and non-repetition conditions; it is not a400 W continuous sink or an arbitrary joule rating. The current [C309871 catalog](https://www.lcsc.com/product-detail/C309871.html) agrees on those characteristic values. The retrieved family sheet is not asserted to be the latest lot-specific supplier sheet.

| Rev2.x capacitor identity | Actual location | Verified manufacturer family rating |
|---|---|---|
|C28323 / Samsung CL21B105KBFNNNE,1 µF±10%|C8 across p2–Q2 gate; C2 on 3V3|[50 Vdc X7R−55…125 °C](https://product.samsungsem.com/mlcc/CL21B105KBFNNN.do)|
|C15850 / Samsung CL21A106KAYNNNE,10 µF±10%|**C9 across p3–GND**; C11 on 5 V; C13 on 3V3|[25 Vdc X5R−55…85 °C](https://product.samsungsem.com/mlcc/CL21A106KAYNNN.do)|
|C28233 / Samsung CL21B104KCFNNNE,0.1 µF±10%|C10 across p3–GND and other bypass positions|[100 Vdc X7R−55…125 °C](https://product.samsungsem.com/mlcc/CL21B104KCFNNN.do)|

Supplier catalog codes were matched to these exact family names; manufacturer pages explicitly list theE packaging suffix. Body/class and ratings are manufacturer facts; no bias/temperature/aging minimum effective capacitance was established. C9 is the limiting named input capacitor at 25 V. If p2/p3 were to approach32.4 V, VGS would exceed 20 V by 12.4 V and C9 would exceed 25 V by 7.4 V. That is a **conditional coordination counterexample**, not a predicted waveform. PMOS drops and slow gating do not supply a documented steady-state voltage clamp. Even a p2 rail between 20 and 25 V would exceed the gate stress rating before TVS breakdown begins.

Rev1 C4/C5 and other capacitors are generic. Its prose calls the100 nF parts0805, while C1–C3 carry retainedEIA-1608/AVX footprint names. No exact purchased capacitance/package/voltage/dielectric set is established. Preserve this ambiguity instead of applying Samsung identities to it.

## Fuses and downstream fault energy

Rev2.x F1/F2=C12604 select **Bourns MF-MSMF030-2**,1812. The [manufacturer MF-MSMF sheet](https://bourns.com/docs/product-datasheets/mf-msmf.pdf), electrical table p 1 and thermal table p 9, gives30 V maximum,10 A maximum fault current,0.30 A hold/0.60 A trip at 23 °C, Rmin0.30 Ω andR1max3.0 Ω. Its maximum 100 ms trip time is specified at **8 A/23 °C**, not at 600 mA. The 300 mA hold limit decreases to 260/220/200/180/140 mA at 40/50/60/70/85 °C. A PPTC is neither a fast fuse nor a300 mA current limiter. The current sheet marks the unsuffixed030 family as available but not recommended for new designs; it does not authorize a different suffix.

At200 mA, the 0.30–3.0 Ω resistance endpoints correspond to60–600 mV drop. R1max is the specified post-reflow/post-trip bound, not an assertion that every fresh part is3 Ω. Loaded source headroom and thermal trip behavior must use the actual part state and temperature. Because Rev2 uses cascaded linear regulators, input current is approximately the3V3 load plus 5 V ancillary load and regulator ground currents, rather than the buck input/output current relation. At70 °C the fuse hold entry already equals200 mA before those other currents; Wi-Fi current above200 mA adds further stress. The facts do not predict a nuisance trip for a particular brief pulse.

Rev1's prose [original purchasing table](https://github.com/mulcmu/esphome-ge-laundry-uart/blob/87984047ee029efb83bf9947dc21818fd18e39b3/pcb/readme.md) specifies **MF-USMF020-2**,1210,0.20 A hold. The [Bourns MF-USMF sheet](https://bourns.com/docs/product-datasheets/mf-usmf.pdf), Rev U, 09/26, gives30 V/10 A max,0.40 A trip at 23 °C,0.40 Ω minimum/5 Ω R1max, and 20 ms maximum trip **at 8 A**. Hold current is180/160/140/120/100 mA at 40/50/60/70/85 °C. The current schematic instead linksMF-MSMF030-2 while retaining a1210 land pattern. These differ in package, hold/trip, resistance and time. No selection or claim about the actual fitted fuse is justified. Buck input current also depends on the unidentified module's efficiency and operating point, so its input fuse cannot be compared directly with an unidentified devboard's3V3 radio current.

D8 in Rev2.1/2.2 is C78479, **JSCJ BZT52B5V1**, shunted directly across+5V/GND. Its [catalog](https://www.lcsc.com/product-detail/C78479.html) identifies 5.1 V/350 mW, with a 5.0–5.2 V nominal range. A manufacturer-family mirror search exposed 350 mW feature versus 500 mW maximum-table language, but its PDF could not be retrieved in this pass. Exact sheet/thermal conditions and supplier-lot identity therefore remain a gate; this review does not upgrade the part to 500 mW. Rev2.0's SOD523 C2993047 exact identity was not resolved. Rev1's prose identifiesNexperia PDZ5.1BGWJ, while its source value says5.2 V; the [manufacturer family page](https://www.nexperia.com/products/diodes/zener-diodes/serie/pdz-gw-series) reports 4.96–5.20 V at 5 mA and 365 mW under its conditions. No exact fitted specimen was inspected.

The 350 mW/5.1 V example corresponds to only 68.6 mA continuous shunt current before thermal derating. Neither the upstream300 mA hold PPTC nor a regulator's current limit establishes that this small shunt diode survives a regulator short/fault. An illustrative 100 mA shunt at 5.1 V dissipates 510 mW while being below the 23 °C PPTC hold rating. There is no series current-limiting resistor atD8. This demonstrates missing coordination; it does not model the actual fault path. Pulse-current/energy survival, allowed source fault current, fuse temperature/time, regulator SOA, rail overshoot and diode junction temperature need an exact reviewed waveform and device sheet. The 5.1/5.2 V value is not an ideal hard rail ceiling.

## Evidence and limits

- [source-bindings.json](source-bindings.json) records fixed-commit paths, git blobs and SHA256 for all eight native schematic/PCB inputs; [fixed-source-identities.json](fixed-source-identities.json) records the four schematic captures.
- [all-numbered-terminals.csv](all-numbered-terminals.csv), [numbered-netlist-extract.json](numbered-netlist-extract.json) and [numbered-board-pad-comparison.csv](numbered-board-pad-comparison.csv) preserve actual numerical endpoints and board equality. Fresh XMLs and export logs are alongside them.
- [verification-result.json](verification-result.json) records the read-only extraction result and engine. Export succeeded; host cache/font warnings are preserved in logs. No native-rule pass is claimed here.
- [illustrative-calculations.json](illustrative-calculations.json) and `verify_legacy_power_evidence.py` (original analytical helper; recorded data/formulas below) retain formulas, assumptions and reproducible source comparisons.
- [primary-source-manifest.json](primary-source-manifest.json) contains actual source URLs, byte lengths and SHA256 for the captured primary PDF/HTML files, including the reused Espressif PDF with original retrieval metadata. The TECH PUBLIC scanned PDF was rendered and all five pages inspected; its pin-table error and missing thermal note are retained explicitly. Diodes rating pages, ST L7805 rating page and Bourns fuse table were also visually inspected.
- The module-sourcing and legacy-intent reviews were read before conclusions. Their module identities, population ambiguity, source preservation and qualification boundaries remain applicable. Bibliographic URL failures/redirects are retained in retrieval logs. Manufacturer-authored distributor copies are identified as copies, not silently presented as official-host downloads.

This completes the desk review's numerical bounds and identifies its unresolved evidence. It does not close exact Rev1 buck/devboard/fuse/capacitor identities, Rev2.0 D8, JSCJ diode thermal documentation, source waveforms/current budget, regulator reversal, RF burst/dropout/startup, enclosure thermal resistance, pulse energy, manufacturing process or appliance qualification. Historical operation reports are context, not guaranteed full-envelope evidence.
