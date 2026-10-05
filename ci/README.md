# Native validation and release gates

This integrated review covers all seven actual board folders (`rev1.0`, `rev2.0`,
`rev2.1`, `rev2.2`, `rev3a`, `rev3b`, `rev3c`) and all eight standalone firmware
profiles. It combines genuine final component histories in a new integration;
it does not reconstruct the omitted original integration commit or its ancestry.
The CI implementation builds on universal candidate
`0d3358af4e732a6e6f5e895d5942ebd1647c79e2`.

```sh
python3 -m unittest discover -s ci -p 'test_*.py'
python3 ci/validate.py inventory
python3 ci/validate.py inventory --revision firmware
python3 ci/validate.py hardware
python3 ci/validate.py manufacturing
python3 ci/validate.py rules
python3 ci/validate.py release
python3 ci/validate.py firmware
```

Use genuine KiCad **9.0.9**, its official pinned libraries and ESPHome
**2026.9.1**. CircleCI pins executable/container versions and registry manifest
digests. Reports and logs go to `ci-artifacts/` and remain available when checks
fail. No command flashes hardware, places orders or publishes a release.

## What each check establishes

- Inventory requires every actual revision directory in the manifest. It records
  native CAD, available factory-file hashes and the complete local source closure
  even when supplier assembly inputs are absent. Every declared firmware profile
  must exist, be unique and have a complete local YAML/include closure; private
  secrets are excluded. A regression also requires every standalone YAML profile
  to be declared; included package files are dependencies, not build targets.
- One canonical checkout-relative design identity includes native CAD/rules,
  project tables, child schematics, local symbol/footprint libraries and every
  referenced local STEP/WRL model. Native, CAM, placement and release checks bind
  to this same closure. Required dependencies must exist; edits or deletions
  invalidate previous evidence. Equal basenames in different folders remain
  distinct. Stock references and official library/model commits are pinned
  separately, without substituting arbitrary system files into source hashes.
- Hardware uses an isolated dependency copy so native project migration cannot
  rewrite committed source. ERC/DRC include all severities; DRC includes all-track
  errors and schematic parity. Every nonzero exit, including violation exit 5,
  fails. Missing tools/reports and infrastructure errors fail too.
- Manufacturing first requires the declared `fabrication_plot` policy to be
  exactly `{"drillshape": 0}` and the native board setting to be 0. Drill markers
  can create positive stencil apertures even when CAM perfectly matches source.
  The native regression regenerates source-matched Rev3C CAM with drillshape 1,
  confirms its unintended 0.35 mm circular paste apertures and successful parity,
  then requires the fabrication guard to reject it.
- Gerber/drill/job content must match native regeneration, removing only creation
  timestamps. CAM identity remains separate from missing supplier assembly data.
  BOM references, values, footprints and purchasing fields must match native
  schematic metadata. CPL coordinates, rotations and sides must match native
  placements or the specific committed, hash-matched centroid policy.
- The current centroid policies cover Rev2.1's legacy pad-bounds convention,
  Rev3A/Rev3B's typed manufacturer/module body datums and Rev3C's typed nominal
  J1 manufacturer body datum. Complete source closure, documentary hashes,
  native part/footprint identity, anchor, rotation, side and local/export geometry
  must match. Stale, missing, unknown or substituted evidence fails. Angles have
  no override. These are geometric conventions, not supplier process approval.
- Rules audit exactly the declared native net names, their explicit memberships
  and intended clearances. Exact sheet-leading slashes matter. Native KiCad 9
  patterns and Rev1's retained explicit legacy class `nets` are both supported;
  automatic/default class selection is not treated as explicit assignment.
  Rev3B/C's unused inherited USB patterns are retained in source; they are not
  claimed as live audited nets. Native DRC and this bounded audit remain separate.
- Firmware requires both `esphome config` and `esphome compile` for each profile,
  using synthetic credentials in a temporary copy. Results bind profile/include
  hashes. A compile requires a fresh binary; config-only, missing dependencies and
  network/tool failures stay red. The exact local ESPHome environment is
  unavailable. Hosted job 47 completed fresh config and compilation for all
  **eight profiles** at published source `2d5a42c`; the
  [hosted receipt](validation/hosted-2d5a42c/REVIEW.json) binds all 22 declared
  input hashes and records 24 factory/OTA/ELF outputs. Test credentials were
  synthetic; no device was flashed or functionally qualified.
- Release requires separate power, source and physical qualification evidence
  for every board: **all 21 gates remain explicitly blocked**. Passed evidence
  must be committed at HEAD, hash-matched, bound to the complete current source
  closure and match external pins. A native/CAM/firmware pass cannot waive gates.

## Explicit unresolved inputs and qualification

Rev1.0 and Rev2.0 now have restored editable historical CAD and current review CAM.
Their original archives remain separately declared as `historical_archive`.
Rev1's original supplier BOM/CPL are absent; Rev2's historical supplier tables and
rotations do not establish a current qualified assembly package. Their inventory
and assembly checks remain red while independently source-matched CAM can pass.
No purchasing data, original archive/source pairing or supplier orientation
approval is invented.

Legacy supply/protection/supervisor and exact module/buck/regulator identities,
supplier library pose/rotation, purchasing identities and physical qualification
remain open. Current Rev2.1/Rev2.2 source and factory files are the reviewed cleaned
packages; historical copies remain separate. Corrected native source does not
close the known Rev2.1 supervisor risk or establish appliance compatibility.

Rev3A/B/C retain the reviewed rated-switch circuits and current source packages.
Exact RJ45 suffix and other purchasing identities, whole-chain transient and
thermal behavior, loaded startup, source capacity, supplier process, antenna/RF,
assembly and enclosure qualification remain open. Rev3C has no default shared
C3/C6 case CAD and no completed physical qualification.

## Verification boundaries

The prior [validator/workflow receipt](validation/VALIDATOR-WORKFLOW-REVIEW.json)
is frozen evidence for the universal four-board/two-profile candidate's bytes and
its October 4 CircleCI schema validation. It does not certify this extended driver,
manifest or its fresh hosted execution. The integrated local review is recorded
separately after the exact final files are checked. CircleCI accepted the current
configuration through its schema validator on October 4; the
[schema receipt](validation/INTEGRATED-CIRCLECI-SCHEMA.json) binds the CLI and
configuration hashes. Hosted native, intended-rule, validator-test and firmware jobs succeeded on
`2d5a42c`. Inventory/manufacturing correctly fail on the two legacy supplier
packages, and all 21 release gates remain blocked. The
[hosted receipt](validation/hosted-2d5a42c/REVIEW.json) separates these results
from physical qualification and the earlier local review.

Do not turn failures green by ignoring native exit codes, lowering rules,
omitting intended coverage, inventing assembly data or removing gates. Add a real
source dependency or tool version deliberately and regenerate affected evidence.
Official references: [KiCad containers](https://www.kicad.org/download/docker/)
and [CircleCI CLI](https://circleci.com/docs/guides/toolkit/circleci-cli/).
