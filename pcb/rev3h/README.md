# Rev3H: Rev3G plus a GEA bus monitor header and one fewer extended part

Rev3H is Rev3G with two changes. Everything else is unchanged: same 99 x 40 mm four-layer carrier, same XIAO C3/C6
sockets, RJ45, TPS259470A eFuse mux, AP63205 buck, same net names and the same positions for every other part.
The editable source is in `design/` (KiCad 9.0.9). The pinned toolchain is
`kicad/kicad:9.0.9@sha256:e638b79b0321f29395a5b783e94bb9f3c73303e8da15da27b8f5cb4b67a37729`.

**Status: unqualified prototype.** Nothing here has been built, powered or quoted. See "Not verified".

## What changed vs Rev3G, and why

| Area | Rev3G | Rev3H |
| --- | --- | --- |
| Bus monitor | Only a way to probe the back of J6's socket joints for RX; no module-side view of GEA3 transmit | **J7**, a fitted 1x4 2.54 mm header (LCSC C492403, PZ254V-11-04P) with **R48-R50** 1k 0603 (C21190) in series with each tap |
| C16, C17 (buck output, /BUCK_5V) | 22u 25V X7R 1210, CL32B226KAJNNNE, **C309062** (extended) | 22u 25V X5R 1206, Samsung CL31A226KAHNNNE, **C12891** (basic), same centre and rotation |
| C9 (raw input) | 10u 50V X7R 1206, C303950 | **Unchanged** |
| JP4 via | Via at (29.1, 22.9) straddles the edge of the exposed JP4.1 land | Moved to (31.5, 23.0), 0.78 mm clear of the land (commit ec3752c) |
| Case | Rev3G closed-USB case | Rev3G's closed-USB lids and light pipes, plus a new base with pin-tail pockets under J7 and JP3 in `case/` (the Rev3G base leaves only 1.25 mm under the board; J7's tails are about 3 mm) |

### Why J7

A serial adapter's RX on J7 lets you watch appliance traffic without soldering to the board. A series 1k resistor on each tap
means a wrongly wired adapter TX cannot fight the U4/U5 buffer outputs. J7 sits on the 3.3 V side only, so it is listen-only
and nothing on it is 5 V.

### J7 pin table (3.3 V, listen only)

Connect the adapter's GND to pin 1 and its RX to **one** of pins 2-4 at a time. Never connect the adapter TX or a 5 V supply.

| Pin | Silk | Net | Direction (traced on the Rev3G netlist) | Series R |
| --- | --- | --- | --- | --- |
| 1 | GND | GND | Ground, square pad, full zone connection | none |
| 2 | GEA2 | `GEA2_RX` | 3.3 V copy of the GEA2 half-duplex bus, as received by the XIAO: U4.6 -> R10 -> J6.4. Carries appliance traffic and the module's own transmissions (U5 drives the bus, U4 reads it back) | R48 |
| 3 | G3IN | `GEA3_TX` | Appliance to module, 3.3 V, what the XIAO receives: U4.4 -> R13 -> J6.1. The net name is from the appliance's perspective | R49 |
| 4 | G3OUT | `GEA3_RX` | Module to appliance, 3.3 V: XIAO TX after the JP2 selector (JP2.2) -> R12 -> U5.3. This is the module side of U5 | R50 |

Trace through the buffers, using the Rev3G netlist: U4 (74LVC2G07, 5 V powered) turns the 5 V bus into 3.3 V:
channel 1 is the half-duplex bus D9.K2 -> U4.1 -> U4.6 (R14 pull-up to +3V3) -> R10 -> `GEA2_RX`; channel 2 is J1.4 through
R25/R21 -> U4.3 -> U4.4 (R17 pull-up) -> R13 -> `GEA3_TX`. U5 (3.3 V powered) goes the other way: `GEA3_RX` -> R12 -> U5.3 ->
U5.4 -> **JP4** -> R24 -> J1.5. JP4 sits on U5's output (the appliance side), so `GEA3_RX` is still the module-side net and
shows module transmit data even with JP4 open.

Placement: J7 pin 1 at (69.0, 13.82), rotated 180 degrees so pin 4 is at y = 6.2; R48-R50 at x = 72.635 (pad 2 at 71.81 next
to the header, pad 1 at 73.46). It is left of the XIAO sockets (J5/J6 start at x = 78.4), the courtyard top is about 4.5 mm
below the top edge, and J7 is not under the XIAO. Silkscreen: `GND` / `GEA2` / `G3IN` / `G3OUT` beside the pins and
`BUS MON 3V3 / LISTEN ONLY` below the header. The schematic has the same text as note 10. R48 and R50 land on vias and
tracks Rev3G already had (the `GEA2_RX` via at 73.463, 15.683 and the `GEA3_RX` run at y = 1.28). R49 reaches `GEA3_TX`
through three vias (a tap on the existing In2 diagonal, F.Cu up x = 74.8, In2 up to y = 8.74). This is the same routing idea
as the Rev3E build of this header (commit 844e6bb), re-checked against Rev3G's neighbours; nothing else moved.

### Why C16/C17

C309062 is an extended part, so every order pays its $3.09 setup fee. C12891 is a basic part, so that fee goes away. The part
count goes 68 to 72 assembled references, and 30 to 32 distinct LCSC codes (one removed, three added: C12891, C21190, C492403).
J7 is through-hole and C21190/C12891 are basic, so J7/R48-R50 should not add a setup fee (the live quote is definitive).

AP63205 datasheet guidance is 22-68 uF of ceramic output capacitance. Two 22 uF 25 V X5R parts at 5 V bias (20 % of rating)
should keep roughly 12-14 uF each, so about 25 uF in total. **That is an estimate from typical DC-bias behaviour, not a
measurement or a vendor-confirmed figure.** It is at the low end of the window and gives less margin than the X7R 1210 pair, so
check the 5 V ripple and a load step on the first board. The 1206 pad centres are the same as the 1210 ones (34.975 and
32.025 at x = 66.5 and 70.5), so every track still lands; the pads are 1.15 x 1.8 mm instead of 1.15 x 2.7 mm.

C9 stays X7R C303950. The raw input sees the highest voltage and temperature stress, and the Rev3E quote review
(`pcb/rev3e/QUOTE-AND-COST-REVIEW.md`) says not to trim C9 to save fees on the first build.

## 3D models

`design/models/` is not copied. It was a byte-for-byte copy of `pcb/rev3e/design/models/` (about 30 MB), so the board and the three
project footprint libraries point at `${KIPRJMOD}/../../rev3e/design/models/`. Rev3H therefore needs `pcb/rev3e/design/models/`
to exist in the checkout. Checked: `kicad-cli pcb export step --subst-models` of Rev3H and of Rev3G give the same STEP entity
count (242244) and byte size, with no missing-model warnings.

## Verification (all on the final design, pinned KiCad 9.0.9 container)

| Check | Result | Evidence |
| --- | --- | --- |
| ERC, `--severity-all` | 0 violations | `validation/ERC.json` |
| DRC, `--schematic-parity --all-track-errors --severity-all`, run on a fresh rsync copy of `design/` | 0 violations, 0 unconnected, 0 parity | `validation/DRC.json` |
| Netlist diff vs Rev3G (Sheetfile rename ignored) | Added J7, R48, R49, R50 and nets `Net-(J7-Pin_2/3/4)`; the three taps join `GEA2_RX`, `GEA3_TX`, `GEA3_RX` and J7.1 joins `GND`; C16/C17 value, footprint, datasheet, MPN, LCSC and Dielectric fields. Nothing else | `validation/netlist-diff-vs-rev3g.txt` |
| Board diff vs Rev3G | Footprints added J7, R48-R50; C16/C17 footprint changed at the same centre and rotation; 15 tracks/vias added and 3 removed (the old JP4 via and its two tracks) | `validation/pcb-diff-vs-rev3g.txt` |
| `.kicad_pro` | Identical to Rev3G apart from the filename | |
| BOM/CPL | 72 assembled references, 32 unique LCSC codes; CPL is identical to Rev3G's review CPL except the four added references; J1 uses the reviewed body datum 8.645, -16.995 | `manufacturing/BOM-GEA-Adapter-Rev3H.csv`, `manufacturing/CPL-GEA-Adapter-Rev3H.csv` |

The ERC/DRC were run in the pinned image without overriding `HOME`; with `HOME=/tmp` that image does not see the stock footprint
libraries and DRC reports 87 spurious `lib_footprint_issues`, which are not real. The placement-origin receipt
(`validation/placement-origin-review.json`, from `validation/make_origin_evidence.py`) binds the unchanged J1 datum to the Rev3H source
hashes. The manufacturing set is regenerated with `python3 pcb/rev3h/manufacturing/generate.py` from the repository root in the
pinned image, after the receipt.

## Not verified

- Nothing has been built or measured. J7 has not been exercised with a real adapter, and the loading of the bus taps (1k plus
  the adapter's input) on the 3.3 V buffer nets is only reasoned, not measured.
- Case fit is CAD-only. Above the board, J7 (8.6 mm) has at least 19.4 mm under both Rev3G closed-USB lids (ray-cast, both frame
  orientations). Below the board, J7's ~3 mm pin tails need the pocketed base in `case/`; the Rev3G base would be hit. Not printed.
- The C16/C17 effective capacitance, ripple and load-step behaviour are an estimate (above). The datasheet window of 22-68 uF is as
  given in the design brief, not re-read here.
- JLC basic/extended status of C12891, C21190 and C492403, stock and price are as given, not re-checked against a live quote.
- Gerbers (`manufacturing/GERBER-GEA-Adapter-Rev3H.zip`) are generated from the source but were not opened in a viewer or put through
  a fabricator DFM check.
- Rev3H is registered in `ci/manifest.json` (commit 4d8cb8c): inventory, hardware, manufacturing and rules pass; release is blocked
  by design until bench evidence exists.
- **Order with 1 oz inner copper.** The board file has no stackup block, so the copper weight is chosen at order time; the
  quoted Rev 3E reference used 1 oz inner, and the In2 power routing (from Rev3F) was sized for it.
- The JP4 via's new spot is the only free one nearby; its tightest gaps are 0.222 mm (In2 `Net-(JP4-B)`) and 0.227 mm
  (B.Cu `GEA_FullTx`) against the 0.2 mm rule.
- All the Rev3G open items (supplier datum, socket and module fit, power qualification) carry over unchanged.
