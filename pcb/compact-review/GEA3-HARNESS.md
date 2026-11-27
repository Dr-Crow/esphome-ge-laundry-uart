# GEA3 harness and logic-level screen

Applies to the as-drawn Rev 3K, 3L and 3M carriers. The nominal 230400-baud GEA3 profile allows 4.34 µs per bit. The design can fail in either direction even when the module monitor shows a clean waveform. First establish the high and low levels, the far-end receiver threshold and the harness load on a representative interface.

## Carrier to appliance, J1 pin 5

With JP4 closed, U5 pin 4 pulls low, and R20 (10 kΩ to +5 V) releases the line high through R24 (1 kΩ). Treat the cable, connector, probe and remote input as one shunt capacitance at J1. A receiver with a 3.5 V threshold, a 5.00 V source and no remote pull-up sees a 200 pF load cross high after **2.649 µs**. Half a bit is **2.170 µs**. Under those assumptions the half-bit capacitance limit is **163.9 pF**, before timing margin. The real appliance's threshold, sampling phase and capacitance are unmeasured.

| External pull-up to 5 V | Capacitance | J1 low with ideal local driver | Time to 3.5 V after release |
| --- | ---: | ---: | ---: |
| None | 100 pF | 0 V | 1.324 µs |
| None | 200 pF | 0 V | 2.649 µs |
| 10 kΩ | 200 pF | 0.455 V | 1.161 µs |
| 4.7 kΩ | 200 pF | 0.877 V | 0.666 µs |

The remote pull-up raises the low level across R24 as it speeds the rise. Actual U5 low voltage, ground offset and cable resistance use up additional margin. A fixture with a strong pull-up can hide a failure that occurs on the real harness. The screen assumes a lumped RC, a fully settled preceding low and a fixed supply. It omits distributed-line effects, clamp conduction and the actual receiver. Use the measured thresholds, noise allowance and sampling point when evaluating bench traces.

## Appliance to carrier, J1 pin 4

R25 (1 kΩ) feeds U4 pin 3. R21 (220 kΩ) weakly pulls that input toward +5 V. A stiff 3.30 V remote high gives about **3.308 V** at the local receiver with nominal values. The fitted Diodes 74LVC2G07W6-7 at 5.00 V requires 3.50 V for a guaranteed high. A 3.3 V remote driver needs qualification. The actual pull-up network, receiver supply, high/low levels, source impedance, temperature and harness ground drop matter. [Diodes 74LVC2G07 datasheet](https://www.diodes.com/datasheet/download/74LVC2G07.pdf)

**Why keep U4 on +5 V for this trial?** Moving its supply to 3.3 V lowers the guaranteed receive-high threshold to 2.0 V, but the second channel shares the same supply and handles GEA2. Its guaranteed low ceiling would fall from 1.5 V at 5.0 V to 0.8 V at 3.3 V. With U5 pin 6 released, a hypothetical 0.60 V at J1 pin 7 and nominal resistors, U4 pin 1 sits between **0.877 and 0.996 V**. Those limits use D9 open and short, respectively, bounding the passive pull-up through R19 and R22. The pull-down is R18 at 220 kΩ and R23 is the 1 kΩ series resistor. This would trade away existing GEA2 low margin. A separate receiver for GEA3 is worth evaluating if actual equipment requires 3.3 V receive-high support. Swapping the common supply or reducing a pull-up across every unit has no established justification.

## Reproduce and qualify

Export each current schematic with KiCad 9.0.9, then run the screen. It verifies the resistor values, receiver and driver supplies, interface pins and link topology on every input netlist before calculating.

```sh
kicad-cli sch export netlist --format kicadxml -o rev3l.xml pcb/rev3l-placement/design/GEA-Adapter-Rev3L.kicad_sch
python3 pcb/compact-review/gea3_harness_screen.py rev3l.xml
```

A qualified reviewer can use an isolated low-voltage fixture to measure J1 and the corresponding receiver with a representative harness, alternating-bit traffic and each module/profile. Record the cable and probe capacitance, pull-ups, supply, actual thresholds, low voltage and timing margin in both directions. For an appliance measurement, first establish the service port's isolation and the instrument grounding arrangement. J7 on K/L is on the module side and cannot establish the voltage or timing seen at J1. Keep USB and appliance harness physically separate during programming. [Module/profile and debug guide](../../firmware/shared-rev3c/README.md)
