# GE adapter source handoff

Latest October5 pre-order analysis and committed fixes: [all-revision review](preorder-2026-10-05/README.md). Earlier checkpoint/quote/source boundaries below remain explicit.

Updated October 4, 2026 after complete independent-source restoration and fresh seven-revision checks. [Validation](VALIDATION.md), [pricing](PRICING.md) and the [finish plan](FINISH-PLAN.md) form the current review checkpoint. The selected shared Rev3C preserves both GE inputs and automatic PIN1 priority. C3 is first; C6 interface/firmware flexibility remains. The Rev3B rated-protection backport is digitally reviewed; Rev3A rated protection, exact connector lands and zero-warning schematic normalization are independently reviewed and staged; all seven revisions now have zero native findings. C/B pin-type corrections and focused current-main candidates have current source-bound evidence. The [fork integration backup](https://github.com/Dr-Crow/esphome-ge-laundry-uart/tree/integration/ge-restored-final-2026-10-04) is published with intact histories. No order, PR or upstream submission is included.

## Current local checkpoints

The final per-revision, firmware, universal CI and comparison candidates below have complete verified local object/history closure. The new `integration/ge-restored-final-2026-10-04` branch merges those genuine histories; it is separately identified from the unavailable original combined ancestry. Historical development/quote/case hashes below are provenance references and are not all restored local commits. Native counts and remaining gates are in [VALIDATION.md](VALIDATION.md).

| Scope | Exact local commit | Source evidence location in that candidate |
| --- | --- | --- |
| Selected Rev3C with stencil correction and illustrated ordering docs | b87d3e8edc0e078946b980988fd45dc0d3b8e482 | `pcb/rev3c/README.md`, `ORDERING.md`, `validation/` |
| Historical Rev3C 83-reference quote trio | b53cfca83c4433b2288f882439c16e083c1fb50d | Corrected J1 body datum; all 83 exact-code quotes refreshed 04:16 UTC |
| Rev3C original electrical protection source | 7bb455fbc85c748f3125ed091a54375de69fbbcc | Rated-switch proof; historical pre-datum manufacturing trio |
| Historical 80-reference quote baseline | ca1fdb1261af8b32a1bf353d37f40439ead5c3b0 | Matched manufacturing trio; sourcing-only D16/D17 successor |
| Rated Rev3A standalone | 615863d8fcaa2519eb84e77fc0bd7690300a7359 | Zero native findings;97-row supplier BOM/body-CPL/current CAM; rated-source/normalization proofs |
| Rev3A electrical routing freeze | d2bde08da836b493f76de03d330aa0489e2c3419 | Frozen native 0E/9W,97 refs/49-row native BOM; current schematic and supplier serialization are separate corrections |
| Rev3A exact quote trio | a5ab24358e1dae680246f21b50552575e21c8792 | 97 exact refs/42 priced groups; $178.90/5 and $227.86/10 USD; factory files preserved by later schematic cleanup |
| Rated Rev3B current-main candidate |ce2979bc67359f9ed3df14e29a74be1f5acbf455 | `pcb/rev3b/validation/` ; 85 fitted refs; DELAY pin type and typed J1/U2 body datums corrected |
| Rev3B development review |dd9e68fbf28ddf23b93d8350e5f5bd9992fc873e | Independent implementation review; frozen source/manufacturing hashes |
| Restored Rev2.1 final package | 3d98559309d667cf295accef5e77e503f2137b63 | `pcb/rev2.1/` native/manufacturing review |
| Restored Rev2.2 final package | b00c96f301462bf8f4ef4080c6ac2c47d64860bd | `pcb/rev2.2/` native/manufacturing review |
| Restored Rev1.0 final package | 53a4b3d83bfd370090d4a4b509c7e575673a1b17 | `pcb/rev1.0/validation/native-kicad-9.0.9/`, `review-manufacturing/` |
| Restored Rev2.0 final package | 5c8afe467b37c1ab9db24d7db6df55da92727ff8 | `pcb/rev2.0/native-review/`, source-bound current CAM and UART map |
| Rev1 classic profiles | dde0af34e63c3a885cac82a07b3c13265028706a | `firmware/rev1-classic/validation/BUILD-REPORT.md`, `build-evidence.json` |
| Standalone universal CI |0d3358af4e732a6e6f5e895d5942ebd1647c79e2 | CI driver/25 tests, typed body-datum policy and service guide; manifest declares two legacy profiles |
| Prior incomplete integrated checkpoint |7df3567e2785f3937ca9884a226c557eda3318e0 | Eight declared profiles; 356 CAD dependencies; independent review passed |
| Prior incomplete combined checkpoint |f85ba987802aa2071cf68192db627bfdd0c48b2b | All seven strict native checks 0; five modern manufacturing checks pass; legacy assembly/policy gaps and all 21 readiness gates blocked |
| Historical C3-only case reference | 5e01d790abac89fbfa031b8d12f00a0a6ce23dad | `case/rev3c/` unchanged CAD and geometry evidence |

Rev1 implementation is `12f82aa5a4b1241e003749b5584b6e64e7fb5e71`; the earlier `3bb5f85` package contains its frozen recovery receipt; current explicit-power source is `53a4b3d`. Both restored historical packages have independent-review closeout and regenerated source-bound CAM. Original archives remain preserved; Rev1 original BOM/CPL absence and Rev2 supplier rotation approval remain procurement/assembly gates.

Documentation-only selection changes do not requalify electrical files. After any CAD/BOM/CPL change, regenerate affected exports and bind all evidence to the new exact source. Current integrated source and future hosted job URLs must be recorded at publication time; no hosted execution is inferred from this table.

## Public historical sources

These links identify published baseline/history, not the unpublished candidates above.

| Public source | Published checkpoint |
| --- | --- |
| Main / legacy Rev2.1/2.2 | [bc0d524](https://github.com/Dr-Crow/esphome-ge-laundry-uart/tree/bc0d52495bd97ed1504bd0ca0775e47feb01a648) |
| Original Rev3A | [a5a9fac](https://github.com/Dr-Crow/esphome-ge-laundry-uart/tree/a5a9fac87cbcb59d337a1fb8d3084ad18867a3e6) |
| Original Rev3B | [c5db989](https://github.com/Dr-Crow/esphome-ge-laundry-uart/tree/c5db989810663caa18226a091bfb105ad26fb00e) |
| Original Rev3C | [38d94d3](https://github.com/Dr-Crow/esphome-ge-laundry-uart/tree/38d94d3dc7c41692e3c41710ec33b9f6e0c38b3e) |
| Original Rev1.0 editable source | [8798404](https://github.com/Dr-Crow/esphome-ge-laundry-uart/tree/87984047ee029efb83bf9947dc21818fd18e39b3) |
| Original Rev2.0 editable source | [af1f2c4](https://github.com/Dr-Crow/esphome-ge-laundry-uart/tree/af1f2c40029ef67c56910fb2c55feac835553525) |

Retain original archives as provenance. Matching Git blobs or filenames do not establish geometry/CPL approval. Rev1's original ZIP has no BOM/CPL; Rev2's archived/standalone semiconductor rotations have historical differences. Regenerated current CAM is source-bound and independently reviewed; original CAD-to-original-CAM identity and supplier placement approval are not inferred.

## Continue from the selected architecture

Keep Rev3C's 99 × 40 mm outline, sockets/header functions, mounts, JP1 default bridge, both input branches, reverse/gate protection, OR diodes and automatic priority. The selected two 40 V switches do not assign a 40 V rating to the whole carrier. AP63205 buck behavior, source current, module headroom, priority/retry and thermal/transient energy remain physical/electrical gates.

Preserve Rev3A's integrated processor/USB-isolation architecture and Rev3B's soldered-module architecture when evaluating applicable protection backports. Older revisions need their own fixes and profile mappings. Rev2 labels use appliance/programmer perspective; document ESP TX/RX explicitly rather than asserting a blanket swapped-label fault.

Use one reviewed power source and keep UART VCC disconnected. The C3-only legacy case is not a shared default; restore the common-case CAD before fit or actuator work. Per-revision source packages, shared firmware/CI and this documentation stay focused review units, with exact hosted checks only after approved publication. The [finish registry](FINISH-PLAN.md) defines the remaining closeout evidence.
