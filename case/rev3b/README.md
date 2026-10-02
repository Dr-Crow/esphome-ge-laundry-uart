# Rev3B printable enclosure candidate

Editable `build123d` source and generated base/lid files for the current
Rev3B carrier PCB (99 x 40 x 1.6 mm, four layers). This is a simple,
nonmagnetic default candidate; it is not a physical-fit, electrical, thermal,
or RF qualification.

## Files and variants

* `enclosure.py` — parametric source.
* `check_geometry.py` — STL/STEP, manifold, dimensional, component-envelope,
  LED-aperture, support, magnet-pocket, and external-bulkhead checks.
* Default: [`base STL`](exports/rev3b_base.stl), [`base STEP`](exports/rev3b_base.step),
  [`lid STL`](exports/rev3b_lid.stl), [`lid STEP`](exports/rev3b_lid.step).
* Internal antenna: [`base STL`](exports/rev3b_base_ant-internal.stl),
  [`lid STL`](exports/rev3b_lid_ant-internal.stl), with matching `.step` files.
* External bulkhead: [`base STL`](exports/rev3b_base_ant-external.stl),
  [`lid STL`](exports/rev3b_lid_ant-external.stl), with matching `.step` files.
* Captive magnets: [`base STL`](exports/rev3b_base_magnets.stl),
  [`lid STL`](exports/rev3b_lid_magnets.stl), with matching `.step` files.
* [`images/rev3b-cad-preview.png`](images/rev3b-cad-preview.png) — native STL
  geometry preview; transparency is for inspection only.

Generate with a build123d 0.11.1 environment:

```sh
python enclosure.py
python enclosure.py --antenna internal
python enclosure.py --antenna external
python enclosure.py --magnets
python check_geometry.py
```

The checked-in exports were generated and `check_geometry.py` completed with
`All checks passed.` The external variant is optional and does not change the
default/internal case.

## Mechanical candidate

The frozen-board transforms are taken from the current Rev3B PCB. H1=(4.5,33.0) and
H2=(94.0,35.0) have one locating support each. The board sits 1.25 mm above
the 2.4 mm floor. Annular lid retainers overlap the board surface around H1/H2
to provide hold-down, while the posts locate through the 3.2 mm drills. J1 and USB-C have generous service windows at opposite ends;
J2 is internal and requires lid removal. Three 2.5 mm LED apertures are at
the extracted D4/D5/D6 positions. Two conservative lid tool apertures are
centered on the BOOT0/RST0 centers from the official Seeed v1.3 project; tool
fit, actuator force, and return must still be checked on hardware.

The lid has two 3.5 mm tool holes above the module's BOOT and RESET buttons.
Their alignment follows Seeed's module layout; the geometry checks include
these positions to catch accidental movement of either opening.

The conservative J1 and XIAO model envelopes are project clearance solids,
not manufacturer CAD. The base includes a conservative 3.0 mm under-board
RJ45-tail relief with a 0.6 mm floor skin because the local evidence does not
specify assembled tail length. Cable plug/latch sweep, USB strain relief,
RJ45 mating, lid retention, and populated-board seating remain physical checks.

## Antenna options

### Internal FPC (`--antenna internal`)

Adds a shallow 40 x 20 mm placement ring on the lid underside, away from the
three LED apertures. It is sized from the candidate Seeed FPC drawing
(M01-0601770R0A), but the identity of the antenna bundled with SKU 113991054
is not confirmed. The ring supplies guidance only; adhesive supplies
retention. FPC bend, metal clearance, coax routing, and closed-case RF
performance are untested.

### External bulkhead (`--antenna external`)

This option is deliberately tied to the named **TE/Linx
CSB-RGFB-102-UFFR** cable assembly, not to an arbitrary SMA/RP-SMA part. Its
primary drawing is the [Toradex-hosted TE/Linx datasheet](https://docs.toradex.com/114003-datasheet-pigtail-antenna-cable-ufl-to-rp-sma-100-mm.pdf),
page 3. The case provides:

* a Ø6.5 mm bulkhead opening;
* a local reinforced seat held to the drawing's 1.5 mm maximum panel
  thickness;
* the drawing's 6.0 mm flat/key datum recorded as a part-specific datum, but
  not guessed as a keyed PCB-oriented cutout;
* a mechanical wall load path for the RP-SMA nut, separate from the U.FL.

The part is an RP-SMA **jack with male pin** to U.FL/MHF1-type female socket,
on 102 mm RG-178 cable, with a 10 mm minimum inside bend radius. Verify the
actual purchased part, nut/washer stack, panel seating, cable bend, and
antenna clearance before printing a production case. No RF or physical-fit
guarantee is made.

## Optional captive magnets (`--magnets`)

The default is nonmagnetic. The optional case widens the perimeter and adds
two fully enclosed pockets for placeholder 4 x 2 mm disc magnets. Pockets are
isolated from the PCB cavity by asserted solid clearances and have printed
skins above and below. Pause **before the first layer that closes the pocket
roof**, at the source constant `MAGNET_PAUSE_Z` (currently 5.2 mm); adapt it to
the slicer's actual layer boundary and printer pause behavior. Magnet material,
polarity, holding force,
RF interaction, and appliance-temperature behavior were not tested.

## Prototype gate and safety

Print base and lid separately and test on an unpowered, populated board.
Check RJ45/USB insertion and latch/strain-relief clearance, BOOT/RESET reach
and release, LED visibility, J2 lead access with the lid removed, board seating,
antenna bend/retention/RF behavior, and magnet captivity if selected. Do not
connect USB, appliance power, and J2 5 V at the same time; the case provides
no electrical interlock.
