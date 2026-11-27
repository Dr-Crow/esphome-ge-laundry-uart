import csv, json, subprocess, sys, tempfile, zipfile, xml.etree.ElementTree as ET
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT, DESIGN = ROOT / "manufacturing", ROOT / "design"
SCH, PCB = DESIGN / "GEA-Adapter-Rev3M.kicad_sch", DESIGN / "GEA-Adapter-Rev3M.kicad_pcb"
ORIGINS = OUT / "placement-origin-review.json"

def run(*args):
    subprocess.run(["kicad-cli", *map(str, args)], check=True, stdout=subprocess.DEVNULL)


def validate_centers(rows):
    with (ROOT / "evidence/component-body-edge.csv").open(newline="") as source:
        bodies = {row["ref"]: row for row in csv.DictReader(source)}
    refs = [row["Designator"] for row in rows]
    if len(set(refs)) != len(refs) or set(refs) != bodies.keys():
        raise ValueError("CPL designators must match all fitted body records exactly once")
    for row in rows:
        ref = row["Designator"]
        if row["Layer"] != "Top":
            raise ValueError(f"{ref}: expected a top-side placement")
        body = bodies[ref]
        mid_x = (float(body["left"]) + float(body["right"])) / 2
        # The body table uses board Y-down. The KiCad CPL uses Y-up.
        mid_y = -(float(body["top"]) + float(body["bottom"])) / 2
        error = math.hypot(float(row["MidX"]) - mid_x, float(row["MidY"]) - mid_y)
        if not error <= 0.10:
            raise ValueError(f"{ref}: CPL is {error:.4f} mm from the reviewed body center")
    return len(refs)


def placement_rows(comps, pos, review):
    datums = review["references"]
    if datums.keys() != {ref for ref, *_ in comps if ref.startswith("J")}:
        raise ValueError("Each fitted connector needs a reviewed placement datum")
    rows = []
    for ref, _, footprint, _ in comps:
        native = pos[ref]
        x, y = float(native["PosX"]), float(native["PosY"])
        rotation = float(native["Rot"])
        side = native["Side"].lower()
        if ref in datums:
            datum = datums[ref]
            if datum["footprint"] != footprint or side != "top":
                raise ValueError(f"{ref}: footprint or side differs from the reviewed datum")
            dx, dy = datum["local_body_center_xy_mm"]
            angle = math.radians(rotation)
            datum.update(native_anchor_xy_mm=[x, y], rotation_degrees=rotation, side=side)
            x += dx * math.cos(angle) + dy * math.sin(angle)
            y += dx * math.sin(angle) - dy * math.cos(angle)
            datum["body_center_xy_mm"] = [round(x, 6), round(y, 6)]
        rows.append({"Designator": ref, "MidX": f"{x:.6f}", "MidY": f"{y:.6f}",
                     "Rotation": f"{rotation:.6f}", "Layer": side.capitalize()})
    validate_centers(rows)
    return rows


def main():
    with tempfile.TemporaryDirectory(dir=OUT) as tmp:
        tmp = Path(tmp)
        cam = tmp / "cam"; cam.mkdir()
        run("sch", "export", "netlist", "--format", "kicadxml", "-o", tmp / "net.xml", SCH)
        run("pcb", "export", "pos", "--format", "csv", "--units", "mm", "-o", tmp / "pos.csv", PCB)
        run("pcb", "export", "gerbers", "--board-plot-params", "-o", str(cam) + "/", PCB)
        run("pcb", "export", "drill", "--excellon-separate-th", "-o", str(cam) + "/", PCB)
        with zipfile.ZipFile(tmp / "CAM-GEA-Adapter-Rev3M-review.zip", "w", zipfile.ZIP_DEFLATED) as z:
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
        with open(tmp / "BOM-GEA-Adapter-Rev3M.csv", "w", newline="") as f:
            w = csv.writer(f, quoting=csv.QUOTE_ALL, lineterminator="\n")
            w.writerow(["Comment", "Designator", "Footprint", "LCSC Part #"])
            for ref, val, fp, lcsc in comps:
                w.writerow([val, ref, fp, lcsc])
        with (tmp / "pos.csv").open(newline="") as source:
            pos = {row["Ref"]: row for row in csv.DictReader(source)}
        review = json.loads(ORIGINS.read_text())
        rows = placement_rows(comps, pos, review)
        with (tmp / "CPL-GEA-Adapter-Rev3M.csv").open("w", newline="") as output:
            writer = csv.DictWriter(output, fieldnames=["Designator", "MidX", "MidY", "Rotation", "Layer"], lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
        (tmp / ORIGINS.name).write_text(json.dumps(review, indent=2) + "\n")
        for name in ("CAM-GEA-Adapter-Rev3M-review.zip", "BOM-GEA-Adapter-Rev3M.csv",
                     "CPL-GEA-Adapter-Rev3M.csv", ORIGINS.name):
            (tmp / name).replace(OUT / name)
        print(f"{len(comps)} assembled references; CAM members: {len(list(cam.iterdir()))}")


if __name__ == "__main__":
    if sys.argv[1:] == ["--check-cpl"]:
        with (OUT / "CPL-GEA-Adapter-Rev3M.csv").open(newline="") as source:
            count = validate_centers(list(csv.DictReader(source)))
        print(f"{count} fitted centers agree with the body audit within 0.10 mm")
    else:
        main()
