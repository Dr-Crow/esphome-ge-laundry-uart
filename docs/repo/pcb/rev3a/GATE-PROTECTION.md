# Rev3A source-referenced PMOS gate protection

This source backport preserves both GE inputs and the original automatic PIN1
presence priority. Q3/Q4 remain exact CJ3407 devices. Their source pin2 is now
`PIN*_PROTECTED`; drain pin3 is `PIN*_FUSED`. The source/drain connection repair
and gate network are part of the selected Rev3C protection review. Native CAD
checks do not demonstrate an appliance voltage envelope or physical protection.

| Component | Current source connection / exact selection |
|---|---|
| Q3/Q4 | CJ3407; pin2 protected source, pin3 fused drain, pin1 gate |
| R31/R32 | Original 5.1 kΩ bias resistance, from gate-clamp bias to GND |
| R33/R34 | Original 51 Ω C17738 gate series parts; exact identities retained |
| C18/C19 | Original 100 pF, protected source to gate-clamp bias |
| D16/D17 | MCC BZT52C12-TP/C668891; K1 protected source, A2 gate-clamp bias |
| D18/D19 | SUNMATE SMF16A/C399290, protected source to GND on each branch |

Frozen Rev3A used MBR0540-TP/C78744 Schottky diodes at D16/D17. The reviewed
nominal 12 V zeners replace them; D14/D15 retain their original MBR0540 identities.
The Nexperia C550251 sourcing history belongs to an earlier Rev3C candidate and
is absent from both frozen and current Rev3A.

## What the MCC sheet establishes

The primary-authored [MCC BZT52 sheet, Rev3-4-12012020](https://www.mouser.com/datasheet/2/258/BZT52C2V4_7eBZT52C75_500mW__SOD_123_-2904721.pdf)
characterizes BZT52C12 at 5 mA/25°C: 11.4–12.7 V, Zzt 25 Ω. Zzk is 150 Ω at 1 mA,
with 0.1 µA reverse leakage at 8 V. The 6–10 mV/K temperature coefficient is typical
with unspecified IZTC. The sheet does not supply an identical capacitance or
fast-clamp guarantee to the earlier Nexperia candidate.

At an illustrative 26 V protected source, 12 V clamp and 5.1 kΩ bias, current is
approximately 2.745 mA and zener dissipation 32.9 mW. This is below the 5 mA
characterization point; the stated voltage limits do not establish VGS at that
actual bias. For steady operation, V²/(4R) gives 33.14 mW nominal or 33.47 mW
with R −1%. The 500 mW/25°C rating derates to 100 mW at 125 °C under the datasheet
conditions. Its 250 °C/W thermal reference does not predict this board's thermal
behavior. Low-current, hot, turn-on/removal and fast-edge VGS must be measured.

## Land and polarity screening

MCC page 1 gives SOD-123 body/terminal dimensions and a cathode mark; page 3
provides the dissipation derating. Suggested pads are 0.91×1.22 mm, inner gap
2.36 mm and overall 4.18 mm. The retained native D16/D17 lands are 0.9×1.2 mm,
centres ±1.65 mm, inner gap 2.4 mm and overall 4.2 mm. Terminal/body overlap and K1/A2
polarity were reviewed for the exact part; retaining this geometry does not
establish assembler/tolerance/thermal acceptance. No unreviewed package or
supplier substitution is permitted.

## Whole-chain qualification remains open

The SMF16A 26 V reference is at 7.7 A, 10/1000 µs and 25 °C. It does not bound an
unknown source waveform, wiring overshoot, energy, repetition or sustained
fault. TPS1H200A has a 40 V device limit, while retained PMOS 30 V VDS/±20 V VGS,
AP63205 operating input≤32 V, 33 V PPTC differential voltage and the capacitors
remain independent constraints. A protected source retaining 26 V while its
fused drain steps to −13.6 V produces 39.6 V differential across the PMOS, beyond
its VDS limit. The source/reverse-step envelope must therefore be established.

Both TVSs remain upstream of switch current limiting. PPTC trip timing cannot
serve as a TVS-energy guarantee, and the larger switch rating does not make this
a 40 V carrier. Loaded nominal 5 V operation, current limit/retry, integrated LDO
temperature, reset timing, both-source handoffs and all GE/USB combinations remain
part of [POWER-QUALIFICATION.md](POWER-QUALIFICATION.md). No physical tests ran.
