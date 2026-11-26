# Audit and integration review, 2026-11-26 (Claude)

This records an independent audit of the work pushed on 2026-11-25/26 (Rev 3E quote docs, the as-quoted Rev 3E, Rev 3F
and Rev 3G), what was changed on `integration/review-2026-11-26` as a result, and what is still open. Every commit on that
branch has a "Why:" paragraph with the reason and the verification. Numbers below were re-run with the pinned
`kicad/kicad:9.0.9@sha256:e638b79b…a37729` container unless marked otherwise.

## Branch layout

`integration/review-2026-11-26` starts from `design/rev3g-service-prototype` (which already contains Rev 3F and the
quote docs) and merges `design/rev3e-as-quoted`. On top of that it adds the commits below. Nothing on the source branches
was rewritten.

## What the audit verified

- **Rev 3E as-quoted** (`9102917`): board, schematic, project, rules, Gerber zip, BOM and CPL hash-match the quote's
  recorded identities. ERC 0, DRC 0/0/0.
- **Rev 3F**: ERC 0, DRC 0/0/0 (fills current); the 8 bypass-cap swaps are exactly as described and all on +3V3/+5V;
  16 In2 segments widened; U9/U10 paste 81.8 % of land with copper unchanged; BOM 69 / 31 SKUs; CPL byte-identical to
  Rev 3E's; SHA256SUMS all match; Gerbers regenerate identically. Rev 3F vs the as-quoted Rev 3E: same 93 parts and
  55 nets, only the 8 capacitors' fields differ.
- **Rev 3G**: ERC 0, DRC 0/0/0 (also after a forced refill); with JP3/JP4 closed the netlist equals Rev 3F's; BOM/CPL =
  Rev 3F minus R47; SHA256SUMS 59/59; its case copy includes the mirror fix (c4cdec5); no part collides with the shipped
  lids/base; the USB wall is 2.032 mm over 240 rays; the 2.94 mm³ C6 overlap is with the conservative probe box only;
  the JP3 0.6 mm bridge is ~2 mΩ and rated ~1.6 A.
- **Quote docs**: every dollar total, break-even and half-ounce projection recomputes; OVLO 18.85 V; copper-resistance
  arithmetic; the YAGEO 50 V 0603 parts are fine on the 3.3/5 V rails.

## Findings and what was done

| # | Severity | Finding | Action (commit) |
|---|---|---|---|
| 1 | risk | The quoted board was not in git | Fixed upstream by `design/rev3e-as-quoted`; merged (119976e) |
| 2 | risk | The quoted Gerber job file (KiCad 9.0.2) labels the inner layers `Copper,L5,Inr` / `Copper,L7,Inr` on a 4-layer board; artwork identical to a 9.0.9 regeneration | Regenerated with 9.0.9; quoted zip archived unchanged in `pcb/rev3e/validation/as-quoted/` (90cd0c8) |
| 3 | risk | As-quoted placement-origin receipt not rebound; CI manufacturing failed | Rebound (90cd0c8) |
| 4 | error | Rev 3F and 3G not in `ci/manifest.json`; CI inventory red | Registered with generated manufacturing sets whose BOM/CPL are byte-identical to the review CSVs (6fe74f2, dc33693, e3b8b3c) |
| 5 | doc | Fee ledger listed J1, J5/J6 (through-hole) and U11 (preferred) and omitted C16/C17. The quote's 8 × $3.09 is exactly the 8 SMT extended SKUs | Corrected (fb0662e, e3ca848) |
| 6 | doc | Two copper-thickness bases (35/17.5 µm vs 30.48/15.24 µm) give 29.3 vs 33.7 mΩ for the same trace | Each Rev 3E doc states its basis (fb0662e) |
| 7 | doc | PIN1 turn-on shown only as the 4.254 V stacked corner; nominal is ~4.08 V | Both stated (fb0662e) |
| 8 | risk | 19 V OVLO sweep had no source limit; SMF17A conducts near 18.9 V | ~100 mA, ~1 s steps (bf298e5) |
| 9 | risk/doc | Stencil table omitted the 0.25 mm eFuse corner pads (area ratio 0.62 even at 0.10 mm foil) | Row added (bf298e5) |
| 10 | doc | "TP16 is TVS return" (it is beside U11, the data-line ESD array); TP5 meaning with JP4 open; In2 GND under the JP4 bridge; 1 oz inner copper exists only in prose | Reworded / noted (bf298e5) |
| 11 | risk | Through-hole tails: the base leaves 1.25 mm under the PCB; a JP3 header (Rev 3G) and J7 (Rev 3H) have ~3 mm tails | Base tail pockets, 3.5 mm free, 1.15 mm floor (3b744a5); Rev 3H base in `pcb/rev3h/case` |
| 12 | risk (low) | Rev 3G via at (29.1, 22.9) straddles the exposed JP4.1 land edge | Moved in Rev 3H to (31.5, 23.0), 0.78 mm clear (9617dee); Rev 3G left as built |
| 13 | doc | `pcb/README.md` had no rows for Rev 3D–3H | Added (bf298e5) |
| 14 | — | Correction to earlier Claude work: the Rev 3E README overstated SRV05-4 protection (REF ties to +5 V, so it is a shunt clamp, not rail isolation); fixed upstream in the as-quoted README | Kept |

## New work on the branch

- **Rev 3H** (merged 90155a9, fixes 9617dee, bffd986): Rev 3G plus the J7 3.3 V listen-only GEA bus monitor header
  (GEA2_RX, GEA3_TX appliance→module, GEA3_RX module→appliance, each through 1 kΩ R48–R50) and C16/C17 moved to the basic
  C12891 (one fewer $3.09 fee). C9 stays X7R as the quote review recommends. ERC 0, DRC 0/0/0; CI registered (4d8cb8c).
  See `pcb/rev3h/README.md`.
- **Case**: the larger C3/C6 roof label and module tag (fa9814b), pin-tail pockets and the closed-USB lid option in
  the main case source (3b744a5).
- **Review hub** in `tools/review-hub` (88ed23b, d71fab8): portable build, private notes excluded from public builds,
  `pages.sh` for GitHub Pages.

## Still open

- Nothing has been built, powered or bench-tested; every release gate stays blocked.
- `.kicad_pro` mask/annular DRC rules are zero on Rev 3E–3H, so DRC does not check JP3/JP4 mask openings; rely on the
  fab DFM check.
- 0.24 mm axial slack between the XIAO envelope and the Rev 3G closed USB wall: print a coupon.
- Magnets vs tail pockets: the corner magnet at (70, 38.5) overlaps JP3, and 8×2/10×2 magnets limit J7 pin 4 to
  1.75 mm. With magnets, trim JP3/J7 tails or move the magnets (not changed).
- C16/C17 X5R effective capacitance (~25 µF estimated) and the J7 tap loading are unmeasured.
- The quote itself is transcribed; no quote PDF or screenshot is in the repo.
