# GE appliance adapter project handoff

Updated October 2, 2026. Start with the [comparison](README.md),
[recorded quotes](PRICING.md) and [C6/Matter findings](C6-MATTER.md).
This handoff is a development snapshot; verify branch heads and issue state
before making changes.

## Goal and working preferences

Deliver inexpensive local GE appliance control through the maintained
ESPHome GEA component, with board source, assembly files, understandable
documentation and printable cases. Aim below the $39.99 FirstBuild price,
using comparable complete costs rather than incomplete carrier quotes.
The owner prefers factory assembly and no user soldering.

Keep work in [Dr-Crow's fork](https://github.com/Dr-Crow/esphome-ge-laundry-uart).
Use small, reviewable changes, atomic Conventional Commits and the owner's
GitHub identity. Do not add co-author attribution. Do not open PRs, including
drafts, or contact/post issues on other repositories without the owner's
direction. Prepare PR text and review packages for the owner to submit.
No PCB purchase or payment has been authorized. Terms needed for quoting
were authorized previously; refresh browser/session state without starting
new credential flows unless the owner authorizes them.

Prefer existing KiCad and CI tooling. Avoid checksum manifests and large
custom validation scripts. Explain electrical changes in plain English.
Use bounded delegated work where helpful and review its actual diff and
evidence before accepting it. Separate reported success from verified results.
For implementation, the owner's preferred order is Claude through its local
CLI, then the exact GPT-5.3-Codex-Spark CLI route if available, then Luna;
use a stronger fallback only when needed. Verify availability and capacity,
give workers reasonable time to finish, and do not enable paid API fallback
or change authentication to obtain capacity. Keep final review and integration
with the coordinating session.

## Source checkpoints

| Work | Branch | Source head at handoff |
| --- | --- | --- |
| Rev2.2 and upstream file organization | `main` | `bc0d52495bd97ed1504bd0ca0775e47feb01a648` |
| Rev3A | `design/rev3a-pr` | `a5a9fac87cbcb59d337a1fb8d3084ad18867a3e6` |
| Rev3B | `design/rev3b-pr` | `c5db989810663caa18226a091bfb105ad26fb00e` |
| Rev3C | `design/rev3c-pr` | `38d94d3dc7c41692e3c41710ec33b9f6e0c38b3e` |
| Separate KiCad CI | `ci/kicad-validation` | `1fc11c700a36b154c5f716b9f37f92a1ea1ea421` |
| This comparison and handoff | `docs/revision-comparison` | Documentation branch based on `bc0d524` |

The five hardware/CI checkpoints above were checked against GitHub and had
clean primary worktrees. The fork and upstream `main` both pointed at
`bc0d524`. Rev2.2's [upstream PR 18](https://github.com/mulcmu/esphome-ge-laundry-uart/pull/18)
is merged. No Rev3A/B/C upstream PR was open at the snapshot.

Canonical local checkouts are `/Users/jim/git/esphome-ge-laundry-uart` for
main and `/Users/jim/git/worktrees/esphome-ge-laundry-uart/rev3a-pr`,
`rev3b-pr`, `rev3c-pr`, and `ci-kicad-validation` for the respective branches.
The comparison checkout is alongside them at `revision-comparison`.

## Open tracking issues

- [#2: fork-only KiCad validation](https://github.com/Dr-Crow/esphome-ge-laundry-uart/issues/2)
- [#3: Rev3A](https://github.com/Dr-Crow/esphome-ge-laundry-uart/issues/3)
- [#4: Rev3B](https://github.com/Dr-Crow/esphome-ge-laundry-uart/issues/4)
- [#6: Rev3A finger-button case option](https://github.com/Dr-Crow/esphome-ge-laundry-uart/issues/6)
- [#7: case magnets and antenna options](https://github.com/Dr-Crow/esphome-ge-laundry-uart/issues/7)
- [#8: Rev3C socketed carrier](https://github.com/Dr-Crow/esphome-ge-laundry-uart/issues/8)

These issues are still open. They were read for this handoff, not updated.

## Revision status and remaining work

### Rev2.2

The small board-fix and repository-organization PR is merged upstream.
It retains the original programming arrangement: no USB connector and no
permanently populated J2 header. The proposed user power-selector jumper and
J2 population were dropped to keep this revision small. Do not claim those
features exist. Physical testing remains pending.

Its native PCB preview lacked an RJ45 body and button models on this KiCad
installation. Private visualization copies supplied those bodies and corrected
library paths for the images in this package. The source revision was not
changed. Backport those visualization improvements only after reviewing the
model provenance and project-relative paths. The fuse stand-in is not a
supplier-exact model.

### Rev3A

Routed four-layer ESP32-C3-WROOM-02 design with native USB-C, automatic
appliance pin-1/pin-3 selection, switching 5 V supply, stronger 3.3 V supply,
BOOT/RESET buttons, three LEDs, J2 recovery header and two mounting points.
USB/appliance diode-isolation paths are intended to allow both connections;
that behavior has not been bench-qualified.

The existing source README reports KiCad 9.0.9 ERC with zero errors and
53 reviewed warnings; DRC has zero errors/unconnected/parity findings and
seven reviewed warnings. Do not replace this with a claim of zero warnings.
The standard case and optional captive finger-button lid are checked in;
the optional lid requires local print supports and a physical switch/return
test. These buttons are for reset/recovery rather than ordinary appliance use.

Before PR preparation: update the stale $149.96 estimate to the October 1
$154.44 quote; reconcile case exports currently in the case folder root with
the later `exports/` structure; review the schematic/render package and warning
dispositions; refresh source-base and validation after any change; obtain the
owner's review. Power-input range, startup headroom, transients and thermal
behavior remain prototype tests. The README contains the bench procedure.

### Rev3B

Routed four-layer 99 × 40 mm carrier with a soldered XIAO ESP32-C3, external
antenna, automatic appliance power-pin selection and J2 recovery including
reset. Native ERC/DRC and schematic parity report zero findings on the
accepted source. The case has antenna and magnet variants. A later alignment
fix corrected its BOOT/RESET access holes.

Only one physical power source is supported. Appliance power energizes the
module USB VBUS rail; USB logging while connected to the appliance is not
supported. Use network logs. Do not copy Rev3A's simultaneous-source claim.

The complete assembled quote is blocked by XIAO availability. The $112.08
quote is deliberately without XIAO/antenna/installation. Standard-column
private BOM/CPL copies were needed for JLC upload; review and commit the
appropriate portable formatting fix before release, preserving actual part
selection and placements. Requote complete assembly if this variant is pursued.
Case fit, RF, module sourcing and electrical/thermal testing remain open.

### Rev3C

Derived from Rev3B with two factory-installed seven-pin female sockets and
a separately bought pre-headered XIAO ESP32-C3. Installation needs no user
soldering. Native ERC/DRC and parity report zero findings; the case accounts
for the taller module and socket tails. This is still a review candidate.

J2 retains UART/power/BOOT access, but pin 6 is unconnected; use the module's
RESET button. The carrier's old EN pull-up/link was removed. It has Rev3B's
single-source restriction. The sockets are not keyed; reversed or offset
insertion is not protected and must be addressed in instructions/fit review.

Five assembled carriers cost $114.65; five separate $5.99 C3 modules produce
the $144.60 combined estimate. Physical socket seating, male-header spacer
height, USB/button alignment and resistance to appliance vibration are
unverified. Case checks use a provisional module height envelope.

### Proposed C6 / Rev3D

Research only. The C6 header pattern matches Rev3C's sockets at 2.54 mm pitch
and 15.24 mm row spacing, and its side-header power positions match. GPIO
numbers differ. No electrical qualification, C6 firmware, new case or quote
has been completed.

The next scoped investigation is one shared carrier with separate C3/C6
firmware configurations. Review D8/D9 pulls, every used GPIO and startup
behavior. C6 BOOT is not on its seven-pin side headers, so use its onboard
BOOT/RESET buttons or review an additional physical contact; a header-selector
jumper alone cannot reach it. Preserve current power restrictions until a
different circuit is demonstrated. Read [C6-MATTER.md](C6-MATTER.md) first.

Matter is a separate optional firmware project. Existing C3 supports Matter
over Wi-Fi; C6 adds Thread. Apple/Google native Matter lists do not presently
include ovens/fridges. GE protocol access and real platform behavior must be
verified before promising features. Do not postpone existing hardware for
speculative platform support.

## Validation and file organization

Hardware revision folders follow `pcb/revX/design`, `manufacturing`, `images`
and `validation`. Cases have README/source/exports/images, with the noted
Rev3A exception. Keep diagrams/SVGs in images and user bring-up instructions
in the revision README instead of adding several overlapping guides.

KiCad 9.0.9 is available locally. The native CLI is
`/Applications/KiCad 9/KiCad.app/Contents/MacOS/kicad-cli`. Do not upgrade the
source file format casually. MCP availability must be checked in the next
session; no live MCP connection was verified for this documentation task.

Use native `kicad-cli sch erc` and `kicad-cli pcb drc --schematic-parity`
against the branch being changed. Preserve full reports and distinguish
warnings from errors. Rev3C's CircleCI config validates Rev3B and Rev3C and
exports preview fabrication files. Rev3A currently has no CircleCI config
in its branch; the separate CI branch requires review before integration.
Do not claim a new CI run occurred for this documentation-only package.

After source edits, regenerate schematic PDF, manufacturing files and board
views, and check part/placement agreement and readable schematic layout.
Run each enclosure's checked-in geometry script when changing its CAD and
inspect the actual generated images. Passing software checks does not replace
prototype measurements or assembler placement review.

The comparison's XIAO/connector shapes are simplified and the antenna cable
is omitted. Exact vendor XIAO CAD was not accessible through the linked
GrabCAD page during rendering. Do not describe these images as photographs
or supplier-exact renders. No rejected assembly overlays are included.

## Local work that is not on GitHub

Older temporary/worker worktrees still contain modified PCBs, drafts and
untracked routing artifacts. The release worktrees above are clean; do not
assume every older change is disposable or already merged. Inventory and
compare useful changes against the accepted branches before any consolidation
or deletion. Never reset a dirty worktree to clean it up.

Private quote evidence and review material are under
`/Users/jim/git/review-packages/esphome-ge-laundry-uart-rev3b`,
`esphome-ge-laundry-uart-rev3c`, and `gea-revision-comparison-2026-10-02`.
Those directories also contain unfinished reports, rejected images and
temporary copies; this published package is the curated reference. Do not
bulk-add those directories, credentials, worker transcripts or scratch scripts.

## Suggested next work

1. Refresh GitHub branch/issue state and compare all work against the source
   checkpoints above. Preserve older worktrees while doing that audit.
2. Review the current Rev3C candidate and any unresolved mechanical/power
   decisions before altering its source. Use its existing circuit and case
   rather than restarting the design.
3. If the owner selects shared C3/C6 support, finish the pin/pull/power and
   case audit, then implement and compile separate firmware configurations.
4. Prepare a small hardware PR with matching documentation and a separate
   review bundle: readable schematic PDF, BOM, copper views and populated
   renders. Keep this fork-level comparison/handoff out of the hardware PR
   unless deliberately selected.
5. Refresh quotes only after the intended assembly package is settled.
   Include complete parts/installation and delivered charges where available.
   The owner handles review and purchase decisions.

The owner wanted external PCB review assets, but no Reddit post has been
made. Check the current community posting rules before preparing a final
submission, including any restrictions on assisted design. Do not post or
claim eligibility on the owner's behalf.
