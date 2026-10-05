# Legacy purchasing conflicts and release decisions

Reviewed October 5, 2026 against integration `2d5a42c`; the quote-only `f111cd4` preserves these electrical sources. Native checks and source/export parity do not establish catalog correctness. **Rev2.0 and Rev2.1 must not be ordered from their current resistor mappings until the intended values are reviewed.** No part, footprint, population or electrical connection has been changed by this finding.

## Three references with conflicting values

| References | Declared source value | Historical purchasing code | Actual catalog value |
| --- | --- | --- | --- |
| R18, R21 | 220k | [C17539, UNI-ROYAL 0805W8F2003T5E](https://www.lcsc.com/product-detail/C17539.html) | 200k |
| R22 | 4K7 | [C17713, UNI-ROYAL 0805W8F4702T5E](https://www.lcsc.com/product-detail/C17713.html) | 47k |

Rev2.2 and current Rev3A/B/C already select [C104108, RALEC RTT052203FTP](https://www.lcsc.com/product-detail/C104108.html) for the stated 220k at R18/R21 and [C17673, UNI-ROYAL 0805W8F4701T5E](https://www.lcsc.com/product-detail/C17673.html) for 4.7k at R22. This bounded inheritance check covers these three references, not every catalog identity or qualification gate.

## Exact interface roles and conditional effect

Numbered connectivity is the same on Rev2.0 and Rev2.1:

- R18 pulls the node at U4.1, D9.2, R22.2, R23.1 and TP4.1 to GND. R23 reaches appliance half-duplex pin J1.7.
- R21 pulls the U4.3/R25.1/TP6.1 node toward +5V. R25 reaches appliance-transmit/adapter-receive pin J1.4.
- R22 bridges the half-duplex node to U5.6/D9.3/R19.1; R19 is 10k to +5V. R22 parallels the physical D9.2-D9.3 diode section.

At fixed voltage, 200k draws 10% more bias current than 220k. A 47k R22 carries one tenth the current of 4.7k at the same voltage difference. If U5.6 is approximately 0V and the actual D9 section is reverse-biased, R18 in parallel with R22 is 4.602k for the stated source pair, versus 38.057k for the historical catalog pair, about 8.27 times higher. Under those assumptions the passive pull-down is weaker and its capacitive decay takes longer. These calculations do not establish a field failure: appliance pull-ups, diode conduction/leakage, driver state, loading and capacitance still matter. Use the [74LVC2G07 manufacturer thresholds](https://www.diodes.com/datasheet/download/74LVC2G07.pdf) for a complete loaded-interface review.

## Pin labels and regulator identity

The preserved Rev2.0/2.1/2.2 BAV99 symbol calls pins 1/2/3 K/A/K. The [Nexperia BAV99 datasheet](https://assets.nexperia.com/documents/data-sheet/BAV99.pdf) specifies 1=A1, 2=K2, 3=K1/A2. Analyze physical pin numbers, actual diode direction and package orientation together. Stale symbol names do not prove a physical pin reversal; no symbol or routing change is made here.

Rev2.0/2.1 code [C5205181](https://www.lcsc.com/product-detail/C5205181.html) identifies Diodes AP2205-33Y-13. The [manufacturer AP2205 sheet](https://www.diodes.com/datasheet/download/AP2205.pdf) assigns the Y package pin 1 VIN, 2 GND, 3 VOUT, matching the preserved +5V/GND/+3V3 numbered nets. The AP2204R library/datasheet alias conflicts with that purchasing identity. Do not infer a required pin swap or substitute the reverse-pin YR variant. Actual fitted-part, supply/current and thermal qualification remain separate.

## Decisions before supplier completion

Choose the intended legacy network explicitly: retain the declared 220k/4.7k circuit with reviewed matching-value purchasing identities, or review and document the historically coded 200k/47k circuit as an intentional electrical variant. A later mapping change needs updated source/BOM evidence, rating/package review and interface qualification. No substitution is selected by this report.

Rev1 has an [original prose purchasing table](https://github.com/mulcmu/esphome-ge-laundry-uart/blob/87984047ee029efb83bf9947dc21818fd18e39b3/pcb/readme.md), although its recovered package lacks a machine-readable supplier BOM/CPL. Capacitor footprint/value, fuse/supervisor, exact external module/buck and alternative pull-up/pull-down population need review. Mechanical holes/test features must be distinguished from purchased placements; do not fill missing supplier paths with invented identities.

All existing power/source/physical release gates remain blocked. Rev2.1's passing source/export consistency check does not close these catalog conflicts. Supplier pose/rotation, assembly and actual appliance operation also remain unqualified. Use one reviewed power source and keep programmer UART VCC disconnected.
