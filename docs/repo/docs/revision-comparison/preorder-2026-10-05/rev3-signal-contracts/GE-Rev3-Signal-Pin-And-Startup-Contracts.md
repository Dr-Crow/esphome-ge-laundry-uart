# GE Rev3 signal pin and startup contracts

Read-only review on 5 October 2026, bound to published commit `acbcb6c5a138fedeb8e93d92838b12381bbce4b4`. Only Rev3A, Rev3B and Rev3C were reviewed. Committed blobs were read directly, avoiding concurrent worktree edits. No circuit, firmware, manufacturing artifact, purchase, eFuse or physical hardware was changed.

**Decision:** no numbered-pin reversal, missing required boot pull, GPIO2 LED boot failure, or firmware GPIO mismatch was established. Preserve both GE inputs, automatic PIN1 priority, integrated WROOM Rev3A, soldered C3 Rev3B and socketed C3/C6 Rev3C. Two specific signal contracts remain conditional: the WROOM/C6 UART TX low-level margin and the purchased Diodes buffer's inconsistent recommended output-voltage wording. Loaded startup/reset timing and ROM traffic still require qualification. None is a demonstrated appliance failure.

## Actionable contract map

| Contract | Finding | Smallest supported next step |
|---|---|---|
| BAV99 numerical pins and inherited labels | Correct at this commit; D9 does not short its parallel 4.7 kΩ during a low transmit state | Preserve numbers, geometry and copper; use corrected A1/K2/K1,A2 names |
| C3 GPIO2 LED and GPIO8/9 boot controls | Explicit carrier pulls agree with boot requirements; GPIO2 does not select SPI versus download mode | Preserve current LEDs and pulls; document the datasheet footnote |
| C6 boot controls | GPIO8/9 and reset remain inside the unmodified module; XIAO D9 header signal is GPIO20 | Preserve module buttons/pulls; keep JP1 1–2 |
| WROOM/C6 UART0 TX to U5.3 | 499 Ω module series resistance tightens the carrier low-state divider | Obtain a loaded GPIO VOL bound or measure U5.3 across intended rail/load/temperature; no resistor edit is mandatory from these sources |
| U5 outputs released toward 5 V while supplied at 3V3 | Purchased Diodes datasheet contains conflicting range statements | Resolve with Diodes/OEM documentation before claiming a guaranteed operating-range pass |
| EN/reset and brownout | A's RC matches the recommended nominal values; B/C retain different module RCs | Qualify actual rail/EN waveforms and recovery timing; an RC is not a brownout supervisor |
| UART ROM traffic | Hardware connects UART0 TX to the GEA3 output on every option, including GEA2 profiles | Measure appliance behavior during reset/download/sag; retain the existing ROM warning |

## Numbered signal nets

Exact component values and pin groups are in [source-bound-numbered-contracts.json](source-bound-numbered-contracts.json), with each committed schematic, PCB and retained native netlist's Git blob and SHA256. The independent comparison found **zero physical net-group differences across 332 inspected PCB terminals**. Rev3A/B J3 has six schematic service terminals but no PCB footprint; those documented absent terminals were excluded from physical comparison, not mistaken for a broken net. This is connectivity evidence, not an energized test.

The purchased signal diode is **C2500, Nexperia BAV99,215, SOT23**. Primary [BAV99 pin table, p2](https://assets.nexperia.com/documents/data-sheet/BAV99.pdf) specifies 1=A1, 2=K2, 3=K1/A2. The older [series sheet linked by current component instances, p2](https://assets.nexperia.com/documents/data-sheet/BAV99_SER.pdf) agrees. Current Rev3A cached and local LegacySymbols BAV99 definitions already carry these names. Earlier K/A/K labels are historical semantic errors, not grounds to swap pads.

All three carriers have:

- D1/D2/D3 pin1=GND, pin2=+5V, pin3 respectively=J1.7 half-duplex/J1.5 appliance receive/J1.4 appliance transmit. These are clamps to the 5 V domain, not 3V3 clamps or precision rail limits.
- D9.3=U5.6/R19.1/R22.1, called T here; D9.2=U4.1/R18.1/R22.2/R23.1/TP4.1, called H; D9.1 is NC. R19.2=+5V, R18.2=GND, R23.2=J1.7. R19=10 kΩ, R18=220 kΩ, R22=4.7 kΩ, R23=1 kΩ. The used diode conducts T toward H. T low with H positive reverse-biases it, leaving R22 as the resistive sink path.
- U4.1→U4.6 is half-duplex receive; U4.6 has R14=10 kΩ to 3V3 then R10=1 kΩ to module GEA2 RX. U4.3 receives J1.4 through R25=1 kΩ, with R21=220 kΩ to +5V; U4.4 has R17=10 kΩ to 3V3 then R13=1 kΩ to module GEA3 RX.
- Module GEA2 TX→JP1.1–2→R11=1 kΩ→U5.1; R15=10 kΩ pulls U5.1 low. U5.6 drives T. Module GEA3 TX→R12=1 kΩ→U5.3; R16=10 kΩ pulls U5.3 to 3V3. U5.4 is pulled toward +5V by R20=10 kΩ and reaches J1.5 through R24=1 kΩ.
- U4.5=+5V; U5.5=+3V3; both pin2=GND. The actual **C151607, Diodes Incorporated 74LVC2G07W6-7, SOT26** is recorded in every current instance and sourcing ledger. Its [DS35162 Rev6-2, p2](https://www.diodes.com/datasheet/download/74LVC2G07.pdf) maps 1/3 to inputs and 6/4 to open-drain outputs: low input sinks, high input releases. Supply labels in inherited library aliases do not change that function. The instances link this actual vendor sheet; an old generic TI library URL is not purchasing evidence.

Firmware uses module direction. Rev3A U2.4/10 are C3 GEA2 TX/RX GPIO5/10; U2.12/11 are GEA3 TX/RX GPIO21/20. Rev3B U2.4/11 and 7/8 implement the same GPIOs. Rev3C J5.4/J6.4 are GEA2 TX/RX, J5.7/J6.1 are GEA3 TX/RX: C3 GPIO5/10 and 21/20; C6 GPIO21/18 and 16/17. Existing GEA2 inversion/19,200 baud and GEA3 noninversion/230,400 baud agree with those retained profiles. JP1 2–3 reaches C3 GPIO9 but C6 GPIO20; it has no supplied supported profile.

## Boot pulls and module reset

The [C3 chip v2.4, pp30–32](https://documentation.espressif.com/ESP32-C3_Datasheet_en.pdf) and [WROOM-02 v1.7, pp12–14](https://documentation.espressif.com/esp32-c3-wroom-02_datasheet_en.pdf) explicitly explain that GPIO2 does not determine SPI versus joint-download boot, although a pull-up is recommended against glitches. SPI uses GPIO9 high; downloader uses GPIO9 low with GPIO8 high. Carrier R5=10 kΩ directly pulls GPIO2 high, independent of the red LED: +3V3→R4 220 Ω→D5 anode2/cathode1→GPIO2. Thus the LED supplies an additional nonlinear high-side path, not a pull-down. Firmware's active-low red LED, ALWAYS_OFF and boot turn-off occur after strap sampling; they cannot repair a hardware strap, and no such repair is needed here. R1 pulls GPIO8 high and R2 pulls GPIO9 high, each 10 kΩ. Green/yellow are GPIO3/4 through 220 Ω LEDs to ground.

WROOM module p32 shows no fitted external GPIO2/8/9 or EN pull network that would replace the carrier's pulls. Rev3A U2.2 EN, R3 10 kΩ, C26 1 µF, SW1 and J2.6 retain the integrated architecture. BOOT is U2.8/SW2/J2.3/R2.

The unmodified [XIAO C3 v1.3 schematic, p3](https://files.seeedstudio.com/wiki/XIAO_WiFi/Resources/XIAO_ESP32C3_v1.3_SCH_260116.pdf) has R6 10 kΩ on chip GPIO9/D9; BOOT0 shorts it to GND. GPIO2/D0 and GPIO8/D8 have no onboard resistor pull. Module R4 10 kΩ/C5 100 nF form EN's RC; RST0 shorts EN to GND. Rev3B adds parallel carrier R3 10 kΩ, giving nominal 5 kΩ/100 nF, τ≈0.5 ms. Rev3C exposes no EN in its 14 sockets and adds no EN resistor or capacitor; its C3 retains τ≈1 ms. Adding A's C26 indiscriminately would alter module timing and is unsupported.

For [XIAO C6 v1.0, p5](https://files.seeedstudio.com/wiki/SeeedStudio-XIAO-ESP32C6/XIAO_ESP32_C6_v1.0_SCH_260114.pdf), onboard R13 5.1 kΩ pulls actual GPIO8 high, R17 10 kΩ pulls GPIO9/BOOT high, K2 asserts BOOT, and R16 10 kΩ/C21 1 µF/K1 implement EN/reset. Carrier R1 instead reaches header D8/GPIO19; R2 reaches header D9/GPIO20, not BOOT. LED GPIO0/1/2 are not C6 straps. Onboard GPIO15's R18 1.5 kΩ/LED network stays unchanged; MTMS/MTDI GPIO4/5 are also not carrier D4/D5. [C6 v1.5, pp33–36](https://documentation.espressif.com/esp32-c6_datasheet_en.pdf) identifies those additional SDIO/JTAG straps, whose defaults are not changed by the carrier.

Both chips require at least 50 µs stable rails before EN activation, 50 µs actually below reset-low, and 3 ms strap hold after EN rises. Nominal RC values satisfy no complete slow-ramp, residual-charge, sag or programmer guarantee. Hold BOOT through delayed EN rise and strap hold, preferably until the downloader starts; manual recovery remains necessary when adapter control lines are absent. See the retained [Rev3A reset analysis](../../../../pcb/rev3a/POWER-QUALIFICATION.md) and [Espressif manual recovery guidance](https://docs.espressif.com/projects/esptool/en/latest/esp32c3/advanced-topics/boot-mode-selection.html).

## Two unresolved signal margins

**UART0 low level:** WROOM's onboard R2 and C6's onboard R14 are each 499 Ω in UART0 TX; C3's onboard R5 is 1 Ω. Carrier R12 adds 1 kΩ and R16 pulls the U5.3 input to module 3V3 through 10 kΩ. Ignoring leakage, VI=(VOL×Rp+VDD×Rs)/(Rp+Rs). This adds about 0.39 V to a 0.33 V WROOM/C6 low at nominal3.3 V, versus 0.27 V for C3.

Espressif's VOL≤0.1VDD row explicitly uses a high-impedance load at 3.3 V/25 °C. Its loaded sink row gives 28 mA **typical** at VOL 0.495 V/PAD_DRIVER 3, not a guaranteed maximum VOL at this approximately0.29 mA load. Neither row certifies a hot/cold assembled divider. The existing profiles specify no explicit drive-strength override. Consequently a guaranteed pass or failure cannot be derived from these rows.

| Clearly labeled sensitivity | WROOM/C6 U5.3 voltage | Interpretation |
|---|---:|---|
|3.3 V, assumed GPIO VOL 0.33 V, nominal resistors, zero leakage|0.7172 V|82.8 mV below VIL 0.8 V|
|3.6 V, assumed VOL 0.36 V, nominal resistors, zero leakage|0.7824 V|17.6 mV margin; extended assumption|
|3.6 V, Rp−1%, Rs+1%, +5 µA leakage|0.7963 V|Mixed sensitivity; module resistor tolerance and loaded VOL not guaranteed|
|Same, +20 µA leakage|0.8160 V|Mixed high-temperature leakage sensitivity, not a guaranteed violation|

The better acceptance contract is **actual loaded GPIO VOL≤0.3415 V** under that last sensitivity, to keep U5.3≤0.8 V; practical qualification should retain additional noise margin. Diodes input leakage is ±5 µA through 85 °C and ±20 µA through 125 °C; WROOM lot rating and carrier component ratings still limit actual usable temperature. Do not promote a 125 °C buffer screen to a qualified 125 °C product.

If measurement or an applicable OEM bound cannot close this contract, a narrow **R16 10 kΩ→22 kΩ** candidate raises the same conditional allowable GPIO VOL to≈0.5751 V. Released-input voltage at 3.0 V with20 µA sinking leakage and 22 kΩ+1% is≈2.556 V, still above 2.0 V in that resistor-only screen. It needs edge/startup/noise checks and exact sourcing; it is an optional candidate, not a required repair or a guaranteed pass. Do not change buffers, protocol or module onboard parts. [Calculations](conditional-divider-calculations.json) retain assumptions and formulas.

**Purchased buffer output range:** Diodes DS35162 p3's recommended VO row gives 0…VCC, but p4 tests released-output leakage to 5.5 V with VCC 3.6 V; p3 permits up to 6.5 V in its absolute high-impedance/IOFF row. The mixed-domain U5.6/U5.4 release toward+5V matches the intended open-drain use and does not prove damage, but those statements are not an internally consistent recommended-range guarantee. Obtain an authoritative clarification for **74LVC2G07W6-7**, not a substitute vendor's guarantee. Native DRC and clean builds cannot resolve it. Actual U4 input rails, 220 kΩ receive bias, appliance pulls, cable capacitance and input slew remain in the existing loaded-interface qualification; preserve their values pending that evidence.

## Firmware and ROM boundary

Reuse [BOARD-COVERAGE](../../../../firmware/BOARD-COVERAGE.md), which records the eight successful pinned ESPHome2026.9.1/ESP-IDF5.5.5 builds and exact earlier hosted receipts. This review checks current pins/configuration against them; it does not claim a fresh build at acbcb6c. Successful compilation establishes generation, not loaded electrical behavior.

GPIO21 UART0 TX on C3/WROOM and GPIO16 on C6 physically reach U5.3→U5.4→R24→J1.5 even with GEA2 selected. R16 holds that buffer released when the pin is high-impedance, but cannot suppress actively driven ROM lows. Default chip ROM messages can therefore reach the GEA3 bus; application logger baud 0 and LED boot priority do not ensure silence during reset/download/brownout. The retained firmware README already discloses this. No eFuse change or hardware containment is proposed without an appliance/OEM silence requirement. Recovery must follow the architecture-specific single-supply procedures; B/C powered USB requires appliance disconnection.

Review stops here: further closure needs applicable OEM/vendor bounds or physical waveforms. No broader catalog, historical-revision audit, native/manufacturing rerun or redesign is needed to answer these contracts.
