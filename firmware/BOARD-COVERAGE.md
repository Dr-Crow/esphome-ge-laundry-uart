# Source-compatible firmware coverage

Reviewed October 5, 2026 against electrical sources at `11826a7`/`8744a29`. Independent schematic/netlist/PCB inspection matches all seven revisions' physical pin memberships to their retained KiCad9.0.9 evidence. Subsequent purchasing-code/ordering-suffix edits preserve those physical memberships. Eight existing profiles cover sixteen revision/module/protocol combinations; no new default-jumper variant is needed.

TX/RX below are the module perspective. GEA2 inverts both pins at 19,200 baud; GEA3 uses noninverted pins at 230,400 baud.

| Board/interface | GEA2 TX/RX | GEA3 TX/RX | Profile pair |
| --- | --- | --- | --- |
| Rev1.0 classic 38-pin ESP32 candidate | GPIO18/19 | GPIO17/16 | [Classic GEA2](rev1-classic/gea2.yaml), [classic GEA3](rev1-classic/gea3.yaml) |
| Rev2.0 C3-WROOM-02 | GPIO5/10 | GPIO21/20 | [Root GEA2](gea2.yaml), [root GEA3](gea3.yaml) |
| Rev2.1 C3-WROOM-02 | GPIO5/10 | GPIO21/20 | Root GEA2/GEA3, independently matched to Rev2.1 |
| Rev2.2 C3-WROOM-02 | GPIO5/10 | GPIO21/20 | Root GEA2/GEA3, independently matched to Rev2.2 |
| Rev3A integrated C3-WROOM-02 | GPIO5/10 | GPIO21/20 | Root GEA2/GEA3, independently matched to Rev3A |
| Rev3B soldered XIAO C3 | GPIO5/10 | GPIO21/20 | [Shared C3 GEA2](shared-rev3c/c3-gea2.yaml), [C3 GEA3](shared-rev3c/c3-gea3.yaml) |
| Rev3C socketed XIAO C3 | GPIO5/10 | GPIO21/20 | Shared C3 GEA2/GEA3 |
| Rev3C socketed XIAO C6 | GPIO21/18 | GPIO16/17 | [Shared C6 GEA2](shared-rev3c/c6-gea2.yaml), [C6 GEA3](shared-rev3c/c6-gea3.yaml) |

All C3/C6 LED maps agree with the actual source: C3 GPIO3 green/Wi-Fi, GPIO2 red/manual/off at boot, GPIO4 yellow/bus-connected; C6 GPIO1,GPIO0,GPIO2 respectively. Classic Rev1 exposes only the proved GPIO13 LED in its profile. Default JP1 1–2 is required for the documented GEA2 maps; alternate 2–3 operation is not a supplied supported profile. C6 D9 is GPIO20, not BOOT.

C6 GPIO3 low enables RF; GPIO14 low selects its ceramic antenna and high selects external U.FL. Existing C6 build selection is internal; a user-selected external profile needs the correct attached antenna and independent validation. C3 and C6 carry different mechanical and supply references. Shared firmware does not make C6 a soldered Rev3B drop-in.

The pinned GEA schema defaults omitted protocol fields to GEA3, so the GEA3 examples' omission is intentional. Destination0x24/GEA2 and0xC0/GEA3 and the example entities remain appliance-specific assumptions. They are not a verified refrigerator configuration. Matter/Thread is not implemented.

The unchanged source inputs passed all eight real builds at [11826a7 job69](https://circleci.com/gh/Dr-Crow/esphome-ge-laundry-uart/69) and [8744a29 job81](https://circleci.com/gh/Dr-Crow/esphome-ge-laundry-uart/81), using ESPHome2026.9.1, ESP-IDF5.5.5 and GEA283ff2b0dfe90a6d14a5417a23176d433be8a5b3. The [detailed recorded artifact receipt](../ci/validation/hosted-2d5a42c/firmware-profiles.json) belongs to its earlier2d5 source. The two yellow-LED comment fixes change file-byte identity while preserving configuration; new exact-head builds must be recorded after publication.

This review does not identify the actual fitted classic Rev1 module. Espressif DevKitC V4's25.40mm header-row drawing differs from that carrier's22.86mm rows; matching logical GPIO names do not establish a physical drop-in. Header/flash/PSRAM/module identities, reset/ROM traffic, loaded power, bus thresholds, ERD behavior, OTA/recovery, RF and appliance qualification remain open. App UART logging is disabled, but ROM reset/download/brownout traffic can still reach the GEA3-connected pins.

The pinned external GEA component still has printf type-contract warnings on the classic target, including decimal ERD/text conversions. Matching32-bit ABI widths do not convert them into a runtime formatting proof. They remain a separate reviewed upstream-input fix; no component pin, firmware behavior or source package is changed by this documentation correction.
