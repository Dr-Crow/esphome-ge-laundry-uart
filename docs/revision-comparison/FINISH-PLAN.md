# Finish plan and outstanding work

[Comparison](README.md) · [Current validation](VALIDATION.md) · [Exact checkpoints](HANDOFF.md) · [Quote comparison](PRICING.md)

Updated October 4, 2026; source and quote snapshot: October 3. Selected standalone Rev3C is `47c2fdc`, with electrical/quoted source `7bb455f`. Rev3B protection is digitally reviewed at `f885fa2`; Rev3A routing remains active with a measured failing draft. Older revisions retain their separate architectures. This plan includes local engineering and review packaging; orders, PRs and upstream publication need their own later authorization.

## Outstanding registry

| Work | Current checkpoint | Closeout evidence | State |
| --- | --- | --- | --- |
| Selected Rev3C final source package | 83-reference source; native/ERC/DRC/parity/manufacturing checks pass; exact five/ten quotes recorded | Final source/export hashes, intended-netclass and antenna proofs, exact-part/source review, refreshed supplier placement/process review; qualify switch/fuse/TVS/gate/diode/buck/module chain | Digital package available; electrical/physical release blocked |
| Common C3/C6 enclosure | Legacy C3-only case `5e01d79` has unchanged CAD/native geometry checks; five-piece common CAD unavailable | Restore exact editable CAD/provenance; calibrate printing, socket stack/retention, C3/C6 USB/buttons/actuators, antenna/pigtail clearance and fit | Source restoration and physical qualification outstanding |
| Focused Rev3A protection backport | Routing repair `d1769b2` has 0 errors, retained 53/5 warnings | Review applicable rated switches, both-path protection and gate/energy/current coordination; preserve both inputs/priority and integrated C3/USB paths; regenerate matched native/manufacturing evidence; resolve TP12/annulus process margins | Active implementation; new validated source/evidence pending |
| Focused Rev3B protection backport | `f885fa2` has all-zero native counts,85 fitted references; independent review complete | Obtain a revision-specific full supplier quote; qualify soldered C3 sourcing/install, loaded power/thermal/USB behavior, local copper/ground-fill effects and actual case | Digital backport complete; supplier/physical release gates open |
| Rev1.0 distinct closeout | Final `3bb5f85` (implementation `12f82aa`), one alias warning; independent receipt/current CAM complete; two classic profiles built | Preserve original archives and reviewed current exports; resolve original BOM/CPL procurement absence; review original PIN1/external-buck path and actual 38-pin module | Digital closeout complete; procurement/power/module/physical gates open |
| Rev2.0 distinct closeout | Final `17b41df`, four alias warnings; independent receipt/current CAM complete | Preserve original archives and source-bound current CAM; qualify supplier rotations; review manual selector, linear regulators/protection, UART perspective and service power | Digital closeout complete; assembly/power/physical gates open |
| Rev2.1 / Rev2.2 distinct closeout | `fe69d276` / `0ee8e021`, native all-zero; 60 / 59 references | Keep manual selector/legacy architecture; supplier review of Rev2.1's three source-bound pad-center conventions; current-source protection/current/thermal and recovery checks | Digital cleanup available; placement/power/physical gates open |
| Focused candidate packaging | Per-revision hardware, shared/classic firmware, universal CI and canonical docs | Keep each review unit coherent, exact source/export hashes and warning limits included; verify integrated source without conflating historical galleries/quotes | Local unpublished candidates; integration review continues |
| Universal CI and hosted checks | Standalone `3d4c7bc` has two manifest profiles/ 14 boundary tests; complete source `7df3567` has eight profiles and 356 dependencies; B/C closeout `0429539` passes digital checks | Integrate final A source, retain explicit native-warning and physical readiness failures, then validate exact permitted publication in pinned containers with source/native/intended-rule/manufacturing/real-build jobs and actual hosted URLs | Local source/dependency review complete; final A integration, fresh containers and hosted jobs pending |

A successful quote, native pass or compilation cannot close the electrical/physical rows. No older revision is an established safe fallback. Any backport changes the source checkpoint and requires regenerated source-bound evidence; do not reuse Rev3C's passes as Rev3A/B proof.

## Physical qualification checklist

1. Identify the actual appliance model and purchased module/buck revisions. Measure loaded source voltage/current allowance and relevant transient/pulse energy across the intended operating envelope.
2. Check each input separately and both together: reverse polarity, PIN1 presence priority, startup/dropout, switch current limit/retry, brownout and recovery. Verify differential/gate and protection/fuse coordination under reviewed fault conditions.
3. Measure the complete supply path at cold/hot startup, inrush and Wi-Fi peaks: fuse/PMOS/switch/OR/buck/output diode/module rails, load margin and temperatures. Define acceptance limits from the exact parts and actual source.
4. Review supplier rotations, pin 1, diode/zener polarity, exposed-pad/stencil and through-hole/socket process. Resolve Rev3A's clearance/finished-annulus margins and Rev2.1 placement conventions before assembly approval.
5. Verify one-source USB/UART behavior, with UART VCC disconnected. Check Rev3A's distinct USB-isolation paths separately; do not assume them on XIAO carriers. Confirm reset/BOOT/recovery and ROM UART effects on the appliance interface.
6. Match the correct classic/C3/C6 GEA2/GEA3 profile to the actual board. Check actual appliance entities, bus reliability, startup/reconnect and functional behavior; compilation alone is insufficient.
7. Restore and print the exact chosen enclosure. Test orientation, all 14 socket contacts/retention, stack height, vibration, USB, BOOT/RESET actuator travel, antenna/pigtail clearance, RF and temperature with the actual module.
8. Record measured results, instruments, acceptance criteria, assembly/source revisions and evidence hashes. Only current-source qualified evidence can release the corresponding gate; later ordering requires final stock/placement review and user approval of the complete landed purchase.

The comparison galleries and old charts remain historical. A later PDF should summarize these canonical Markdown files and their current source identities, rather than become a separate status authority.
