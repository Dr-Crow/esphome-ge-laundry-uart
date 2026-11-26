#!/usr/bin/env python3
"""Regenerate the Rev3F JLCPCB manufacturing set from the KiCad 9.0.9 source.

Run inside the pinned kicad/kicad:9.0.9 image from the repository root:
    python3 pcb/rev3f/manufacturing/generate.py

Outputs (overwritten):
    pcb/rev3f/manufacturing/GERBER-GEA-Adapter-Rev3F.zip  native gerbers (board plot params) + split drills
    pcb/rev3f/manufacturing/BOM-GEA-Adapter-Rev3F.csv     one row per assembled reference (JLCPCB columns)
    pcb/rev3f/manufacturing/CPL-GEA-Adapter-Rev3F.csv     KiCad-native centroids/rotations; J1 uses the reviewed body datum

All geometry comes from kicad-cli exports; this script only reshapes columns. ci/validate.py
re-exports the same data and fails if anything here differs from the source.
"""
import csv, json, subprocess, sys, tempfile, zipfile, xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DESIGN = ROOT / "pcb/rev3f/design"
OUT = ROOT / "pcb/rev3f/manufacturing"
SCH, PCB = DESIGN / "GEA-Adapter-Rev3F.kicad_sch", DESIGN / "GEA-Adapter-Rev3F.kicad_pcb"
ORIGINS = ROOT / "pcb/rev3f/validation/placement-origin-review.json"


def run(*args):
    subprocess.run(["kicad-cli", *map(str, args)], check=True, stdout=subprocess.DEVNULL)


def main():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        cam = tmp / "cam"; cam.mkdir()
        run("sch", "export", "netlist", "--format", "kicadxml", "-o", tmp / "net.xml", SCH)
        run("pcb", "export", "pos", "--format", "csv", "--units", "mm", "-o", tmp / "pos.csv", PCB)
        run("pcb", "export", "gerbers", "--board-plot-params", "-o", str(cam) + "/", PCB)
        run("pcb", "export", "drill", "--excellon-separate-th", "-o", str(cam) + "/", PCB)
        with zipfile.ZipFile(OUT / "GERBER-GEA-Adapter-Rev3F.zip", "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(cam.iterdir()):
                z.write(f, f.name)
        comps = []
        for c in ET.parse(tmp / "net.xml").findall("components/comp"):
            props = {p.get("name"): p.get("value", "") for p in c.findall("property")}
            if c.findtext("footprint") and not {"dnp", "exclude_from_bom"} & props.keys():
                comps.append((c.get("ref"), c.findtext("value"), c.findtext("footprint"), props.get("LCSC", "")))
        missing = [r for r, _, _, l in comps if not l]
        if missing:
            sys.exit(f"LCSC code missing for: {missing}")
        key = lambda r: (r[0].rstrip("0123456789"), int(r[0][len(r[0].rstrip("0123456789")):] or 0))
        comps.sort(key=key)
        with open(OUT / "BOM-GEA-Adapter-Rev3F.csv", "w", newline="") as f:
            w = csv.writer(f, quoting=csv.QUOTE_ALL, lineterminator="\n")
            w.writerow(["Comment", "Designator", "Footprint", "LCSC Part #"])
            for ref, val, fp, lcsc in comps:
                w.writerow([val, ref, fp, lcsc])
        pos = {r["Ref"]: r for r in csv.DictReader(open(tmp / "pos.csv", newline=""))}
        origins = {}
        if ORIGINS.exists():
            for ref, rec in json.loads(ORIGINS.read_text())["references"].items():
                origins[ref] = rec["body_center_xy_mm"]
        with open(OUT / "CPL-GEA-Adapter-Rev3F.csv", "w", newline="") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(["Designator", "MidX", "MidY", "Rotation", "Layer"])
            for ref, *_ in comps:
                p = pos[ref]
                x, y = origins.get(ref, (float(p["PosX"]), float(p["PosY"])))
                w.writerow([ref, f"{float(x):.6f}", f"{float(y):.6f}", f"{float(p['Rot']):.6f}", p["Side"].capitalize()])
        print(f"{len(comps)} assembled references; CAM members: {len(list(cam.iterdir()))}")


if __name__ == "__main__":
    main()
