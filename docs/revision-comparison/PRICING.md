# Recorded assembly estimates

[Comparison](README.md) · [Project handoff](HANDOFF.md)

All prices are USD. Each quote is for five PCBs and assembly of all five
carriers. Shipping, tax, printed enclosures, appliance cables, external UART
programmers, optional SMA pigtails and screw-on antennas are excluded.
The comparison does not contain a final delivered quote or a purchase order.
Historical quotes do not price the pending corrected shared dual-input Rev3C.
The rejected PIN1-only experiment is not an accepted cost or part-count baseline.

| Revision | Quote date | PCB and assembly scope | Total for five | Per adapter |
| --- | --- | --- | ---: | ---: |
| Rev2.2 | September 19, 2026 | Fully assembled boards | $78.07 | $15.61 |
| Rev3A | October 1, 2026 | Fully assembled boards, including ESP32 module | $154.44 | $30.89 |
| Rev3B | October 1, 2026 | Assembled carriers with XIAO deliberately excluded | $112.08 | $22.42, incomplete |
| Rev3C carrier | October 1, 2026 | Assembled carriers, including female sockets | $114.65 | $22.93 |
| Rev3C with retail modules | October 1, 2026 | Carriers above plus five $5.99 pre-headered C3 modules | $144.60 | $28.92 |

## Rev3A

JLCPCB Economic assembly, top side, four layers, 88.7 × 40 mm, 1.6 mm,
lead-free HASL, ordinary vias. All 40 purchasing groups and 93 placements
were included, with no stock shortages reported at quote time.

| Charge | Batch of five |
| --- | ---: |
| PCB fabrication and lead-free finish | $13.10 |
| PCBA total | $141.34 |
| Vendor total | **$154.44** |

PCBA includes $49.50 in components and $74.16 in extended-component fees,
plus setup, stencil, placement and other assembly charges. No special-drill
or four-wire Kelvin-test surcharge appeared in this quote. The earlier
$149.96 planning estimate in the Rev3A README is superseded by this snapshot;
the hardware branch still needs that documentation update.

## Rev3B

Four layers, 99 × 40 mm, top-side Economic assembly, lead-free HASL.
PCB fabrication/finish was $13.10 and assembly $98.98, totaling $112.08.
The XIAO module could not be supplied for a complete batch at quote time.
The amount deliberately excludes the module, antenna and module installation.

A retail-module price added to this carrier amount does not establish a
factory-assembled price: sourcing, revision, antenna inclusion and soldering
still need a quote. JLC's import accepted standard-column private BOM/CPL
copies; that formatting follow-up remains outstanding on the hardware branch.

## Rev3C

Four layers, 99 × 40 mm, 1.6 mm, top-side Economic assembly, lead-free HASL.
The carrier quote included all 82 carrier parts in 33 purchasing groups,
including J1, J2 and both J5/J6 female sockets.

| Charge | Batch of five |
| --- | ---: |
| PCB fabrication | $8.00 |
| Lead-free finish | $5.10 |
| Assembly setup | $8.24 |
| Stencil | $1.55 |
| Components | $30.96 |
| Extended-component fees | $52.53 |
| SMT assembly | $1.93 |
| Hand-soldering labor | $3.61 |
| Manual assembly | $1.82 |
| Nitrogen reflow | $0.91 |
| Vendor carrier total | **$114.65** |
| Five retail modules at $5.99 | $29.95 |
| Combined estimate | **$144.60** |

Displayed charge lines are rounded independently; use the vendor total.
The retail module is [Seeed XIAO ESP32-C3 Pre-Soldered, SKU 102010633](https://www.seeedstudio.com/Seeed-Studio-XIAO-ESP32C3-Pre-Soldered-p-6331.html),
including its external antenna. The user seats it in the carrier sockets.

The carrier quote was made from source commit `163c98f`; the later source
head `38d94d3` includes case-alignment changes and the quote documentation.
No revised hardware quote was obtained for this comparison package.

## C6 and case costs

The [pre-headered C6, SKU 102010636](https://www.seeedstudio.com/Seeed-Studio-XIAO-ESP32C6-Pre-Soldered-p-6328.html)
was listed at $6.20, versus $5.99 for the C3: $0.21 more for the module only.
There is no Rev3D quote, and the final shared-carrier design is not qualified.
Do not report a Rev3D adapter price by simply adding that difference.

Printed cases, magnets and optional external antennas have not been quoted.
The $39.99 FirstBuild target is a comparison goal, not a delivered-cost claim.
Refresh component stock, module availability and all fees before ordering.

## Bounded October 3 component comparison

Public catalog snapshots compare only one fuse, one diode and one divider
resistor per board, including a 100-resistor minimum purchase. They are not
a complete BOM, assembled-board quote or required dual-input design price.

| Parts purchased | Five boards | Ten boards |
| --- | ---: | ---: |
| Littelfuse 1812L075/33DR + PMEG6010ER,115 + 2.4 kΩ resistor | $2.10 | $3.88 |
| Bourns MF-MSMF075/33X-2 + same diode/resistor | $5.13 | $9.32 |

Sources: [Littelfuse C151170](https://www.lcsc.com/product-detail/C151170.html),
[exact Bourns DigiKey](https://www.digikey.com/en/products/detail/bourns-inc/MF-MSMF075-33X-2/16357034),
[diode C456121](https://www.lcsc.com/product-detail/C456121.html),
[resistor C17526](https://www.lcsc.com/product-detail/C17526.html).
LCSC listed exact Bourns C3760814 unavailable in the checked snapshot.
The [JLC C151170 listing](https://jlcpcb.com/partdetail/Littelfuse-1812L07533DR/C151170)
confirms an Extended assembly part, without verified live price or stock.
LCSC stock does not establish JLC inventory. Manufacturer lands, thermal
response and qualification differ; the fuses are not asserted drop-in equivalents.

These totals exclude all other parts, PCB, module, assembly setup, placement,
attrition, shipping, tax and tariffs. Do not extrapolate the rejected experiment's
58-part count or these purchases into a finished adapter saving. The required
automatic dual-input power repair remains unquoted.
