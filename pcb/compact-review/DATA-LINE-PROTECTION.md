# Data-line power injection and protection choices

The fitted ProTek SRV05-4 (U11, C85364) connects J1.7, J1.5 and J1.4 to its I/O pins 1, 3 and 4 respectively. The upper steering diodes meet at pin 5 on module +5 V. Pin 2 returns to ground. The connector reaches U11 before the 1 kΩ series resistor on each signal. With the module rail unpowered, a driven line can conduct into the rail through U11, bypassing that series resistance. The actual current depends on the remote source, wiring, diode and carrier load. JP3 opens the buck feed. The XIAO USB return and the appliance return still share ground. Keep the appliance harness unplugged during USB programming. [ProTek device and manufacturer datasheet](https://protekdevices.com/products/series-details/?id=5150)

### Candidate comparison

| Candidate | What it would do | Decision |
| --- | --- | --- |
| **TI TPD4E1U06DBVR**, C124691 | Independently clamps four lines to ground. Same signal pin numbers and pin-2 GND. Pin 5 is internally NC and TI permits a VCC connection. Rated 5.5 V working, 0.8 pF typical, ±15 kV IEC contact and air, and 3 A for an 8/20 µs surge. | Single-placement experiment only. Loses the original rail clamp and the ProTek part's advertised 24 A surge capability. Package pitch matches but TI's example land dimensions differ. An experimental variant could route the spare fourth channel on pin 6 to +5 V if the rail and ESD limits check out. JLC lists the genuine TI part as Extended. [TI datasheet](https://www.ti.com/lit/ds/symlink/tpd4e1u06.pdf) · [JLC part](https://jlcpcb.com/partdetail/TexasInstruments-TPD4E1U06DBVR/C124691) |
| **Three Littelfuse SP4021-01FTG** | One unidirectional SOD-323 each, cathode to line and anode to the local connector return. 5 V working, 2.5 pF typical, 25 A for an 8/20 µs surge, ±30 kV IEC contact and air. | Candidate when retaining a comparable per-line surge current matters. Requires three placements, suitable ground returns and a separate decision about the 5 V rail clamp. Vendor current ratings alone do not establish protection at the receiver. No verified savings. [Littelfuse datasheet](https://www.littelfuse.com/assetdocs/tvs-diode-array-sp4021-datasheet?assetguid=836a04c6-f908-434c-8717-46b603bf72d2) |
| **Nexperia PESD5V0S4UD** | Pin 5 is electrically common with GND pin 2. Capacitance is 165 pF typical at zero bias. | Reject for the existing board. It would short module +5 V to ground. The extra capacitance would also consume much of the modeled GEA3 timing budget even after a reroute. [Nexperia datasheet](https://assets.nexperia.com/documents/data-sheet/PESD5V0S4UD.pdf) |
| **Retain ProTek and float REF** | Would disconnect the upper steering rail from the XIAO supply, while retaining the chip's internal TVS. | No-cost topology under investigation. No ProTek qualification for this usage was found in the fitted part's datasheet. Do not use instructions for a different manufacturer's similarly named array as approval. |

### Residual injection through pull-ups

Even with independent clamps, each line still has a resistive path back to module +5 V. With a stiff 5 V source and the carrier rail artificially held at zero, the nominal current screens are:

| J1 signal | Resistive path | Approximate current |
| --- | --- | ---: |
| Pin 4 | R25 + R21, 221 kΩ | 23 µA |
| Pin 5 | R24 + R20, 11 kΩ | 455 µA |
| Pin 7 | R23 + R22 + R19, 15.7 kΩ | 319 µA |

These values require a remote driver or pull-up to supply current. They describe the passive paths with the local driver released and ignore component tolerances and leakage. They are not limits for an assembly with the original U11 conducting. A high-impedance rail can charge from currents this small.

Before enabling any combined-source use, characterize each input line separately and together on an isolated fixture with no USB host attached. Record source impedance, loaded and unloaded carrier rail voltages, currents into module VBUS, and reset behavior with both module variants and with the module absent. Test against agreed interface and protection requirements. Clamp replacement alone does not provide galvanic isolation. [Signal screen](GEA3-HARNESS.md) · [Full fix register](../COMPACT-FIX-REGISTER.md)
