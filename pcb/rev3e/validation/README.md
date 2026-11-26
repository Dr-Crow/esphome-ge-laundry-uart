# Rev 3E validation folder

## as-quoted/

`as-quoted/GERBER-GEA-Adapter-Rev3E-as-quoted-kicad-9.0.2.zip` is the Gerber/drill archive exactly as it was
sent for quote (sha256 `5dee78db...cff2`), produced by KiCad 9.0.2 (Debian build, `9.0.2+dfsg-1`). It is kept as
evidence of what was quoted and is not read by CI. `AS-QUOTED-SHA256SUMS` (paths relative to the repository root)
records the as-quoted source and output hashes.

The CI-checked archive is `../manufacturing/GERBER-GEA-Adapter-Rev3E.zip`, regenerated from the same source with the
pinned KiCad 9.0.9 container by `../manufacturing/generate.py`.

### Why the archive was regenerated: job-file layer-number defect

KiCad 9.0.2 wrote the inner copper layers into `GEA-Adapter-Rev3E-job.gbrjob` as `Copper,L5,Inr` (In1_Cu) and
`Copper,L7,Inr` (In2_Cu). On this 4-layer board they are the 2nd and 3rd copper layers, and 9.0.9 writes them as
`Copper,L2,Inr` and `Copper,L3,Inr`. The job file also carries the 9.0.2 generator version. `ci/validate.py
manufacturing` compares the job file with a fresh native export, so the quoted archive failed with "Gerber job/source
metadata differs".

Nothing else differs. The 13 artwork and drill members (F/B Cu, In1/In2 Cu, F/B Mask, F/B Paste, F/B Silkscreen,
Edge_Cuts, PTH and NPTH drill) are identical between the quoted archive and the 9.0.9 regeneration once the
generator-version and creation-date header lines are ignored (those lines are the only volatile content that
`gerber_content()` in `ci/validate.py` also ignores). Only the `.gbrjob` differs, in its header and the two inner-layer
function labels. The BOM and CPL regenerate byte-identical to the quoted ones
(sha256 `f33a4467...0599f` and `7eb98361...5536`).

### Placement-origin receipt

`placement-origin-review.json` was rebound to the current Rev 3E source hashes (the probe-pad board changed the
`.kicad_pcb` and `.kicad_sch`). The J1 datum (EVERCOM body centre, CPL 8.645, -16.995) is unchanged. The matching
line in `AS-QUOTED-SHA256SUMS` was updated to the new hash.

### Files edited after the quote

`AS-QUOTED-SHA256SUMS` records the files as they were quoted, so it is expected to stop matching any of them that is
edited later. `pcb/rev3e/README.md` was edited after the quote (commit e3ca848: the fee-bearing count corrected to the
8 SMT extended SKUs the quote actually charged). It is documentation only and is not part of the fabrication package.
The design, Gerber archive under `as-quoted/`, BOM and CPL still match their recorded hashes.
