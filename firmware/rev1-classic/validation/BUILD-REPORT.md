# Rev1 classic ESP32 actual build results

Both candidates passed actual ESPHome `config` and `compile` commands on October 3, 2026. Factory, OTA and ELF artifacts were produced for each profile. No firmware was flashed and no device or appliance was connected.

| Profile | Config exit | Compile exit | Compile time | Target and framework |
| --- | ---: | ---: | ---: | --- |
| [GEA2](../gea2.yaml) | 0 | 0 | 86.707 s | nodemcu-32s / classic ESP32 / ESP-IDF 5.5.5 |
| [GEA3](../gea3.yaml) | 0 | 0 | 43.838 s | nodemcu-32s / classic ESP32 / ESP-IDF 5.5.5 |

Tool: ESPHome **2026.9.1** from the existing engineering virtual environment. The native build actually selected ESP32 and Xtensa toolchain `esp-14.2.0_20260121`. The fetched GEA checkout's HEAD was independently verified as **283ff2b0dfe90a6d14a5417a23176d433be8a5b3**; it had no tracked working-tree changes. Its `erd-definitions` submodule was `c0de08ce3d3a55d5d7b0c0ba0a10e2688f224e58`.

## Exact inputs and procedure

The isolated worktree starts at public main `bc0d52495bd97ed1504bd0ca0775e47feb01a648`. UART/LED mapping comes from recovered Rev1 hardware commit `87984047ee029efb83bf9947dc21818fd18e39b3`: schematic blob `884cae1950066274f54545e730efb9746e1474ba`, board blob `7202d06e51b573ea9181b7dff6960e35402ede7d`.

- GEA2: GPIO18 TX / GPIO19 RX, inverted, 19,200 baud.
- GEA3: GPIO17 TX / GPIO16 RX, non-inverted, 230,400 baud.
- Only carrier LED: GPIO13/U3.15 → R19 220 Ω → D6 anode, cathode at GND, active high. GPIO14/SW1 remains unconfigured.

Only these profiles/packages were copied to a new temporary directory, with synthetic Wi-Fi/OTA secret values supplied there. Both actual `config` and `compile` commands ran; no real credentials were read. All five YAML/package SHA-256 hashes, exact commands, exits, durations and raw/readable log hashes are in [build-evidence.json](build-evidence.json). Original stdout, normalized readable logs and the archived validation driver remain local under ignored `artifacts`; upstream CI owns compile orchestration. Readable logs normalize terminal colors, line endings and trailing whitespace. Package cleanup did not change any build input: their hashes and the retained outputs were verified again without recompiling.

## Actual local artifacts

These ignored local binaries were compiled with dummy credentials for software review. They are not deployment or hardware-qualified images.

| Profile and artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| [GEA2 factory](artifacts/gea2/firmware.factory.bin) | 947232 | 3ef3b77c8717152f68e6e8ebce908d78963078b6689e2e436315b2fe73144bd2 |
| [GEA2 OTA](artifacts/gea2/firmware.ota.bin) | 881696 | 0eed22a2d6a29cfd44f4bd40b2af83b2e37f8636c794822b5202ef92c2e4c46d |
| [GEA2 ELF](artifacts/gea2/firmware.elf) | 14146024 | a9518d8a34989105791ddadaf3107e97555e159858ace995089a2c41b87b8fd2 |
| [GEA3 factory](artifacts/gea3/firmware.factory.bin) | 944400 | afb1a67ef4fc4feca71a405eb99d6fac77d683c9e4dce161181dd64503ce984f |
| [GEA3 OTA](artifacts/gea3/firmware.ota.bin) | 878864 | 0c28d3fd67636da52d6c0fdd1c245e9cbc246e3bea7cf105110b0f1b3a8d6116 |
| [GEA3 ELF](artifacts/gea3/firmware.elf) | 14062720 | 32edfba2046450fc481c50b04ec2d28f0c989256ce201464156820253daa0b18 |

GEA2 reports 46,392 bytes RAM used (25.7%) and 881,587 bytes application flash (48.0%). GEA3 reports 46,104 bytes RAM (25.5%) and 878,747 bytes application flash (47.9%). Those percentages use the build target's partition/memory assumptions, not measurements of a purchased module.

## Warnings and remaining limits

These successful builds retain inherited warnings: GEA2 has eight printf-format diagnostics and one unused generated ERD lookup diagnostic; GEA3 has seven format diagnostics and the same unused-function diagnostic. In both profiles, six `%u` diagnostics pass `uint32_t` (`unsigned long`) and one `%d` passes `int32_t` (`long`); GEA2 adds one signed `%d` diagnostic in the text sensor. These are printf type-contract defects, even though the affected arguments retain the intended signedness.

The actual pinned Xtensa compiler reports 32-bit `int` and `long`, a four-byte word and 32-bit argument alignment; `int32_t`/`uint32_t` are `long`/`unsigned long`. Existing compiled-object inspection confirms one 32-bit poll-value load into an outgoing argument register. For these particular diagnostics, no width truncation, extra variadic-slot consumption or argument shift is evidenced. The warnings also cover two ERD decimal conversions and GEA2's text-sensor conversion. Correct runtime formatting was not established: target decimal conversions and logging were not exercised. The unused `erd_lookup` warning has no printf/ABI effect. The pinned component remains unchanged. Exact diagnostic source lines and compiler evidence are recorded in [build-evidence.json](build-evidence.json); complete raw/readable logs remain local under ignored `artifacts/logs`.

Compilation does not identify an installed classic-ESP32 module, flash layout or pin-compatible product. These profiles do not match C3/C6 boards. Appliance-specific entities, actual source/current/protection and external-buck behavior, loaded startup, power/USB/UART isolation, thermal performance, module/case fit and appliance compatibility remain unqualified. Keep UART programmer VCC disconnected and use one reviewed supply. No order or remote publication occurred.
