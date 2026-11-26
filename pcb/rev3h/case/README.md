# Rev 3H case

Rev 3H uses the Rev 3G closed-USB case with one change: the base has pockets in its floor for the pin tails of the new J7 header and the optional JP3 header. The lids and light pipes are not rebuilt.

## What to print

| Part | File | Notes |
|---|---|---|
| Base | `parts/matching-base-rev3h.stl` (STEP alongside) | **New.** Rev 3G's matching base plus the J7 and JP3 tail pockets |
| Lid | `../../rev3g/case/parts/closed-usb-lid-c3.stl` or `closed-usb-lid-c6.stl` | Rev 3G file, unchanged. Pick the one for the fitted XIAO module |
| Light pipes | `../../rev3g/case/parts/lightpipe-wifi.stl`, `lightpipe-aux.stl`, `lightpipe-bus.stl` | Rev 3G files, unchanged |

Do not print Rev 3G's `matching-base.stl` for a Rev 3H board with J7 fitted: only 1.25 mm is free under the board there, and J7's tails are about 3 mm.

## The pockets

The base floor top is at z 2.4 mm and the board bottom at z 3.65 mm. Rev 3G's base therefore leaves 1.25 mm under every through-hole pin outside J1 and the J5/J6 sockets. The new pockets (KiCad frame; the part itself is mirrored about y = 20 mm on export as for every case part):

| Pocket | Covers | Footprint | Free depth under the board | Floor left |
|---|---|---|---|---|
| J7 | 1x4 header, LCSC C492403 (PZ254V-11-04P), pins at x 69.0, y 13.82 / 11.28 / 8.74 / 6.2 | x 67.6-70.4, y 4.8-15.22 | 3.50 mm | 1.15 mm |
| JP3 | the two 1.0 mm holes at (68.73, 37.0) and (71.27, 37.0), for an optional 2-pin header and shunt | x 67.33-72.67, y 35.6-38.4 | 3.50 mm | 1.15 mm |

3.50 mm is a 3.2 mm tail plus 0.3 mm. J7's tail is taken as about 3.0 mm from the part description (2.5 mm body, 6.1 mm pin above, about 3.0 mm below); the datasheet drawing was not re-read here. The pockets are open to the cavity and closed at the bottom: they do not reach the outside.

## Checks (`case-checks.json`, reproduced by `python export_base.py`)

- **Same base as Rev 3G, plus the pockets.** Built with Rev 3G's parameters (recessed-end envelope, original USB and RJ45 styles, 11.0 mm stack, no magnets) and the pockets off, the base is 28171.031 mm3, Rev 3G's recorded volume. With the pockets it is 28071.743 mm3. A boolean of Rev 3G's `matching-base.step` against the new STEP removes 99.288 mm3, which is exactly the pocket boxes intersected with the Rev 3G base, and adds 0 mm3. A random point sample (400000 points) of the two STLs differs only inside the pockets.
- **Free depth.** A line down from the board bottom (z 3.65) under each of the four J7 pins and the two JP3 holes finds 3.50 mm free. A ray-cast over the tail footprint (0.4 mm either side of each pin) gives 3.50 mm as well. Rev 3G's base gives 1.25 mm at the same points.
- **Floor.** Rays up from below the pockets find 1.15 mm of solid floor at 3480 sample points; the base is one watertight solid.
- **Lid and light pipes.** J7 reaches 8.6 mm above the board (2.5 mm body plus 6.1 mm pin). The first lid solid above the J7 footprint is 23.25 mm above the board (both lids), and the light pipes and base have nothing above it, so there is no collision with the Rev 3G lids.

## Not covered

- The base has no corner magnets. Magnet pockets overlap these pins: a fitted JP3 header cannot be combined with magnets at all, and J7 only with 6x2 magnets (see the case README).
- Nothing has been printed or fitted. The J7 and JP3 pin tails, solder joints and shunt are checked in CAD only, against the nominal part dimensions above.
- The lids are Rev 3G's, so they do not have the larger C3/C6 roof labels or the roof-underside module tag that newer builds from `case/rev3c/analytical` add. Check the lid against the module before closing the case.

## Rebuilding

```sh
python export_base.py          # writes parts/matching-base-rev3h.{step,stl} and case-checks.json
```

It uses `case/rev3c/analytical/enclosure.py`, the single source for every variant. Other variants (closed-USB lids, flush ends, magnets) are built with `case/rev3c/analytical/export_review.py`; see `--closed-usb` and `--no-tail-pockets` there.
