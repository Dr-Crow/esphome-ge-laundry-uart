# Firmware profiles and board service

Choose the profile family for the actual board. [Shared profiles](shared-rev3c/README.md) cover socketed Rev3C C3/C6 and the compatible soldered Rev3B C3 interface; [classic Rev1 profiles](rev1-classic/README.md) cover its distinct ESP32 wiring. The two root reference configurations cover Rev2.x and the compatible Rev3A C3 interface. The [per-board coverage review](BOARD-COVERAGE.md) proves these mappings separately from compilation. All eight profiles compiled in hosted jobs [69 at11826a7](https://circleci.com/gh/Dr-Crow/esphome-ge-laundry-uart/69) and [81 at8744a29](https://circleci.com/gh/Dr-Crow/esphome-ge-laundry-uart/81). The committed detailed binary-hash receipt remains bound to earlier2d5a42c; it is not relabeled as a later build. Runtime/appliance behavior remains untested.

## Rev2.x reference setup

These examples use the maintained [ESPHome GEA component](https://github.com/mguaylam/esphome-gea) and are software references for the historical Rev 2.x interface. They do not establish board power or appliance qualification.

[Back to the project overview](../README.md) · [PCB Rev 2.2 reference](../pcb/rev2.2/README.md) · [Revision history](../pcb/README.md)

## Choose a configuration

| Configuration | Connection | Typical use |
| --- | --- | --- |
| [`gea2.yaml`](gea2.yaml) | GPIO5 TX and GPIO10 RX, inverted, 19,200 baud | Rev 2.x reference for GEA2 appliances. |
| [`gea3.yaml`](gea3.yaml) | GPIO21 TX and GPIO20 RX, non-inverted, 230,400 baud | Rev 2.x reference for GEA3 appliances. |

The appliance model determines whether it uses GEA2 or GEA3. Establish that protocol and its electrical interface for the exact appliance before selecting a profile. Do not connect an unqualified board to an appliance to try configurations.

## Prepare ESPHome

If ESPHome is not installed yet, start with the official [ESPHome installation guide](https://esphome.io/install/) and [getting-started guide](https://esphome.io/install/getting-started/).

1. Copy the matching YAML file into your ESPHome configuration directory.
2. Change the `name` and `upper_name` substitutions near the top of the file.
3. Add these values to the `secrets.yaml` file in the same directory:

```yaml
wifi_ssid: "..."
wifi_password: "..."
esp_home_ota_pw: "..."
```

You can use the ESPHome Device Builder or the command line. The examples are starting points, so appliance-specific entities may need to be added or changed.

## Reproduce the reference build

The reference profiles pin ESP-IDF **5.5.5** and the GEA component to commit
`283ff2b0dfe90a6d14a5417a23176d433be8a5b3`. CI uses ESPHome **2026.9.1** and
runs actual compilation for both profiles. To run those checks locally with the
same ESPHome version, use `python3 ci/validate.py firmware` from the repository
root. The driver uses temporary dummy credentials and never flashes a device.

These build checks establish software compilation only. Match the board and
appliance configuration and complete physical qualification before use.

## First flash

Rev 2.x boards do not have USB. Programming uses a **3.3 V logic** USB-to-UART adapter connected to the unpopulated J2 holes or J3 Tag-Connect pads. Keep the UART adapter's VCC/power lead disconnected; do not apply 5 V logic to RX/TX or the control pins.

J2 pin 1 and J3 pin 2 are the board's **+3V3 rail on the regulator output**, not approved programming-power inputs. Do not feed either contact from the UART adapter or an external 3.3 V supply. Driving a regulator output while its input is absent can reverse-feed the regulator and other board rails.

| J2 pin | Board signal | Connect to |
| --- | --- | --- |
| 1, square pad | +3V3 regulator output rail | Leave disconnected; UART adapter VCC stays disconnected |
| 2 | Ground | Adapter ground, once a reviewed board-power arrangement exists |
| 3 | Boot | Ground only while entering the bootloader |
| 4 | Board RX / GPIO20 | Adapter TX, 3.3 V logic |
| 5 | Board TX / GPIO21 | Adapter RX, 3.3 V logic |
| 6 | Enable | Optional reset control |

TX/RX in this table means the adapter/ESP perspective: the native Rev 2.x netlist places J2.4 on U2 IO20/RXD and J2.5 on U2 IO21/TXD. Historical net names and printed labels can use a different perspective; confirm the exact schematic and revision before wiring.

Use only a **single reviewed board-input supply and power/reset procedure** matched to that exact schematic, revision and fitted regulator/protection parts. No approved supply voltage range, source, current limit or bench procedure is established by this guide. Do not combine appliance power with a programmer supply, and do not connect to an appliance before electrical and physical qualification.

This corrects the output-rail power advice in the historical guide at public-main commit `bc0d524` and the original Rev 2-era instructions. It changes documentation only; the circuit and its open qualification gates remain unchanged.

After that power arrangement and the serial logic/interface have been reviewed:

1. Connect J2 Boot to Ground.
2. With Boot held low, follow the reviewed board-input power/reset procedure for this exact revision to enter the serial bootloader. Keep UART adapter VCC disconnected and leave the +3V3 service contacts disconnected from external power.
3. In ESPHome Device Builder, choose **Install** and select the serial adapter. With the command line, run:

   ```console
   esphome run your-config.yaml --device /dev/cu.your-usb-serial-device
   ```

4. When the upload finishes, disconnect Boot from Ground and restart using the same reviewed power/reset procedure.

Later updates can be installed over Wi-Fi from ESPHome Device Builder. From the command line, run the same `esphome run` command and choose the network device when prompted.

## Before connecting to an appliance

Complete electrical/source, startup/current, regulator/protection/thermal, serial-level and connector/enclosure qualification for the exact board and appliance first. The native checks and firmware builds do not supply that evidence. After qualification, disconnect the programming adapter before connecting the board to the appliance service port. This connector is not Ethernet.

With the supplied configurations, the green LED follows Wi-Fi connection and the yellow LED follows the GEA component's `is_bus_connected()` state, checked once per second. Yellow is a connected-state indicator, not a per-message activity indicator. The red LED is initialized off at boot and has no ongoing status assignment in these examples.
