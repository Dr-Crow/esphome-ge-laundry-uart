# Shared Rev3C enclosure review prototype

The editable all-printed enclosure source has been recovered. It has one common base, separate C3 and C6 lids, integral printed BOOT/RESET mechanisms, three light guides, and internal or external antenna variants. **It is a review prototype, not a qualified default enclosure for the selected carrier.**

[Enclosure index](../README.md) · [Selected carrier](../../pcb/rev3c/README.md) · [Prototype qualification plan](../../pcb/rev3c/PROTOTYPE-QUALIFICATION.md)

The [independent mechanical finding matrix](review/recovered-enclosure-review.md) and [compact check receipt](review/provenance-counts.json) record actual source/STEP/STL inspection, current-board datums and unresolved fit assumptions. [Detailed export checks](review/inspection-receipt.json) and the [current datum comparison](review/current-datum-comparison.json) preserve the individual measurements and hashes.

## Current analytical derivative

[Parametric review source](analytical/README.md) now registers current component screens and samples installed stacks from11.0 to11.65 mm. It offers separately reviewed longer-leaf and local guide-relief candidates, with explicit per-button controls and five-piece review exports. Correct-lid nominal screens pass; original fixed reaches and wrong-lid prevention fail their stated checks. Actual switch, plug, print, optical, thermal and RF qualification stays open.

![Actual C3/C6 prototype geometry](analytical/review/presentation_compare_c3_c6.png)

These are fresh source-derived presentation renders, with recorded geometry/tool hashes and illustrative materials. The following original-recovery evidence remains historical; its uncorrected proxy and regeneration limitations are preserved rather than relabeled as a current result.

## Recovered source

The [build123d source](prototype/enclosure.py), [interface datums](prototype/interface_baseline.py), [electronic proxies](prototype/component_envelopes.py), [pinned dependencies](prototype/requirements.txt) and [license](prototype/LICENSE) are copied without changes from `GE-enclosure-CAD-and-review.zip`. [Source provenance](prototype/SOURCE-PROVENANCE.json) records the archive and individual file hashes. STEP and STL exports are geometry outputs; the Python files are the editable parametric source.

The separate `GE-tapered-enclosure-review-2026-10-02.zip` contains the older spring/cassette design. It is preserved as historical material and is not the recommended starting point. The existing [Rev2 Fusion archive](../rev2/README.md) belongs to another board family. Historical C3-only cases do not establish shared C3/C6 fit.

The recovered source was reviewed against carrier commit `11826a7f6ba1ed19131ddba46e4d62b06196a8c6`. Its original mounting, socket, LED and module XY datums remain useful. Its electronic proxies still include removed J2 and omit the selected rated-switch/fuse/PIN3-TVS changes. They must be reconciled with the current populated board before new collision results can be used. Module/header seating and button height remain provisional.

There is also a concrete difference between the provisional height models: the case uses 8.65 mm maximum socket height plus 3.0 mm male spacer, while the current board preview assumes 8.5 + 2.5 mm. Comparing those assumptions increases the nominal released actuator gap from 0.25 to 0.90 mm, beyond the C3/C6 stop travels of 0.40/0.36 mm. This is a source-assumption mismatch, not a measured physical failure; actual seated dimensions must determine the reaches.

The C3 lid must not be installed over C6. One C3 contact is approximately 0.19 mm from the C6 U.FL datum and the other falls inside its ceramic antenna projection. Module swaps require the correct labeled lid and antenna configuration.

## What must be checked next

- Measure each actual module, installed header/socket stack, USB shell and plug, BOOT/RESET switches and safe actuator travel. The C6 fixed-height mechanism can under-travel or over-travel across its conditional switch-height tolerance; do not press it against an installed module before calibration.
- Register current component bodies and solder tails, check base/support clearances and cable access, then generate and inspect source-matched meshes and slicer previews. The original archive's nominal collision counts do not qualify the selected 40 V-switch board.
- Print the button and closure coupons without electronics. Verify release, return, accessible latch release, repeated-use wear and creep in the chosen printer/material/profile before an enclosure assembly trial.
- Verify light-guide fit, retention, brightness and leakage. `WIFI` means green D4 Wi-Fi connected; `AUX` means red D5 manually controlled and off at startup; `BUS` means yellow D6 GEA bus connected, not packet activity or a power-good indicator.
- Check the C3 FPC and both U.FL cable routes, C6 ceramic-antenna clearance, external bulkhead nut/strain relief and remote-antenna cable slack. Actual RF and metal-appliance proximity need separate qualification.

Both appliance power inputs enter through the same J1 8P8C connector; no second power opening is needed. Leave room to unplug that cable before powered USB recovery. Keep the two module-specific lids visibly identified, and preserve BOOT-held/RESET-pressed recovery access.

## Regeneration boundary

The original source pins build123d 0.11.1 and trimesh 5.1.0. `enclosure.py` writes its own adjacent `exports` folder and uses the DejaVu Sans font path declared in the source. Run it only in a working copy after installing the pinned tools and reviewing the parameters. The recovered STEP/STL validation helpers and historical exports remain in the original archive. The delivered printed-case archive omits `exports/summary.json`, and its rendering manifests reference additional electronics, cutaway and supplier meshes; regenerate or legitimately obtain those inputs before claiming a reproducible complete render.

A fresh read-only inspection found all 15 delivered printed-case STEP/STL pairs valid, closed and positive-volume, with close volume agreement; that is export integrity, not source regeneration or current-board fit. Installed build123d 0.10.0 differs from the pinned version and trimesh is absent. Neither regeneration nor physical printing is claimed by this recovery.

Disconnect all power before inserting/removing the module or assessing mechanical fit. Disconnect the appliance cable before powered USB; UART VCC stays disconnected. The complete proposed review sequence is in [PROTOTYPE-QUALIFICATION.md](../../pcb/rev3c/PROTOTYPE-QUALIFICATION.md).
