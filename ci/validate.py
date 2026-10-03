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


def command(args, output, name, cwd=ROOT):
    with (output / f"{name}.log").open("w") as log:
        result = subprocess.run(list(map(str, args)), cwd=cwd, stdout=log,
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


def inventory(board, output, manifest):
    files = sources(board)
    files += [path(board[key]) for key in ("bom", "cpl", "archive")]
    return {"files": {str(file.relative_to(ROOT)): sha(file) for file in files}}


def hardware(board, output, manifest):
    tool("kicad-cli", manifest["tools"]["kicad"])
    _, sch, pcb = sources(board)
    results = {}
    for mode, source, extra in [("erc", sch, []), ("drc", pcb, ["--schematic-parity", "--all-track-errors"])]:
        report = output / f"{mode}.json"
        results[mode] = command(["kicad-cli", "sch" if mode == "erc" else "pcb", mode,
                                "--severity-all", "--exit-code-violations", "--format", "json",
                                "--output", report, *extra, source], output, mode)
    # Run both checks before failing so inherited issues remain available as artifacts.
    require(all(code == 0 for code in results.values()), f"Native checks failed: {results}; see reports")
    require(all((output / f"{mode}.json").is_file() for mode in results), "Native report missing")
    return {"native_exit_codes": results, "source_sha256": {p.name: sha(p) for p in sources(board)}}


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


def manufacturing(board, output, manifest):
    tool("kicad-cli", manifest["tools"]["kicad"])
    _, sch, pcb = sources(board)
    netlist, positions = output / "netlist.xml", output / "positions.csv"
    generated = output / "gerbers"
    generated.mkdir(exist_ok=True)
    for name, args in [
        ("netlist", ["sch", "export", "netlist", "--format", "kicadxml", "-o", netlist, sch]),
        ("positions", ["pcb", "export", "pos", "--format", "csv", "--units", "mm", "-o", positions, pcb]),
        ("gerbers", ["pcb", "export", "gerbers", "--board-plot-params", "-o", str(generated) + "/", pcb]),
        ("drills", ["pcb", "export", "drill", "--excellon-separate-th", "-o", str(generated) + "/", pcb])
    ]:
        require(command(["kicad-cli", *args], output, name) == 0, f"Native {name} export failed")
    components = {}
    for item in ET.parse(netlist).findall("components/comp"):
        properties = {p.attrib["name"]: p.attrib.get("value", "") for p in item.findall("property")}
        if item.findtext("footprint") and not {"dnp", "exclude_from_bom"} & properties.keys():
            components[item.attrib["ref"]] = (item.findtext("value"), item.findtext("footprint"), properties)
    bom, cpl, pos = rows(path(board["bom"]), "Designator"), rows(path(board["cpl"]), "Designator"), rows(positions, "Ref")
    expected = set(components)
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
            delta = value - float(pos[ref][native])
            if native == "Rot":
                delta = (delta + 180) % 360 - 180
            require(math.isfinite(value) and abs(delta) <= 0.00001, f"CPL {native} differs from PCB: {ref}")
        require(cpl[ref]["Layer"].lower() == pos[ref]["Side"].lower(), f"CPL side differs from PCB: {ref}")
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
    return {"assembled_references": len(expected), "native_matched_gerber_and_drill_files": len(generated_files),
            "source_sha256": {p.name: sha(p) for p in sources(board)}}


def rules(board, output, manifest):
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
    (output / "intended-rule-audit.json").write_text(json.dumps({"intended": intended, "findings": findings}, indent=2) + "\n")
    require(not findings, "; ".join(findings))
    return {"explicit_net_assignments_checked": len(intended), "notice": "Configured native DRC and intended-rule coverage are separate checks"}


def release(board, output, manifest):
    current_sources = {str(p.relative_to(ROOT)): sha(p) for p in sources(board)}
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
        elif sha(path(evidence["evidence"])) != evidence["sha256"]:
            findings.append(f"BLOCKED {gate}: evidence hash differs")
    (output / "readiness.json").write_text(json.dumps({"gates": readiness, "findings": findings}, indent=2) + "\n")
    require(not findings, "; ".join(findings))
    return {"readiness": "passed", "notice": "Readiness evidence is reviewed independently from native CI checks"}


def firmware(output, manifest):
    tool("esphome", manifest["tools"]["esphome"])
    profiles = manifest.get("firmware", [])
    require(profiles, "MISSING: no firmware compile profiles declared")
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
            results[profile] = {"source_sha256": sha(source), "config_exit_code": config,
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
    selected = {"firmware": None} if args.stage == "firmware" else manifest["boards"]
    require(args.revision == "all" or args.revision in selected, f"Unknown revision: {args.revision}")
    for revision, board in selected.items():
        if args.revision != "all" and args.revision != revision:
            continue
        destination = output / revision
        destination.mkdir(exist_ok=True)
        try:
            result = firmware(destination, manifest) if args.stage == "firmware" else globals()[args.stage](board, destination, manifest)
            results[revision] = {"status": "passed", "details": result}
        except (ValueError, OSError, KeyError, StopIteration, ET.ParseError, zipfile.BadZipFile, subprocess.CalledProcessError) as error:
            results[revision] = {"status": "failed", "reason": str(error)}
        print(f"{args.stage}/{revision}: {results[revision]['status']}: {results[revision].get('reason', '')}")
    (output / "summary.json").write_text(json.dumps(results, indent=2) + "\n")
    return 0 if results and all(r["status"] == "passed" for r in results.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
