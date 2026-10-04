# Historical pre-backport source review

This audit describes frozen Rev3B `0b957ba996e7e7a86f8776c9289b6cfb634421ee` before the rated-protection backport. Its counts and electrical part statements are historical. Current source evidence is [rated-protection-proof.json](rated-protection-proof.json); see [RATED-PROTECTION.md](../RATED-PROTECTION.md) and [POWER-QUALIFICATION.md](../POWER-QUALIFICATION.md).

# Rev3B source and export review

Review date: 3 October 2026 UTC. Baseline: `c5db989810663caa18226a091bfb105ad26fb00e` (the verified `origin/design/rev3b-pr` head). Reviewed editable source: `498a8a90901ef5dbb1b778c16f3e59c5b35dbdc6` on `fix/rev3b-reviewed-source`. This remains an unqualified dual-input design candidate. No ordering, publishing, appliance connection or physical testing was performed.

## Native checks and rule coverage

Native KiCad **9.0.9**, with the matching 9.0.9 symbol and footprint libraries, was used for both runs. PCB flags were `--severity-all --all-track-errors --schematic-parity`; ERC used `--severity-all`.

| Result | Baseline | Reviewed source |
| --- | ---: | ---: |
| ERC errors / warnings / exclusions | 0 / 0 / 0 | 0 / 0 / 0 |
| DRC errors / warnings / exclusions | 0 / 0 / 0 | 0 / 0 / 0 |
| Unconnected items | 0 | 0 |
| Schematic-to-board parity issues | 0 | 0 |
| Populated BOM references | 82 | 82 |
| Populated CPL references | 82 | 82 |

The configured DRC pass also covers the intended currently named Power and Switching nets. All 13 live Power patterns and both Switching patterns match the actual board names, including `/PIN1_*`, `/PIN3_*`, `/V_INPUT`, `/ALT_PWR`, `/5V_IN`, `/BUCK_5V`, `/BUCK_BST` and `/BUCK_SW`. There is **no hierarchy-prefix mismatch** to correct in this Rev3B source. Power clearance remains 0.25 mm and Switching clearance remains 0.30 mm. Eight USBData/USBPower patterns match no board net after the XIAO migration; they do not relax these live power rules. No netclass, rule value, severity or exclusion was changed.

`--severity-all` includes configured errors, warnings and exclusions; it does not enable checks whose project severity is `ignore`. Existing ignored PCB checks are footprint filters, missing courtyards and PTH/NPTH inside courtyards. A separate source inventory found courtyard graphics on all 99 placed footprints. That inventory is not a mechanical qualification or a substitute for enabling every optional DRC check. ERC is a connectivity check, not a component-rating or power-budget analysis.

## Narrow source corrections

- U2's placed and local XIAO courtyards followed `x=0..17.8 mm`, omitting the retained official land-pattern extremes `x=-0.54..18.375 mm`. The reviewed rectangle is `x=-0.79..18.63 mm`, `y=-23.05..0.25 mm`: at least 0.25 mm around body/lands and 0.5 mm beyond the nominal USB-shell front. The [footprint source notes](../design/footprints/SOURCE.md) bind the geometry and [KiCad courtyard convention](https://klc.kicad.org/footprint/f5/f5.3/). Cable approach and physical module installation remain open.
- J3 remains the DNP schematic alternate excluded from both PCB and BOM; its copied description now identifies Rev3B's populated J2 correctly.
- The saved board plot option now disables drill-center markers. The previous manufacturing archive contained 0.35 mm marker flashes on every Gerber layer. The regenerated files remove only those markers: 106 on each of the four copper layers and 12 on each of the seven other plotted layers. Comparison after removing timestamps and that exact terminal marker block found every remaining Gerber command identical. PTH and NPTH drill files match after timestamp removal. This avoids unintended marker apertures on paste, mask, silkscreen and outline plots.

Pads, nets, tracks, vias, fills, component locations, models, outline and the dual-input topology are preserved. Both original appliance inputs and the automatic selection circuitry remain present.

## Export and part consistency

Gerbers, separate PTH/NPTH Excellon drills, native BOM/CPL, schematic PDF, four copper SVGs and three native 3D views were regenerated or reproduced from the reviewed source. The final archive contains the same 15 file roles as the previous package: 11 Gerbers, one Gerber job, two drill files and a drill report. The [manifest](source-artifact-manifest.json) records the editable-source and distributed-artifact hashes.

All 82 populated BOM references have the same value, footprint, LCSC part, MPN and manufacturer as the baseline. All 82 CPL rows preserve the exact native positions, rotation and top-side placement. The later metadata normalization labels the native Ref/PosX/PosY/Rot/Side columns as JLCPCB Designator/Mid X/Mid Y/Rotation/Layer and normalizes top to Top. Native Val and Package columns are omitted from CPL; those exact values and full footprint identifiers remain in the BOM. No placement or source geometry changes. The schematic netlist contains 100 component references; J3 is intentionally excluded from the PCB, leaving 99 placed footprints. DNP/test/mounting items excluded from assembly explain the remainder. Native parity reports zero mismatches. Assembly polarity, supplied part variants, module underside soldering and actual reflow results still need verification.

The models for XIAO, RJ45 and J2 are approximate review envelopes/drawing models, not proof of seating or enclosure fit. Regenerated renders provide source review views only.

## Electrical release gates

These independent inherited gates remain open even though configured native checks pass. Rating comparisons identify a coordination problem to resolve; they do not establish that field failure is inevitable.

1. **PIN1 transient coordination.** D18 is Sunmate SMF16A on `/PIN1_PROTECTED`. The exact manufacturer-authored [SMF table](https://jlcpcb.com/api/file/downloadByFileSystemAccessId/8757789523080564736), page 2, specifies 16 V standoff, 17.8–19.7 V breakdown and 26 V maximum clamp at **7.7 A** for the 10/1000 µs rating condition. U9's VIN and EN connect to that rail. [TI TPS22810 Rev C](https://www.ti.com/lit/ds/symlink/tps22810.pdf), section 7, specifies an 18 V recommended maximum and 20 V absolute maximum for VIN/EN. Actual stress depends on source waveform, impedance, TVS current, temperature/tolerance and layout overshoot. Define and test that envelope or change the protection design before release; the TVS is not active sustained-overvoltage cutoff.
2. **PMOS orientation and gate stress.** Q3/Q4 are CJ3407, pin 1 gate, 2 source, 3 drain. The source pins connect to `/PIN1_FUSED` and `/PIN3_FUSED`; drains connect to the downstream protected rails. Review this source-upstream body-diode orientation for required reverse-input and reverse-current behavior. D16/D17 and resistors pull the gate toward circuit ground, rather than providing a gate-to-source Zener clamp. [Changjing's CJ3407 datasheet](https://www.jscj-elec.com/pdf/f3fb09e55afae446e8a8f8a35ab44e62.pdf), page 1, specifies ±20 V VGS absolute maximum and -30 V VDS. The source-side fuse does not set a safe VGS ceiling, and the downstream TVS does not establish source/gate safety. Bound positive and negative stress, current and fault duration, then approve the circuit orientation and clamp behavior.
3. **PIN3 protection and low-voltage path.** `/PIN3_PROTECTED` supplies U10 VIN without a corresponding D18 TVS. U10 still has the 18 V / 20 V limits. Both source branches feed `/V_INPUT` through output Schottkys and then the AP63205 5 V buck; D11 adds a further drop to the module's 5 V input. [The AP63205 datasheet](https://www.diodes.com/datasheet/download/AP63200-AP63201-AP63203-AP63205.pdf) describes buck operation; it cannot raise a low input to a regulated 5 V output. A nominal 5 V PIN3 source plus path loss is therefore an unresolved loaded-startup/regulation case. Verify the actual model's PIN3 supply and required module rail, then choose and qualify the power architecture.
4. **Source current, startup and thermal budget.** No reviewed OEM source allowance establishes continuous or pulse current for the intended appliance. F1/F2's 0.75 A PPTC hold rating and U8's 2 A nominal capability do not provide an appliance current budget. Bound module/Wi-Fi bursts, capacitor inrush, fuse hot resistance, diode loss, buck/inductor heating, cold/hot restart and brownout. Validate model-specific pin mapping, grounding/isolation and transient energy before appliance use.

Keep only one external supply physically connected. USB and appliance input share the module VBUS rail and can backfeed; J2 requires its own qualified regulated 5 V source with 3.3 V UART logic. Module 3V3 is output only. Physical fit, RF performance, firmware/application behavior and assembled-board bring-up remain release gates.
