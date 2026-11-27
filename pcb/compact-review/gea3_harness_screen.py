"""Check compact-board GEA3 topology and calculate a lumped harness screen.

Run with one or more native KiCad XML netlists. See GEA3-HARNESS.md for
scope, reference planes and the physical validation that this cannot supply.
"""

import argparse
import math
import xml.etree.ElementTree as ET
from pathlib import Path


def check_schematic(path):
    root = ET.parse(path)
    values = {c.get("ref"): c.findtext("value") for c in root.findall(".//components/comp")}
    expected = {"R20": "10K", "R21": "220k", "R24": "1K", "R25": "1K"}
    for ref, value in expected.items():
        if values.get(ref, "").upper() != value.upper():
            raise ValueError(f"{path}: {ref} should be {value}, found {values.get(ref)}")
    net = {(p.get("ref"), p.get("pin")): n.get("name")
           for n in root.findall(".//nets/net") for p in n.findall("node")}
    for group in ("J1.5 R24.2 U11.3", "R24.1 R20.1 JP4.2", "JP4.1 U5.4",
                  "J1.4 R25.2 U11.4", "R25.1 R21.1 U4.3", "R20.2 R21.2 U4.5"):
        nets = {net[tuple(pin.split("."))] for pin in group.split()}
        if len(nets) != 1:
            raise ValueError(f"{path}: expected connected {group}, found {nets}")
    if net["U4", "5"] != "+5V" or net["U5", "5"] != "+3V3":
        raise ValueError(f"{path}: receiver or driver supply changed; re-evaluate screen")
    print(f"{path.name}: expected resistor values, rail and interface nets verified")


def rising_edge(cap_pf, local_v, remote_pull, remote_v, driver_low, threshold):
    """J1.5 external capacitor, JP4 closed, driver releasing a prior low."""
    local_pull, series = 10_000, 1_000
    local_r = local_pull + series
    conductance = 1 / local_r + 1 / remote_pull
    final = (local_v / local_r + remote_v / remote_pull) / conductance
    initial = (driver_low / series + remote_v / remote_pull) / (1 / series + 1 / remote_pull)
    if threshold >= final:
        return initial, final, math.inf
    if threshold <= initial:
        return initial, final, 0.0
    time_us = -math.log((final - threshold) / (final - initial)) * cap_pf * 1e-6 / conductance
    return initial, final, time_us


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("netlist", type=Path, nargs="+")
    args = parser.parse_args()
    for path in args.netlist:
        check_schematic(path)
    print("TX nominal 5.00 V, ideal low driver, remote pull to 5.00 V, threshold 3.50 V")
    print("pull_ohm cap_pF initial_V final_V time_us")
    for pull in (math.inf, 10_000, 4_700):
        for cap in (50, 100, 200, 400):
            initial, final, time = rising_edge(cap, 5, pull, 5, 0, 3.5)
            print(f"{pull:8g} {cap:6} {initial:9.3f} {final:7.3f} {time:7.3f}")
    half_bit_us = 0.5e6 / 230_400
    cap_limit = half_bit_us / (11_000 * -math.log(0.30)) * 1e6
    rx_high = (3.3 / 1_000 + 5 / 220_000) / (1 / 1_000 + 1 / 220_000)
    print(f"Half-bit {half_bit_us:.3f} us; no-remote-pull limiting capacitance {cap_limit:.1f} pF.")
    print(f"RX U4.3 at 3.30 V low-impedance appliance high: {rx_high:.3f} V (VIH,min 3.50 V).")


if __name__ == "__main__":
    main()
