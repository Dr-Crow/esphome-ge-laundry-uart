# Rev3E candidate: PIN3 overvoltage lockout, data-line ESD, debug provisions

Rev3E is Rev3D with small additions in three areas. The carrier is still 99 × 40 mm on four layers, with the same
XIAO C3/C6 sockets, RJ45, GEA2/GEA3 interface, TPS259470A eFuse priority mux and AP63205 buck. Every Rev3D part
keeps its position except D1–D3 (removed) and R37 (moved and changed in value). Same footprint outline, so the
Rev3D cases fit unchanged.

## What changed

| Area | Rev3D | Rev3E |
| --- | --- | --- |
| PIN3 overvoltage | None. U10 OVLO was used for PIN1 priority, so PIN3 had no overvoltage lockout | TI SLVSFC9C Fig. 8-13 (Option 2). U10 OVLO gets its own **R45 1M / R37 68k** divider: lockout ≈18.85 V rising / 17.1 V falling, the same as PIN1. **Q1 AO3400A** (C20917, basic) acts as a source follower: gate on AUXOFF1, drain on ALT_PWR, source on U10 OVLO |
| PIN1 priority | U9 AUXOFF drives U10 OVLO directly (Fig. 8-10) | Unchanged in behaviour. With PIN1 good, AUXOFF1 sits at 3.3 V (R36), so Q1 lifts U10 OVLO to about 1.85–2.65 V (AO3400A Vth 0.65–1.45 V). That is above the ≈1.2 V OVLO threshold, so U10 stays off. With PIN1 absent, AUXOFF1 ≤ 1.0 V keeps the lift ≤ ~0.6 V, so only the divider acts |
| Data-line ESD | BAV99 clamp to +5V/GND on each of J1 pins 4, 5, 7 (D1–D3) | One **SRV05-4** (C85364, preferred) TVS array on the same three lines (IO4 unused). It adds low-capacitance steering diodes and a rail-to-ground shunt clamp; REF still connects directly to +5V, so this is not rail isolation |
| 5 V debug link | D11 cathode tied straight to +5V | **R47 0R 0805** (C17477) between D11 cathode (`/D11_K`, Power class) and +5V |
| Test points | TP1–TP11 | **TP12** on BUCK_5V, before D11. Pad only, not populated |
| Bulk input cap | C9 10 µF | Optional **C30 47 µF 35 V 1210** footprint on V_INPUT, near C9 (not fitted) |
| Basic-part swaps | 5 extended passives | Swapped to basic parts with the same footprint and equal or better ratings: 100n 100V X7R 0805 → C28233, 1u 50V X7R 0805 → C28323, 100n 50V 0603 → C14663 (C10, and C15, where X7R replaces X8L; fine for the buck bootstrap cap), 220k 0805 → C17556 |
| Parts | 68 assembled refs, 31 unique. 16 non-basic: 15 extended + 1 preferred (no fee). Of the 15, 13 are SMT and carry the setup fee; J1 and J5/J6 are through-hole and appear fee-free | 69 assembled refs, 32 unique. 12 non-basic: 10 extended + 2 preferred (no fee). **8** SMT parts carry the setup fee, five fewer: $15.35 less per order in setup fees, $0.22 more per board in parts (JLC list prices, 2026-11-23). Estimated 5-board order ≈$102.66 vs ≈$116.66 for Rev3D |

Why Option 2 and not Option 3 (a single shared divider): with Option 3, PIN3-only operation would sit right at
the OVLO threshold with no margin. Option 2 keeps the full Rev3D PIN1 priority behaviour and gives PIN3 the
same lockout point as PIN1.

## Power, USB and batteries

As Rev3D: no battery is needed or supported, and **USB and the appliance must not be connected at the same
time**. Flash over USB with the carrier out of the appliance, then use ESPHome OTA updates.

| Situation | Protected? | Why |
|---|---|---|
| PIN3 above ~18.85 V with PIN1 absent | **Yes (new)** | U10 OVLO trips, keeping V_INPUT below U9's OUT abs max |
| USB power flowing back into the appliance's power pins | Yes | U9/U10 eFuses block reverse current |
| USB power flowing back into the buck | Yes | D11 blocks it |
| Appliance power flowing into the USB host | **No** | The XIAO 5V pin *is* USB VBUS. No carrier-side fix without a power switch on VBUS; use a USB isolator dongle if a live connection is ever needed |
| Appliance and USB grounds joined | **No** | Same as Rev3D |
| USB-only: appliance data lines | Partly | USB-powered +5V biases the SRV05-4 rail and the bus pull-ups even with the appliance off |

## Debug and rework provisions

| Provision | Purpose |
| --- | --- |
| TP8 / TP9 | PIN1 / PIN3 at the connector side of each eFuse |
| TP10 / TP11 | eFuse ILM pins: analog current monitor per channel |
| **TP12** | Buck output before D11. TP12 minus TP1 is the D11 drop under load |
| **R47** | Lift it to separate the buck from +5V. Then you can load the buck alone (measure at TP12), or power the XIAO from USB with the carrier power path out of the circuit |
| TP3, TP1, TP2, TP7 | V_INPUT, +5V, +3V3, GND |
| Remove R31 (or R38) | Holds U9 (or U10) off, to test the other input alone |
| Remove Q1 | Restores Rev3D-like behaviour minus priority: both eFuses run independently with their own OVLO |
| JP2 | GEA3 module TX source (unchanged from Rev3D) |

## Bring-up probe pads

These are bare pads only. They do not change the populated BOM or placement list.

| Ref | Signal | Access | Use |
| --- | --- | --- | --- |
| TP13 | AUXOFF1 | Front | U9 priority command at Q1 gate |
| TP14 | PIN3_OV | Back | Actual U10 OVLO voltage when PIN3 is inhibited or released |
| TP15 | GND_MUX | Both | Plated ground near the mux; reference for front/back measurements |
| TP16 | GND_ESD | Front | Local ground tied to the U11 return via; use a short probe ground |
| TP17 | PIN1_FLT_N | Front | U9 active-low open-drain fault |
| TP18 | PIN3_FLT_N | Back | U10 active-low open-drain fault |

The FLT pads have no on-board pull-up and do not drive or control any other circuit.
For isolated, current-limited bench bring-up, read them with a temporary pull-up to board
3.3 V (for example, 10 kΩ) and common ground. Use a high-impedance, low-capacitance
probe on AUXOFF1 and PIN3_OV; loading either can shift the measurement, especially with
a scope set to 50 Ω termination. Do not scope a connected appliance with an ordinary
ground-referenced probe or connect a USB host with the appliance attached.

The stock C30 population remains DNP. If tried, capture PIN3-only cold startup and a
handoff with PIN3 already present separately: the eFuse can bypass its dV/dt soft-start
during OVLO recovery. U11's direct REF connection and the power/protection topology are
otherwise unchanged.

## Verification status (digital only)

- **ERC:** native KiCad 9.0.9 at full severity, 0 errors / 0 warnings.
- **DRC:** all-track errors plus schematic parity, 0 violations, 0 unconnected, 0 parity differences, using
  the Rev3D `.kicad_dru` (U9/U10 courtyard clearance relaxation only).
- **Stock netlist:** 57 intended connections were asserted against the exported netlist, and
  D1–D3 confirmed gone. For the local probe-pad spin, netlist comparison found exactly the six new pads;
  U9/U10 FLT are now passive-access-only test nets. See [the probe validation receipt](validation/bringup-probe-pads.md).
- **BOM/CPL:** generated by `manufacturing/generate.py` from `kicad-cli` exports. The BOM differs from
  Rev3D only by the changes in the table above. J1 uses the unchanged EVERCOM body datum.
- **Live JLCPCB stock (2026-11-23):** every part in stock. Lowest is the existing 74LVC2G07 (506).

**Not done:** supplier quote and preview review, appliance pin measurements, bench power tests (including the
PIN1/PIN3 switchover with Q1 fitted), thermal and transient tests, enclosure fit. The release gates stay blocked
until there is physical evidence. Order Rev3D first if you only want a working board; Rev3E is the next spin.
