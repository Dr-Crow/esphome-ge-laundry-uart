# Rev3C assembly dimensions and review limits

Reviewed October 5, 2026. The selected carrier retains both appliance power inputs, automatic PIN1 priority and interchangeable unmodified XIAO C3/C6 interfaces. The installed assembly, buttons, cables and printed case remain unqualified.

## Socket and installed height

J5/J6 are **HCTL PM254-1-07-Z-8.5 / C2897370**. The [manufacturer drawing](https://www.hctldz.com/static/upload/2026/01/28/202601285507.pdf) gives these limits:

| Feature | Nominal | Published range |
| --- | ---: | ---: |
| Body length | 18.18 mm | 17.88–18.48 mm |
| Body width | 2.50 mm | 2.35–2.65 mm |
| Body height above seat | 8.50 mm | 8.35–8.65 mm |
| Bare tail below seat | 3.20 mm | 2.95–3.45 mm |

The analytical proxies now use maximum body dimensions. The PCB and footprint courtyard extends 0.25 mm beyond that maximum, centred on the nominal row. Pads, holes, centroids, routes and the nominal fabrication body are retained. Body-to-pin registration and assembly-placement tolerances are unpublished and are separate terms.

The existing assumed male spacer range is 2.0–3.0 mm. Together with socket height, it implies **10.35–11.65 mm**, before unmeasured seating and solder lift. The analytical configuration accepts that full declared range. The [pinned endpoint receipt](review/socket-stack-endpoints.json) checks eight C3/C6/internal/external lower/upper cases with maximum socket bodies and conditional switch-height extremes: all have zero component and closure overlap with 0.25 mm release gap. Four lower-end lids pass STEP/STL readback under build123d 0.11.1 and trimesh 5.1.0. It is not a published range for the fitted factory header. A nominal 1.6 mm carrier leaves 1.35–1.85 mm of bare tail below the board; the existing 2.4 mm underside allowance provides 0.55 mm beyond that nominal-PCB maximum. Solder, board thickness and seating require their own bounds.

The drawing does not specify receiving-mouth width, contact-start depth, insertion stop, accepted mating-pin section/length, contact wipe or retention. Detailed cavities in retained illustrative STEP models must not be used as specifications.

## Factory module and header selection

Use the factory preheadered package candidates [C3 102010633](https://www.seeedstudio.com/Seeed-Studio-XIAO-ESP32C3-Pre-Soldered-p-6331.html) and [C6 102010636](https://www.seeedstudio.com/Seeed-Studio-XIAO-ESP32C6-Pre-Soldered-p-6328.html) for the no-user-solder assembly. Bare C3 113991054 and bare C6 113991254 are distinct packages. The manufacturer has not authenticated the retail fitted header MPN, assembled tolerances or supplied PCB revision in the public documents reviewed.

Loose Seeed 102010490, Samtec TSW-107-07-G-S and Würth 61300711121 are review candidates only. They require explicit factory assembly and mating qualification. The Würth drawing's independently derived spacer range is 1.94–3.14 mm, giving socket plus spacer **10.29–11.79 mm** before seating/solder; it cannot be declared covered by the generic 10.35–11.65 mm screen.

## BOOT and RESET

| Conditional reference | Height screen | Identity and actuation limit |
| --- | ---: | --- |
| C3 TD1183 family A | 1.4–1.6 mm | Archive names TD-1183SN-A3N-D1R. Family drawing supports 1.5 mm option; complete suffix, electrical make and safe overtravel unresolved |
| C3 TD1183 family B | 1.6–1.8 mm | Separate 1.7 mm family option; not interchangeable with an A-calibrated foot |
| C6 Jinbeili TS-1001S | 0.45–0.65 mm | Current schematic names this part; manufacturer gives 0.55 ±0.10 mm, but travel/make/overtravel absent |
| C6 Alps SKTAAAE010 | 0.43–0.63 mm | Older schematic/current PCB retain this different part; 0.53 mm height and 0.11 mm nominal travel do not establish safe overtravel |

The [Jinbeili drawing](https://www.jbl-ec.com/uploads/TS-1001S1_1.png), [Alps part](https://tech.alpsalpine.com/e/products/detail/SKTAAAE010/) and [TD1183 family drawing](https://atta.szlcsc.com/upload/public/pdf/source/20220901/234954DA4D26CA925E3AFEBBCE0B4B64.pdf) support separate conditional profiles. The C6 schematic/PCB conflict prevents assigning either to an actual retail lot. `export_review.py` requires independent BOOT/RESET heights and stops. Its illustrative stops are not manufacturer depression allowances. Never substitute a taller switch profile without recalibrating the foot and checking actuation limits.

## Real USB cable corridor

[StarTech USB2CC2M](https://www.startech.com/en-us/cables/usb2cc2m) is a named candidate, not a selected cable. Its [manufacturer drawing](https://sgcdn.startech.com/005329/media/sets/USB2CC2M/Diagram/USB2CC2M_Diagram.PDF) specifies a maximum **12.2 × 6.5 mm** overmold, maximum body length 22.7 mm, exposed shank 6.55–6.75 mm and maximum strain-relief length 12.4 mm. The older synthetic 12 × 6 mm plug gauge understates this candidate. Corners and cable-OD tolerance are undimensioned.

Both module archives identify native receptacle UBF31-0171. The retained GCT USB4105 body is a visual substitute, so its front face and axis height cannot establish native mating coordinates. With carrier +X pointing outward, define native mouth X as M, full metal-tip insertion as D and exposed shank as S. At full insertion, tip X is M−D and overmold shoulder X is M−D+S. The overmold then extends 22.7 mm, followed by up to 12.4 mm of relief. **Native M, D and axis Z are unresolved.** A parameterized corridor is useful, but a final cable-fit claim requires these coordinates or an actual seated-shoulder measurement.

The [named cable corridor screen](review/cable-corridor/README.md) now accepts explicitly supplied shoulder and axis coordinates, with source-hashed conditional results. It shows why the C6 body corridor depends on those unknown coordinates; it does not adopt a support cut or turn the GCT substitute into a native datum.

Disconnect the appliance RJ45 before powered USB. The case does not add USB backfeed isolation.

## Closure, light and antenna checks

The common base permits the wrong lid. A C3 BOOT foot can contact the C6 U.FL connector. Labels and an assembly check remain necessary. A [preserved separate review study](../review-studies/wrong-lid-pairs/README.md) demonstrates integral keyed base/lid pairs with nominal wrong-pair contact before latch engagement; these require changing both base and lid when changing module. They detect the pair, not the actual module. That tradeoff is not adopted into the common-base default.

Maximum capacitor relief, LED inlet registration and roof retention remain source-bound review features. Optical transmission, snap fatigue, print shrinkage, safe button force, antenna pigtail bend/slack, exact bulkhead hardware and RF performance require additional evidence. Partial module STEP models cannot close those limits.

## Evidence and next inputs

[Machine-readable dimensions](review/dimensions/dimension-evidence.json), [module schematic identities](review/dimensions/module-schematic-identities.json), [module PCB identities](review/dimensions/module-pcb-identities.json) and [source retrieval hashes](review/dimensions/retrieval-manifest.json) preserve the primary-source review against 77f4c88. This document records subsequent socket/range corrections; historical reports retain their original scope.

The minimum remaining inputs are the actual preheadered module/header revision and seated height; HCTL engagement/retention limits; fitted switch identity, released heights and make/overtravel/force bounds; native USB/selected seated-plug coordinates; and production printing/material tolerances. These are specific unresolved assembly inputs, not a claim that CAD or native PCB checks failed.
