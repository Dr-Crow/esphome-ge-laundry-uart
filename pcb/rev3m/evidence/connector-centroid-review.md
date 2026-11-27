# Compact prototypes — assembly placement centers

The earlier placement lists gave JLCPCB pin 1 as the assembly coordinate for the two XIAO sockets (J5, J6) and, where fitted, the four-pin debug header (J7). JLCPCB requests component center coordinates. These changes correct eight placement records across three prototype revisions. The corrected positions below are in the exported top-side CPL frame, in millimeters.

| Revision | J5 X, Y | J6 X, Y | J7 X, Y | Fitted references checked |
| --- | --- | --- | --- | ---: |
| 3K | 58.576650, −3.727500 | 58.576650, −18.967500 | 40.287501, −7.040000 | 72 |
| 3L | 53.606650, −3.597500 | 53.606650, −18.837500 | 37.571895, −6.599707 | 72 |
| 3M | 48.550650, −1.947498 | 48.550650, −17.187498 | Absent | 68 |

Each revised socket center lies 7.62 mm from pin 1. On 3K and 3L the J7 center lies 3.81 mm from pin 1. The existing J1 position also agrees with its manufacturer body center. Each generator now applies audited local offsets to freshly exported native placement coordinates and angles. The accompanying placement-origin-review.json records the local offsets, native placement and resulting body center.

The independent check compared every fitted center against the midpoint of its four bounds in the revision's evidence/component-body-edge.csv. It caught all eight original errors. The largest distance after correction was 0.000051 mm or less (the bounds table rounds some coordinates). The 0.10 mm check threshold screens for wrong origins and stale tables. It does not specify machine placement accuracy. Every fitted row remained on top and all angles matched the prior list.

To repeat the checked-in-file regression without KiCad, run:

```sh
python3 pcb/rev3k/manufacturing/generate.py --check-cpl
python3 pcb/rev3l-placement/manufacturing/generate.py --check-cpl
python3 pcb/rev3m/manufacturing/generate.py --check-cpl
```

The normal generator applies the same check before publishing its outputs. Refresh the independent body table after an intentional footprint, placement or population change. Confirm imported centers, rotation and pin 1 against the actual JLCPCB footprint overlays, and confirm through-hole handling and fit before release. This coordinate review does not establish supplier acceptance or bench performance.

[JLCPCB pick-and-place format](https://jlcpcb.com/help/article/pick-place-file-for-pcb-assembly) · [JLCPCB assembly terms](https://jlcpcb.com/help/article/terms-and-conditions-of-jlcpcb-assembly-service)
