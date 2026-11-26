# Rev 3E prototype quote and cost review

Snapshot: 2026-11-25. Five 99 × 40 mm four-layer carriers, Economic top-side assembly, 1 oz inner copper. This is a quote for the submitted Rev 3E Gerber/BOM/CPL set, not the later stencil-only trial. It does not qualify the hardware or release it for manufacture.

## Verified quote

| Item | Five boards (USD) |
| --- | ---: |
| PCB special | 8.00 |
| Inner copper option | 16.71 |
| PCB subtotal | 24.71 |
| Assembly setup + stencil | 9.79 |
| Components (32 line items) | 28.04 |
| Extended-component fees | 24.72 |
| SMT assembly labor | 1.53 |
| Hand-soldering labor | 3.61 |
| Manual assembly | 1.82 |
| Assembly subtotal | 69.51 |
| PCB and assembly subtotal | **94.22** |
| Earlier freight preview, not a confirmed checkout rate | 25.99 |
| Subtotal with freight preview, before duties and tax | **120.21** |

All seven previously unchecked placements were enabled using the original BOM parts: C2/C20/C21 (C28323, 15 total), J5/J6 (C2897370, 10 total), U4/U5 (C151607, 10 total). No substitutions. Via covering, panel fee, large-board fee and selected build-speed surcharge were zero. Economic packing is listed as free; the factory assembly stencil is not a shipped item. No separate targeted X-ray line was shown. No order was placed. U.S. personal shipments can have prepaid import duties; confirm the live landed total rather than treating freight as duty-inclusive. [JLCPCB pricing](https://jlcpcb.com/help/article/pcb-assembly-price) · [U.S. tariff policy](https://jlcpcb.com/help/article/us-tariff-policy-faq).

## Module and socket decision

The quote includes the two removable XIAO sockets per carrier, not a XIAO. Five [pre-soldered C3s](https://www.seeedstudio.com/Seeed-Studio-XIAO-ESP32C3-Pre-Soldered-p-6331.html) at $5.90 make the provisional carrier + module total $149.71 including carrier freight preview, before module freight, duties/tax, enclosure and cable. The [pre-soldered C6](https://www.seeedstudio.com/Seeed-Studio-XIAO-ESP32C6-Pre-Soldered-p-6328.html) at the listed $6.20 gives $151.21 on the same basis.

JLCPCB catalogs the [Seeed XIAO ESP32-C3 113991054 / C18212168](https://jlcpcb.com/partdetail/Seeed-113991054/C18212168) as an Extended SMD part. That makes a permanent factory-placed C3 variant worth quoting, but it does not confirm stock, low-quantity allocation, final landed price, antenna handling, or compatibility with the existing socket-only land pattern. Treat it as a separate layout and mechanical variant. Retain socketed C3/C6 for first articles and field replacement.

## Cost-down priorities, not BOM changes

- The clearest lever is eliminating distinct Extended SKUs where a physically and electrically verified Basic substitute exists. Use the live quote to confirm the fee actually disappears; do not assume each placement adds a separate fee. Repeated parts such as U9/U10 already share a SKU.
- Do not remove the eFuses, ESD protection, or C9 to save fees on the first build. Protect the regulator's required inductor and capacitor characteristics, TVS behavior, rectifier reverse-voltage and drop margin, and connector geometry. Catalog queries are screening only, not substitute approval.
- Compare 0.5 oz and 1 oz inner copper with otherwise identical options. [JLCPCB's stackup guide](https://jlcpcb.com/help/article/jlcpcb-copper-weight) lists 0.5 oz as the usual FR-4 inner default; eligibility depends on the selected stackup. Copper weight means foil thickness per layer, not the total area routed. Removing pours does not remove this surcharge. Before changing stackup, verify the current path layer by layer, voltage drop and heat at the low-voltage/load corners, via neckdowns, ground returns and the antenna keep-out; widen or parallel the power routes only where needed. Do not reduce board dimensions on price alone; check enclosure mounting, clearances and antenna fit first.

## Follow-up: sourcing and stackup screening

- **Factory-place a C3:** The manufacturer lists the matching [bare castellated SKU 113991054](https://www.seeedstudio.com/Seeed-XIAO-ESP32C3-p-5431.html) at $4.90 retail, including an antenna, versus $5.90 for the headered C3. This is not JLCPCB's price. Confirm five-unit Economic allocation, extra handling or feeder fees, and whether the antenna is supplied loose or attached. The known socket parts cost $1.643 for the batch; the C3s cost $29.50 separately. Before labor or freight changes, the factory-placed module needs to be below about **$5.61 each** if it adds a $3.09 feeder fee with no offset, or **$6.23 each** if a removed socket feeder fee offsets it. Requote; do not subtract the entire through-hole labor charge because J1 remains. Even at $4.90 with an incremental $3.09 fee, the modeled savings are only $3.55 for all five before labor and freight. A direct-mount variant needs a verified land pattern, USB/button and antenna clearance, and a mechanical fit check.
- **Feeder fees:** $24.72 is eight $3.09 equivalents, and it matches the BOM exactly. The as-quoted BOM has 8 SMT Extended SKUs: C9 (C303950), C16/C17 (C309062), D11 (C82288), D18/D20 (C2994190), L1 (C305174), U4/U5 (C151607), U8 (C2071056) and U9/U10 (C3662799). The other non-basic codes were not charged: J1 (C3097717) and J5/J6 (C2897370) are through-hole, and R31/R38 (C23146) and U11 (C85364) are JLC preferred parts. (An earlier version of this line listed ten candidates including J1, J5/J6 and U11 and omitted C16/C17; corrected 2026-11-26. The Rev 3E README now gives the same 8.) Confirm per-SKU status in the live assembler before relying on it for a different BOM. There is no verified fee-free drop-in from this screening. Moving C16/C17 to the basic C12891 (22 µF 25 V X5R 1206) is the one candidate inside the AP63205's 22–68 µF output guidance; see Rev 3H.
- **What to price first:** [C89632](https://jlcpcb.com/partdetail/CL31B106KBHNNNE/C89632) matches C9's nominal 10 µF/50 V/X7R/1206/±10% specs but is also Extended; confirm capacitance under DC bias and landed price before using it. [TI C37708](https://jlcpcb.com/partdetail/TexasInstruments-SN74LVC2G07DBVR/C37708) is a U4/U5 sourcing fallback and is also Extended; verify fit and bus behavior. Screen L1 only against matching footprint, inductance, saturation current, DCR and temperature rise. Keep D11's drop and reverse-voltage margin, D18/D20's clamp envelope, the dedicated buck/protection ICs, and the exact connectors for the first batch. Removing one real feeder would save about $3.09 per order, not per board.
- **Copper A/B:** If the only change in the live quote is removing the $16.71 option, the $94.22 manufacturing subtotal becomes $77.51 and the subtotal with the same freight preview becomes $103.50, both unverified. Roughly 17 µm inner foil has about twice the sheet resistance of 35 µm at equal geometry. Width, parallel copper and via sizing can recover electrical margin; measure/estimate the actual stackup and loaded voltage drop by net, especially the VIN/5 V path and returns. This is a stackup optimization, not a call to delete copper, shrink the PCB, or replace the four-layer design. Thickness basis: this file and the other Rev 3E docs use nominal foil, 35 µm (1 oz) and 17.5 µm (0.5 oz). The Rev 3F/3G docs use 30.48 µm and 15.24 µm (1.2 and 0.6 mil), about 13% thinner, so the same trace reads about 15% higher in resistance there (for example 29.3 vs 33.7 mΩ for the J1 VDC In2 run). Compare numbers within one basis only.

## Before manufacture

Confirm the live checkout total, eFuse stencil geometry and thickness, U9/U10 placement, J1/J5/J6 through-hole placement, factory tooling and appropriate inspection on the exact release package. JLCPCB's [Review Before Payment](https://jlcpcb.com/help/article/review-before-payment-service-for-pcba-orders) creates an unpaid order and is not part of this quote-only check. The native validation gate and isolated hardware bring-up remain separate from quoting.
