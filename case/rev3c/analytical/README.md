# Parametric Rev3C enclosure review

This is an editable analytical derivative of the [recovered prototype](../prototype/). It keeps a common base, module-specific C3/C6 lids and three light guides. The selected carrier outline and both appliance power inputs are preserved. The four lids support internal/external antenna concepts; exact cable, switch and printed-assembly qualification remains open.

**Use review exports for dimensional review and coupons. They are not approved production files.** Fixed original button reaches fail nominal actuation at an installed stack of 11.0 mm. The common closure permits a wrong lid: a C3 BOOT foot can contact C6 U.FL. Check the module label before assembly; labels do not mechanically prevent this mistake.

The [source-bound report](review/CASE-ANALYSIS.md) records valid solids, installed-stack samples, component envelopes, actual guide routes, plug gauges and antenna provisions. Analytical geometry was generated with build123d 0.10.0 / cadquery-ocp 7.8.1.1.post1. The original analysis used a different toolchain from the recovered historical requirements; the subsequent pinned reproduction is recorded below. These versioned checks are not physical fit, material or RF tests.

The [subsequent pinned reproduction](review/pinned-reproduction/GE-Pinned-CAD-Reproduction-2026-10-05.md) closes that setup/reproduction limitation for the frozen 77f4c88 source. build123d 0.11.1/trimesh 5.1.0 produces 51 independently checked STEP/STL pairs, and the 20 nominal shape comparisons and 12 stack samples agree with the prior engine. The original two top-level requirements do not establish the old transitive dependency closure; all 47 packages used in the new run are recorded. Future parameter/source changes require their own checks. Printed fit and physical qualification remain open.

## Coordinate frame fix (2026-11-23)

**Exports made before this change are mirror images of the real part and must not be printed.** All dimensions in `enclosure.py`, `interface_baseline.py` and `current_carrier_bounds.json` are KiCad board coordinates: x right, y *down* in the top view. The geometry was built in that frame with z up, which is left-handed. The printed case therefore had the J1 (RJ45), USB-C and light-guide features on the wrong long side of the board.

Three checks confirmed this:

- **Handedness.** KiCad's own 3D export maps board +y to −y in a z-up frame, and the Rev2 Fusion case also uses y = −KiCad y.
- **Placement sampling.** With the corrected exports, sample points inside the J1 body and both XIAO socket rows of the real Rev3D board are clear of printed solid. The old convention collides at J1 and J5.
- **End-wall opening.** The J1 opening used to span physical y 7.8–25.9 mm against an RJ45 body at y 14.8–31.2 mm, so the plug would hit the wall. It now spans 14.1–32.2 mm.

Geometry is still built and checked in the KiCad frame, so every existing clearance screen keeps its meaning. `enclosure.export()` and `interface_baseline._export()` now mirror each part once about the board centreline (y = 20 mm) into the physical frame. `legend()` pre-mirrors each label glyph about its own centre so the embossed text still reads correctly. The check: a readable text solid at each label's physical position overlaps the carved lid by 0 mm³, and a mirrored one does not. Volumes are unchanged. Earlier slicer times and filament figures still apply, but re-slice before printing.

## Magnet mount option (2026-11-23)

`--magnets 6x2|8x2|10x2` adds four corner pockets to the base for N52 disc magnets (diameter × thickness in mm), so the case can sit on a steel appliance panel. `--magnet-style` picks how the magnets are held:

| Style | How | Hold | Skin to cavity floor |
|---|---|---|---|
| `glue` (default) | Open pocket on the bottom; glue the disc flush (CA or epoxy) | Strongest: the magnet touches the steel | 1.3 mm |
| `press` | Open pocket with three 0.6 mm crush ribs standing 0.25 mm into it; press the disc in, no glue | Same as glue | 1.3 mm |
| `embedded` | Sealed pocket 0.55 mm above the bottom face. Pause the print before the reported layer (2.95 mm for a 0.35 mm first layer and 0.2 mm layers), drop the discs in with the same pole up, and resume | About a third less, because of the 0.55 mm skin; invisible and cannot fall out | 0.65 mm |

Pockets are at x 9/70 mm, y 1.5/38.5 mm (KiCad frame). Every size and style keeps a single valid solid with full skins. Pressed discs meet only the ribs (about 0.18 mm³ of interference), and the embedded pockets are fully enclosed. The export receipt records the pocket coordinates and the pause height. Gluing magnets inside the case is not offered: the floor would leave about 1.2 mm of plastic between magnet and steel, and the magnets would sit under the electronics. For no reprint at all, put adhesive magnet tape on a plain base. Without `--magnets` the base is unchanged, and `base(magnets=True)` keeps the original two-pocket layout.

Expect much less holding force on thin, painted or curved panels than the catalogue pull rating. Sliding on a vertical panel is the weak direction. A metal panel behind the module also shortens Wi-Fi range; the external-antenna lid helps if range suffers. Keep away from hot spots: PLA softens around 55–60 °C, so use PETG or ASA there.

## Antenna options (2026-11-23)

`--antenna` picks the lid roof. The options apply to both modules:

| Option | What the lid has | Use it for |
|---|---|---|
| `fpc` | Keeper rails, an entry stop and two cable keepers under the roof for a 40 × 20 mm flat FPC antenna on the module U.FL | The FPC antenna that ships with the XIAO C3 (the C3 has no onboard antenna), or a C6 set to its U.FL port |
| `smooth` | Plain roof, no antenna features | The C6 onboard ceramic antenna, or your own antenna mounting |
| `external` | 12 mm bulkhead bore through the long side wall at x 56 mm, z 15.5 mm, plus a printed cable keeper | An SMA/RP-SMA pigtail from the module U.FL |
| `internal` | The original pairing: C3 → `fpc`, C6 → `smooth` | Reproducing earlier exports |

The `fpc` export also writes `proxy_fpc_antenna_40x20`, a reference body for checking clearance. It is not a printed part. Checks: in every option, all 67 Rev3D 3D models clear printed solid. The FPC body sits at z 26.4–28.2 mm, clear of the lid and every part (module top ≤ 22.4 mm). The keeper fit, cable bend room, bulkhead hardware and RF performance are unverified. The C6 module's own U.FL position is taken from the C3 layout and is not modelled separately.

## Flush USB-C port option (2026-11-23)

With the original end wall, the module's USB-C mouth (x ≈ 100.0 mm) sits about 4.3 mm behind the outer face, so the 14.8 × 9.0 mm opening must pass a cable overmold. `--usb-style flush` moves the end wall out to the port instead:

- **End face.** The outer face sits `USB_RECESS` = 0.5 mm in front of the mouth, on a 1.2 mm end plate, so the USB end is 6 mm shorter.
- **Opening.** 9.64 × 4.36 mm with rounded top corners. That is a Type-C shell (8.94 × 3.26 mm) plus 0.35 mm a side. The height also covers a module PCB of 1.2–1.6 mm at the configured stack.
- **Assembly.** The lid drops on from above, so the port is a slot open at the bottom. A tower on the base fills it below the port, with a 0.2 mm sliding gap.
- **C6 lid.** Its BOOT/RESET release voids reach x 100.55, so above z 27.6 the end face steps out to x 101.35 to keep 0.8 mm of skin.
- **Removed.** The two USB-end datum lands no longer fit and are omitted. Closure height rests on the other two lands and the end plate.

Checks, done in the build frame against the review parameters:
- All 67 Rev3D 3D models are clear of printed solid.
- The receptacle shell and the lid's drop path are clear at a 1.2 mm and a 1.6 mm module PCB.
- The carrier edge and module PCB are clear.
- A 12.2 × 6.5 mm overmold in front of the face is clear.
- The tower and lid, and the base and lid, do not overlap.

**Not measured:**
- the native mouth position and receptacle shell (the vendor KiCad files give the mouth; the UBF31-0171 drawing was not checked);
- whether a cable's overmold seats with a 0.5 mm recess.

The flush export also writes `coupon_usb_end_base` and `coupon_usb_end_lid_<module>`: a short USB-end slice to print with a real module and cable before a full case. The default stays `original`, so earlier commands reproduce unchanged.

```sh
python export_review.py --module c3 --stack 11.325 --boot-height 1.5 --reset-height 1.5 \
  --boot-stop 0.4 --reset-stop 0.4 --leaf-offset 17.3 --relieved-guides --usb-style flush \
  --output exports-review-c3-flush
```

## Reviewable corrections

- `configure()` sets the declared generic installed stack from 10.35 to 11.65 mm, independent BOOT/RESET heights, gaps and stops, plus optional stack-adjusted USB height. It does not establish a safe switch overtravel limit.
- A separate C3 leaf-root offset of 17.3 mm, instead of 16.6 mm, lowers the nominal fixed-guided strain screen to 0.427–0.495%. This meets the stated example screen, with material/fatigue and tolerance margin still unproved.
- `pipe_with_cap_relief()` removes only local lower crescents near manufacturer maximum capacitor bodies. The chosen 0.15 mm solder-lift allowance and 0.25 mm clearance are design requirements. The nominal LED inlet projection, upper path and roof retention stay unchanged; reduced inlet area needs optical/print testing.

![Guide relief and preserved LED inlet](review/guide-relief-candidate.png)

## Explicit review export

Use an existing authorized installation of the recorded analysis tools. `export_review.py` requires an explicit module, stack and switch/stop dimensions so a known-bad default is not silently presented as a print-ready assembly. An illustrative C3 command is:

```sh
python export_review.py --module c3 --stack 11.325 \
  --boot-height 1.5 --reset-height 1.5 --boot-stop 0.4 --reset-stop 0.4 \
  --leaf-offset 17.3 --relieved-guides --output exports-review-c3
```

Those are conditional analytical parameters, not measured switch limits or a recommended production calibration. For C6, use its separately verified switch identity and dimensions. The report's 0.53 ±0.10 mm C6 height remains conditional; the nominal 0.36 mm stop is not a manufacturer overtravel allowance. The export includes the explicit parameter/source receipt and five review pieces. Extra coupons or proxy electronics are excluded from that five-piece set.

## Current dimension review

The [October 5 dimensions review](MECHANICAL-DIMENSIONS.md) binds socket maximum dimensions, the full declared 10.35–11.65 mm assumed-stack range, conditional switch identities and the named StarTech USB2CC2M cable. Its 12.2 × 6.5 mm maximum overmold exceeds the old synthetic gauge. The actual fitted header, C6 switch identity and native USB mating coordinates remain unresolved.

The [named cable tool and sensitivity receipts](review/cable-corridor/README.md) require explicit shoulder/axis coordinates and retain the source uncertainty. Named switch-height references are also available without changing the fitted default.

## Open assembly checks

The historical maximum-body and base/lid screens cleared at three sampled stacks within 11.0–11.65 mm. The [subsequent source-bound endpoint check](review/socket-stack-endpoints.json) passes eight C3/C6 × internal/external × lower/upper cases with maximum socket bodies and conditional switch-height extremes. All have zero nominal component/base-lid intersections and 0.25 mm released button gaps. Four lower-end lids also pass STEP single-solid and untouched watertight STL readback. These are explicit review parameters, not factory seating or safe-actuation proof. A 12 ×6 mm synthetic USB plug gauge clears; a 14 ×8 mm gauge fails the rounded aperture. Choose a real plug and verify shank depth, strain relief, insertion and finger/latch access. Antenna maximum slabs and nominal bulkhead hardware clear their stated screens, while cable terminations, bend/slack, panel tolerance and RF remain open.

Before fitting a board, verify the actual male/female header seating and retention, both switch make/overtravel/force specifications, wrong-lid prevention, slicer/coupon clearances, light transmission and actual antenna/plug envelopes. Leave UART VCC disconnected. Disconnect the appliance cable before powered USB. The 40 V switch selection is not a 40 V rating for the complete carrier.
