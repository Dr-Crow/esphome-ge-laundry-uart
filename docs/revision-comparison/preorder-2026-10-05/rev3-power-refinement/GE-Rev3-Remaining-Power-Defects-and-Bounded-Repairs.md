# GE Rev 3 remaining power defects and bounded repairs

5 October 2026 UTC. Read-only review of Rev3A, Rev3B and Rev3C at exact commit `77f4c8893db6c018640e25c55a3af624a3eb06b3`. The nine schematic, board and netlist byte hashes match the earlier completed power analysis. `source-bindings.json` binds this review directly to the fixed commit and records independently extracted part identities, numbered terminals and board lands. No source, order or physical assembly was changed. Historical Rev 1 and Rev 2 revisions are outside this review.

**Review at the fixed baseline:** the narrowly justified common component repair is D14/D15, presently MCC MBR0540-TP/C78744, to exact STMicroelectronics STPS140Z/C155662. This repairs the 0.5 A versus programmed 0.606 A nameplate coordination gap and raises the diode junction limit from 125°C to 150°C while retaining the existing 25°C forward-drop screening ceiling, both OR branches and automatic PIN1-presence priority. It does not establish a continuous hot-board rating, complete fault coordination or appliance compatibility. Keep D11 and each revision's module/regulator/USB architecture. A cheap SMA alternative is documented below, with separate A layout and case gates.

## What the source establishes

| Function | Rev3A | Rev3B | Rev3C |
|---|---|---|---|
| PIN1 branch | J1.1 VDC → F2 → Q3 → U9 → D14 | Independently identical numbered branch | Independently identical numbered branch |
| PIN3 branch | J1.3 ALT_PWR → F1 → Q4 → U10 → D15 | Independently identical numbered branch | Independently identical numbered branch |
| CL resistors | R39/R40, 3.3 kΩ | R38/R39, 3.3 kΩ | R38/R39, 3.3 kΩ |
| DELAY resistors | R41/R42, 100 kΩ to respective protected supply | R40/R41 | R40/R41 |
| Priority | Q5/R35/R36/R37, PIN1 presence inhibits PIN3 | Same function | Same function |
| Output | AP63205/D11 → AP2112K-3.3 U6 → WROOM U2 | AP63205/D11 → soldered XIAO C3 v 1.3 | AP63205/D11 → socket J6, C3 or C6 |
| USB/service | J4 → F3 → D10 OR to +5V | Module USB directly on +5V; J2/D19 recovery source | Module USB directly on J6.7/+5V |

Numbered terminals common to all three: Q3/Q4 drain 3=fused input, source 2=protected input, gate 1=gate bias. U9 VS8/IN1=PIN1_PROTECTED; U10 VS8=PIN3_PROTECTED and IN1=PIN3_EN; both OUT7 feed their branch diode anode 2. D14/D15 cathode 1=/V_INPUT; U8 VIN3/EN2=/V_INPUT, SW5 feeds L1 and FB1 senses /BUCK_5V. D11 anode 2=/BUCK_5V, cathode 1=+5V. U9/U10 CL4 and DELAY5 retain the revision-specific resistor references above. GND2/DIAG_EN6/exposed pad 9 are grounded; FAULT3 is unconnected. Q5 base 1=/PRIORITY_BASE, collector 3=/PIN3_EN, emitter 2=GND.

Rev3A D10 anode 2=/USB_VBUS_FUSED, cathode 1=+5V; F3.1=/USB_VBUS and F3.2=/USB_VBUS_FUSED. U6 VIN1/EN3=+5V, VOUT5=+3V3, GND2. Rev3B D19 is a PMEG2010ER recovery OR diode, while Rev3A D19 is a PIN3 SMF16A TVS. Rev3C has no corresponding recovery D19. These are not interchangeable references.

## Diode defect and realistic bounds

The current MCC-authored [MBR0540 sheet, Rev 3-4-12012020, p 1](https://www.megastar.com/content/pdfs/MBR0520-MBR0580%28SOD123%29.pdf) gives 0.5 A at ambient 50°C, operating junction 125°C, θJA244°C/W on its stated single-sided FR4 lands and VF0.55 V at 0.5 A/25°C. Its storage 150°C is not an operating 150°C allowance.

The earlier nominal carrier allowance is 20.626 mA on 3V3 plus 1.033 mA on 5V. Published RF operating-point proxies give 356.66 mA carrier output for C3 and 366.66 mA for A/WROOM. They are not all-process/temperature/startup maxima. A separate 500 mA chip provision plus carrier stress is 521.66 mA in the linear paths. C6's upstream current depends on conversion when regulating and approaches output current in dropout.

| D14/D15 case | Forward screen | MCC reference junction at 85°C local ambient | Interpretation |
|---|---:|---:|---|
| C3 low-input current proxy 356.66 mA |196.2 mW|132.9°C|Above 125°C reference ceiling; not a measured fault |
| A low-input current proxy 366.66 mA |201.7 mW|134.2°C|Same thermal gate, independently applied |
| C3 at 13.6 V, earlier assumed 85% carrier efficiency, input 162.56 mA |89.4 mW|106.8°C|Higher input reduces input-diode current while output current remains 356.66 mA |
| 521.66 mA provision stress |286.9 mW|155.0°C|Also exceeds 0.5 A nameplate; not asserted normal continuous demand |
| Partial CL upper 708.26 mA at 85°C |389.5 mW|180.0°C if continuous|Actual retry is pulsed; steady θJA must not be used to predict its pulse peak |

With the mixed-condition 0.55 V/244°C/W screen, the 85°C reference current ceiling is 298.1 mA. Equivalently,356.66/366.66 mA require local ambient no higher than 77.1/75.8°C on that thermal reference. These are conditional screening limits, not allowed appliance ambient claims. Hot/cold VF, reverse leakage, actual copper, neighboring heat and actual load duty must be measured.

A45 ms attempt at 708.26 mA and 0.55 V is 17.53 mJ diode forward energy. A5.5 A/8.3 ms half-sine surge entry does not qualify that repetitive waveform. The source must not present a larger current-rated diode as completed protection coordination.

## Bounded replacement and actual land compatibility

Exact [STPS140Z primary sheet, pp 1–2 and 5](https://www.st.com/resource/en/datasheet/stps140z.pdf): SOD123,1 A continuous at ambient 60°C,40 V reverse,150°C junction,0.55 V maximum at 1 A/25°C and 0.51 V at 1 A/100°C. θJA175°C/W requires 50 mm² of 35µm copper. Leakage maxima are 10µA at 5 V/25°C,40µA at 40 V/25°C and 5mA at 40 V/100°C. Thermal runaway remains an explicit condition. Use the 0.55 V table row, not the inconsistent 0.49 V front-page summary.

All three source D14/D15 lands are 0.90×1.20 mm, centers±1.65 mm, inner gap 2.40 mm, overall 4.20 mm, cathode 1 at negative localX. ST recommends 0.97×0.65 mm lands,2.51 mm inner gap and 4.45 mm overall. Therefore these are **compatible lead-overlap lands**, not identical manufacturer-recommended lands. The ST body/terminal drawing gives overall 3.55–3.95 mm, terminal width 0.55 mm typical and minimum lead length 0.25 mm. Existing pads cover localX1.20–2.10 mm andY±0.60 mm: at the maximum reach the outer lead ends at 1.975 mm and the minimum 0.25 mm contact extends inward to 1.725 mm, within the pad. Cathode marking and existing K1/A2 mapping must be retained. Manufacturer paste/joint acceptance remains separate.

At the 366.66 mA/0.55 V screen, ST's 50 mm² reference would give 35.3°C rise,120.3°C junction at 85°C. At 521.66 mA it would give 50.2°C rise,135.2°C junction. These calculations show useful *potential* thermal margin. The actual boards only have GND planes; none has a V_INPUT cathode pour. Do not assign 50 mm² diode heat spreading or 175°C/W merely because the board has four layers. Retaining the current pads with this part is a current/junction-rating repair; adding/qualifying same-net heat-spreading copper would be a further bounded layout repair.

Current [LCSC exact C155662 page](https://www.lcsc.com/product-detail/C155662.html) displayed 4,930 pieces, USD0.1463 each at 5+,0.1178 at 50+,0.1036 at 150+. Two cost approximatelyUSD0.293/board before assembly, shipping and tax. Stock/price are a retrieved catalog snapshot and need rechecking for an order. No purchase was made.

The cheaper [LRC LMBR140T1G primary RevC](https://www.lrc.cn/Upload/PDF/Product/SBD/LMBR140T1G.pdf) and [C81142 catalog](https://www.lcsc.com/product-detail/C81142.html) give 1 A/40 V/150°C,0.56 V at 1 A,θJA312°C/W,124,860 pieces andUSD0.0399 each 20+. Its nominal 366.66 mA screen rises 64.1°C, leaving only 0.9°C below 150°C at 85°C before leakage or adjacent heat. Reject it as a claimed hot-margin repair. The Diodes B140HW SOD123 option has a 250°C/W typical reference requiring 1 inch square 2oz copper, so it supplies no verified thermal advantage on these lands.

### Cheap SMA option for a later local layout candidate

Exact [Diodes B140-13-F primary DS13002 Rev 20-2, pp 2/4/5](https://www.diodes.com/datasheet/download/B120.pdf) is 1 A at terminal 130°C,40 V,150°C junction,0.50 V maximum at 1 A/25°C. Its 20°C/W figure is **junction to terminal**, measured with specified 5 mm² copper pads; it is not ambient resistance. Leakage limits at 40 V are 0.5mA/25°C and 10mA/100°C. Package maximum 5.59×2.92×2.40 mm; recommended lands 2.50×1.70 mm, centers 4.00 mm,6.50 mm overall. Cathode band must remainpad 1. Its 0.50 V screen improves the existing room-temperature input-drop screen by 50 mV.

At 704.01 mA, forward screen 0.352 W gives 7.04°C junction-over-terminal on that reference. A measured terminal no hotter than 130°C would therefore retain about 13°C junction margin in this mixed-condition calculation. At a 1 A capacity check, the same model gives 10°C rise above terminal. Actual hot forward/reverse losses and a thermal-runaway check remain required. Do not derive an 85°C ambient allowance from θJT.

[LCSC C15759](https://www.lcsc.com/product-detail/C15759.html) displayed 57,360 pieces and USD0.0877 each 5+,0.0699 at 50+,0.0611 at 150+, aboutUSD0.175/board at 5+. This is a cheap option, not an exact-price assembly quote.

A6.50×2.92 mm maximum mechanical/land envelope, plus 0.25 mm courtyard margin, was screened at the current centers. B/C D14=(73,8) and D15=(73,22.5) mm have no source footprint-courtyard overlap with a 7.0×3.42 mm candidate courtyard; B's actual XIAO footprint remains clear. Rev3A D14=(66,11) and D15=(64,27) conflict with nearby TPS/decoupling/USB courtyards when enlarged. Small blind offsets also collide. A needs a separately reviewed local placement/reroute. The 2.40 mm package-height/case screen is unverified for all three. Accordingly SMA is feasible for exploration in B/C but is not an automatic common substitution and does not yet meet the complete board/case-clearance gate.

## D11 and USB diodes are a separate output budget

All three D11, A's D10 and B's recovery D19 are exact [Nexperia PMEG2010ER,115, July 2023](https://assets.nexperia.com/documents/data-sheet/PMEG2010ER.pdf), CFP3/SOD123W:20 V,1 A,150°C junction, VFmax 0.34 V at 1 A/25°C; standard FR4 θJA220°C/W, or 130°C/W with 1cm² cathode copper. The 1 A/130°C ambient entry uses ceramic and a specified switching waveform, not these FR4 DC boards.5 V leakage is 60µA typical, not a maximum;20 V/25°C maximum is 1mA. Hot reverse leakage remains a gate.

| Output diode current scenario | Forward screen 0.34 V | Standard-FR4 reference junction at 85°C |
|---|---:|---:|
| C3+carrier 356.66 mA |121.3mW|111.7°C|
| A+carrier 366.66 mA |124.7mW|112.4°C|
| 500 mA+carrier 521.66 mA stress |177.4mW|124.0°C|
|1 A capacity screen |340mW|159.8°C|

The first three cases provide no demonstrated normal-current component defect requiring a D11/D10 replacement. Their 1 A label does not prove 1 A DC at 85°C on this layout. An input 606 mA limiter can feed over 1 A at 5 V after conversion from a higher input; U8's 2 A rating and fault/startup waveforms remain distinct. Do not use CL as D11's output ceiling. Replacing these parts with a 0.50/0.55 V40 V diode would consume 5 V/module headroom and is unjustified. A's D10 USB reverse isolation and B's D19 recovery-source isolation remain their original functions.

## Fuse and control choices

F1/F2 are exact [1812L075/33DR](https://www.littelfuse.com/assetdocs/resettable-ptcs-1812l-datasheet?assetguid=ca5c80cb-504e-4a8a-8e74-0107520a1717):0.75 A room hold,1.5 A trip,33 V/20 A fault ratings,20°C post-reflow/trip resistance maximum 0.4Ω. Manufacturer reference hold is 0.47 A at 70°C and 0.36 A at 85°C. At low input, the C3 proxy 356.66 mA leaves only 3.34 mA before upstream bias; A366.66 mA already exceeds the 85°C reference. At 13.6 V the earlier C3 input proxy 162.56 mA leaves much more reference current budget. The fuse carries switch/bias current in addition to converter current. The switch's 5 mA supply test point is not an unconditional complete budget. No larger-fuse recommendation is justified before the OEM current/source-energy contract and required temperature are known.

A's F3 is exact 1206L050YR:0.5 A hold/20°C,0.31 A/70°C,0.25 A/85°C and 20°C R1max 0.7Ω. At 366.66 mA its room resistance screen is 257mV/94mW; the same load held continuously at 70/85°C exceeds the reference hold. USB service at intermittent load is not thereby a proven field failure. Increasing F3 materially changes upstream fault current and does not remove AP2112 heat or USB-current limits, so retain it pending the explicit service envelope. [Littelfuse primary 1206L sheet](https://www.mouser.com/datasheet/2/240/Littelfuse_PTC_1206L_Datasheet_pdf-2956361.pdf).

[TI TPS1H200A-Q1 RevE, pp 4–7/11/14](https://www.ti.com/lit/ds/symlink/tps1h200a-q1.pdf) explicitly supports IN tied to VS and 100kΩ DELAY-to-VS auto-retry. This is not an overvoltage-input defect. Logic thresholds are 1.8 V high/0.8 V low; UV restart 3.5–4.0 V and shutdown 3.0–3.4 V. The 0.8 V×2500/RCL formula gives 606.06 mA; partial±15%/R±1% gives 510.05–704.01 mA, or 507.01–708.26 mA with 85°C resistor drift. Accuracy requiresVS−OUT≥2.5 V. Retry on 35–45 ms/off 0.8–1.2 s; minimum unloaded charge budget 17.85mC excludes all startup demand. FAULT is unused.

Lowering CL to protect the present 0.5 A diode is not a harmless fix: below a 0.5 A setting TI's±20% regime applies, and a 4.99kΩ choice would have a partial minimum about 317mA, below the published low-input RF-plus-carrier proxies. Conversely the current partial 510mA minimum does not guarantee the 521.66mA linear provision stress. Leave CL and retry settings until startup/source data supports a setting; a larger diode is the bounded rating repair.

The priority circuit senses PIN1_PROTECTED voltage, not U9 output or useful power. An undervoltage, current-limited/retrying or weak PIN1 can inhibit healthy PIN3 while supplying insufficient power. That behavior is demonstrable from the net dependencies; exact crossover voltage and transients depend on Q5/R values/temperature. Changing it to fault-aware selection or a new UV supervisor is a new control/safety choice requiring user review. Preserve the existing automatic presence priority in this repair.

## Remaining defects and decisions

1. **Feasible component edit now:** exact D14/D15 STPS140Z in A/B/C, with K1/A2 retained, corresponding CAD/BOM metadata updated and assembled land approval. This closes the stated part-capacity/junction-rating gap only.
2. **Feasible further local thermal edit after review:** add same-net cathode heat spreading or explore B140 SMA in each revision independently. Current 175/312/220°C/W references do not prove mounted resistance. Case height, installed module envelope, clearances, routes, refill and native DRC must be checked on final CAD.
3. **Retain output diode/module architectures:** A AP2112 is 600mA but has a separate SOT25 thermal gate; at 4.7 V/365.626mA the earlier 0.512W/184°C/W screen is 94°C rise. C3's TLV module has a 500mA series fuse/diode path with unresolved fuse identity and its own LDO heat. C6's SGM6029C is a buck; its internal LMBR4010 diode and module heat remain separate. A larger carrier input diode cannot close these gates.
4. **OEM/bench gates:** establish each PIN1/PIN3 voltage tolerance, continuous/transient current allowance, source impedance and positive/negative fault waveforms. Measure minimum source/protected/V_INPUT/+5V/3V3, peak startup/RF currents, fuse/diode/LDO/buck temperature, and handoff/brownout behavior using the actual enclosure and module lot. Define both 3.3 V target and 3.0 V absolute operating-floor criteria; do not discard nominal 5/7.5/9/13.6 V support to force a pass.
5. **Safety decisions remain open:** The retained CJ3407 has a −30 V drain–source rating. In the exact selected Rev3A/B/C source, D18 cathode 1 is at PIN1_PROTECTED/Q3.source 2 and its anode 2 is GND; the second SMF16A is A D19 or B/C D20, cathode 1 at PIN3_PROTECTED/Q4.source 2 and anode 2 at GND. D13 is absent. Neither fused drain 3 node has a directly connected TVS. An intact unidirectional TVS forward-conducts if its protected source node goes negative, but that connection does not impose a documented negative voltage bound on the fused drain. The exact SUNMATE C399290 sheet publishes no maximum forward voltage/current condition, so a numerical negative clamp cannot be borrowed from another maker. If a protected source were momentarily at +26 V while its fused drain actually reached −13.6 V, VDS would be −39.6 V; this is an unbounded-node, unmeasured transient counterexample, not a demonstrated normal-source condition or a proven failure. Even the +26 V reference belongs to the specified 7.7 A,10/1000 µs,25°C positive-pulse test. Actual drain/source/gate waveforms, source impedance and clamp/current survival must establish the differential before selecting a higher-voltage PMOS. TVS remains upstream of switch CL; the PPTC trip curve alone does not coordinate TVS fault energy. Gate/bias resistors have distinct high-local-temperature limits. No full 40 V carrier rating follows. See PMOS-Transient-Example-Correction.md and pmos-tvs-placement-correction.json for the corrected numbered-node binding.
6. **USB qualification remains revision-specific:** A keeps its original two-diode OR. B/C raw module USB is tied to carrier+5V and must retain the existing disconnect-before-powered-USB operating instruction; a carrier diode change does not add host isolation. A fault-aware fallback, USB-source isolation or regulator/module redesign exceeds this bounded repair.

The accompanying `calculated-bounds.json` and `thermal-reference-screens.csv` expose the arithmetic and assumptions. The original evidence-generation recipe extracted the fixed commit without writing the repository. Source bindings and calculations are retained alongside this report. New PDF retrievals include exact LRC and ST bytes; PMEG/B140/B140HW direct-byte retrieval was blocked, so verified official web-PDF content is used without invented hashes. Prices are unauthenticated catalog observations, not assembly availability or supplier-lot qualification.
