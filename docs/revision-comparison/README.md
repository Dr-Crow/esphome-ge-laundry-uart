# Board and enclosure comparison

[Project overview](../../README.md) · [Pricing details](PRICING.md) · [C3/C6 and Matter options](C6-MATTER.md) · [Project handoff](HANDOFF.md)

Snapshot: October 2, 2026. Rev2.2 is the current manufacturing candidate;
Rev3A, Rev3B and Rev3C are design-review candidates with physical testing
outstanding. The source branches and exact revisions are linked below.

## Cost and functionality

USD, batches of five, with all five carriers assembled. Shipping, tax, printed
cases and appliance cables are excluded. Quotes were recorded September 19
for Rev2.2 and October 1 for the Rev3 variants; they have not been refreshed
for this comparison. Rev3B's amount excludes its processor module and installation.

| Revision | Processor and programming | PCB | Five-board cost | Per adapter |
| --- | --- | --- | ---: | ---: |
| Rev2.2 | ESP32-C3-WROOM-02; external UART programmer | 88.7 × 30.1 mm, 2 layers | $78.07 | $15.61 |
| Rev3A | Same ESP32 and built-in antenna; native USB-C and recovery header | 88.7 × 40 mm, 4 layers | $154.44 | $30.89 |
| Rev3B | Soldered XIAO ESP32-C3; module USB-C and external antenna | 99 × 40 mm, 4 layers | $112.08 **without XIAO or installation** | $22.42 **incomplete** |
| Rev3C | Socketed, pre-headered XIAO ESP32-C3; module USB-C and external antenna | 99 × 40 mm, 4 layers | $144.60 including five separately purchased modules | $28.92 |

Rev3C's total combines the $114.65 assembled-carrier quote with five $5.99
retail modules. The user plugs each module into its sockets. It is $1.97 less
per adapter than Rev3A at this batch size. Relative to the $39.99 FirstBuild
price used as the project target, it leaves $11.07 for other costs; delivered
cost below that target has not been established. [Pricing details](PRICING.md).

Rev3A/B/C add automatic selection between appliance power on pin 1 and pin 3,
two board mounting points, and permanent J2 recovery headers. Rev3A has separate
USB and appliance isolation paths intended for simultaneous connection,
pending bench verification. Rev3B/C require only one physical power source at
a time: appliance power energizes the XIAO USB VBUS rail. A C6 substitution
does not automatically remove this restriction.

## How to read the images

These are CAD previews, not photographs of manufactured boards. They show
the populated-board layout and case geometry from several angles. Common
parts use KiCad package models; the RJ45 body and XIAO module use simplified
clearance models. The XIAO shield outline is approximate, and the antenna
cable and flat antenna are omitted. Rev2.2's fuse bodies use an 1812-package
stand-in whose exact height is unverified. Colors are illustrative.

The images help compare layouts but do not establish connector fit, socket
retention, thermal performance or RF reception. Rev2.2 and Rev3A show base
and lid separately. Rev3B/C include assembly previews and exploded views;
the exploded lid offset is for presentation.

### Rev2.2 and the existing Rev2 case

![Rev2.2 board and Rev2 case, multiple views](images/rev2.2-gallery.png)

Board: [top](images/rev2.2/board-top.png) · [bottom](images/rev2.2/board-bottom.png) · [angled](images/rev2.2/board-oblique.png) · [side](images/rev2.2/board-side.png).

Case: [base inside](images/rev2.2/case-base-inside.png) · [base side](images/rev2.2/case-base-side.png) · [lid outside](images/rev2.2/case-lid-outside.png) · [lid inside](images/rev2.2/case-lid-inside.png).

Source: [Rev2.2 PCB](https://github.com/Dr-Crow/esphome-ge-laundry-uart/tree/bc0d52495bd97ed1504bd0ca0775e47feb01a648/pcb/rev2.2) · [Rev2 case](https://github.com/Dr-Crow/esphome-ge-laundry-uart/tree/bc0d52495bd97ed1504bd0ca0775e47feb01a648/case/rev2).

### Rev3A

Built-in antenna, separate USB-C connector, BOOT/RESET buttons and recovery
header. The gallery shows the standard tool-access lid; a separate optional
finger-button lid is available in the source branch.

![Rev3A board and standard case, multiple views](images/rev3a-gallery.png)

Board: [top](images/rev3a/board-top.png) · [bottom](images/rev3a/board-bottom.png) · [angled](images/rev3a/board-oblique.png) · [side](images/rev3a/board-side.png).

Case: [base inside](images/rev3a/case-base-inside.png) · [base side](images/rev3a/case-base-side.png) · [lid outside](images/rev3a/case-lid-outside.png) · [lid inside](images/rev3a/case-lid-inside.png).

Source: [Rev3A PCB](https://github.com/Dr-Crow/esphome-ge-laundry-uart/tree/a5a9fac87cbcb59d337a1fb8d3084ad18867a3e6/pcb/rev3a) · [Rev3A case and optional button lid](https://github.com/Dr-Crow/esphome-ge-laundry-uart/tree/a5a9fac87cbcb59d337a1fb8d3084ad18867a3e6/case/rev3a).

### Rev3B

XIAO soldered to the carrier. Its module is lower than Rev3C's removable
version. BOOT and RESET are on the XIAO itself; J2 remains inside the case.

![Rev3B board and case, multiple views](images/rev3b-gallery.png)

Board: [top](images/rev3b/board-top.png) · [bottom](images/rev3b/board-bottom.png) · [angled](images/rev3b/board-oblique.png) · [side](images/rev3b/board-side.png).

Case: [closed](images/rev3b/case-closed.png) · [side](images/rev3b/case-side.png) · [lid removed](images/rev3b/case-open.png) · [exploded](images/rev3b/case-exploded.png).

Source: [Rev3B PCB](https://github.com/Dr-Crow/esphome-ge-laundry-uart/tree/c5db989810663caa18226a091bfb105ad26fb00e/pcb/rev3b) · [Rev3B case](https://github.com/Dr-Crow/esphome-ge-laundry-uart/tree/c5db989810663caa18226a091bfb105ad26fb00e/case/rev3b).

### Rev3C

The pre-headered XIAO plugs into factory-installed female sockets. This
requires a taller case but permits replacing the module without soldering.

![Rev3C board and case, multiple views](images/rev3c-gallery.png)

Board: [top](images/rev3c/board-top.png) · [bottom](images/rev3c/board-bottom.png) · [angled](images/rev3c/board-oblique.png) · [side](images/rev3c/board-side.png).

Case: [closed](images/rev3c/case-closed.png) · [side](images/rev3c/case-side.png) · [lid removed](images/rev3c/case-open.png) · [exploded](images/rev3c/case-exploded.png).

Source: [Rev3C PCB](https://github.com/Dr-Crow/esphome-ge-laundry-uart/tree/38d94d3dc7c41692e3c41710ec33b9f6e0c38b3e/pcb/rev3c) · [Rev3C case](https://github.com/Dr-Crow/esphome-ge-laundry-uart/tree/38d94d3dc7c41692e3c41710ec33b9f6e0c38b3e/case/rev3c).

## Package scope

This comparison branch contains documentation and accepted images. It does
not modify any PCB, schematic, case CAD or manufacturing files. Rendering
corrections were applied to private visualization copies; they have not been
backported to the hardware branches. Native source files remain authoritative.
