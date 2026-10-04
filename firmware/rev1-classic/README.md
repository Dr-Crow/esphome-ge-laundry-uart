# Rev1 classic ESP32 firmware candidates

These two isolated profiles follow the recovered Rev1 UART wiring and the original `nodemcu-32s` target. They preserve the existing Rev2.x and shared Rev3C profiles. Compilation is a software check; these remain unqualified hardware/profile candidates.

| Profile | UART TX / RX from ESP perspective | Electrical encoding |
| --- | --- | --- |
| [GEA2](gea2.yaml) | GPIO18 / GPIO19, U3 pads 30 / 31 | Inverted, 19,200 baud |
| [GEA3](gea3.yaml) | GPIO17 / GPIO16, U3 pads 28 / 27 | Non-inverted, 230,400 baud |

The profiles pin ESP-IDF 5.5.5 and the GEA component at commit `283ff2b0dfe90a6d14a5417a23176d433be8a5b3`, with ESPHome minimum 2026.9.1. Their common services and protocol behavior derive from the modern shared Rev3C packages. Appliance entities/address examples still require appliance-specific review.

## Exact source identity and GPIO limits

Recovered Rev1 hardware source is commit `87984047ee029efb83bf9947dc21818fd18e39b3`. U3 is custom symbol `onionStraws:ESP32`, value ESP32, footprint `Library:DIP-38_900_ELL`, symbol UUID `4b8c3e21-2d12-4f69-bdf2-b8db31da1d87`. This establishes a generic 38-pin classic ESP32 development-board interface; the exact purchased module, silicon, flash size and physical pin compatibility are unknown. `nodemcu-32s` is the original firmware build target, not identification of an installed device.

Native netlist and board pin-membership review establishes one carrier LED: U3.15/GPIO13 → R19 220 Ω → D6 anode, with D6 cathode at GND. It is active high. The generic D6 LED source does not establish its color. This candidate uses that single LED as a Wi-Fi indicator with 4% maximum PWM duty and an off startup state. GPIO14 is SW1's input and is left unconfigured. No C3 red/green/yellow LED pins or module-specific LEDs are assumed.

These GPIO mappings do not match the C3/C6 revisions. Current legacy C3 profiles use GEA2 TX5/RX10 and GEA3 TX21/RX20; they do not match Rev1. Do not treat these classic ESP32 candidates as replacements for those profiles.

## Power and physical gates

Rev1 takes GE power only on RJ45 J2.1 through F1 and Q1/Q2, then needs an external buck through J1. The source does not establish the actual buck module, source envelope/current allowance, protection coordination, loaded startup, thermal behavior, purchased development-board power path, or physical/case compatibility. The module's 3V3 output supplies carrier logic. Check those independently before any device/appliance use.

Use one reviewed supply. Keep any UART programmer VCC disconnected; do not inject carrier/module 3V3 or combine appliance/buck power with USB/programmer power. The actual development-board USB/5VIN relationship needs review. This change includes no flashing, device connection or approved physical commissioning procedure.

## Validation

Validation uses ESPHome 2026.9.1 `config` and real `compile` commands for both profiles with ESP-IDF 5.5.5. A separate temporary source receives only synthetic `secrets.yaml` values; no real credentials are read. Full results, exact source hashes and actual binary hashes are recorded in [BUILD-REPORT.md](validation/BUILD-REPORT.md) and [build evidence](validation/build-evidence.json). Local generated binaries are under the ignored `validation/artifacts` directory. A config-only result or dependency failure is not reported as a compile pass.
