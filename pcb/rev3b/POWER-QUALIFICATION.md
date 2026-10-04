# Rev3B loaded-power qualification gates

The rated-protection backport preserves both original GE input branches, original automatic PIN1-presence priority, the AP63205 buck, D14/D15 input OR, D11 buck-output isolation and soldered Seeed XIAO ESP32-C3. It has no C6 compatibility claim or new simultaneous-source protection. Native CAD passes are not appliance qualification. The intended nominal5/7.5/9/13.6 V examples remain; no narrower source envelope or fault-aware fallback is introduced.

## B's actual module supply path

U2 remains exact Seeed113991054 / C18212168, XIAO ESP32-C3. Its retained carrier footprint follows the official22-pad v1.3 drawing. The [Seeed v1.3 schematic, Jan15 2026](https://files.seeedstudio.com/wiki/XIAO_WiFi/Resources/XIAO_ESP32C3_v1.3_SCH_260116.pdf), sheet3/3, shows carrier+5V into VUSB, then moduleF1 marked6 V/500 mA, internalD1 MSK4005, and TLV75733PDBVR. Its VIN node has C1/C3 2.2 µF each; outputC23 is2.2 µF plus SoC decoupling. Carrier D11 PMEG2010ER is an additional series drop ahead of the module. The carrier leaves battery pad21 unconnected.

This is evidence for the version-specific module comparison; exact installed hardware must be verified. No LDO is substituted. Module fuse/internal diode, charger/USB coexistence, TLV input/current/thermal behavior and loaded 3V3 need measurement together. [TI TLV757P Rev C, March2024](https://www.ti.com/lit/ds/symlink/tlv757p.pdf) gives DBV3.3 V dropout maximum425 mV at1 A/TJ≤85°C and475 mV atTJ≤125°C; guaranteed interpolation to364 mA is unavailable. Its JEDECθJA231.1°C/W is not a prediction for this module. Die current rating is not an assembled-module/current-source budget.

[Seeed's guide](https://wiki.seeedstudio.com/XIAO_ESP32C3_Getting_Started/) calls VIN5 V. Its500 mA output table row comes from a3.8 V battery/3 A source test; it does not prove nominal5 V loaded startup through this carrier. Module EN has10 kΩ/100 nF and carrier pull-up remains. Verify actual stabilization≥50 µs, resets, RF bursts and success within the switch's35–45 ms retry attempt.

## Current, inrush and low-input margin

TPS1H200A with exact3.3 kΩ ±1% CL gives provisional0.606 A nominal and conditional0.510–0.704 A; VS−OUT≥2.5 V accuracy and temperature drift matter. This setting does not establish OEM allowance, converter input current or permitted continuous diode/PPTC/module load. Its own-VS100 kΩ DELAY configuration replaces the original22 nF CT ramp; continuous limiting gives35–45 ms on/0.8–1.2 s off, with thermal interruption able to shorten an attempt.

A deliberately mixed-condition 5 V screen gives 5−0.323−0.55−0.34 =3.787 V before unfilled buck and internal-module losses. Using the TLV1 A/≤85°C maximum425 mV dropout row only as a screening reference leaves62 mV, or29 mV with a1% high-setpoint reserve, for all unfilled buck/module fuse/module diode/PCB losses. No guaranteed364 mA dropout interpolation exists, so this flags measurement urgency rather than a B pass/fail. The conditional extra4.915 mA active-supply comparison flows through fuse and PMOS before VS, not the switch channel; with0.400+0.087 Ω it adds about2.394 mV under unmatched source conditions.

Both PIN1-only and PIN3-only nominal5 V cold starts remain explicit gates. An illustrative86 mV additional protection-path drop at364 mA reduces buck/dropout headroom upstream of the buck. Conditional active switch supply current can be as high as5 mA under TI's stated13.5 V/5 V/0.5 A test conditions. D14/D15, AP63205 dropout/inductor/current, D11 and unknown internal module drops remain to be measured. A buck cannot restore missing low-input headroom or source power. Include effective capacitors/DC bias, converter startup,44 µF buck output, carrier/module capacitance, RF demand and source impedance in the startup budget. Local switch VS must stay above the maximum4 V restart threshold.

## Required controlled qualification

1. Establish exact appliance model/pin map, loaded supply tolerance, continuous and peak current allowance, source impedance and positive/negative waveforms. Nominal voltage examples are not universal GE specifications.
2. Bound raw/protected nodes, PMOS VDS/VGS, switch/control pins,33 V PPTC differential,32 V buck operating limit, TVS pulse energy/repetition and sustained overvoltage. SMF16A26 V at7.7 A/10/1000 µs/25°C is a conditional table point. Charged26 V source plus−13.6 V drain can exceed retained30 V PMOS VDS; upstream TVS energy is not limited by switch CL.
3. On an isolated bench with reviewed source bounds, measure each input alone and both inputs, priority, weak PIN1 inhibition, removal/recovery, startup/inrush, brownout, actual module5V/3V3 and bus levels through cold/hot starts and RF bursts. Do not reduce the intended input specification to force a pass.
4. Reconcile measured draw with OEM allowance and enclosed hot PPTC hold, D14/D15 duty/thermal limits, converter loss and module/internal regulator temperatures. Verify actual startup completes within retry attempts without repeated resets.
5. Qualify MCC low-current/hot clamp, actual fast VGS/Miller peaks and gate-network temperatures. Its softer25/150 Ω impedance, typical coefficient and unbounded comparable capacitance are distinct from the former Nexperia selection.
6. Approve vendor lands/local same-switch0.20 mm pad rule for the real environment, final stencil,≥85% EP solder coverage and thermal process. Confirm component/connector/module seating, unchanged case USB/button/LED access and RF with physical hardware. Recheck exact85-part BOM stock, process fees and module/antenna assembly before any approved order.

Only one supply may be physically connected at a time: USB, appliance or regulated5 V recoveryJ2. The XIAO VUSB/USB VBUS remains directly on carrier+5V and simultaneous sources can backfeed a computer. D11 isolates the buck; it does not protect a USB host. Never inject power into the module's3V3 output. No battery is included.

No physical appliance test, thermal qualification, order, publication or quote revision is performed. See [RATED-PROTECTION.md](RATED-PROTECTION.md), [GATE-PROTECTION.md](GATE-PROTECTION.md) and [native proof](validation/rated-protection-proof.json).
