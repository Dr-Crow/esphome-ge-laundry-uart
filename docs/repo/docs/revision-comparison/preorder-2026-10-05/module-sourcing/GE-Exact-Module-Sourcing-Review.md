# GE module sourcing and compatibility review

Reviewed **5 October 2026, 12:58–13:18 UTC**, against checkout **11826a7f6ba1ed19131ddba46e4d62b06196a8c6**. This is a public sourcing and source-CAD review. No purchasing, reservation, consignment, supplier-session change, BOM substitution, redesign or physical test was performed.

**Rev3B has an external exact-SKU sourcing route:** Seeed and DigiKey list bare XIAO ESP32C3 **113991054**. This does not clear JLCPCB's module shortage, confirm the supplied PCB revision, or qualify the soldered assembly. The distinct **101991467 tape/reel** SKU is a promising review candidate. Preheadered C3, C6 and S3 modules are not proven replacements for Rev3B's soldered 22-pad module.

## Source identity by revision

| GE revision | Actual module interface | Exact sourcing identity | Qualification boundary |
|---|---|---|---|
| Rev1.0 | U3, generic classic ESP32 development board; 38 PTH positions, two 19-pin rows at **2.54 mm pitch / 22.86 mm row spacing** | No manufacturer, MPN or purchased module revision established | Keep identity unresolved. A classic ESP32 firmware target does not identify a physical devboard. |
| Rev2.0 / 2.1 / 2.2 / 3 A | U2, ESP32-C3-WROOM-02; **18 edge contacts + ground pad 19**; carrier includes ground-pad vias and separate paste apertures | **ESP32-C3-WROOM-02-N4 / C2934560**; Rev2.0 purchasing code is also preserved in Description | Exact N4 procurement is preferable to changing chip/module family. |
| Rev3B | U2, **XIAO ESP32-C3 v1.3**, custom **22-contact SMD** land pattern; EN and ground underneath are wired | **Seeed113991054 / C18212168** | Require bare, header-free module, correct revision/contact layout and approved assembly process. |
| Rev3C | J5/J6, two HCTL PM254-1-07-Z-8.5 female sockets; **all 14 side pins** | Separately installed XIAO C3 **113991054** or C6 **113991254** | Modules and male headers are excluded from carrier quotes. Installed height, header engagement, USB/buttons and RF remain physical checks. |

All numbered carrier contacts, coordinates, functions and nets are in [carrier-module-pads.csv](carrier-module-pads.csv). The WROOM footprint contains 40 KiCad pad primitives because ground-pad vias and nine unnumbered paste apertures share the physical package; it has 19 numbered electrical contacts, not 40 module pins.

## Public availability, separated by inventory owner

Prices are USD per unit unless specified. These are inspected public observations, not allocation or fulfillment commitments. Crawl age is preserved because opening a page does not guarantee fresh inventory.

| Part / inventory owner | Public observation | Evidence age | Source |
|---|---|---|---|
| C3 **113991054**, Seeed | In stock, **$4.90**, count not exposed | Today | [Manufacturer](https://www.seeedstudio.com/Seeed-XIAO-ESP32C3-p-5431.html) |
| C3 **113991054**, DigiKey US | **9,888**, **$5.25**; headers not installed; U.FL antenna included | Today | [Exact manufacturer number](https://www.digikey.com/en/products/detail/seeed-technology-co-ltd/113991054/16652880) |
| C3 **C18212168**, LCSC | **Out of Stock** on canonical page; older 42–64-unit views conflict | Today; conflicting views 2–4 weeks old | [LCSC](https://www.lcsc.com/product-detail/C18212168.html) |
| C3 **C18212168**, JLCPCB | Exact Extended/SMT catalog listing; present orderable quantity unverified in public text | Last month | [JLC catalog](https://jlcpcb.com/partdetail/SEEED_DEVELOPMENTLTD-113991054/C18212168) |
| C3 **101991467**, Seeed tape/reel | In stock, **$4.49**, **10+ $4.20**, count not exposed | Today | [Manufacturer](https://www.seeedstudio.com/Seeed-Studio-XIAO-ESP32C3-Tape-Reel-p-6471.html) |
| C3 **102010633**, Seeed pre-soldered | In stock, **$5.90**, count not exposed | Today | [Manufacturer](https://www.seeedstudio.com/Seeed-Studio-XIAO-ESP32C3-Pre-Soldered-p-6331.html) |
| WROOM **N4**, Espressif | Exact manufacturer listing and distributor links; manufacturer stock not published | Today | [Manufacturer](https://www.espressif.com/en/products/modules/esp32-c3) |
| WROOM **C2934560**, LCSC | **4,369**, **$3.3224**;10-unit tier **$2.9217** | Today | [LCSC](https://www.lcsc.com/product-detail/C2934560.html) |
| WROOM **N4**, DigiKey US / Mouser US | **5,185 / 8,238**, **$3.38 / $3.64** |3 / 4 days old | [DigiKey](https://www.digikey.com/en/products/detail/espressif-systems/ESP32-C3-WROOM-02-N4/14553036), [Mouser](https://www.mouser.com/en/ProductDetail/Espressif-Systems/ESP32-C3-WROOM-02-N4?qs=stqOd1AaK7%2FqjTZKEOgfUg%3D%3D) |
| WROOM **C2934560**, JLCPCB | Exact listing; current public quantity unverified. Cached 6,055 stock / 5,167 available is historical | Yesterday listing; counts 3 weeks old | [JLC catalog](https://jlcpcb.com/partdetail/ESP32-C3-WROOM-02-N4/C2934560) |
| C6 **113991254**, Seeed / DigiKey US | Seeed In stock **$5.20**; DigiKey **229 at $5.38**, headers not installed; external antenna not included | Today | [Seeed](https://www.seeedstudio.com/Seeed-Studio-XIAO-ESP32C6-p-5884.html), [DigiKey](https://www.digikey.com/en/products/detail/seeed-technology-co-ltd/113991254/24613066) |

Seeed itself [names DigiKey, Mouser and Arrow as distributors](https://www.seeedstudio.com/blog/distribution-service/). Espressif's module page provides DigiKey/Mouser purchasing links. Loose-board inventory cannot be transferred into a JLC assembly quote by assumption. Complete A/C quote evidence and B's previous shortage remain separate supplier observations. This pass did not refresh an authenticated quote.

Full stock/cache conflicts, packaging and price limits: [availability evidence](public-stock/module-availability-2026-10-05.json). **113991355 is unidentified**; it must not be treated as a verified C3 preheader SKU. Seeed's [packaging PCN](https://files.seeedstudio.com/wiki/Seeeduino-XIAO/res/PCN-XIAO_Series_Packaging_Upgrade.pdf) independently identifies preheadered C3 as 102010633 and C6 as 102010636.

## Screened alternatives

“Exact sourcing” means the same manufacturer identity from another seller, with lot/assembly checks still required. “Proven drop-in” would require the complete electrical, physical and firmware replacement case. No different module SKU is assigned that full classification here.

| Candidate | Target | Classification | Evidence and remaining difference |
|---|---|---|---|
| Bare **113991054** from Seeed/DigiKey | Rev3B | **Exact sourcing**, conditional on v1.3 lot | Same SKU; current official C3 SMD library matches all 22 carrier-library pads. Store SKU alone does not specify supplied hardware revision, reflow history or shipment format. |
| **101991467**, C3 tape/reel | Rev3B | **Review candidate** | Manufacturer's [20 September2026 datasheet](https://files.seeedstudio.com/Bazaar/product_pdf/101991467.pdf) describes a single-sided SMD C3 with no through-hole headers. Different SKU: verify all 22 contacts/lot revision, antenna bundle, feeder/reflow data and assembly-library eligibility. |
| **102010633**, C3 preheadered | Rev3B / Rev3C | **Redesign or different assembly approach for B; header-fit review for C** | Installed pins prevent the intended flat soldered22-pad seating. C's two sockets are the appropriate interface concept, but pin length/section, mating depth and installed height need measurement/drawings. |
| Earlier C3 v1.0/1.1/1.2 under base SKU | Rev3B | **Review candidate** | Current vendor revision history records charger, SoC and crystal/component changes. v1.2 mechanical drawing supports nominal side/header and underside locations; it does not certify every earlier revision or actual supplied lot. |
| **113991254**, XIAO C6 | Rev3B / Rev3C | **Redesign/requalification for B; as-designed module option for C** |24 SMD contacts; different hidden battery/BOOT pads and side GPIOs. C already has separate C6 firmware and consumes only14 side contacts. Its module buttons/USB provide the download controls. |
| **113991114**, XIAO S3; Sense/Plus variants | Rev3B / Rev3C | **Redesign/requalification** | S3 has25 SMD contacts, different GPIOs/boot pin, memory, power and firmware target. Sense/Plus add contacts/components; no reviewed GE S3 profile. Shared XIAO outline is insufficient. |
| **ESP32-C3-WROOM-02-H4** | Rev2.x /3 A | **Review candidate; package/pin compatibility established** | Same 19-pin definition, 18×20×3.2 mm package and 4 MB flash in manufacturer's common datasheet; ambient rating changes 85→105 °C. No complete assembled-system substitution test performed. |
| **ESP32-C3-WROOM-02-N8** | Rev2.x /3 A | **Review candidate; package/pin compatibility established** | Same package/pins; 4→8 MB flash requires firmware/partition and sourcing review. |
| **ESP32-C3-WROOM-02U-N4** | Rev2.x /3 A | **Review candidate with RF/mechanical changes** | Same pin functions but18×14.3×3.2 mm body; U.FL-compatible external antenna connector replaces PCB antenna. Cable, antenna/connector clearance and appropriate land-pattern placement need review. Antenna is not supplied by default. |
| **ESP32-C3-MINI-1-N4X / MINI-1U-N4X**, bare C3 SoC, generic C3 devboard | Any current interface | **Redesign** | Different lands/pin numbering and body. MINI-1 uses 53 numbered lands and 13.2×16.6×2.4 mm body; the U version is shorter. No XIAO regulator, USB connector or buttons on bare radio modules. |
| Official **ESP32-DevKitC V4**, WROOM version | Rev1 | **Redesign / incompatible physical rows** | [Official drawing](https://dl.espressif.com/dl/schematics/esp32_devkitc_v4_dimensions.pdf) gives25.40 mm header rows versus source 22.86 mm. WROVER versions also reserve GPIO16/17 used by Rev1. No exact Rev1 devboard replacement established. |

WROOM variant facts come from the [Espressif common datasheet v1.7](https://www.espressif.com/sites/default/files/documentation/esp32-c3-wroom-02_datasheet_en.pdf), §§1.2,3,10,11. MINI facts: [manufacturer datasheet](https://documentation.espressif.com/esp32-c3-mini-1_datasheet_en.html). DevKitC variants: [official guide](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html).

## All XIAO side pins and hidden contacts

Numbers below are **module SMD-library pad numbers**, not MCU package pins. Source: Seeed's [official footprint/symbol collection](https://github.com/Seeed-Studio/OSHW-XIAO-Series/tree/main/Seeed%20Studio%20XIAO%20Series%20Library), plus current [C3](https://files.seeedstudio.com/wiki/XIAO_WiFi/Resources/XIAO_ESP32C3_v1.3_SCH_260116.pdf), [C6](https://files.seeedstudio.com/wiki/SeeedStudio-XIAO-ESP32C6/XIAO_ESP32_C6_v1.0_SCH_260114.pdf) and [S3](https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/) manufacturer documentation. Underneath-pad numbering is variant-specific.

| Pad / label | C3 GPIO | C6 GPIO | S3 GPIO | GE side-interface function |
|---|---:|---:|---:|---|
|1 D0|2|0|1|Red/debug LED|
|2 D1|3|1|2|Green LED|
|3 D2|4|2|3|Yellow LED|
|4 D3|5|21|4|GEA2 MCU TX|
|5 D4|6|22|5|Unused side pin|
|6 D5|7|23|6|Unused side pin|
|7 D6|21|16|43|GEA3 MCU TX, carrier net GEA3_RX|
|8 D7|20|17|44|GEA3 MCU RX, carrier net GEA3_TX|
|9 D8|8|19|7|Carrier BOOT_SEL|
|10 D9|9 /BOOT|20|8|Carrier BOOT; actual BOOT only on C3|
|11 D10|10|18|9|GEA2 MCU RX|
|12 3V3_OUT|Regulator output|Regulator output|Regulator output|Carrier3.3 V rail|
|13 GND|Ground|Ground|Ground|Ground|
|14 VBUS|USB VBUS /5 V|USB VBUS /5 V|USB VBUS /5 V|Carrier5 V rail|

| Hidden pad number | C3 22-pad | C6 24-pad | S3 25-pad |
|---|---|---|---|
|15|D3/GPIO5/MTDI|GPIO5/MTDI|GPIO41/MTDI|
|16|D5/GPIO7/MTDO|GPIO7/MTDO|GPIO40/MTDO|
|17|EN|EN|EN|
|18|GND|GND|GND|
|19|D2/GPIO4/MTMS|GPIO4/MTMS|GPIO42/MTMS|
|20|D4/GPIO6/MTCK|GPIO6/MTCK|GPIO39/MTCK|
|21|VBAT|GPIO9/BOOT|USB DN|
|22|GND|3V3_OUT|USB DP|
|23|Absent|VBAT|VBAT|
|24|Absent|GND|GND|
|25|Absent|Absent|PAD; electrical meaning must be checked against exact source/variant|

Rev3B wires underside pad 17 to EN and pads 18/22 to GND; underside pads 15/16/19/20/21 are unconnected carrier lands. **Pad numbers do not establish geometric overlap:** C6's battery lands 23/24 are at different positions from C3's 21/22. Same-number comparison found 14 exact C6 pad geometries, 8 different and 2 extra; S3 found 20 same, 2 different and 3 extra. This is geometry evidence, not proof of compatible net function.

Rev3B's local C3 library and the current vendor C3 library match **all 22** normalized number/type/shape/position/size/layer definitions. Side SMD land centers span16.165 mm with 2.54 mm pitch. The actual module's male-header holes use 15.24 mm row spacing; Rev3C sockets are also 15.24 mm apart. These are different mating interfaces. The [v1.2 underside drawing](https://files.seeedstudio.com/wiki/Seeed-Studio-XIAO-ESP32/XIAO_ESP32C3_v1.2_Dimensioning.zip) also shows unnumbered 2.794 mm ground/thermal copper. It is not an invented 23rd contact in Rev3B's official 22-pad footprint; inspect the actual underside and process clearances.

Detailed coordinate/size differences: [land-pattern-comparison.json](land-pattern-comparison.json). Manufacturer module contacts and carrier placement: [module-pad-evidence.json](module-pad-evidence.json).

## WROOM contacts, physical features and firmware

WROOM-02 N4, H4 and N8 share these pin functions: **1=3V3,2=EN,3=IO4,4=IO5,5=IO6,6=IO7,7=IO8,8=IO9,9=GND,10=IO10,11=IO20/RXD,12=IO21/TXD,13=IO18/USB DN,14=IO19/USB DP,15=IO3,16=IO2,17=IO1,18=IO0,19=GND exposed pad**. There is no onboard USB socket, regulator, charger, header or pushbutton; the carrier supplies these functions. Supply is 3.0–3.6 V, not 5 V. The 19-pad interface differs completely from a XIAO module, despite the shared C3 processor.

| Feature | XIAO C3 v1.3 | XIAO C6 v1.0 | XIAO S3 base | WROOM-02-N4 |
|---|---|---|---|---|
|Nominal body|21×17.8 mm|21×17.8 mm|21×17.8 mm|18×20×3.2 mm|
|Flash / PSRAM|4 MB / none|4 MB / none|8 MB / 8 MB|4 MB / none|
|USB /buttons|Onboard USB-C, native Serial/JTAG; EN andGPIO9 boot|Onboard USB-C, native Serial/JTAG; EN andGPIO9 boot|Onboard USB-C; EN andGPIO0 boot|Chip USB pins only; external EN/boot controls|
|RF /U.FL|External antenna required; module U.FL, retail antenna included|Onboard ceramic antenna or U.FL; RF switch GPIO3 low enables, GPIO14 selects antenna|External U.FL antenna; Sense adds camera/mic/SD, Plus differs further|PCB antenna;02U instead uses external connector|
|Power conversion|5 V VBUS input, TLV75733 LDO; underside battery/charger circuitry|5 V VBUS input, SGM6029 buck; distinct battery/charger circuitry|5 V VBUS / battery circuitry; load and regulator differ|Carrier-regulated3.3 V input|
|Headers|Base SKU bare;102010633 installed;101991467 tape/reel|Base113991254 bare;102010636 installed|Base113991114 bare;102010634 installed|No14-pin XIAO headers|

Both reviewed XIAO C3/C6 tie side VBUS to USB VBUS; using a different purchase package does not add isolation. The module 3V3 pin is treated as an output in the reviewed GE design. Module-store sleep-current figures do not qualify appliance startup or Wi-Fi burst current.

Firmware evidence was inspected rather than rebuilt in this sourcing pass. Rev2.x reference configurations target C3 and use GEA2 GPIO5/10 and GEA3 GPIO21/20. Rev3C has distinct C3 and C6 profiles: C6 uses GEA2 GPIO21/18 and GEA3 GPIO16/17, plus GPIO3/GPIO14 RF-switch control. These profiles demonstrate deliberate GPIO/target differences; they do not authorize loading a C6 image onto a soldered C3 carrier. Rev1 uses its separate classic ESP32 profile family. There is no reviewed S3 profile. Fresh integration build status belongs to the separate firmware audit; stored build receipts are historical evidence.

## Decision and remaining checks

1. Preserve **113991054/C18212168** for Rev3B; investigate bare exact-SKU availability and supplier acceptance without silently changing the BOM. Require actual v1.3 lot identity, underside/photo or drawing confirmation, moisture/reflow handling, packaging/orientation and accepted 22-pad process before production.
2. **101991467 tape/reel** is the best screened alternate SKU for an assembly review. It has manufacturer identity and header-free SMD packaging evidence, but not a proven lot-specific substitution or JLC part-code match.
3. Preserve **ESP32-C3-WROOM-02-N4/C2934560** for Rev2.x/3 A. H4/N8/02U are review options with explicit differences, not emergency purchasing substitutions.
4. For Rev3C, purchase the chosen C3/C6 separately and verify all 14 male pins against both sockets, engagement, installed Z, button/USB access and antenna/enclosure clearance. Carrier quotes exclude this cost and labor.
5. Keep **Rev1 devboard identity open**. The named official DevKitC V4 fails the source row spacing check. A generic38-pin seller listing or classic firmware build cannot close it.

These checks supplement the existing board/appliance electrical, thermal and RF qualification gates; none is closed by public stock or native CAD checks.

## Verification record

- [input-hashes.json](input-hashes.json):54 byte-hashed source/BOM/firmware/reference files, bound to 11826a7.
- [primary-source download manifest](primary-sources/download-manifest.json): public URLs, exact byte counts, SHA-256 and UTC retrieval times. Current C3 archive hash **477bc61cec652eaeefa887cb1f97abb1514e8a61ea9659240b88be7213c3b6ff**; current C6 archive hash **cea2ed66da575e4a1dd6c7a9acd60583ed4a9adbf6b1d2952851c1e4199c05fc**.
- `extract_module_evidence.py` (original analytical helper; recorded data/formulas below): reproducible read-only extraction. Parsed all seven carrier revisions, official C3/C6 boards and three manufacturer SMD patterns; checked all 22 C3 land definitions.
- Official DevKitC dimensions, C3 package drawing and v1.2 DXF were rendered and visually inspected. The 25.40 mm versus 22.86 mm Rev1 mismatch is a drawing/CAD measurement, not a guessed retail-board size.
- Web evidence records inspection and reported crawl age separately. No stock was reserved and no current authenticated JLC quantities, landed prices or assembly acceptance were claimed.
