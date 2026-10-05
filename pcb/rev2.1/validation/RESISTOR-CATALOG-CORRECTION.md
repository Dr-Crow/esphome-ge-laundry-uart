# Rev2.1 intended resistor purchasing correction

Reviewed October 5, 2026 from published source `8744a29446a1937134525496c2a5dfdc0a59a004`. This current review package adopts R18/R21 = 220 kΩ and R22 = 4.7 kΩ, retaining the schematic's electrical values and connections. It corrects their purchasing fields and BOM to the matching parts already identified as intended in [the later Rev2.2 source](https://github.com/Dr-Crow/esphome-ge-laundry-uart/blob/bc0d52495bd97ed1504bd0ca0775e47feb01a648/pcb/rev2.2/README.md).

| References | Previous conflicting code | Current reviewed purchasing identity |
| --- | --- | --- |
| R18, R21 | C17539 / 200 kΩ | [C104108](https://www.lcsc.com/product-detail/C104108.html), RALEC RTT052203FTP, 220 kΩ ±1%, 0805 |
| R22 | C17713 / 47 kΩ | [C17673](https://www.lcsc.com/product-detail/C17673.html), UNI-ROYAL 0805W8F4701T5E, 4.7 kΩ ±1%, 0805 |

Both selected series rate 125 mW through 70°C, then derate to zero at 155°C, with ±100 ppm/°C and a 150 V family working-voltage ceiling. The continuous limit also follows √(P×R): at full rated power it is approximately 24.24 V for 4.7 kΩ. These are part limits, not a board-input rating. Primary specifications: [RALEC RTT](https://www.ralec.com/upload/media/product/file/IE-SP-010%20.pdf) and [UNI-ROYAL chip series](https://www.uni-royal.cn/en/images/userfile/file/1769240915c56505e6d9ab55c7.pdf).

The original archives and original purchasing tables are unchanged. Their 200 kΩ/47 kΩ codes remain historical evidence; actual fitted values and an intentional alternate-build rationale are unproven. This correction does not replace resistors on an existing board or claim to recreate its as-built behavior. Rev1's R5 ambiguity is a separate review because its circuit and population options differ.

The source-bound history review found the same conflicting labels/codes in twelve complete-network backup schematics and six source stages. The later Rev2.2 correction changes only these purchasing fields while preserving values and wiring. That supports this explicit new purchasing choice; it does not retroactively establish the original author's intent.

R18 pulls the half-duplex receive node down; R21 biases the full-duplex receive node high; R22 links the transmit sink to the half-duplex receive node. Using physical BAV99 pin numbers, D9 conducts from pin3 toward pin2. When the transmit sink is low and that diode is reverse-biased, the corrected R18∥R22 is about 4.602 kΩ versus 38.057 kΩ for the old coded pair, an 8.27× stronger passive sink. Actual appliance pull-ups, driver voltage, leakage, cable capacitance and rail limits are unknown; no observed fault or guaranteed bus margin is claimed.

The existing 0805 pads, placements, copper, net memberships, rules, outline, CPL and Gerber ZIP are unchanged. [The exact correction receipt](purchasing-code-correction.json) records before/after hashes and preserved original files. The typed placement proof is rebound only for purchasing metadata; new exact-commit KiCad9.0.9/native manufacturing checks must pass before describing the current source as digitally checked. Earlier reports/netlists remain frozen evidence for their recorded sources.

Before release, qualify the 74LVC2G07 input thresholds/slew and actual loaded GEA2/GEA3 bus behavior, along with the separate source/protection/current/thermal/assembly gates. Matching source/BOM codes alone do not establish purchasing availability, supplier pose or physical qualification.
