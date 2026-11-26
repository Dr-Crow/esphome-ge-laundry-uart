# Rev3A architecture-specific power qualification

The rated-protection backport retains AP63205 U8, D11 isolation, AP2112K-3.3TRG1 U6 and the integrated ESP32-C3-WROOM-02-N4 U2. USB-C/F3/D10, native USB data, RESET/BOOT and recovery headers retain their original nets. C26 implements the separately reviewed external EN RC recommendation. No source voltage/current envelope, thermal pass or compatibility result follows from native CAD checks.

## Integrated 3.3 V chain

[Diodes AP2112 DS39724 Rev2-2](https://www.diodes.com/datasheet/download/AP2112.pdf), pp 3/8/11/12, identifies K-3.3TRG1/SOT25. Recommended VIN is 2.5–6 V and ambient −40…85°C;6.5 V input/150°C junction are absolute ratings, not operating targets. The 3.3 V table uses VIN 4.3 V:±1.5% accuracy at 1–30 mA,≥600 mA capability, dropout maximum 200 mV at 300 mA/400 mV at 600 mA, no-load IQ55 µA typical/80 µA maximum and 20 µs no-load typical startup. Lower VIN can be in dropout; it does not preserve a regulated3.3 V output merely because it exceeds2.5 V.

[Espressif WROOM-02 v1.7](https://documentation.espressif.com/esp32-c3-wroom-02_datasheet_en.pdf), pp 15/22–23, gives 3.0–3.6 V supply and recommends≥500 mA external supply capability. Its345 mA Wi-Fi TX row is at 3.3 V/25°C, 100% duty, a particular modulation/power setting; it does not bound all startup/firmware/carrier loads or measured average appliance traffic. The supply-capability requirement is not an OEM current allowance or a continuous draw claim.

### Nominal 5 V source and dropout headroom

The AP63205 cannot produce regulated5 V from a raw 5 V source after fuse/FET/switch/D14 losses. Near dropout, downstream voltage also includes buck losses and D11. Retain nominal 5 V as an intended loaded qualification case; no source is excluded to force a pass.

A deliberately mixed-condition364 mA illustration uses old237 mV versus selected323 mV pre-OR path loss, D14/15 at 0.55 V and D11 at 0.34 V. Then raw 5 V gives 4.127 V before unknown buck loss and 3.787 V at the LDO before unknown buck/PCB losses. Using the 600 mA dropout row only as a screen gives 87 mV above 3.3+0.4 V; adding a1.5% high-setpoint reserve leaves37.5 mV, versus 123.5 mV for the old path. These conditions are not a matched assembled-board corner, the 600 mA row is not a guaranteed364 mA interpolation, and the voltage-tolerance row is low-current. This is a headroom warning, not a pass/fail proof.

When the buck regulates at higher input, the additional86 mV input-path loss changes input current/thermal margin rather than automatically lowering3V3 by 86 mV. The conditional TPS 5 mA versus old85 µA bias reference adds 4.915 mA before VS;0.487 Ω fuse+PMOS gives 2.394 mV additional pre-VS loss. It does not include switch-channel resistance in that bias-current drop or directly reduce OUT CL. Validate actual currents, diode drops, source impedance, duty/temperature and both GPIO supply domains.

### Regulated high-input thermal screen

For a regulated buck near5 V, D11 can leave an illustrative 4.5–4.8 V into U6. At 3.3 V output and 335 mA continuous RF illustration, U6 dissipates approximately:

| Actual U6 VIN illustration | Dissipation before ground current | Published 184°C/W reference rise |
|---|---:|---:|
|4.5 V |0.402 W |74.0°C |
|4.7 V |0.469 W |86.3°C |
|4.8 V |0.5025 W |92.5°C |

The SOT25 sheet's θJA 184 °C/W is a no-heatsink reference, not a prediction for this four-layer board/enclosure. Ground-current dissipation, actual average duty, carrier overhead, ambient, copper and airflow must be included. A separate345 mA/4.7 V example gives 0.483 W/88.9 °C reference rise. At 85 °C ambient either illustration approaches or exceeds the 150 °C absolute-junction reference; actual operation must retain margin and be measured. Typical160°C thermal shutdown is above that absolute figure and cannot be treated as a normal-operation guardrail. The 600 mA current rating alone is not a thermal pass, and these illustrations do not authorize regulator redesign or equate continuous TX with average appliance traffic.

## Startup/current/retry and retained priority

TPS CL is nominal 0.606 A with 3.3 kΩ. The conditional 15%/1% screen is 0.510–0.704 A and needs VS−OUT≥2.5 V under the specified setting/test conditions. It is not an unconditional draw ceiling. The upstream source, temperature-dependent PPTC hold/trip, D14/D15, copper and integrated module/LDO current budgets remain independent. The WROOM ≥500 mA supply recommendation refers to its 3.3 V domain; it cannot be compared directly with the switch current on a different voltage/converter path.

Continued limit yields35–45 ms ON/0.8–1.2 s OFF, with thermal interruption possible. The unloaded 0.510 A×35 ms≈17.9 mC calculation excludes converter/rail/MCU demand. AP63205 typical 4 ms, AP2112 no-load typical 20 µs and the EN RC calculations cannot be added into a loaded startup certificate. Capture cold/hot startup, slow ramps, residual charge, repeated retries, RF reconnect/transmit and recovery from sag; keep TPS local VS above its maximum 4 V restart threshold.

Original Q5/R35/R36/R37 sense PIN1 presence rather than useful output. Weak/faulting PIN1 can still inhibit PIN3. No fault-aware fallback or narrower source range is added. Validate both handoffs and all eight PIN1/PIN3/USB combinations, including source-current spikes, brownout/retry, inactive-input voltage and host VBUS isolation. No physical tests ran here.

## CHIP_EN correction and programming contract

[Espressif's C3 schematic checklist](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c3/schematic-checklist.html#chip-power-up-and-reset-timing), printedp 7/local PDF p10, recommends10 kΩ/1 µF at CHIP_EN with actual supply timing reviewed. C26 uses [Yageo CC0805KKX7R9BB105](https://yageogroup.com/download/specsheet/CC0805KKX7R9BB105), C91185,1 µF ±10%, 50 V X7R 0805. Existing R3 remains10 kΩ±1% C17414; U2.EN, SW1, J2 pin 6 and DNP J3pin 1 retain their original connections. No external USB-to-EN transistor path exists, and USB circuitry is unchanged.

For an initially discharged capacitor and ideal stable 3.3 V step, nominal τ 10 ms gives 2.877 ms to 0.25 VDD and 13.863 ms to 0.75 VDD. R±1%/C±10% alone givesτ8.91–11.11 ms, low-boundary2.563–3.196 ms and high-boundary12.352–15.402 ms. The family X7R±15% temperature reference broadens that partial τ screen to 7.5735–12.7765 ms. DC bias, aging, resistor drift, leakage, external drive and residual charge are excluded; effective capacitance is not guaranteed by typical simulations.

Stored charge/energy are3.3 µC/5.445 µJ at 3.3 V. Steady reset pullup current is 0.330 mA (0.364 mA at 3.6 V/R −1%), but capacitor discharge flows directly through SW1 or the programmer; R3 does not limit its instantaneous peak. Neither SW1's50 mA catalogue rating nor small stored energy proves pulse capability. An unspecified100 Ω sink illustration needs140 µs to reach0.825 V plus≥50 µs below reset-low, so a50 µs command is not automatically a valid reset. Verify real adapter resistance, sink/pulse width and switch behavior.

Hold BOOT low through delayed EN rise and≥3 ms strap hold, preferably until the downloader starts. A slowly rising rail can let EN leave reset before complete rail stabilization; a falling rail can leave C26 charged above VDD+0.3 V, with possible clamp/back-power current. This RC is not a brownout supervisor. Measure actual3V3/EN ramps/dips, discharge, RESET/BOOT/J2 flashing, native USB enumeration/software reset and every retry/handoff condition; do not infer a pass from 20 µs no-load startup.

## Protection, process and release gates

The shared positive-pulse reference is SMF16A 26 V at 7.7 A/10×1000 µs/25°C. It does not bound wiring overshoot, source energy, repetitive/sustained stress or raw voltage across a tripped33 V PPTC. Retained PMOS30 V VDS/±20 V VGS and AP63205≤32 V operating must keep their own margins. Charged26 V protected source and −13.6 V drain give39.6 V differential beyond the PMOS. The switch does not limit upstream TVS current, and PPTC trip time is not a TVS-survival proof.

Source envelope and availability, actual low-current/hot/fast gate clamp, protection energy, current/inrush, both loaded nominal 5 V paths, integrated LDO thermal behavior, EN/reset/programmer behavior, USB/RF, stencil/EP coverage, finished annuli/spacing, assembly/case fit and all appliance behavior remain qualification gates. Native source/BOM/CPL/exports must be independently paired before quotation. No publication, order, physical test or manufacturing release is performed by this cleanup.
