# GE pinned CAD reproduction check

Engineering checkpoint | 5 October 2026

Pinned CAD regeneration passes nominal export integrity: all 43 prototype and 8 analytical STEP/STL pairs pass. The 15 previously delivered STEP models match their regenerated volumes and bounds exactly. Both CAD engines agree within the stated tolerances across 20 shape comparisons and 12 stack cases. The geometry remains provisional and physically unqualified.

## Frozen source and environment

Published source unchanged at 77f4c8893db6c018640e25c55a3af624a3eb06b3.

An isolated environment installed from official PyPI: Python 3.12.14, build123d 0.11.1, trimesh 5.1.0 and OCP 7.9.3.1.1. The 47 resolved package versions are recorded. The two historical top-level pins do not establish the original transitive dependency closure.

## Reproduction evidence

| Check | Result | Measured evidence |
| --- | --- | --- |
| Prototype export readback | 43 of 43 pairs pass | Valid STEP; watertight positive STL meshes. Maximum mesh/STEP volume discrepancy: 0.0933%. |
| Previously delivered STEP | 15 of 15 match | Regenerated volume difference: 0 mm³. Maximum bounds difference: 0 mm. |
| Analytical export readback | 8 of 8 pairs pass | The explicit C3 five-piece set matches prior 0.10 bounds and solid counts; rounded base/lid volumes differ by 0.001 mm³. |
| CAD engine comparison | 20 of 20 agree | build123d 0.10.0 versus 0.11.1: maximum volume difference 0.000886 mm³; bounds 1.46e-13 mm. All shapes valid and single. |
| Analytical STEP roundtrip | 8 of 8 pass | Maximum memory/STEP volume difference: 0.17556 mm³ (0.0007113%); bounds 1.47e-13 mm. |
| C3 and C6 stack screens | 12 of 12 clear | Both modules, internal/external antenna lids and 11.0, 11.325, 11.65 mm stacks. Component and expanded-cap guide screens clear in both engines. |

The prototype count includes electronic proxies, coupons and optional inlays alongside enclosure geometry. Stack screens use illustrative switch and stop heights, a 0.25 mm release gap and specified guide relief. Engine thresholds: 0.01 mm³ volume and 0.0001 mm bounds. STEP roundtrip thresholds: 0.01% volume and 0.0001 mm bounds. Mesh readback uses the historical 2% volume threshold. These checks do not prove geometric identity or physical fit.

## Remaining qualification gates

Wrong-lid U.FL interference remains at 0.084948665 mm³ in both engines. Actual switch identity, electrical make, overtravel and force; seated header stack; USB body corridor and antenna cable routing; print tolerances, material and fatigue; optical/RF behavior; and supplier and physical verification gates remain open. No design change or physical test was performed.

## Evidence receipts

- SOURCE-RECEIPT.json
- INSTALL-RECEIPT.json
- resolved-cad-packages.txt
- prototype-export-readback.json
- all-review-export-readback.json
- explicit-c3-old-receipt-comparison.json
- FINAL-COMPARISON-RECEIPT.json
- analytical-step-roundtrip.json
