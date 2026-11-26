#!/usr/bin/env python3
"""Regenerate pcb/rev3h/validation/placement-origin-review.json (the J1 CPL body-datum receipt).

Adapted from the Rev3E receipt generator. Rev3H keeps the Rev3C/Rev3D/Rev3E/Rev3G J1 footprint, native anchor,
rotation and EVERCOM nominal body datum; this checks that against the exported Rev3H position file and rebinds the
datum record to the Rev3H source hashes. The source-file closure comes from ci/validate.py (read only) using an
in-memory board entry, because Rev3H is not registered in ci/manifest.json yet.

Run inside the pinned kicad/kicad:9.0.9 image with the repository mounted at /w:
    python3 /w/pcb/rev3h/validation/make_origin_evidence.py
"""
import csv, json, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path("/w")
sys.path.insert(0, str(ROOT / "ci"))
import validate as Vd  # noqa: E402

DESIGN = "pcb/rev3h/design/GEA-Adapter-Rev3H"
board = {"source": DESIGN, "design_rules": DESIGN + ".kicad_dru",
         "library_tables": ["pcb/rev3h/design/fp-lib-table", "pcb/rev3h/design/sym-lib-table"]}
inputs = Vd.design_inputs(board)
hashes = {str(p.relative_to(ROOT)): Vd.sha(p) for p in inputs}
tmp = Path(tempfile.mkdtemp())
subprocess.run(["kicad-cli", "pcb", "export", "pos", "--format", "csv", "--units", "mm", "-o", str(tmp / "pos.csv"),
                str(ROOT / (DESIGN + ".kicad_pcb"))], check=True, stdout=subprocess.DEVNULL)
pos = {r["Ref"]: r for r in csv.DictReader(open(tmp / "pos.csv"))}
c = json.load(open(ROOT / "pcb/rev3c/validation/placement-origin-review.json"))["references"]["J1"]
j1 = pos["J1"]
assert abs(float(j1["PosX"]) - c["native_anchor_xy_mm"][0]) < 1e-6 and abs(float(j1["PosY"]) - c["native_anchor_xy_mm"][1]) < 1e-6, j1
assert abs(float(j1["Rot"]) - c["rotation_degrees"]) < 1e-6 and j1["Side"].lower() == "top", j1
assert c["body_center_xy_mm"] == [8.645, -16.995], c["body_center_xy_mm"]
ev = {
    "source_reference_commit": "87c93d249b641d8abe0ecabc039018aa60343f8c",
    "source_sha256": hashes,
    "references": {"J1": c},
    "supplier_qualification": "Blocked; nominal body datum only; no actual supplier zero/orientation/process/placement approval.",
    "source_rebind_note": "Rev3H keeps the Rev3C/Rev3D/Rev3E/Rev3G J1 footprint, native anchor, rotation and EVERCOM manufacturer datum unchanged (checked against the exported Rev3H position file when this receipt was generated). Rev3H changes are the J7 bus-monitor header with R48-R50 and C16/C17 to C12891; this receipt rebinds the unchanged J1 datum to the Rev3H source hashes.",
}
out = ROOT / "pcb/rev3h/validation/placement-origin-review.json"
out.write_text(json.dumps(ev, indent=2) + "\n")
print("inputs", len(inputs), "J1 ok", Vd.sha(out))
