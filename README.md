# ESPHome GE Laundry UART

Local Home Assistant control and monitoring for compatible GE appliances through ESPHome and the appliance's GEA serial bus.

> [!WARNING]
> The appliance uses an 8P8C modular connector that looks like Ethernet, but it is **not Ethernet**. Do not connect it to network equipment.

![Assembled Rev 2-era adapter](pcb/rev2.0/images/assembled-board.jpg)

The project began as an effort to integrate a GE washer and dryer with Home Assistant. An ESP32 powered by the appliance communication port reports information such as remaining time and cycle completion through ESPHome. Early work involved researching the GEA2 and GEA3 protocols and the U+ Connect module; later, [GE Appliances](https://github.com/geappliances) and [FirstBuild](https://firstbuild.com/inventions/home-assistant-adapter/) published additional hardware and protocol information. The maintained ESPHome implementation now lives in [mguaylam/esphome-gea](https://github.com/mguaylam/esphome-gea), while this repository provides compatible hardware, reference configurations, manufacturing files, and enclosures.

## Getting started

### I already have a board

Follow the [firmware setup guide](firmware/README.md) to choose a GEA2 or GEA3 configuration, flash the board, connect it to Home Assistant, and check the status LEDs. The [Rev 2 enclosure](case/rev2/README.md) includes ready-to-print files.

### I want to review a new board

The selected development focus is [Rev3C](pcb/rev3c/README.md), a shared socketed XIAO C3/C6 carrier with both GE appliance power inputs and automatic PIN1 priority. C3 comes first. Its higher-rated switches preserve the original source-selection and buck topology.

The illustrated [Rev3C JLCPCB guide](pcb/rev3c/ORDERING.md) identifies the matched files and settings. Complete October 3, 2026 quotes were **$134.64 for five carriers** or **$168.91 for ten**, before shipping, tax and separately supplied XIAO modules. It remains a prototype: source/current/transient, loaded startup, thermal, assembly and enclosure qualification are open. Disconnect appliance RJ45 before powered USB and leave UART VCC disconnected. No qualified shared C3/C6 enclosure is included.

Older boards are listed in the [PCB revision index](pcb/README.md). Rev2.2 is not a manufacturing-ready fallback; its power ratings and thermal/current limits also require qualification. Hardware contributors should read the [contribution guide](CONTRIBUTING.md).

## Related projects

- [GE Appliances organization](https://github.com/geappliances)
- [FirstBuild Home Assistant adapter](https://firstbuild.com/inventions/home-assistant-adapter/)
- [puddly/casserole](https://github.com/puddly/casserole)
- [GEMakers/green-bean](https://github.com/GEMakers/green-bean)
- [doitaljosh/gea-interface-board](https://github.com/doitaljosh/gea-interface-board)
- [doitaljosh/ge-appliances-re](https://github.com/doitaljosh/ge-appliances-re)
- [doitaljosh/geabus-documentation](https://github.com/doitaljosh/geabus-documentation)
- [simbaja/gehome](https://github.com/simbaja/gehome)
- [GE Appliances Home Assistant adapter](https://github.com/geappliances/home-assistant-adapter)
- [GE Appliances Home Assistant examples](https://github.com/geappliances/home-assistant-examples)
- [GE Appliances Home Assistant bridge](https://github.com/geappliances/home-assistant-bridge)
