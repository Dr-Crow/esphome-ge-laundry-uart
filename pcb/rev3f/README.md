# Rev 3F GE appliance adapter: experimental review

**Not released for ordering or appliance use.** The quoted Rev 3E, 1 oz inner copper, remains the reference for first articles. Use 1 oz for a Rev 3F first article if reviewing the candidate. Treat 0.5 oz as a separate, conditional comparison using the same artwork. No powered testing, factory approval or assembled Rev 3F quote.

Start with [the engineering review](OPEN-FIRST.html) (open locally in a browser), the [native KiCad project](design/GEA-Adapter-Rev3F.kicad_pro), [schematic](evidence/schematic.pdf), [BOM](assembly-review/BOM-3F-review.csv), [placements](assembly-review/CPL-3F-review.csv), [CAM for review only](evidence/Rev3F-CAM-review-only.zip) and [bench acceptance plan](evidence/first-article-plan.md). See the [Rev 3E model provenance](../rev3e/design/models/README.md) and the retained [Seeed asset notice](design/models/XIAO-ASSET-LICENSE.md). The KiCad local preferences file is not tracked.

## Changes and cost

- Eight regulated-rail bypass sites changed from Samsung C28233 to YAGEO C14663, a 100 nF 50 V X7R used elsewhere on the board. No raw-input capacitor changed. 69 placements, 31 unique parts (from 32); no feeder fee credit. Keep the raw input reservoir, inductor, eFuses, TVS parts, sockets and debug access.
- Widened 16 In2 segments across PIN1 VDC, XIAO 5 V and 3.3 V branches, added one local ground stitching via, and split the paste openings on U9/U10 without changing their copper land pattern. Placement file exactly matches the reference. KiCad 9.0.9 ERC and all-track DRC with schematic parity passed; 216 pin-to-net memberships match.
- Five-carrier pre-freight/pre-tax basis: [quoted Rev 3E 1 oz](../rev3e/QUOTE-AND-COST-REVIEW.md) $94.22; modeled 3F 1 oz $93.78, or $77.07 if the separate $16.71 bare-board copper differential translates to assembly. Neither 3F value is a quote. For bring-up, a same-stack quote for five fabricated with only two assembled is an alternative cost lever, not yet priced. Bare extras may have tinned pads. Compare landed prices before making a quantity decision.

## Why half-ounce is not signed off

At room temperature, the modeled half-ounce 3F spans are 34.7 mΩ on PIN1 and 28.4 mΩ on the XIAO 5 V path, compared with 33.7 and 25.8 mΩ on quoted 3E at 1 oz. Under the separate 85 °C/80%-width screen the assumed 0.60 A drops 32.7 and 26.7 mV, respectively; actual input/output currents differ across the regulator. At 15.24 µm a 1.00 mm inner run screens to about 0.65 A at +10 °C by [IPC-2221 curve fit](https://www.advancedpcb.com/en-us/tools/trace-width-calculator/), or 0.56 A at 80% width. Not a thermal or current rating. The eFuse nominal limit is around 1 A; 0.60 A is only a scenario. Confirm the factory's actual finished cross-section, plating, return paths and stencil.

Before any appliance connection, use the isolated current-limited fixture in the plan: compare PIN1/PIN3 startup, supply handoff, rail minima, hot-plug transients, grounds and sustained Wi-Fi with both modules. The AP63205 cannot boost a 4.3 V input to 5 V, and the raw-input TVS clamp test point is close to the eFuse absolute maximum before ringing. Establish the startup baseline at J1 without a series current meter before repeating with a characterized shunt or a current probe. ILM pads are useful to observe handoff, but verify the actual pad map and total capacitive loading below 50 pF per [TI's layout guidance](https://www.ti.com/lit/ds/symlink/tps25947.pdf); gain is unqualified below 0.5 A. Leave R38 fitted. Never connect an appliance and host USB together.

[Input hashes and toolchain](evidence/input-identities.json) · [Copper calculation](evidence/inner-span-model.csv) · [Repository snapshot checksums](SHA256SUMS).
