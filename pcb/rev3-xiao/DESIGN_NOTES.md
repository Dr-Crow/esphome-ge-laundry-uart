# Revision 3B design notes

## Plain-English comparison

| Question | Revision 3A bare module | Revision 3B XIAO |
| --- | --- | --- |
| USB connector | Designed on the carrier | Built into the XIAO |
| Wi-Fi antenna | Built into the ESP32 module | Separate antenna connected to the XIAO U.FL socket |
| USB trace difficulty | Carrier must route a controlled pair | Handled inside the XIAO |
| Carrier layer target | Two layers if rerouting works; four-layer fallback | Two layers |
| MCU/module cost | Lower | Higher, currently about $5 retail |
| Carrier part count | Higher | Lower |
| Dual-source power | Carrier has explicit blocking paths | Manual appliance-pin and RUN/USB-DEBUG selectors plus a protected 9-16 V buck input |
| Assembly | One assembled PCB | Carrier plus an assembled XIAO module |

The XIAO can still be competitive because its module premium replaces the USB connector, USB protection, configuration resistors, series resistors, boot/reset support, flash, RF layout, and 3.3 V supply. Only matched assembled quotes can determine the real winner.

## Power facts and implications

- Seeed documents `BAT` for a 3.7 V lithium battery and allows USB while that battery is attached.
- Seeed's maintained guidance describes the XIAO 5 V/VBUS pad as USB-derived. An external supply may feed that pad through a diode.
- The XIAO 3V3 pin is an onboard regulator output, not the preferred carrier power input.
- The published schematic connects USB VBUS to the onboard charger and connects the charger to the battery node.

Therefore a regulated supply on `VBAT` is not equivalent to a battery. With USB present, the charger can try to charge that regulated node. A regulator with reverse-current protection toward its own input does not by itself prove that the shared node is safe.

## Safe development directions

### Mutually exclusive sources

Feed regulated appliance-derived 5 V into the XIAO 5 V pad through the vendor-required diode and prohibit simultaneous USB. This has the fewest carrier parts, but the operating rule must be physically enforceable or very clear because firmware cannot prevent electrical backfeed.

### Simultaneous appliance and USB power

Use a dedicated source selector, ideal-diode controller, or load switch whose data sheet explicitly covers reverse blocking and the required voltage/current range. Validate source-only, USB-only, both, neither, and both insertion orders. No appliance-derived voltage may reach the host VBUS.

Rev 3B deliberately does not select this automatic circuit. It uses the cheaper manual RUN/USB-DEBUG jumper described below. Automatic source selection remains a possible later revision after bench testing establishes the current paths, handoff behavior, voltage drop, startup, thermal margin, and fault behavior.

## Mechanical and assembly gates

- Confirm the exact XIAO hardware revision and fitted charger before testing.
- Compare the project footprint with the official pad drawing and a physical module.
- Confirm the assembler supports turnkey placement of the XIAO underside pads; do not assume the user will solder the module.
- Keep carrier copper away from the U.FL connector and provide a safe antenna/cable location in the enclosure.
- Verify the USB-C opening, buttons, antenna lead, appliance connector, and mounting holes with a printed enclosure sample.

## Cost gate

The finished-unit goal is below the former $39.99 FirstBuild retail price, not merely a cheap bare PCB. Compare JLCPCB and PCBWay at 5, 10, and 30 complete units using the same board finish, parts, through-hole assembly, XIAO sourcing, enclosure, shipping, and expected yield. Do not publish a per-board price until the live parts review and assembly quote are complete.

## Primary references

- [Seeed XIAO ESP32-C3 getting-started and battery guidance](https://wiki.seeedstudio.com/XIAO_ESP32C3_Getting_Started/)
- [Seeed XIAO ESP32-C3 source repository](https://github.com/Seeed-Studio/OSHW-XIAO-Series/tree/main/XIAO-ESP32C3)
- [Seeed XIAO ESP32-C3 schematic](https://files.seeedstudio.com/wiki/XIAO_WiFi/Resources/XIAO_ESP32C3_v1.3_SCH_260116.pdf)
- [Diodes Incorporated 74LVC2G07 data sheet](https://www.diodes.com/datasheet/download/74LVC2G07.pdf)

## Rev 3B minimal-carrier schematic draft

This section describes the carrier schematic draft. It is a review
artifact, not an approval to fabricate or attach a board to an appliance.

### Intended power-source operating rule

```text
appliance regulator +5 V -> D5 SS14 -> JP_PWR pin 1 (RUN) --shunt--> pin 2 -> XIAO_VBUS
                                                    pin 3 (USB DEBUG): no circuit connection
```

- `JP2` and `JP_PWR` are distinct removable-shunt headers. `JP2` is the appliance-input selector: bridge pins 1-2 to use 8P8C pin 1 (`VDC`) or pins 2-3 to use 8P8C pin 3 (`ALT_PWR`); only one shunt position is allowed. `JP_PWR` is a 1x3, 2.54 mm header for a removable two-position shunt. In RUN,
  the shunt bridges pins 1-2. In USB DEBUG, it is parked across pins 2-3;
  pin 3 is intentionally unconnected, so appliance power is open.
- D5 is labeled with its anode on appliance-regulated `APPL_5V` and cathode on `PWR_RUN`.
  This is the intended appliance-side Schottky drop before the removable shunt.
- The intended appliance-powered state is appliance attached, USB absent, and
  shunt on RUN. The allowed USB-debug state is appliance attached or not,
  USB attached, and shunt parked on USB DEBUG; appliance data and ground stay
  connected. The explicitly forbidden state is appliance attached + RUN + USB
  attached. This is manual source exclusion, not automatic source selection.

### Intended XIAO and GEA3 assignments

- XIAO pad 7 (GPIO21/D6) is `UART_TX`; pad 8 (GPIO20/D7) is `UART_RX`.
- XIAO pad 12 is the 3.3 V output; pads 13, 18, and 22 are ground; pad 14 is
  `XIAO_VBUS`. Pad 21 (`BAT`) is explicitly no-connect: the legacy battery
  fixture and its charger-facing net have been removed.
- J1 is the actual 8P8C appliance connector: pin 1 is `VDC`, pin 3 is `ALT_PWR`, pin 4 is adapter TX / appliance RX (`GEA3_APPL_RX`), pin 5 is appliance TX / adapter RX (`GEA3_APPL_TX`), and pin 8 is GND. Pins 2, 6, and 7 are NC; pin 7 is deliberately NC because this Rev 3B prototype is GEA3-only. `D3` and `D4` are BAV99 rail clamps to `APPL_5V`/GND.
  `U3` is a 3.3 V 74LVC2G07 dual non-inverting open-drain buffer. Appliance
  TX enters through R3 and D3 before U3; XIAO TX leaves U3 through R6, then
  D4. R4 pulls MCU-side `UART_RX` to XIAO 3.3 V; R5 pulls appliance RX to
  `APPL_5V`; C3 is U3 local 100 nF decoupling. GEA2 is intentionally deferred.
- TP1 is `APPL_5V`, TP3 is `UART_TX`, TP4 is `UART_RX`, TP5 is `XIAO_VBUS`,
  TP6 is XIAO 3.3 V, and TP7 is ground.

### Preliminary BOM status

| Ref(s) | Candidate | Identifier/status |
| --- | --- | --- |
| J1 | Amphenol 54602-908LF 8P8C jack | LCSC `C2847314`; through-hole assembly required |
| JP2, JP_PWR | 1x3 2.54 mm headers plus removable 2-position shunts | exact manufacturer/LCSC identifiers unverified |
| U2 | Seeed XIAO ESP32-C3 | MPN 113991054; JLCPCB/LCSC C18212168, SMD 21x17.8 mm, Extended; supported for Economic and Standard SMT assembly (live source checked 2026-09-14) |
| U8 | Diodes Incorporated AP63205WU-7, TSOT-23-6 | LCSC `C2071056`; fixed 5 V buck converter |
| D5 | SS14, SOD-123 Schottky | MPN SS14; LCSC selection unverified |
| U3 | Diodes Incorporated 74LVC2G07W6-7, SOT-23-6 | LCSC `C151607`; 3.3 V open-drain dual buffer with inputs specified to 5.5 V |
| D3, D4 | BAV99, SOT-23 | GEA3 rail clamps; exact vendor/LCSC identifier unverified |
| R3/R6/R4/R5 | 4.7 k/1 k/10 k/10 k, 0805 | values are review starting points, not yet bench-validated |
| C3 | 100 nF, 0805 | U3 local decoupling; exact dielectric/vendor unverified |
| TP1, TP3–TP7 | test pads | footprint chosen; manufacturer/LCSC identifier unverified |

### Validation status and board gate

KiCad 9.0.9 parses the rebuilt schematic and exports distinct `/APPL_5V`,
`/PWR_RUN`, `/XIAO_VBUS`, `/UART_TX`, `/UART_RX`, `/GND`, and
`/XIAO_3V3_OUT` nets. The previous `+3V3`/GND collision is gone. ERC reports
zero errors and 101 warnings: 39 missing-global-library warnings from the CLI
environment, 58 inherited off-grid endpoint warnings, and 4 unconnected wire
endpoint warnings. These findings still require cleanup before layout release
and do not substitute for electrical review.

The rebuilt netlist proves no direct J2-to-XIAO GPIO net: appliance TX reaches
U3 only through R3/D3, and appliance RX is driven only from U3 through R6/D4.
The selected Diodes Incorporated `74LVC2G07W6-7` data sheet specifies inputs
up to 5.5 V and partial-power-down protection, so a nominal 5 V appliance input
is within the component's published input range. Physical prototypes must still
verify the appliance's actual levels, waveforms, clamp current, and sequencing.
The board fixture remains deliberately unsynchronized and is not presented as
a first-pass electrical PCB. Before layout, bench-validate the assumed GEA3
levels, clamp current, pull-up strengths, and buffer power sequencing; add
top-side `RUN`, `USB DEBUG`, pin-1, and `POWER OFF BEFORE MOVING SHUNT`
silkscreen.
