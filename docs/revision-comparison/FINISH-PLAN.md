# Finish plan and outstanding work

[Comparison](README.md) · [Current validation](VALIDATION.md) · [Exact checkpoints](HANDOFF.md) · [Quote comparison](PRICING.md)

Updated October 4, 2026 at 06:58 UTC; strict seven-revision native checks and exact source-bound quote snapshots. Selected standalone Rev3C is `5542734`, with original electrical source `7bb455f` and current exact factory trio/quote `b53cfca`. Rev3B protection is digitally reviewed at `ce2979b`; Rev3A rated protection, exact connector lands and zero-warning schematic normalization are independently reviewed and staged; all seven revisions now have zero native findings. Older revisions retain their separate architectures. This plan includes local engineering and review packaging; orders, PRs and upstream publication need their own later authorization.

## Outstanding registry

| Work | Current checkpoint | Closeout evidence | State |
| --- | --- | --- | --- |
| Selected Rev3C final source package | 83-reference source; native/ERC/DRC/parity/manufacturing checks pass; corrected J1 body CPL quoted 04:16; partial C3/C6 models preserved | Final source/export hashes, intended-netclass and antenna proofs, exact-part/source review, refreshed supplier placement/process review; qualify switch/fuse/TVS/gate/diode/buck/module chain | Digital package available; electrical/physical release blocked |
| Common C3/C6 enclosure | Legacy C3-only case `5e01d79` has unchanged CAD/native geometry checks; five-piece common CAD unavailable | Restore exact editable CAD/provenance; calibrate printing, socket stack/retention, C3/C6 USB/buttons/actuators, antenna/pigtail clearance and fit | Source restoration and physical qualification outstanding |
| Focused Rev3A protection backport | `615863d`:97 refs, all native findings 0, independently reviewed source/body-CPL/CAM and 14 pixel views; exact complete97-row quote $178.90/5, $227.86/10 | Actual source/load/retry/thermal/USB isolation; J4 solder delivery/inspection/retention, TP12/annulus/stencil/fill process; module/case/RF | Digital backport and quote complete; process/physical release blocked |
| Focused Rev3B protection backport | `ce2979b` has all-zero native counts,85 fitted references; independent review complete | Exact U2 module stock is unavailable in supplier 5/10 quotes; qualify typed J1/U2 body datum, soldered C3 sourcing/install, loaded power/thermal/USB behavior, local copper/ground-fill effects and actual case | Digital backport complete; supplier/physical release gates open |
| Rev1.0 distinct closeout | Current `53a4b3d`, native 0 findings,166 physical tuples unchanged; independent receipt/current CAM complete; two classic profiles built | Preserve original archives and reviewed current exports; resolve original BOM/CPL procurement absence; review original PIN1/external-buck path and actual 38-pin module | Digital closeout complete; procurement/power/module/physical gates open |
| Rev2.0 distinct closeout | Current `5c8afe4`, native 0 findings,186 physical tuples unchanged; independent receipt/current CAM complete | Preserve original archives and source-bound current CAM; qualify supplier rotations; review manual selector, linear regulators/protection, UART perspective and service power | Digital closeout complete; assembly/power/physical gates open |
| Rev2.1 / Rev2.2 distinct closeout | `fe69d276` / `0ee8e021`, native all-zero; 60 / 59 references | Keep manual selector/legacy architecture; supplier review of Rev2.1's three source-bound pad-center conventions; current-source protection/current/thermal and recovery checks | Digital cleanup available; placement/power/physical gates open |
| Focused candidate packaging | Per-revision hardware, shared/classic firmware, universal CI and canonical docs | Keep each review unit coherent, exact source/export hashes and warning limits included; verify integrated source without conflating historical galleries/quotes | Local unpublished candidates; final exact-source matrix complete; readable/durable closeout packaging |
| Universal CI and hosted checks | Standalone `0d3358a`: two profiles/25 tests; integrated `f85ba98`: seven strict native passes, eight source-matched real builds, 380 dependencies/28 STEP assets | Keep legacy BOM/CPL and intended-policy absence, all 21 physical/source/power gates explicit; run fresh pinned containers and exact hosted jobs after permitted fork publication | Local source/test/schema checks complete; container runtime unavailable locally; fork-publication approval and hosted jobs pending |

A successful quote, native pass or compilation cannot close the electrical/physical rows. No older revision is an established safe fallback. Any backport changes the source checkpoint and requires regenerated source-bound evidence; do not reuse Rev3C's passes as Rev3A/B proof.

## Remaining dependency boundaries

- Local documentation, proposed PR descriptions, source-bound manifests and durable source/PDF preservation can be completed now. No additional source defects remain from this bounded digital review.
- Exact common five-piece enclosure CAD requires legitimate file attachment/selection before design/fit review; old C3-only geometry is not a shared default. Actual module/button/header dimensions and prints are also needed for physical qualification.
- Target appliance model, source voltage/current/transient envelope and a reviewed bench procedure are required for startup/load/retry/thermal/RF/appliance tests. No physical test has occurred.
- Supplier part stock, footprint-zero/pin1 and assembly process remain gates. Rev3A's quote is complete but J4 solder/retention is unapproved; Rev3B's exact module is unavailable. Rev1 lacks purchasing provenance; Rev2's 60 archived component codes need explicit source/identity/rotation review before a current supplier package can be declared.
- Fork publication is pending the existing tool approval; no alternate route is used. PR creation/upstream submission, merge and orders are not performed. Hosted checks require the permitted published exact commit; fresh local containers lack a runtime here.

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
