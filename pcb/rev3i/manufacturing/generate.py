import csv, json, subprocess, sys, tempfile, zipfile, xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT, DESIGN = ROOT / "manufacturing", ROOT / "design"
SCH, PCB = DESIGN / "GEA-Adapter-Rev3I.kicad_sch", DESIGN / "GEA-Adapter-Rev3I.kicad_pcb"
ORIGINS = OUT / "placement-origin-review.json"

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
        with zipfile.ZipFile(OUT / "CAM-GEA-Adapter-Rev3I-review.zip", "w", zipfile.ZIP_DEFLATED) as z:
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
        with open(OUT / "BOM-GEA-Adapter-Rev3I.csv", "w", newline="") as f:
            w = csv.writer(f, quoting=csv.QUOTE_ALL, lineterminator="\n")
            w.writerow(["Comment", "Designator", "Footprint", "LCSC Part #"])
            for ref, val, fp, lcsc in comps:
                w.writerow([val, ref, fp, lcsc])
        pos = {r["Ref"]: r for r in csv.DictReader(open(tmp / "pos.csv", newline=""))}
        origins = {}
        if ORIGINS.exists():
            for ref, rec in json.loads(ORIGINS.read_text())["references"].items():
                origins[ref] = rec["body_center_xy_mm"]
        with open(OUT / "CPL-GEA-Adapter-Rev3I.csv", "w", newline="") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(["Designator", "MidX", "MidY", "Rotation", "Layer"])
            for ref, *_ in comps:
                p = pos[ref]
                x, y = origins.get(ref, (float(p["PosX"]), float(p["PosY"])))
                w.writerow([ref, f"{float(x):.6f}", f"{float(y):.6f}", f"{float(p['Rot']):.6f}", p["Side"].capitalize()])
        print(f"{len(comps)} assembled references; CAM members: {len(list(cam.iterdir()))}")


if __name__ == "__main__":
    main()
