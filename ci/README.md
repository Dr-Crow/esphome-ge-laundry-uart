# Native validation and release gates

CircleCI runs independent jobs for source inventory, native hardware validation,
manufacturing parity, intended netclass assignments, real firmware compiles and
release readiness. Local runs use the same small Python driver:

```sh
python3 ci/validate.py inventory
python3 ci/validate.py hardware --revision rev2.2
python3 ci/validate.py manufacturing --revision rev2.2
python3 ci/validate.py rules --revision rev2.2
python3 ci/validate.py firmware
python3 ci/validate.py release --revision rev2.2
```

Install KiCad **9.0.9**, its official symbol/footprint libraries and ESPHome
**2026.9.1**. The CircleCI configuration pins those container versions and checks
the executable versions. Container tags and immutable manifest digests were
verified against the official Docker registry. Local native checks ran with the
installed official tools; fresh container execution and hosted jobs have not run.
Native reports and command logs go to `ci-artifacts/`
and are retained even when jobs fail. No command flashes hardware, places orders
or publishes a release.

## What each result means

- Inventory records source and factory-file hashes. Every revision directory must
  be declared in `ci/manifest.json`. The current Rev1.0 and Rev2.0 package directories lack editable sources;
  their checks explicitly fail as missing. Historical source recovery and exact
  export provenance review are pending; existing archives do not establish parity.
- Hardware runs native ERC and DRC with all severities and schematic parity.
  Any nonzero exit, including KiCad exit 5 for violations, fails. The project rules
  and existing exclusions are preserved; this does not claim that configured
  native DRC proves intended electrical rules, DFM or physical qualification.
- Manufacturing compares schematic assembly designators and metadata with BOM,
  and verifies CPL coordinates, rotation and side against native PCB exports.
  The archive must match regenerated Gerber, drill and job content from the
  current source. Only creation timestamps are removed before comparison.
  Source or generator-version changes require deliberate export regeneration.
- Rules checks the declared intended net-to-netclass assignments against actual
  native net names and explicit project patterns. Sheet-leading slashes matter.
  This is a bounded coverage audit, not a second DRC implementation: its coverage
  is exactly the net names in `intended_netclasses`.
- Firmware runs `esphome config` and **`esphome compile`** for every declared
  profile. Dummy CI credentials are created in a temporary source copy. Actual
  compile failures and network/dependency failures remain red; configuration
  validation alone does not count as compilation.
- Release checks separate power, source and physical qualification gates. Every
  gate must explicitly be passed and cite a committed evidence file with its
  SHA-256, plus the exact current project/schematic/PCB hashes in `source_sha256`.
  Evidence must be tracked in git and match its committed HEAD contents.
  Source changes invalidate qualification until that evidence is reviewed again.
  Current gates remain blocked. A native or firmware pass is not release
  readiness, permission to order, or evidence of appliance compatibility.

Public main intentionally has blocking results: missing historical sources,
unresolved legacy ERC/DRC findings, Rev2.1 BOM/CPL disagreement, and unclosed
qualification gates. Rev2.2 manufacturing/source parity passes with KiCad 9.0.9.
Do not turn these jobs green by ignoring exit 5, lowering rules or deleting gates.

## Add a revision or profile

Extend the manifest with the revision's source stem, matched BOM/CPL/archive,
explicit intended netclass assignments and reviewed readiness evidence. Declare
only profiles whose files actually exist. Every listed firmware profile is built,
so a prototype overlay must add its four shared profiles rather than reusing old
configuration-only results. Package/include YAML files are dependencies, not
standalone firmware profiles.

New prototype revisions and their qualification state belong in their integration
branch; no unpublished prototype source is implied by this public-main manifest.
Add any genuinely new dependency or tool requirement explicitly. Resolve and
review findings before changing a readiness gate to passed.

The previous public `origin/ci/kicad-validation` configuration supplied the
CircleCI job structure. Its old paths and report-only handling of violations are
replaced here. Official container/CLI references:
[KiCad containers](https://www.kicad.org/download/docker/),
[CircleCI CLI](https://circleci.com/docs/guides/toolkit/circleci-cli/).

Native .kicad_dru files are included in source hashes for inventory, native checks, manufacturing and readiness. A revision using a required sidecar declares its exact path as design_rules; absence fails. Qualification collected before adding or changing rules cannot pass the current source-hash gate. The intended audit also enforces declared netclass clearance values, so lowering a class cannot hide routing errors while leaving its net names assigned correctly.
