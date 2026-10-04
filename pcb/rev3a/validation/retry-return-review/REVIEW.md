# Bounded native routing-peer review, 2026-10-04

The copied source PCB is SHA256 `0194bda407f1d2323738b68d1455d265475d19e1af1f6bb2bd0fefbf4e93e515`; before/copy/after source hashes match. This is a scratch proposal review, not an applied/final manufacturing result.

## R42 retry escape

Accept the one guided diagonal shift of the prior proposal's via to (58.75,33.2). R42 position, exact part, pin nets and own-VS main contact remain unchanged. Add .2 mm F.Cu from R42.2 (57.9125,33.25) to (58.75,33.2), a .7/.3 mm through-via there, and three .2 mm In1.Cu segments to (58.75,35.55), (61.4,35.55), then the existing DELAY via (61.4,28.55). No removal. The .20 mm annulus/.30 mm drill remain within existing constraints.

Fresh native9.0.9 reload/refill plus all-track/schematic-parity DRC gives **0 errors/3 unconnected/0 parity/36 warnings**. Proposal PCB SHA256 `dc156e9bd11345c74f29efe3cd526017c18f99f08b7d8ca09956c67e7d629fe3`.

Native nominal hole-to-R42.2-paste improves from .075 to **.175 mm**. Other-net via gaps: V_INPUT F.Cu .277683 mm (Power .25), PIN3_GATE In2.Cu .350000 mm (Default .20), actual finite D6 B.Cu .411864 mm. Nearest other drilled hole gap1.284778 mm. This is nominal geometry; tenting defaults and zero mask expansion do not prove finished-hole, mask registration, paste printing, placement, reflow or assembly reliability.

The exact same three inner link segments fail on B.Cu (3 errors: D6/R10) and In2.Cu (3 errors: Gate/D6); these are two fixed layer comparisons, no broad search. In1 introduces an explicit GND-plane slot: meaningful removed9.9599153757115 mm², bbox(58.0995,28.996547)–(61.944109,35.9505). In1 filled component count1→1 does not mean unchanged local reference paths. The new via removes2.017662606264821 mm² of local In2 ground. F/B meaningful removed fill is zero. Raw Boolean differences include <1e-6 mm² numerical retessellation polygons elsewhere; raw polygon records are preserved, and the projection screen excludes only those negligible slivers.

Projection against original native copper finds0 USBData crossings,0 Switching crossings,0 RF-rule-area intersections, and11 other original items across the meaningful slot (PIN3_GATE/SW_OUT, V_INPUT, D6/R10). Their reference-return qualification remains open. No USB/RF/thermal/boot physical pass is claimed.

## R31 isolated front ground contact

Accept a .8/.4 mm GND through-via at (50.2,7.8), plus .5 mm F.Cu GND spur from the existing endpoint (50.9,7.8) to (50.2,7.8). No removal/move/rule change. Native refill/all-track/parity gives **0 errors/3 unconnected/0 parity/37 warnings** from baseline4 unconnected: the R31 island is connected. Scratch PCB SHA256 `bb2c20a4a91a2ddbaa1d38d93a3b14c2041e1c162a1e34d27387a0836fa058b0`. Near other-net via gap is PIN1_PROTECTED In2 .400000 mm (Power .25); nearest nominal drill-to-paste1.175 mm.

Rejected exact probes: R31 (49.7,9.25) coincides with protected-main copper and normalizes its intended GND via to PROTECTED during refill, leaving the island open. R31 (50.9,7.8) hits the PROTECTED In2 diagonal. R32 (48.1,31) connects ground but shorts original R10 B.Cu and leaves.043907 mm to GEA2_RX; it is rejected. No rejected probe touched active source.

Files: proposal.json, drc.json, via-geometry.json, fill-delta.json, return-plane-review.json, R42-B-drc.json, R42-IN2-drc.json; r31-ground-shift-proposal.json, r31-shift-drc.json, r31-via-geometry.json. Active-source integration and final export/hash review still await the writer/owner.

## Correction to unvalidated R32 orientation guidance

A later rough90° same-center R32 suggestion was independently tested by the writer's bounded helper and rejected before source. Original FullTx via72d14ea3 at(50.1635,32.7746) and its original front strip were omitted from that rough screen. They are present unchanged in both source0194bda4 and source07338030. The proposed ground-via location(50.2,32.75) overlaps that retained drilled hole; the rotated pads/spur also conflict with original front FullTx copper, and the rotated GateClamp pad leaves.175 mm to PROTECTED under Power.25. My initial interpretation that a newer fused-area detour caused this obstacle was incorrect. No90° R32 geometry was approved or applied, and no further broad search was performed here. Exact rejected check is /workspace/shared/ge-oct3-rev3a-rated-proof/r32-rotation-check/summary.json.
