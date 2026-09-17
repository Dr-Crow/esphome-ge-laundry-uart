# ESPHome GE Laundry UART

Local Home Assistant control and monitoring for compatible GE appliances through ESPHome and the appliance's GEA serial bus.

> [!WARNING]
> The appliance uses an 8P8C modular connector that looks like Ethernet, but it is **not Ethernet**. Do not connect it to network equipment.

![Assembled Rev 2-era adapter](pcb/rev2.0/images/assembled-board.jpg)

*Assembled Rev 2-era adapter.*

The project began as an effort to integrate a GE washer and dryer with Home Assistant. An ESP32 powered by the appliance communication port reports information such as remaining time and cycle completion through ESPHome. Early work involved researching the GEA2 and GEA3 protocols and the U+ Connect module; later, [GE Appliances](https://github.com/geappliances) and [FirstBuild](https://firstbuild.com/inventions/home-assistant-adapter/) published additional hardware and protocol information. The maintained ESPHome implementation now lives in [mguaylam/esphome-gea](https://github.com/mguaylam/esphome-gea), while this repository provides compatible hardware, reference configurations, manufacturing files, and enclosures.

## Start here

> [!IMPORTANT]
> New hardware builds should start with [PCB Rev 2.2](pcb/rev2.2/README.md). It corrects the known Rev 2.0/2.1 board-file problems, but assembled prototypes still require physical validation before it can be considered a proven release.

- [Review Rev 2.2 and its known validation gates](pcb/rev2.2/README.md)
- [Prepare a PCB assembly order](pcb/ORDERING.md)
- [Configure ESPHome](firmware/README.md)
- [Download or modify the Rev 2 enclosure](case/rev2/README.md)

Older hardware and the full change history remain available in the [PCB revision index](pcb/README.md).

## New-user path

1. Read the [Rev 2.2 guide](pcb/rev2.2/README.md), especially its appliance-power and prototype-testing notes.
2. Follow the shared [PCB ordering guide](pcb/ORDERING.md) using only the matched Rev 2.2 manufacturing files.
3. Start with the appropriate reference configuration in [firmware](firmware/README.md).
4. Print or adapt the [Rev 2 enclosure](case/rev2/README.md).
5. Inspect and power the prototype cautiously before connecting it to an appliance.

Interested in improving the project? Read the [contribution guide](CONTRIBUTING.md) before changing hardware or manufacturing files.

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
