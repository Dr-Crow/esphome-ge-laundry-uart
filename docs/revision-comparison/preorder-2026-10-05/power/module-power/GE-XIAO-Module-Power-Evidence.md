# GE XIAO module power evidence and bounded assumptions

Reviewed 5 October 2026 against the requested carrier baseline `bf581ac`. The shared checkout advanced during this read-only pass; its observed HEAD is recorded in `module-path-evidence.json`. No carrier or module CAD was changed. This is primary-document review and DC arithmetic, not circuit simulation, measurement, production qualification, or an authenticated supplier check.

**Decision:** 3.2 V at a XIAO side VBUS pin cannot provide a regulated 3.3 V rail through either reviewed module. 3.7 V is a marginal input after each module's own diode and other losses. 4.5/5.0 V provides useful regulator headroom, but current capability and enclosure temperature remain unqualified. USB VBUS connects directly to side VBUS before the module's regulator-input isolation diode on both modules.

## Exact paths established from manufacturer native CAD

The official C3 v1.3 archive is dated 16 January 2026; its schematic's circuit page is PDF page 3. The official C6 v1.0 archive is dated 14 January 2026; its power page is PDF page 4. Both pages were rendered and inspected; native PCB pad-net extraction independently confirms the paths. Full component properties and pad nets are in [module-path-evidence.json](module-path-evidence.json).

| Item | XIAO ESP32-C3 v1.3 | XIAO ESP32-C6 v1.0 |
|---|---|---|
| Side input and USB | J1 pin 7 / library side pad 14 and USB0 VBUS share `VUSB` | U2 side pad 14 and USB1 VBUS share `VBUS` |
| VBUS conversion path | `VUSB` → F1 `6V_500mA_Fuse` → `USB_FUSED_5V` → D1 MSK4005 → `VIN` → U2 TLV75733PDBVR → `VCC_3V3` | `VBUS` → D1 LMBR4010BST5G → `+5V` → U1 SGM6029CYG/TR → SW → L1 0.47 µH → `+3V3` |
| Regulator enable | U2 pins 1/3 both `VIN` | U1 B1/C2 both `+5V` |
| Output / feedback | U2 pin 5 and J1 pin 5 are `VCC_3V3` | U1 A2/VOS and side pad 12 are `+3V3` |
| Selection / output cap | Fixed 3.3 V; C23 2.2 µF nominal | R1 249 kΩ to GND at C1/MODE selects 3.3 V; C4 10 µF nominal; effective capacitance requires checking |
| Battery branch | Q1 drain `VBAT`, source `VIN`, gate `USB_FUSED_5V`; charger at fused USB | Q1 drain `VBAT`, source `+5V`, gate driven from raw VBUS through R20; separate SGM40567 charger on raw VBUS |

C3's circuit label says 700 mA by the regulator output. That annotation cannot establish module current capability: the exact series fuse label and manufacturer's MSK4005 catalog are both 500 mA. The fuse has no resolved manufacturer part number, resistance, hold/trip curve, or temperature derating in the reviewed source. C6's diode is nominally 1 A, but its heat dissipation matters well below 1 A. Neither module diode isolates the raw side pin from the USB connector. C6's Q2/Zener shunt is also not source-selection isolation. Simultaneous live appliance supply and module USB therefore require the carrier's separate source-contention assessment.

Sources: [C3 official schematic](https://files.seeedstudio.com/wiki/XIAO_WiFi/Resources/XIAO_ESP32C3_v1.3_SCH_260116.pdf), [C6 official schematic](https://files.seeedstudio.com/wiki/SeeedStudio-XIAO-ESP32C6/XIAO_ESP32_C6_v1.0_SCH_260114.pdf). Archive URLs and SHA-256 values are in [all-primary-source-manifest.json](all-primary-source-manifest.json).

## Chip current and voltage meaning

The C3 v2.4 and C6 v1.5 datasheets list the highest Wi-Fi entries as 335 mA and 354 mA respectively, for 1 Mbps 802.11b at 21 dBm, measured at 3.3 V / 25 °C with TX at 100% duty. Their tables label these entries as peaks; they do not supply a guaranteed maximum over process, temperature, firmware, startup, or assembled-module loads. Treat them as published operating-point proxies, not a hard current ceiling. C3 RX is 84/87 mA for HT20/HT40; this does not establish worst-case input supply capacity. [C3 datasheet §§5.2/5.6](https://www.espressif.com/sites/default/files/documentation/esp32-c3_datasheet_en.pdf), [C6 datasheet §§5.2/5.6](https://www.espressif.com/sites/default/files/documentation/esp32-c6_datasheet_en.pdf).

Both chip families have a recommended 3.0–3.6 V supply range, with 3.3 V nominal. Both datasheets show 0.5 A in the minimum column for cumulative input-current provision. The [C3 hardware guide](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c3/schematic-checklist.html#power-supply) and [C6 hardware guide](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c6/schematic-checklist.html#power-supply) independently recommend a 3.3 V supply able to provide at least 500 mA. That is a supply-design recommendation, not a measured continuous 500 mA chip load. Falling just above 3.0 V does not meet a 3.3 V target or establish RF, flash, startup, or carrier circuit margins.

For the carrier budget add its 3.3 V loads to the module load; do not silently allocate the full regulator rating to external peripherals. The 500 mA rows below are a total-rail stress point, not a substitute for that complete budget. Batteries are assumed absent. Charger draw, RF-switch/LED loads, GPIO loads and startup charging are additional unresolved loads; published chip-current measurements should not be doubled by adding an invented second CPU/flash allowance.

The separately extracted nominal carrier case adds 20.626 mA on 3V3 and 1.033 mA on the carrier5 V rail (all three LEDs and six 10 kΩ sink paths under its stated voltage assumptions). Thus module-plus-carrier rail proxies are355.626 mA for C3 and374.626 mA for C6. The 5 V overhead is separate; do not run it through the module's 3V3 converter model. Those nominal carrier currents are held constant in the following sensitivity examples; actual LED/resistor current changes with rail voltage.

## Regulator and diode evidence

**C3 TLV75733PDBVR, DBV SOT-23-5:** recommended input 1.45–5.5 V, output up to 1 A, junction −40…125 °C. At 3.3 V output / 1 A, dropout is 300 mV typical; maximum 425 mV through 85 °C and 475 mV through 125 °C. TI describes linear dropout scaling with current; scaling is a model, not a separately specified module guarantee at 335/500 mA. Ground current is 25 µA typical, 40 µA maximum through 125 °C. Accuracy is ±1% through 85 °C / ±1.5% through 125 °C under stated test conditions. Current-limit range 1.2–1.78 A and typical 165 °C shutdown protect faults, not continuous operation. DBV θJA references are 100.8 °C/W on TI's EVM and 231.1 °C/W on JEDEC PCB; neither qualifies XIAO. Reverse output bias can damage the part; absolute VOUT ≤ VIN+0.3 V and external protection is needed where reverse current is expected. [TI SBVS322C §§5,7.1](https://www.ti.com/lit/ds/symlink/tlv757p.pdf).

**C6 SGM6029CYG/TR:** recommended VIN 1.95–5.5 V; C variant output rating 1 A at VIN ≥2.3 V, 0.7 A below, with 4 MHz nominal switching and 100% duty operation near dropout. High-side resistance is 185 mΩ typical / 310 mΩ maximum at the stated test condition. No fixed guaranteed dropout number is specified. PSM no-switch IQ is 2.3 µA typical / 5.5 µA maximum; forced-PWM switching no-load draw is 8.5 mA typical. The ±2% output specification is stated for PWM/no-load; it cannot certify the assembled rail under bursts. Recommended junction ceiling is 125 °C; θJA reference 214 °C/W. Typical 160 °C shutdown has 20 °C hysteresis; thermal protection is absent in PSM. No reverse-blocking capability is qualified by the datasheet; output discharge and SW's VIN+0.3 V absolute limit matter if externally driving 3V3. [SGMICRO Rev A.1, November 2022, pp.2–6,16](https://www.sg-micro.com/rect/assets/3323f5dc-718f-4b81-b820-398ddb702989/SGM6029.pdf).

**Module series diodes:** Shikues' [official catalog p.7](https://api.shikues.com/product_category.pdf) identifies MSK4005 as 40 V / 0.5 A with VF 0.49 V at 0.5 A. The catalog is not a complete temperature-qualified limit table; do not adopt conflicting distributor 50 V entries. LRC's [LMBR4010BST5G Rev C p.1](https://www.lrc.cn/Upload/PDF/Product/SBD/LMBR4010BST5G.pdf) gives 1 A, VF maximum 0.39/0.50/0.55/0.60 V at 0.10/0.50/0.70/1.00 A at 25 °C, 250 mW at 25 °C with minimum pads, derating 2.5 mW/°C, θJA 400 °C/W and TJ 125 °C. Current rating alone is insufficient. Manufacturer-authored MSK4005 PDF at LCSC could be read in web cache, but direct-byte retrieval returned403; no hash or complete limit-table claim is made for that mirror.

**C6 inductor identity:** Native CAD specifies TDK TFM160808ALC-R47MTAA,0.47 µH±20%. The [TDK datasheet dated 16 June 2025](https://product.tdk.com/info/en/catalog/datasheets/inductor_commercial_power_tfm160808alc_en.pdf) gives 54 mΩ typical /62 mΩ maximum DCR, and 2.6 A rating by its 40 °C self-heating criterion. The 0.08 Ω resistance below is a deliberately higher temperature-sensitivity proxy; it is not the part's nominal DCR or a guaranteed hot limit. Actual mounted lot, bias, temperature and effective module capacitors remain physical qualifications.

## Explicit DC sensitivity assumptions

These are algebraic scenarios selected to expose margin; none is a guaranteed bound. Inputs are **actual module side VBUS**, after carrier losses. For both modules assume diode VF =0.35 V. C3 additionally assumes fuse resistance 0.20 Ω and LDO dropout resistance 0.30 Ω, the latter obtained from TI's typical 1 A dropout point. C6 assumes high-side resistance 0.185 Ω and inductor DCR 0.08 Ω; DCR is an unverified sensitivity value, not the native board's specified part. For regulated C6 cases sweep converter efficiency80/90/95%, excluding its input diode; the datasheet's typical curves support investigating high efficiency, but they guarantee no floor. Side current excludes auxiliary loads and startup.

| Side VBUS | C3 at 335 mA rail: estimated rail / input current | C6 at 354 mA rail: estimated rail / input current | Interpretation |
|---:|---|---|---|
|3.2 V|2.683 V /≈335 mA|2.756 V /≈354 mA in dropout|3.3 V impossible; this scenario also misses3.0 V |
|3.7 V|3.183 V /≈335 mA|3.256 V /≈354 mA in dropout|Above3.0 V in this scenario, below3.3 V target; not a qualification pass |
|4.5 V|3.3 V /≈335 mA|3.3 V /296–352 mA|Regulation plausible; C6 current interval depends entirely on the selected efficiency sweep |
|5.0 V|3.3 V /≈335 mA|3.3 V /264–314 mA|Regulation plausible; C3 dissipates more heat |

At500 mA total rail load the same assumptions give C3/C6 rails2.60/2.718 V at 3.2 V, and3.10/3.218 V at 3.7 V. At4.5/5.0 V, C6 regulated input proxies are419–497 /374–444 mA; C3 remains≈500 mA plus auxiliary draw. That leaves no demonstrated margin around C3's500 mA series path.

Equations: C3 VIN=Vside−VF−Iout·Rfuse; Vrail=min(3.3,VIN−Iout·Rdrop). C6 dropout Vrail≈min(3.3,Vside−VF−Iout·(RHS+RL)); when regulated Iin≈3.3·Iout/[η·(Vside−VF)]. Do not use the regulated3.3 V power formula in dropout. Diode current is C6 input current, not its output current. [dc-sensitivity.json](dc-sensitivity.json) contains all 16 rows, assumptions, losses and thermal-reference sensitivity values.

Changing C3 to VF0.49 V and scaled125 °C dropout resistance 0.475 Ω, while keeping the unverified fuse resistance 0.20 Ω, gives about 2.984 V at 3.7 V/335 mA and2.873 V at 3.7 V/500 mA. This illustrates why nominal 3.7 V cannot establish even3.0 V throughout operation. It is not a guaranteed corner because fuse, diode temperature behavior, regulator resistance behavior and dynamics remain unresolved.

For the carrier-inclusive case, the moderate assumptions give C3/C6 about 3.172/3.251 V at side3.7 V. The conditional side-VBUS thresholds for at least 3.0 V are 3.528/3.449 V; the corresponding thresholds for reaching 3.3 V are 3.828/3.749 V. These are two different regions, not a pass/fail conclusion from a pre-regulator voltage alone. In particular, an actually measured LDO VIN of3.21 V at C3 load355.626 mA gives3.041 V in the scaled0.475 Ω dropout model. This alone establishes neither a guaranteed rail-floor pass nor failure: actual dropout, output copper loss, ripple and transient response remain unknown. If3.21 V is instead a calculated upstream node with additional series loss still unfilled, an additional0.1155 Ω would move this model below3.0 V. Do not subtract module-fuse loss twice after actual LDO VIN has already been measured.

## Thermal implications and stopping boundary

In the0.35 V diode scenario C3 LDO loss is0.262 W at 4.5 V/335 mA and0.430 W at 5 V/335 mA. The two TI reference θJA values produce temperature-rise proxies26–61 °C and43–99 °C. At500 mA they become0.375/0.625 W, with 38–87 °C /63–144 °C rise. These reference spans are not bounds on the actual module. With less diode/fuse loss, more heat shifts into the LDO; do not use maximum diode drop as a conservative LDO-heating case. At5 V/335 mA the total rail-conversion loss before auxiliary loads is0.570 W, distributed among fuse/diode/LDO.

For C6 at 354 mA, the80–95% converter sweep corresponds to0.061–0.292 W total converter loss. Assigning all of it to the IC solely as a sensitivity proxy yields13–62 °C rise using214 °C/W; some real loss belongs to the inductor. The diode dissipates another0.104–0.123 W at 4.5 V or0.093–0.110 W at 5 V under the0.35 V assumption. At500 mA rail/4.5 V input withη0.80 and VF0.50 V, Iin≈0.516 A and diode loss≈0.258 W. That exceeds the diode's25 °C minimum-pad dissipation reference; it does not predict actual XIAO temperature. At60 °C that reference dissipation allowance is only0.1625 W. Actual copper, neighboring chip heat, enclosure temperature and intermittent RF duty must be established.

The useful next evidence is simultaneous minimum sideVBUS / minimum3V3 / peak input current at startup and sustained RF, plus LDO/buck/diode temperatures in the intended enclosure and actual module-lot identity. Static arithmetic cannot close transient regulation, fuse derating, charging, reverse-feed, simultaneous USB, or thermal gates. A 3.0 V floor and a 3.3 V target must remain separate acceptance criteria.

## Integrity

The manifest records official URLs, exact downloaded bytes, retrieval times and SHA-256 values. Key hashes: C3 datasheet `833fc000b4b3c3d39c496fcbd597fed5806956503ce7390b19cc8ae82f19f968`; C6 datasheet `372a5b42b2900c83ef4309149c8835e9ae2d1be19244995bf2fb83af4dc5edf1`; TLV757P `9f5e9602ed9366124dfee01dd773ceafca6b54c5c22cf3a7999453432c5cefb9`; SGM6029 `79d7e25abc3acfd18ab9c394e082663e07dc169151b4bfe0314c13510ced63e0`. The official source-CAD/PDF hashes were rechecked against the earlier sourcing manifest. No load-current maximum, simulation result, assembled-board thermal resistance, or module-lot qualification was invented.
