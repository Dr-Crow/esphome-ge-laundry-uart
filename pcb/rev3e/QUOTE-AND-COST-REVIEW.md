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

## Before manufacture

Confirm the live checkout total, eFuse stencil geometry and thickness, U9/U10 placement, J1/J5/J6 through-hole placement, factory tooling and appropriate inspection on the exact release package. JLCPCB's [Review Before Payment](https://jlcpcb.com/help/article/review-before-payment-service-for-pcba-orders) creates an unpaid order and is not part of this quote-only check. The native validation gate and isolated hardware bring-up remain separate from quoting.
