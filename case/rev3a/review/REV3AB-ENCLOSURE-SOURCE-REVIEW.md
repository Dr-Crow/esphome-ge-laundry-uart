# Rev3A/B recovered enclosure source review

Reviewed 2026-10-05 against committed integration `bf5c2318b4c9ee775c19f7b9327cd1a8fea02d27`, using `git show`, never the parent's dirty worktree. This is a bounded source and geometry screen. No shared-repository edits, installs, order, print, powered operation, or physical qualification occurred.

## Result

Both editable enclosure families are recoverable, with the correct original A/B board families and preserved printable assets. The current integration lacks their directories, but the complete preserved Git mirror retains them. All mounting, connector, LED, and button interface anchors still agree with the current respective boards. The reviewed rated protection packages clear both default case halves at their nominal assembly positions.

A's USB documentation needs a specific dimensional clarification: the 15 x 7 mm number describes the source cutter's X/Y footprint; the outward-facing aperture is **15 x 4.4 mm**, X/Z. That opening is unchanged by closing the lid. No physical opening resize is recommended from the generic six-pin model. Exact SHOU HAN mating-axis Z and selected seated-plug dimensions remain missing.

## Recovery and provenance

- Rev3A source: `refs/remotes/origin/design/rev3a-pr`, commit `a5a9fac87cbcb59d337a1fb8d3084ad18867a3e6`.
- Rev3B source: `refs/remotes/origin/design/rev3b-pr`, commit `c5db989810663caa18226a091bfb105ad26fb00e`.
- Preserved mirror: `ge-rev3-refinement-work/backup-acbcb6c/complete-stage.git`.
- [Recoverability manifest](recoverability-manifest.json): 38 exact original case files, 4,432,228 bytes, with source commit/ref/path, Git blob, SHA-256 and extraction path; both original repository licenses are also retained. Ref targets and every extracted original were byte-reverified.
- Original files are preserved in the complete backup’s genuine source refs. [A source](https://github.com/Dr-Crow/esphome-ge-laundry-uart/tree/a5a9fac87cbcb59d337a1fb8d3084ad18867a3e6/case/rev3a) and [B source](https://github.com/Dr-Crow/esphome-ge-laundry-uart/tree/c5db989810663caa18226a091bfb105ad26fb00e/case/rev3b) retain their original editable CAD/exports; no original geometry is replaced.
- [Pinned baseline manifest](baseline-source-manifest.json) binds current native boards, models and prior review facts. [Primary manifest](primary-source-manifest.json) binds downloaded/cached primary documents. The SHOU HAN RevA PDF was re-fetched byte-identically to its retained primary receipt and visually inspected. The EVERCOM live drawing retrieval failed; its older committed receipt/generator is used with an explicit limit in [retrieval limits](primary-retrieval-limits.json).

## Current board applicability

The native [datum extraction](pcb-datum-extraction.json) and [source-era interface comparison](enclosure-era-interface-comparison.json) establish these anchors in carrier coordinates, X right and Y down:

| Family | Native outline/thickness | Supports | Connectors/module | Buttons and LEDs |
| --- | --- | --- | --- | --- |
| A | 88.7 x 40 x 1.6 mm | H1(4,30), H2(48,4); 3.2 mm drills | J1(13.97,12.555), -90 degrees, left; J2(11.7,32.5); J4(72,36.325), 0 degrees, opens +Y at y40; integrated WROOM U2(81.6,17), -90 degrees | RESET SW1(5,3.4), BOOT SW2(13,3.4); D4(49,24), D5(82.5,1.5), D6(80,36.5) |
| B | 99 x 40 x 1.6 mm | H1(4.5,33), H2(94,35); 3.2 mm drills | J1(13.97,12.55), -90 degrees, left; J2(20,32); soldered, unmodified C3 U2(77.39,4), -90 degrees; official module grid datum(87.89,12.9175); USB faces +X | BOOT0(79,8.4725), RST0(79,17.3625), mapped from official C3 v1.3 source; D4(84,26), D5(84,30), D6(88,26) |

Each listed interface anchor matches the enclosure source-era board. Rated switch/fuse placements differ from those much older sources; they were checked at current coordinates. A's J4 same-part forward land repair changes pads, while retaining its body anchor and orientation. The later STPS140Z metadata repair preserves current SOD123 pads and centers. No B C6 soldered drop-in or socketed C header stack is implied.

A WROOM antenna nominally occupies x88.7..94.7, y8..26, with the retained RF keepout x88.7..99.7, y3..31. The original base cavity ends x100.2; that keepout remains inside the cavity with 0.5 mm nominal clearance at its far end. This is geometric clearance, not installed RF performance.

## Default closed-assembly findings

The independent diagnostic and [receipt](closed-assembly-diagnostic.json) use the existing authorized CAD environment: build123d 0.11.1 and trimesh 5.1.0. No package installation or original export rewrite occurred. This runtime matches B's pins; A originally declares trimesh 4.12.2, so this is a fresh narrow readback, not reproduction of its complete historical pinned test suite.

Both default base/lid pairs are valid single solids. Recovered default STLs are watertight positive volumes. Their STEP bounds match regenerated source within 0.00001 mm, source/STEP volumes agree to floating-point noise, and STEP/STL volume relative differences are below 0.000007. All six LED holes and four tool apertures have zero roof material overlap at their current source datums. Optical visibility and real button actuation remain unqualified.

A case PCB bottom is z3.65 and top z5.25: floor 2.4 + standoff 1.25 + PCB thickness 1.6, counted once. Its roof underside is z19.4. B uses the same board seat/top, with roof underside z18.7.

| Current selected part | Maximum package height above seat | A roof margin | B roof margin |
| --- | ---: | ---: | ---: |
| D14/D15 STPS140Z/C155662 | 1.45 mm, ST SOD123 primary p5 | 12.70 mm | 12.00 mm |
| U9/U10 TPS1H200A | 1.10 mm, retained TI DGN drawing maximum | 13.05 mm | 12.35 mm |
| F1/F2 1812L075/33DR | 1.55 mm, retained Littelfuse maximum | 12.60 mm | 11.90 mm |

All twelve rectangular rated-package screens have zero base/lid overlap at current centers. These are dimensional screens with nominal seating, excluding extra solder lift, and give no thermal rating. A WROOM published maximum 3.35 mm height gives 10.8 mm nominal roof margin. A's historical J2 proxy 11.06 mm leaves 3.09 mm; B's drawing-derived stacked preassembly maximum 9.60 mm leaves 3.85 mm. B's old 4.5 mm module proxy is an assumption, not a complete maximum: its currently placed partial Seeed reference omits RF shield, switches, U.FL and other unresolved bodies.

The retained EVERCOM nominal body transforms to A x-0.38..17.67/y9.4..24.6 and B x-0.38..17.67/y9.395..24.595. Its 11.45 mm nominal body clears both halves. Cable/latch margins remain assumptions. The older A comment/README uses 11.50 mm and says the model is absent, while current source actually includes an 11.45 mm approximate envelope; those are source/provenance wording differences, not a demonstrated height collision.

### A USB opening: supported finding and limits

Source cut: x64.5..79.5, y39..46, z2..6.4. The whole closed assembly is clear across that 15 x 4.4 mm facing aperture. A 15 x 7 mm facing aperture starting z 2 would encounter 136.5 mm3 of base wall. Thus documenting it as a 15 x 7 mm facing cable opening would be inaccurate.

Exact SHOU HAN TYPE-C 16PIN 2MD(073)/C2765186 RevA source confirms body 8.94 x7.35 x3.16 mm, anchor (72,36.325), rotation 0 and face +Y/y40. The drawing's recommended board is 0.8 mm versus retained 1.6 mm. It does not explicitly dimension the mating-axis Z from the installed PCB-top seating plane, so no physical plug-axis clearance is certified here.

The retained STEP internally names a six-pin model. Its raw Z is -2.58..1.581, and native model offset is +2.58. Applied once above case PCBtop 5.25, its diagnostic top is 9.411 mm. A generic-body-height corridor extended from y 40 through the wall intersects 94.215 mm3 of base and 2.756 mm3 of lid. A 3.16 mm exact-body-height corridor assuming the contact-level line is PCBtop intersects 62.893 mm3 of base. These are explicit proxy/conditional-seating observations, not an authenticated physical mating failure, and do not justify adopting the generic model height as the case dimension.

B's retained assumed USB corridor x98..105.2/y2.536..23.125/z4.75..12.25 clears both assembled halves. Its native UBF31-0171 axis/mating depth and selected cable remain unresolved; the generic GCT shell does not supply them.

## Narrow recommendation and remaining inputs

The prepared [documentation-only patch](rev3a-usb-documentation-only.patch), corrected current guide and retained source provenance clarify A's actual opening and exact-part limits while preserving physical source and all exports. No opening resize is proposed for integration.

Needed before a geometry or physical-fit acceptance:

1. A exact 16-pin connector seating/mouth-axis Z on the retained 1.6 mm carrier; selected plug shell/overmold cross-section, insertion depth and seated shoulder coordinates. B needs these same native UBF31-0171 facts at its soldered-module seat, plus an assembled solder stand-off and complete populated-module maxima.
2. Exact fitted EVERCOM full suffix and authenticated tail/body-seat datum, assembled tail/solder protrusion and selected cable/latch swept envelope. The committed manufacturer-derived generator represents 3 mm tails below body seat. If body seat is PCBtop, a 1.6 mm PCB leaves 1.4 mm below its bottom versus A's 1.25 mm floor gap, a conditional 0.15 mm clash. Live drawing retrieval failed, so that datum was not reverified and no tail-pocket edit is recommended from this finding alone. B already reserves 3 mm below carrier bottom with a 0.6 mm floor skin.
3. Actual A switch force/make/overtravel/return with optional 0.20 mm captive sliders; B factory switch identity/released height and tool access. Retainer contact, print shrink/tolerances, snap fatigue and magnet captivity/holding force remain untested.
4. LED emission/visibility, antenna identity and routed coax/mating U.FL clearance, FPC/bulkhead seating and closed-case RF/thermal measurements. Partial STEP omissions are not zero-height or clearance proof.

These are recoverable A/B prototypes with specific qualification inputs. They are not missing designs and do not inherit C6 or socketed-C geometry. Historical Rev1/2.x files remain outside this review.
