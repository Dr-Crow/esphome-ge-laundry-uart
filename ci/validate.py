#!/usr/bin/env python3
"""Small native validation driver. Every failed or unavailable check stays red."""
import argparse
import csv
import hashlib
import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def path(name):
    result = (ROOT / name).resolve()
    require(result.is_relative_to(ROOT), f"Path outside checkout: {name}")
    require(result.is_file(), f"MISSING: {name}")
    return result


def sha(file):
    return hashlib.sha256(file.read_bytes()).hexdigest()


def command(args, output, name, cwd=None):
    with (output / f"{name}.log").open("w") as log:
        result = subprocess.run(list(map(str, args)), cwd=ROOT if cwd is None else cwd, stdout=log,
                                stderr=subprocess.STDOUT, check=False)
    return result.returncode


def tool(name, version):
    result = subprocess.run([name, "--version"], capture_output=True, text=True, check=True)
    actual = (result.stdout + result.stderr).strip()
    require(re.search(rf"(?<![\d.]){re.escape(version)}(?![\d.])", actual),
            f"Expected {name} {version}, got {actual}")
    return actual


def sources(board):
    require(board.get("source"), "MISSING: editable KiCad source absent from current revision package")
    return [path(board["source"] + ext) for ext in
            (".kicad_pro", ".kicad_sch", ".kicad_pcb")]


def design_dependencies(board):
    """Canonical local CAD/library/model closure; stock references stay external."""
    core = sources(board)
    project = core[0].parent
    files = {file for file in core}
    external, local_libraries = set(), {}

    def reference(uri):
        if re.match(r"^\$\{(?:KICAD[689]_(?:SYMBOL|FOOTPRINT|3DMODEL)_DIR|KISYS3DMOD)\}/", uri):
            external.add(uri)
            return None
        uri = uri.replace("${KIPRJMOD}", str(project))
        require("${" not in uri and not re.match(r"^[a-zA-Z]+://", uri),
                f"Unsupported design dependency: {uri}")
        resolved = (project / uri).resolve()
        require(resolved.is_relative_to(ROOT), f"Design dependency outside checkout: {uri}")
        return resolved

    native_rules = core[0].with_suffix(".kicad_dru")
    if board.get("design_rules"):
        require(path(board["design_rules"]) == native_rules,
                "Declared native rules do not match the source stem")
    if native_rules.is_file():
        files.add(native_rules)
    # Manifest declarations make removal of a real project table a missing input.
    tables = {path(name) for name in board.get("library_tables", [])}
    tables |= {project / name for name in ("fp-lib-table", "sym-lib-table")
               if (project / name).is_file()}
    for table in sorted(tables):
        files.add(table)
        entries = re.findall(r'\(lib\s+\(name\s+"([^"\n]+)"\).*?\(uri\s+"([^"\n]+)"\)',
                             table.read_text(), re.DOTALL)
        require(len(entries) == len(re.findall(r"\(lib\s", table.read_text())),
                f"Unsupported library table entry: {table.relative_to(ROOT)}")
        for name, uri in entries:
            resolved = reference(uri)
            if resolved is None:
                continue
            local_libraries[(table.name, name)] = resolved
            if resolved.suffix == ".pretty":
                require(resolved.is_dir(), f"MISSING: {resolved.relative_to(ROOT)}")
                footprints = list(resolved.glob("*.kicad_mod"))
                require(footprints, f"MISSING: local footprint library empty: {resolved.relative_to(ROOT)}")
                files.update(footprints)
            else:
                files.add(path(str(resolved.relative_to(ROOT))))
    # Bind additional project-local library/models too, including retained envelopes.
    files.update(p for p in project.rglob("*") if p.is_file() and
                 p.suffix.lower() in (".kicad_mod", ".kicad_sym", ".step", ".stp", ".wrl"))
    pending = [core[1]]
    while pending:
        schematic = pending.pop()
        for uri in re.findall(r'\(property\s+"Sheetfile"\s+"([^"\n]+)"', schematic.read_text()):
            dependency = path(str((schematic.parent / uri).resolve().relative_to(ROOT)))
            if dependency not in files:
                files.add(dependency)
                pending.append(dependency)
    for file in list(files):
        if file.suffix not in (".kicad_sch", ".kicad_pcb", ".kicad_mod"):
            continue
        text = file.read_text()
        for uri in re.findall(r'\(model\s+"([^"\n]+)"', text):
            dependency = reference(uri)
            if dependency is not None:
                files.add(path(str(dependency.relative_to(ROOT))))
        footprints = re.findall(r'\(footprint\s+"([^"\n]+)"', text)
        footprints += re.findall(r'\(property\s+"Footprint"\s+"([^"\n]+)"', text)
        for footprint in footprints:
            if ":" not in footprint:
                continue
            library, name = footprint.split(":", 1)
            local = local_libraries.get(("fp-lib-table", library))
            if local is not None:
                files.add(path(str((local / (name + ".kicad_mod")).relative_to(ROOT))))
    return sorted({path(str(p.relative_to(ROOT))) for p in files}), sorted(external)


def design_inputs(board):
    return design_dependencies(board)[0]


def source_identity(board):
    return {str(p.relative_to(ROOT)): sha(p) for p in design_inputs(board)}


def external_identity(board, manifest):
    references = design_dependencies(board)[1]
    provenance = manifest.get("external_kicad", {})
    if references:
        require(provenance.get("version") == manifest["tools"]["kicad"] and
                all(re.fullmatch(r"[0-9a-f]{40}", provenance.get(name, ""))
                    for name in ("symbols_commit", "footprints_commit", "models_commit")) and
                re.fullmatch(r"sha256:[0-9a-f]{64}", provenance.get("container_digest", "")),
                "MISSING: pinned external KiCad library/model provenance")
    return {"references": references, "provenance": dict(provenance) if references else {}}


def inventory(board, output, manifest):
    files, missing, external = [], [], {}
    try:
        files += design_inputs(board)
        external = external_identity(board, manifest)
    except ValueError as error:
        missing.append(str(error))
    for key in ("bom", "cpl", "archive"):
        if not board.get(key):
            missing.append(f"MISSING: supplier {key.upper()} not declared")
        else:
            try:
                files.append(path(board[key]))
            except ValueError as error:
                missing.append(str(error))
    if board.get("historical_archive"):
        files.append(path(board["historical_archive"]))
    result = {"files": {str(file.relative_to(ROOT)): sha(file) for file in files},
              "missing": missing, "external_kicad": external}
    (output / "files.json").write_text(json.dumps(result, indent=2) + "\n")
    require(not missing, "; ".join(missing))
    return result


def firmware_inputs(profile):
    """Hash the declared local YAML/include closure, excluding private secrets."""
    files, pending = {}, [path(profile)]
    while pending:
        source = pending.pop()
        relative = str(source.relative_to(ROOT))
        require(source.is_relative_to(ROOT / "firmware") and source.suffix in (".yaml", ".yml")
                and source.name != "secrets.yaml", f"Invalid firmware input: {relative}")
        if relative in files:
            continue
        files[relative] = sha(source)
        for include in re.findall(r"^[^#\n]*!include\s+([^\n]+)", source.read_text(), re.MULTILINE):
            # These profiles use plain or quoted local paths, not substitutions/maps.
            include = include.split(" #", 1)[0].strip().strip("\"'")
            require(include and not any(c in include for c in "{}$"),
                    f"Unsupported local include in {relative}: {include}")
            pending.append(path(str((source.parent / include).relative_to(ROOT))))
    return dict(sorted(files.items()))


def firmware_inventory(output, manifest):
    profiles = manifest.get("firmware", [])
    require(isinstance(profiles, list) and profiles, "MISSING: no firmware compile profiles declared")
    require(all(isinstance(p, str) for p in profiles), "Invalid firmware profile declaration")
    require(len(set(profiles)) == len(profiles), "Duplicate firmware compile profile")
    result = {profile: {"source_sha256": sha(path(profile)),
                        "input_sha256": firmware_inputs(profile)} for profile in profiles}
    (output / "profiles.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


def hardware(board, output, manifest):
    inputs = design_inputs(board)
    tool("kicad-cli", manifest["tools"]["kicad"])
    _, sch, pcb = sources(board)
    results = {}
    # ERC can migrate old project metadata. Preserve committed inputs and libraries.
    with tempfile.TemporaryDirectory(prefix="gea-native-") as temporary:
        checkout = Path(temporary) / "checkout"
        for file in inputs:
            destination = checkout / file.relative_to(ROOT)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file, destination)
        for mode, source, extra in [("erc", checkout / sch.relative_to(ROOT), []),
                                   ("drc", checkout / pcb.relative_to(ROOT), ["--schematic-parity", "--all-track-errors"])]:
            report = output / f"{mode}.json"
            report.unlink(missing_ok=True)
            results[mode] = command(["kicad-cli", "sch" if mode == "erc" else "pcb", mode,
                                    "--severity-all", "--exit-code-violations", "--format", "json",
                                    "--output", report, *extra, source], output, mode)
    details = {"native_exit_codes": results, "source_sha256": {str(p.relative_to(ROOT)): sha(p) for p in inputs},
               "external_kicad": external_identity(board, manifest)}
    (output / "native-checks.json").write_text(json.dumps(details, indent=2) + "\n")
    # Run both checks before failing so inherited issues remain available as artifacts.
    require(all((output / f"{mode}.json").is_file() for mode in results), "Native report missing")
    require(all(code == 0 for code in results.values()), f"Native checks failed: {results}; see reports")
    return details


def rows(file, key):
    with file.open(newline="", encoding="utf-8-sig") as stream:
        result = {}
        for row in csv.DictReader(stream):
            refs = [item.strip() for item in row[key].split(",")]
            require(all(refs), f"Empty designator in {file.name}")
            if "Quantity" in row:
                require(int(row["Quantity"]) == len(refs), f"BOM quantity mismatch: {refs}")
            for ref in refs:
                require(ref not in result, f"Duplicate designator {ref}: {file.name}")
                result[ref] = row
    require(result, f"Empty file: {file.name}")
    return result


def gerber_content(data):
    # Only creation timestamps are volatile. Keep geometry, attributes and generator version.
    return "\n".join(line for line in data.decode("utf-8").splitlines()
                     if not (line.startswith(("%TF.CreationDate,", "; #@! TF.CreationDate,"))
                             or re.match(r"G04 Created by KiCad \(PCBNEW [^)]+\) date ", line)
                             or re.match(r"; DRILL file \{KiCad [^}]+\} date ", line)))


def placement_numbers(value, size, ref):
    require(isinstance(value, list) and len(value) == size and
            all(type(number) in (int, float) and abs(number) <= sys.float_info.max and
                math.isfinite(number) for number in value),
            f"Malformed or nonfinite placement-origin evidence: {ref}")
    return value


def committed_placement_evidence(declaration, label):
    require(isinstance(declaration, dict) and
            isinstance(declaration.get("evidence"), str) and declaration["evidence"] and
            not Path(declaration["evidence"]).is_absolute() and
            ".." not in Path(declaration["evidence"]).parts and
            isinstance(declaration.get("sha256"), str) and
            re.fullmatch(r"[0-9a-f]{64}", declaration["sha256"]),
            f"Malformed {label} declaration")
    evidence = path(declaration["evidence"])
    require(sha(evidence) == declaration["sha256"], f"{label} hash differs")
    relative = str(evidence.relative_to(ROOT))
    committed = subprocess.run(["git", "show", "HEAD:" + relative], cwd=ROOT,
                               capture_output=True, check=False)
    require(committed.returncode == 0 and
            hashlib.sha256(committed.stdout).hexdigest() == declaration["sha256"],
            f"{label} is not committed at HEAD")
    return evidence


def reviewed_placement_origins(board, inputs, positions, output, components=None):
    if "cpl_centroid_policy" not in board:
        return {}
    policy = board["cpl_centroid_policy"]
    evidence = committed_placement_evidence(policy, "Placement-origin evidence")

    def unique_keys(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, f"Duplicate placement-origin evidence key: {key}")
            result[key] = value
        return result

    review = json.loads(evidence.read_text(), object_pairs_hook=unique_keys)
    require(isinstance(review, dict) and isinstance(review.get("references"), dict) and
            review["references"], "Malformed placement-origin review")
    require(set(inputs) == set(design_inputs(board)),
            "Placement-origin inputs omit current source dependencies")
    require(review.get("source_sha256") == {str(p.relative_to(ROOT)): sha(p) for p in inputs},
            "Placement-origin review does not match current source hashes")
    requested = policy.get("required_references")
    if "required_references" in policy:
        require(isinstance(requested, list) and requested and
                all(isinstance(ref, str) and ref for ref in requested) and
                len(set(requested)) == len(requested),
                "Malformed required placement-origin references")
        require(set(requested) <= set(positions), "Required placement-origin reference absent from PCB")
        require(set(requested) == set(review["references"]),
                "Placement-origin review differs from required references")
    origins = {}
    for ref, record in review["references"].items():
        require(isinstance(record, dict) and isinstance(record.get("footprint"), str) and
                record["footprint"], f"Malformed placement-origin evidence: {ref}")
        require(ref in positions, f"Placement-origin reference absent: {ref}")
        native = positions[ref]
        require(native["Package"] == record["footprint"].split(":")[-1],
                f"Placement-origin footprint differs: {ref}")
        anchor = placement_numbers(record.get("native_anchor_xy_mm"), 2, ref)
        rotation = placement_numbers([record.get("rotation_degrees")], 1, ref)[0]
        require(all(math.isfinite(float(native[key])) and
                    abs(anchor[i] - float(native[key])) <= 0.00001
                    for i, key in enumerate(("PosX", "PosY"))),
                f"Placement-origin geometry differs: {ref}")
        require(math.isfinite(float(native["Rot"])) and
                abs((float(native["Rot"]) - rotation + 180) % 360 - 180) <= 0.00001,
                f"Placement-origin rotation differs: {ref}")
        # An omitted type retains the original Rev2.1 pad-bounds convention.
        datum = record.get("datum_type", "pad_bbox_center")
        require(datum in ("pad_bbox_center", "module_pcb_body_bbox_center",
                          "manufacturer_nominal_body_bbox_center"),
                f"Unknown placement-origin datum type: {ref}")
        if datum == "pad_bbox_center":
            require(not {"body_center_xy_mm", "local_body_center_xy_mm", "manufacturer_datum"} & record.keys(),
                    f"Body datum cannot use the pad-bounds convention: {ref}")
            center = placement_numbers(record.get("pad_bbox_center_xy_mm"), 2, ref)
            bounds = placement_numbers(record.get("native_pad_bbox_xy_mm"), 4, ref)
            require(all(bounds[i] <= bounds[i+2] and
                        abs(center[i] - (bounds[i] + bounds[i+2]) / 2) <= 0.00001 for i in range(2)),
                    f"Placement-origin geometry differs: {ref}")
        else:
            require(requested is not None and ref in requested,
                    f"Body-datum reference must be explicitly required: {ref}")
            require(not {"pad_bbox_center_xy_mm", "native_pad_bbox_xy_mm"} & record.keys(),
                    f"Body datum cannot substitute pad-bounds evidence: {ref}")
            require(components is not None and ref in components and
                    record["footprint"] == components[ref][1],
                    f"Body-datum full footprint differs or component identity missing: {ref}")
            require(record.get("side") == "top" == native.get("Side", "").lower(),
                    f"Body-datum side differs or is unsupported: {ref}")
            manufacturer = record.get("manufacturer_datum")
            require(isinstance(manufacturer, dict) and
                    all(isinstance(manufacturer.get(key), str) and manufacturer[key].strip()
                        for key in ("manufacturer", "mpn", "source_url", "datum_description")) and
                    re.fullmatch(r"https://[^\s]+", manufacturer["source_url"]),
                    f"Malformed manufacturer datum basis: {ref}")
            properties = components[ref][2]
            require(manufacturer["manufacturer"] == properties.get("Manufacturer") and
                    manufacturer["mpn"] == properties.get("MPN"),
                    f"Manufacturer datum part identity differs: {ref}")
            committed_placement_evidence(manufacturer, f"Manufacturer datum evidence for {ref}")
            local = placement_numbers(record.get("local_body_center_xy_mm"), 2, ref)
            center = placement_numbers(record.get("body_center_xy_mm"), 2, ref)
            angle = math.radians(rotation)
            expected = [anchor[0] + math.cos(angle) * local[0] + math.sin(angle) * local[1],
                        anchor[1] + math.sin(angle) * local[0] - math.cos(angle) * local[1]]
            require(all(abs(center[i] - expected[i]) <= 0.00001 for i in range(2)),
                    f"Body-datum local/export geometry differs: {ref}")
        origins[ref] = {"PosX": center[0], "PosY": center[1]}
    (output / "placement-origin-review.json").write_text(json.dumps(review, indent=2) + "\n")
    return origins


def matched_archive(board, generated):
    generated_files = {p.name: p.read_bytes() for p in generated.iterdir() if p.is_file() and not p.name.endswith(".gbrjob")}
    with zipfile.ZipFile(path(board["archive"])) as archive:
        require(archive.testzip() is None, "Gerber ZIP integrity failure")
        names = archive.namelist()
        require(len(set(names)) == len(names), "Duplicate ZIP members")
        require(all(Path(n).name == n and n not in (".", "..") for n in names), "ZIP must contain flat safe filenames")
        jobs = [n for n in names if n.endswith(".gbrjob")]
        require(len(jobs) == 1, "Expected one Gerber job file")
        job = json.loads(archive.read(jobs[0]))
        native_job = json.loads((generated / jobs[0]).read_text())
        job["Header"].pop("CreationDate", None)
        native_job["Header"].pop("CreationDate", None)
        require(job == native_job, "Gerber job/source metadata differs")
        plotted = {entry["Path"] for entry in job["FilesAttributes"]}
        drills = {n for n in names if n.endswith(".drl")}
        require(plotted and drills, "Missing Gerber/drill members")
        require(plotted | drills == set(generated_files), "Stored archive and native export file sets differ")
        require(plotted | drills <= set(names), "Gerber job references missing members")
        require(all(n in plotted | drills | set(jobs) or n.endswith((".txt", ".rpt")) for n in names),
                "Archive contains undeclared manufacturing members")
        for name, data in generated_files.items():
            require(gerber_content(archive.read(name)) == gerber_content(data), f"Manufacturing/source geometry or metadata differs: {name}")
        copper = [entry for entry in job["FilesAttributes"] if entry["FileFunction"].startswith("Copper,")]
        require(len(copper) == job["GeneralSpecs"]["LayerNumber"], "Gerber job copper layer count mismatch")
    return len(generated_files)


def manufacturing(board, output, manifest):
    inputs = design_inputs(board)
    (output / "cam-parity.json").unlink(missing_ok=True)
    tool("kicad-cli", manifest["tools"]["kicad"])
    _, sch, pcb = sources(board)
    netlist, positions = output / "netlist.xml", output / "positions.csv"
    # Preserve earlier artifacts without mixing them into the current export set.
    generated = Path(tempfile.mkdtemp(prefix="gerbers-", dir=output))
    for name, args in [
        ("netlist", ["sch", "export", "netlist", "--format", "kicadxml", "-o", netlist, sch]),
        ("positions", ["pcb", "export", "pos", "--format", "csv", "--units", "mm", "-o", positions, pcb]),
        ("gerbers", ["pcb", "export", "gerbers", "--board-plot-params", "-o", str(generated) + "/", pcb]),
        ("drills", ["pcb", "export", "drill", "--excellon-separate-th", "-o", str(generated) + "/", pcb])
    ]:
        require(command(["kicad-cli", *args], output, name) == 0, f"Native {name} export failed")
    # CAM identity is independent of missing/unqualified assembly metadata.
    cam_count = matched_archive(board, generated)
    cam = {"archive": board["archive"], "status": "passed",
           "native_matched_gerber_and_drill_files": cam_count,
           "source_sha256": {str(p.relative_to(ROOT)): sha(p) for p in inputs},
           "external_kicad": external_identity(board, manifest)}
    (output / "cam-parity.json").write_text(json.dumps(cam, indent=2) + "\n")
    missing = [key.upper() for key in ("bom", "cpl") if not board.get(key)]
    require(not missing, "MISSING: supplier " + "/".join(missing) +
            "; current review CAM/source parity passed; " + board.get("assembly_note", "assembly inputs absent"))
    components = {}
    for item in ET.parse(netlist).findall("components/comp"):
        properties = {p.attrib["name"]: p.attrib.get("value", "") for p in item.findall("property")}
        if item.findtext("footprint") and not {"dnp", "exclude_from_bom"} & properties.keys():
            components[item.attrib["ref"]] = (item.findtext("value"), item.findtext("footprint"), properties)
    bom, cpl, pos = rows(path(board["bom"]), "Designator"), rows(path(board["cpl"]), "Designator"), rows(positions, "Ref")
    origins = reviewed_placement_origins(board, inputs, pos, output, components)
    expected = set(components)
    require(set(origins) <= expected, "Placement-origin policy includes unassembled references")
    require(set(bom) == set(cpl) == expected,
            f"Assembly reference mismatch: BOM-only={sorted(set(bom)-expected)}, "
            f"CPL-only={sorted(set(cpl)-expected)}, missing-BOM={sorted(expected-set(bom))}, "
            f"missing-CPL={sorted(expected-set(cpl))}")
    for ref, (value, footprint, properties) in components.items():
        require(ref in pos, f"PCB placement missing: {ref}")
        require(bom[ref]["Comment"] == value, f"BOM value differs from schematic: {ref}")
        require(bom[ref]["Footprint"] in (footprint, footprint.split(":")[-1]), f"BOM footprint mismatch: {ref}")
        require(pos[ref]["Val"] == value and pos[ref]["Package"] == footprint.split(":")[-1], f"PCB/schematic metadata mismatch: {ref}")
        require(bom[ref]["LCSC Part #"] == properties.get("LCSC", "") and properties.get("LCSC"), f"LCSC mismatch/missing: {ref}")
        for field in ("Manufacturer", "MPN"):
            if field in bom[ref]:
                require(bom[ref][field] == properties.get(field), f"{field} mismatch: {ref}")
        for alternatives, native in [(("Mid X", "MidX"), "PosX"), (("Mid Y", "MidY"), "PosY"), (("Rotation",), "Rot")]:
            value = float(next(cpl[ref][key] for key in alternatives if key in cpl[ref]))
            delta = value - float(origins.get(ref, {}).get(native, pos[ref][native]))
            if native == "Rot":
                delta = (delta + 180) % 360 - 180
            require(math.isfinite(value) and abs(delta) <= 0.00001, f"CPL {native} differs from PCB: {ref}")
        require(cpl[ref]["Layer"].lower() == pos[ref]["Side"].lower(), f"CPL side differs from PCB: {ref}")
    return {"assembled_references": len(expected), "reviewed_centroid_references": len(origins),
            "native_matched_gerber_and_drill_files": cam_count,
            "source_sha256": {str(p.relative_to(ROOT)): sha(p) for p in inputs},
            "external_kicad": external_identity(board, manifest)}


def rules(board, output, manifest):
    identity = source_identity(board)
    external = external_identity(board, manifest)
    tool("kicad-cli", manifest["tools"]["kicad"])
    project, sch, _ = sources(board)
    intended = board.get("intended_netclasses", {})
    require(intended, "MISSING: intended netclass audit policy not declared")
    netlist = output / "netlist.xml"
    require(command(["kicad-cli", "sch", "export", "netlist", "--format", "kicadxml",
                     "-o", netlist, sch], output, "netlist") == 0, "Native netlist export failed")
    nets = {item.attrib["name"] for item in ET.parse(netlist).findall("nets/net")}
    settings = json.loads(project.read_text())["net_settings"]
    patterns = settings.get("netclass_patterns", [])
    classes = {item["name"] for item in settings["classes"]}
    findings = []
    # Require explicit full net-name assignments, including the sheet-leading slash.
    # This bounded policy intentionally avoids reimplementing KiCad's rule engine.
    for net, expected in intended.items():
        if net not in nets:
            findings.append(f"Intended net absent from native netlist: {net}")
        if expected not in classes or not any(p["pattern"] == net and p["netclass"] == expected for p in patterns):
            findings.append(f"Missing explicit netclass pattern: {net} -> {expected}")
    for name, expected in board.get("intended_clearance_mm", {}).items():
        actual = next((item.get("clearance") for item in settings["classes"]
                       if item["name"] == name), None)
        if not isinstance(actual, (int, float)) or not math.isclose(actual, expected, abs_tol=1e-9):
            findings.append(f"Intended {name} clearance differs: expected {expected} mm, got {actual}")
    (output / "intended-rule-audit.json").write_text(json.dumps({"intended": intended, "findings": findings}, indent=2) + "\n")
    require(not findings, "; ".join(findings))
    return {"explicit_net_assignments_checked": len(intended), "source_sha256": identity,
            "external_kicad": external, "notice": "Configured native DRC and intended-rule coverage are separate checks"}


def release(board, output, manifest):
    current_sources = source_identity(board)
    external = external_identity(board, manifest)
    readiness = board.get("readiness", {})
    findings = []
    for gate in ("power", "source", "physical"):
        evidence = readiness.get(gate, {})
        if evidence.get("state") != "passed":
            findings.append(f"BLOCKED {gate}: {evidence.get('reason', 'qualification evidence missing')}")
        elif not evidence.get("evidence") or not evidence.get("sha256"):
            findings.append(f"BLOCKED {gate}: evidence/hash missing")
        elif evidence.get("source_sha256") != current_sources:
            findings.append(f"BLOCKED {gate}: qualification does not match current source hashes")
        elif external["references"] and evidence.get("external_kicad") != external:
            findings.append(f"BLOCKED {gate}: qualification does not match pinned external KiCad dependencies")
        elif command(["git", "ls-files", "--error-unmatch", "--",
                      path(evidence["evidence"]).relative_to(ROOT)], output,
                     gate + "-evidence-tracked") != 0:
            findings.append(f"BLOCKED {gate}: qualification evidence is not tracked in git")
        elif sha(path(evidence["evidence"])) != evidence["sha256"]:
            findings.append(f"BLOCKED {gate}: evidence hash differs")
        else:
            committed = subprocess.run(["git", "show", "HEAD:" + str(path(evidence["evidence"]).relative_to(ROOT))],
                                       cwd=ROOT, capture_output=True, check=False)
            if committed.returncode != 0 or hashlib.sha256(committed.stdout).hexdigest() != evidence["sha256"]:
                findings.append(f"BLOCKED {gate}: qualification evidence differs from committed HEAD")
    (output / "readiness.json").write_text(json.dumps({"gates": readiness, "findings": findings,
                                                        "source_sha256": current_sources, "external_kicad": external}, indent=2) + "\n")
    require(not findings, "; ".join(findings))
    return {"readiness": "passed", "notice": "Readiness evidence is reviewed independently from native CI checks"}


def firmware(output, manifest):
    tool("esphome", manifest["tools"]["esphome"])
    declared = firmware_inventory(output, manifest)
    profiles = list(declared)
    # Dummy CI credentials stay outside the checkout. Never flash or run a device.
    with tempfile.TemporaryDirectory(prefix="gea-firmware-") as temporary:
        workspace = Path(temporary)
        shutil.copytree(ROOT / "firmware", workspace / "firmware", ignore=shutil.ignore_patterns(".esphome", "secrets.yaml", "__pycache__"))
        (workspace / "firmware" / "secrets.yaml").write_text('wifi_ssid: "ci-test"\nwifi_password: "ci-password"\nesp_home_ota_pw: "ci-ota-password"\n')
        results = {}
        for profile in profiles:
            source = path(profile)
            candidate = workspace / profile
            # Nested package profiles load secrets from their own directory.
            if candidate.parent != workspace / "firmware":
                shutil.copyfile(workspace / "firmware" / "secrets.yaml", candidate.parent / "secrets.yaml")
            name = str(Path(profile).with_suffix("")).replace("/", "-")
            config = command(["esphome", "config", candidate], output, name + "-config", workspace)
            started = time.time()
            compile_status = command(["esphome", "compile", candidate], output, name + "-compile", workspace) if config == 0 else None
            artifacts = [{"path": str(p.relative_to(workspace)), "bytes": p.stat().st_size, "sha256": sha(p)}
                         for p in workspace.rglob("firmware.*")
                         if p.is_file() and p.suffix in (".bin", ".elf") and p.stat().st_mtime >= started]
            results[profile] = {**declared[profile], "config_exit_code": config,
                                "compile_exit_code": compile_status, "artifacts": artifacts}
            if compile_status == 0 and not any(a["path"].endswith(".bin") for a in artifacts):
                results[profile]["compile_exit_code"] = "MISSING: fresh compiled binary"
        (output / "profiles.json").write_text(json.dumps(results, indent=2) + "\n")
        require(all(r["config_exit_code"] == r["compile_exit_code"] == 0 for r in results.values()), "Firmware validation/compilation failed; see profile logs")
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=["inventory", "hardware", "manufacturing", "firmware", "rules", "release"])
    parser.add_argument("--revision", default="all")
    parser.add_argument("--manifest", default="ci/manifest.json")
    parser.add_argument("--output", default="ci-artifacts")
    args = parser.parse_args()
    manifest = json.loads(path(args.manifest).read_text())
    if args.stage == "inventory":
        folders = {p.name for p in (ROOT / "pcb").iterdir() if p.is_dir() and p.name.startswith("rev")}
        require(folders == set(manifest["boards"]), f"Board inventory differs from manifest: undeclared={sorted(folders-set(manifest['boards']))}, missing={sorted(set(manifest['boards'])-folders)}")
    require(manifest.get("schema") == 1, "Unsupported manifest schema")
    output = ROOT / args.output / args.stage
    output.mkdir(parents=True, exist_ok=True)
    results = {}
    selected = {"firmware": None} if args.stage == "firmware" else dict(manifest["boards"])
    if args.stage == "inventory":
        selected["firmware"] = None
    require(args.revision == "all" or args.revision in selected, f"Unknown revision: {args.revision}")
    for revision, board in selected.items():
        if args.revision != "all" and args.revision != revision:
            continue
        destination = output / revision
        destination.mkdir(exist_ok=True)
        try:
            if args.stage == "firmware":
                result = firmware(destination, manifest)
            elif args.stage == "inventory" and revision == "firmware":
                result = firmware_inventory(destination, manifest)
            else:
                result = globals()[args.stage](board, destination, manifest)
            results[revision] = {"status": "passed", "details": result}
        except (ValueError, OSError, KeyError, StopIteration, ET.ParseError, zipfile.BadZipFile, subprocess.CalledProcessError) as error:
            results[revision] = {"status": "failed", "reason": str(error)}
        print(f"{args.stage}/{revision}: {results[revision]['status']}: {results[revision].get('reason', '')}")
    (output / "summary.json").write_text(json.dumps(results, indent=2) + "\n")
    return 0 if results and all(r["status"] == "passed" for r in results.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
