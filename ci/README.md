# Native validation and release gates

This standalone upstream CI candidate covers the four board folders and two legacy
firmware profiles currently present on public main. It builds on standalone CI
`563f5b`, based on public main `bc0d524`. Its generic driver requires real local
source dependencies and keeps native, intended-rule, manufacturing and release
failures visible. It does not add board designs or imply that missing source exists.

The selected standalone Rev3C source candidate is `409dc01`. The separate complete
integration review at `7df3567` combines seven board revisions and eight firmware
profiles, with recovered historical CAD and reviewed A/B/C source packages. Its
seven-board native/manufacturing checks and eight-profile source-bound real build
receipts are separate evidence. Those sources, classic/shared profiles, local models
and rendered assets are absent from this upstream CI change. Combine clean source
packages first, then extend the manifest to the actual new folders and profiles.

```sh
python3 ci/validate.py inventory
python3 ci/validate.py inventory --revision firmware
python3 ci/validate.py hardware --revision rev2.2
python3 ci/validate.py manufacturing --revision rev2.2
python3 ci/validate.py rules --revision rev2.2
python3 ci/validate.py firmware
python3 ci/validate.py release --revision rev2.2
python3 -m unittest discover -s ci -p 'test_*.py'
```

Use genuine KiCad **9.0.9**, its official symbol/footprint/model libraries and ESPHome
**2026.9.1**. CircleCI pins executable/container versions and registry manifest
digests. The CircleCI configuration is byte-identical to `563f5b`; its earlier schema
validation remains the existing evidence. This staging work did not call external
CircleCI validation, execute hosted jobs or start fresh containers. Existing real
legacy firmware builds are source-matched; they were not repeated here. Reports and
logs go to `ci-artifacts/`, retained even when jobs fail. No command flashes hardware,
places orders or publishes a release.

## Independent checks

- Inventory requires every actual revision directory in `ci/manifest.json`. It
  records available CAD and factory-file hashes even when assembly inputs are
  missing. Every declared firmware profile must exist, be unique and have a
  complete local YAML/include closure. Private secrets are excluded.
- One canonical checkout-relative design identity includes native CAD/rules,
  declared project tables, local symbol/footprint libraries, child schematics and
  local STEP/WRL models, including every referenced local model. Native,
  manufacturing, centroid and release evidence use this same closure. Required
  references must exist. Edits and deletions invalidate previous evidence; full
  relative paths prevent collisions between equal filenames in different folders.
- Stock library/model URI names and fixed KiCad 9.0.9 symbols/footprints/models
  commits and container digest are separately pinned in the manifest. Arbitrary
  installed system files are not substituted into source hashes. Release evidence
  must match the external pins too. Referenced legacy model variable names remain
  visible; a declared pin does not prove physical model or supplier qualification.
- Hardware checks use an isolated dependency copy so native project migration
  cannot rewrite committed source. ERC/DRC include all severities; DRC includes
  all-track errors and schematic parity. Every nonzero exit, including warning
  exit 5, fails. Both reports and source-bound exit codes remain available.
- Manufacturing first compares current Gerber/drill/job content with native
  regeneration, removing only creation timestamps. It records CAM identity
  separately from missing supplier assembly data. BOM references, values,
  footprints and purchasing fields must match the schematic; CPL coordinates,
  rotations and sides must match native placements. Archives alone are not CAD
  parity or manufacturing approval.
- A committed, hash-matched `cpl_centroid_policy` can attest exact native geometry
  for specifically listed alternative centroids. Source/anchor/rotation/evidence
  changes invalidate it. Footprint anchors apply to all other references. This
  manifest has no such attestation; this branch does not import another package's
  centroid proof or supplier rotation approval.
- Rules audits exactly the declared native net names, explicit class patterns and
  intended clearances. Sheet-leading slashes matter. A missing audit policy fails;
  configured native DRC and intended-rule coverage remain separate checks.
- Firmware runs both **`esphome config` and `esphome compile`** for each declared
  profile with synthetic credentials in a temporary copy. Results bind profile
  and include hashes. Compile/dependency/network failures stay red; a successful
  compile requires a fresh binary. Configuration validation alone is not a build.
- Release requires separate power, source and physical evidence. Every gate must
  be explicitly passed with committed evidence, its SHA-256, exact canonical
  local source identity and matching external pins. Required native sidecars
  declare `design_rules`; project tables declare `library_tables`. Missing or
  changed dependencies cannot reuse a passed receipt.

## Public-main source remains blocked

Rev1.0 has its historical Gerber archive but no editable CAD or supplier BOM/CPL
in this branch. Its classic ESP32/external-buck architecture, module identity and
ratings are historical context, not qualification. Rev2.0 retains its historical
PCBA archive and prior supplier tables, without current editable source or a
source-matched assembly package. Historical rotations and archive/source pairing
remain unqualified. Every source-dependent check fails explicitly for both folders;
no CAD is reconstructed from factory files.

Rev2.1/Rev2.2 retain public main's unchanged editable source, original factory files
and seven intended Power-net assignments at 0.2 mm. Previous genuine native checks
have unresolved ERC/DRC errors and warnings. Rev2.1 retains the known reset-supervisor
boot-loop issue, historical UART-label concerns, an archive missing the required
native Gerber job, a legacy `LCSC` BOM heading rather than the current `LCSC Part #`
contract, missing Q1 source purchasing metadata and supplier CPL origin disagreements.
Rev2.2's native factory-source parity is independent of its unresolved native,
electrical and physical qualification. These source defects are not repaired or
waived by this CI change. **All twelve release gates remain blocked.**

## Add a revision or profile

When a clean source package is combined, add its actual revision folder and source
stem to schema-1 `ci/manifest.json`, with current source-matched BOM/CPL/archive,
required project tables/rules, intended net names/classes/clearances and explicit
qualification reasons. Keep original historical archives separately as
`historical_archive`; never qualify edited CAD with old factory exports. A genuinely
new dependency or tool version requires fresh evidence for the affected checks.

Declare only existing standalone firmware YAML profiles in `firmware`. Included
package YAMLs are dependency inputs, not standalone build targets. Adding the four
shared C3/C6 and two classic ESP32 profiles requires those source files and a deliberate
six-profile manifest extension. The resulting eight profiles must all have real
compiles and matching profile/include hashes. Previously recorded eight-profile
results belong to the complete integration review, not this two-profile branch.

Do not make public main green by ignoring exit 5, lowering rules, omitting intended
coverage, inventing assembly data or removing gates. Keep missing inputs, native
findings, supplier convention review and physical/electrical qualification distinct.

Official references: [KiCad containers](https://www.kicad.org/download/docker/) and
[CircleCI CLI](https://circleci.com/docs/guides/toolkit/circleci-cli/).
