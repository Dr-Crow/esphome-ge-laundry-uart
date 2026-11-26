# Shared Rev3C antenna and mechanical review

The shared C3/C6 candidate preserves the original 99 × 40 mm carrier, socket positions and mounting datums. Its local C6 antenna exclusion is a layout improvement with RF and physical qualification still open.

[Carrier overview](README.md) · [Shared firmware and RF selection](../../firmware/shared-rev3c/README.md) · [Power qualification](POWER-QUALIFICATION.md)

## C6 antenna projection and copper exclusion

The [official C6 PCB archive](https://files.seeedstudio.com/wiki/SeeedStudio-XIAO-ESP32C6/XIAO_ESP32_C6_v1.0_SCH%26PCB_260114.zip) maps to the fixed socket rows by x−20.5077, y−59.9585 mm. Its Kinghelm KH5220-A36 antenna projects to centre **(78.6285, 16.0415) mm**. The [Kinghelm V1.3 drawing](https://www.kinghelm.com.cn/upload/file/20230213/KH5220-A36.pdf) gives a maximum body projection of **x77.5285–79.7285, y13.3415–18.7415 mm**. The antenna is over carrier interior rather than the right edge.

Original carrier ground fills and `GEA2_RX`/`GEA2_MCU_TX` copper crossed that projection. The candidate carries an all-copper-layer rule area **x77.0–80.9, y11.8–19.2 mm**, excluding pours, tracks, vias and pads, with no carrier components inside it. Minimal reroutes of `GEA2_RX`, `GEA2_MCU_TX` and `BOOT_SEL` preserve existing connections. This change does not relocate sockets, cut the board or alter power circuitry.

The 0.2 mm F.Cu `GEA2_RX` detour runs from (73.4626, 15.6828) through (76.85, 15.6828), (76.85, 11.3) and (81.4, 11.3) into its right-side route. This upper detour preserves original TP12 at (76, 13) and the original power copper.

The rectangle covers the maximum antenna body and much of Seeed's pour void while ending before fixed `J6.1` at (80.27, 20.5375) mm. Seeed's exclusion extends toward required module header pads; copying it as an absolute carrier no-pad/no-track area would collide with the socket. This local rectangle is an engineering compromise, not a vendor-qualified carrier keepout.

The restored candidate passes genuine KiCad 9.0.9 full-severity [DRC](validation/native-kicad-9.0.9-drc.json), including zero unconnected items, schematic-to-board parity differences and keepout violations. Independent native geometry inspection finds exactly **0.0 mm² filled copper** inside the antenna rectangle on each of four layers, and regenerated copper-view pixels were inspected. The native rule excludes tracks/vias/pads/pours; these CAD checks do not establish RF performance.

Review the regenerated [front](images/rev3c-copper-f-cu.svg), [inner ground](images/rev3c-copper-in1-cu.svg), [inner routing](images/rev3c-copper-in2-cu.svg) and [bottom](images/rev3c-copper-b-cu.svg) views. The [source-restoration proof](validation/source-restoration-proof.json) also confirms original sockets, pad geometry, surviving footprint placements and outline are preserved.

[Espressif's C6 guidance](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c6/pcb-layout-design.html) describes antenna-edge placement and housing clearance, including a 15 mm example for a PCB antenna. That is not an exact KH5220-A36 carrier specification. Kinghelm's test-board geometry likewise does not validate this socketed assembly. No measured range improvement or former RF failure is claimed.

## Antenna options and enclosure constraints

Unchanged C6 firmware holds GPIO3 low to enable RF; GPIO14 low selects ceramic/internal and high selects U.FL/external. The profile's `c6_external_antenna: true` selects external. Install the correct external antenna before using that selection. C3 uses its own U.FL antenna arrangement; cable and antenna position need separate clearance/RF checks.

Reference CAD datums in carrier coordinates are:

| Feature | C3 | C6 |
| --- | --- | --- |
| USB footprint origin | (92.5890, 12.9175) | (92.6237, 12.9215) |
| BOOT switch origin | (79.0000, 8.4725) | (97.3483, 19.4927) |
| RESET switch origin | (79.0000, 17.3625) | (97.3483, 6.3355) |
| U.FL footprint origin | (78.8730, 12.9175) | (78.8825, 8.6215) |

These are layout origins, not measured actuator targets or USB-shell envelopes. Similar USB XY supports a future common access region; the opening needs both actual connector shells, plugs and mating Z. C3 BOOT/RESET holes do not serve C6's differently located buttons. C6 BOOT is not side-header D9.

No default shared/C6 Rev3C enclosure is included. The original C3-specific case was not copied into this candidate. A future case must preserve module BOOT/RESET and USB access, permit unpowered insertion/removal, and keep retention pieces, fasteners, magnets, metal and coatings away from the ceramic antenna and both U.FL/pigtail routes.

Measure socket/header insertion depth, module height and retention on physical assemblies before fixing USB Z, actuator length or retention pressure. Test vibration, cable strain relief and range/throughput with the actual module, antenna, final plastic case, appliance-adjacent metal and orientation. Physical fit, retention and RF remain untested; copper exclusion does not close these gates.
