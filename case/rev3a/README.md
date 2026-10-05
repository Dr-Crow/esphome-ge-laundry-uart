# Rev3A enclosure review

The editable Rev3A enclosure and optional captive-button source remain preserved at [original source a5a9fac](https://github.com/Dr-Crow/esphome-ge-laundry-uart/tree/a5a9fac87cbcb59d337a1fb8d3084ad18867a3e6/case/rev3a). Their physical geometry is unchanged. The [current A/B source review](review/REV3AB-ENCLOSURE-SOURCE-REVIEW.md) binds their interfaces to rated-board checkpoint bf5c231, with exact recovery and geometry receipts. This companion is a review prototype, not a physically qualified case.

## Correct USB opening dimensions

J4 is at carrier (72, 36.325), opening toward +Y. The source cutter spans **X64.5–79.5, Y39–46 and Z2–6.4 mm**. Its outward-facing X/Z opening is **15 mm wide × 4.4 mm high**; **7 mm is the cutter depth through Y**. The closed lid does not enlarge that opening. The original guide's “15 × 7 mm cable window” conflated these axes; use the corrected facing dimensions here.

The selected connector is SHOU HAN TYPE-C 16PIN 2MD(073)/C2765186. Exact mating-axis Z above the assembled 1.6 mm PCB, shell seating and the chosen seated plug remain unresolved. The retained locally named STEP internally identifies a six-pin model, so its height is not exact sixteen-pin mating evidence. The [documentation-only source patch](review/rev3a-usb-documentation-only.patch) records the correction; no opening resize is adopted from that generic model.

## Current applicability and limits

The carrier is **88.7 × 40 × 1.6 mm**. Mounting holes, J1/J2/J4, WROOM, switches and LEDs retain the source-case anchors. Default base/lid STEP/STL readback passes under the recorded pinned CAD environment. Current STPS140Z, TPS1H200A and fuse package screens clear the roofs at nominal seating; those are dimensional screens, not thermal or complete populated-assembly approval.

J1's exact full suffix, body-seat/tail datum, solder protrusion and cable/latch sweep remain to be authenticated. A conditional 0.15 mm tail/floor conflict depends on the retained 3 mm tail datum being measured from PCB top; live drawing retrieval did not reverify that assumption, so no pocket resize is adopted. J4 solder delivery/inspection/retention, switch make/force/overtravel, printing/fatigue, light visibility and RF/thermal behavior remain open.

J2 uses a programmer with 3.3 V logic; **leave UART VCC disconnected** and use one reviewed input supply. The enclosure does not qualify simultaneous USB/appliance power. Match the actual populated board and all qualified dimensions before choosing or printing a production case. Orders and powered testing require their separate review.
