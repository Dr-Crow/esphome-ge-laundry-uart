# Rev2.0 intended resistor purchasing correction

Reviewed October 5, 2026 from `8744a29446a1937134525496c2a5dfdc0a59a004`. This source now records C104108 / RALEC RTT052203FTP for R18/R21 (220 kΩ) and C17673 / UNI-ROYAL 0805W8F4701T5E for R22 (4.7 kΩ), matching its declared values. The [source-bound Rev2.1 recommendation](../../rev2.1/validation/RESISTOR-CATALOG-CORRECTION.md) also applies to these same physical numbered connections and 0805 lands; the later Rev2.2 source identifies these as intended parts.

Only three purchasing-code strings change in each native schematic/PCB file. Resistor values, numerical pin/net mappings, footprints, placements, routes, clearances, outline and existing current CAM remain unchanged. The exact before/after hashes are in [purchasing-code-correction.json](purchasing-code-correction.json). Original archives and their conflicting 200 kΩ/47 kΩ purchasing tables remain preserved, and no installed board is modified.

The selected parts are 0805 ±1%, 125 mW through 70°C with high-temperature derating, and ±100 ppm/°C; use the manufacturer limits and conditional bus analysis in the linked review. This correction is an explicit new procurement choice, not proof of historical fitted values or loaded bus margin.

Rev2.0 still needs a qualified current supplier BOM/CPL, exact D8 identification or a separately reviewed replacement, physical supplier pose, and its distinct supervisor, regulator/current, protection/thermal and appliance qualification. New exact-commit native9.0.9 checks are required; old netlists/reports remain frozen evidence for earlier sources. No missing supplier input is waived or invented here.
