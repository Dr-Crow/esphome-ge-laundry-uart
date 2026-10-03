# GE adapter engineering handoff

Updated October 3, 2026. Start with [validation and decisions](VALIDATION.md),
[comparison](README.md), [historical pricing](PRICING.md) and
[shared C3/C6 findings](C6-MATTER.md). This is a source/review checkpoint,
not a fabrication or appliance qualification.

## Required Rev3C direction

Use the original public dual-input Rev3C as the starting point. Preserve BOTH
appliance PIN1 and PIN3 power paths and automatic selection/PIN1 priority.
Cost matters within that functionality. The PIN1-only experiment is rejected
and archived; its files and passing digital checks remain historical evidence.
Do not rebuild the new circuit from its input deletions or replace automatic
behavior with a factory/manual mode.

C3 is the first target while shared C6 firmware, GPIO/header compatibility,
antenna clearance and future common-case access remain goals. Keep the 99×40 mm
outline, socket functions, mounts and default JP1 bridge. One external supply
at a time remains mandatory; module VBUS connects directly to USB.

## Public source checkpoints

| Revision | Exact public source |
| --- | --- |
| Main / Rev2.1 / Rev2.2 | bc0d52495bd97ed1504bd0ca0775e47feb01a648 |
| Original Rev3A | a5a9fac87cbcb59d337a1fb8d3084ad18867a3e6 |
| Original Rev3B | c5db989810663caa18226a091bfb105ad26fb00e |
| Original Rev3C | 38d94d3dc7c41692e3c41710ec33b9f6e0c38b3e |
| Published comparison | 0593f1ef4c6d6a18f48f0c4c56d5d72aef156e9f |
| Historical Rev1.0 editable snapshot | 87984047ee029efb83bf9947dc21818fd18e39b3 |
| Historical Rev2.0 editable snapshot | af1f2c40029ef67c56910fb2c55feac835553525 |

New cleanup/CI candidates are local review work; their exact heads and results
are in [VALIDATION.md](VALIDATION.md). They do not recreate inaccessible prior
staged trees. Public historical CAD was recovered exactly from the commits
above; matching exports and older-library migration still require review.

## Electrical decisions still open

The original Rev3C really does connect both inputs. Nominal 5 V PIN3 operation
may work at light load, but complete cold-start/RF/thermal margin is unproven
through the fuse, PMOS, switch, source diode, buck dropout, output diode and
module regulator. An ideal 5.000 V carrier rail is not inherently necessary;
the actual purchased C3/C6 module's operating headroom is the criterion.

Minimum corrections first: PMOS reverse/gate protection, coordinated switch
and TVS ratings on both inputs, hot fuse/diode/current limits. Keeping the old
buck preserves architecture; it does not close the missing low-input proof.
A direct low-voltage bypass can exclude higher PIN3 supplies, and a buck-boost
changes cost/layout/source demand. Neither is silently selected. No appliance
current or transient envelope has been established from the nominal manuals.

Rev2.2 retains manual JP2 input selection. Its regulator/current, PMOS gate,
TVS/capacitor and thermal gates are unresolved. Do not call it a safe fallback
or power its 3V3 service output from a UART adapter. Leave UART VCC disconnected.

## Verification and delivery boundary

Native KiCad9.0.9 and pinned libraries check source connectivity, complete
severities, parity and intended netclasses. Firmware uses actual config plus
compilation, not config-only validation. Manufacturing checks compare source
references/metadata and native placements/Gerbers to factory files.

Rev3A's corrected Power patterns expose real routing clearance findings;
legacy C9/C10 has an unresolved courtyard conflict. These remain release gates.
All current power/source/physical qualification gates remain blocked in CI,
with current-source-bound committed evidence required before passing.
CircleCI schema validation is distinct from hosted execution. No current
hosted job, assembled-board, RF, case or appliance test is claimed.

The comparison galleries are historical source previews. New cleanup packages
include matched native PDFs, plots and renders. The retained Rev3C case is
C3-only legacy; the new five-piece common-case concept remains unqualified
and its exact final CAD was not recovered. Keep enclosure work separate until
chosen and physically calibrated.

Prepare focused upstream candidates per revision, with universal CI/docs
separate. No PR, merge, order or deployment is part of this checkpoint.
