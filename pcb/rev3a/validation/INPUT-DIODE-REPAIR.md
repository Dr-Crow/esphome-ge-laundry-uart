# Input OR diode rating repair

D14/D15 now select exact STMicroelectronics STPS140Z (`C155662`) instead of MCC MBR0540-TP. Each part is rated 1 A/40 V with 150 °C maximum junction, addressing the former 0.5 A nameplate versus approximately 606 mA programmed switch-limit mismatch. Both appliance input branches and automatic PIN1-presence priority are retained.

The two numbered terminals remain cathode 1/anode 2. Pad centers, sizes, drills, footprints, placements, routes and CPL are unchanged. The existing lands overlap the ST terminals but are not identical to the manufacturer's recommended lands; solder/paste and supplier placement acceptance remain open. The inherited MBR0540 graphical alias remains a generic K1/A2 Schottky drawing; exact instance fields and BOM determine the new part. No old simulation-model assignment is retained.

[ST primary datasheet](https://www.st.com/resource/en/datasheet/stps140z.pdf) gives 0.55 V maximum at 1 A/25 °C and 175 °C/W only with 50 mm² copper. This preserves the existing room-temperature loss screen and supplies no measured or guaranteed hot-board thermal rating. [Part and numerical-source proof](input-diode-part-repair.json) records exact fields, hashes and isolated netlist/BOM checks. Strict KiCad 9.0.9 and manufacturing checks must bind the new commit; historical reports are not a current pass.

PMEG2010ER downstream/USB diodes, CL/retry resistors, fuses, PMOS, regulator and module architectures are unchanged. OEM source/fault energy, startup/RF loads, actual copper/temperatures and physical qualification remain independent gates. No order or powered test has occurred.
