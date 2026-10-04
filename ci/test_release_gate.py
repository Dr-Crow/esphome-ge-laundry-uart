"""Regression coverage for qualification evidence outside version control."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import validate


class ReleaseEvidenceTest(unittest.TestCase):
    def test_native_rule_added_after_qualification_invalidates_it(self):
        with tempfile.TemporaryDirectory(prefix="native-rule-evidence-") as temporary:
            root = Path(temporary)
            for extension in (".kicad_pro", ".kicad_sch", ".kicad_pcb"):
                (root / ("board" + extension)).write_text("test source\n")
            board = {"source": "board"}
            evidence = root / "evidence.json"
            evidence.write_text('{"qualification": "test-only"}\n')
            with patch.object(validate, "ROOT", root):
                source_hashes = {str(p.relative_to(root)): validate.sha(p)
                                 for p in validate.design_inputs(board)}
                board["readiness"] = {
                    gate: {"state": "passed", "evidence": evidence.name,
                           "sha256": validate.sha(evidence), "source_sha256": source_hashes}
                    for gate in ("power", "source", "physical")
                }
                (root / "board.kicad_dru").write_text('(version 1)\n')
                output = root / "output"
                output.mkdir()
                with self.assertRaisesRegex(ValueError, "qualification does not match current source hashes"):
                    validate.release(board, output, {})

    def test_declared_native_rule_missing_is_an_error(self):
        with tempfile.TemporaryDirectory(prefix="native-rule-missing-") as temporary:
            root = Path(temporary)
            for extension in (".kicad_pro", ".kicad_sch", ".kicad_pcb"):
                (root / ("board" + extension)).write_text("test source\n")
            with patch.object(validate, "ROOT", root):
                with self.assertRaisesRegex(ValueError, "MISSING: board.kicad_dru"):
                    validate.design_inputs({"source": "board", "design_rules": "board.kicad_dru"})

    def test_untracked_evidence_cannot_pass_readiness(self):
        manifest = json.loads((validate.ROOT / "ci/manifest.json").read_text())
        board = manifest["boards"]["rev2.2"]
        source_hashes = {str(p.relative_to(validate.ROOT)): validate.sha(p)
                         for p in validate.design_inputs(board)}
        # Keep the fixture in the actual checkout so git, rather than a mock,
        # determines whether this otherwise valid qualification file is tracked.
        with tempfile.NamedTemporaryFile(dir=validate.ROOT, prefix="qualification-test-",
                                         suffix=".json") as temporary:
            evidence = Path(temporary.name)
            evidence.write_text('{"qualification": "test-only"}\n')
            board["readiness"] = {
                gate: {"state": "passed", "evidence": str(evidence.relative_to(validate.ROOT)),
                       "sha256": validate.sha(evidence), "source_sha256": source_hashes,
                       "external_kicad": validate.external_identity(board, manifest)}
                for gate in ("power", "source", "physical")
            }
            with tempfile.TemporaryDirectory(prefix="qualification-result-") as output:
                with self.assertRaisesRegex(ValueError, "qualification evidence is not tracked in git"):
                    validate.release(board, Path(output), manifest)
                result = json.loads((Path(output) / "readiness.json").read_text())
                self.assertEqual(len(result["findings"]), 3)


class NativeClearanceTest(unittest.TestCase):
    def test_legacy_explicit_membership_cannot_be_removed(self):
        manifest = json.loads((validate.ROOT / "ci/manifest.json").read_text())
        board = manifest["boards"]["rev1.0"]
        with tempfile.TemporaryDirectory(prefix="legacy-membership-") as temporary:
            root = Path(temporary)
            source = validate.ROOT / "pcb/rev1.0/design"
            destination = root / "pcb/rev1.0/design"
            shutil.copytree(source, destination)
            output = root / "output"
            output.mkdir()
            with patch.object(validate, "ROOT", root):
                validate.rules(board, output, manifest)
                project = destination / "OnionStraws.kicad_pro"
                settings = json.loads(project.read_text())
                next(item for item in settings["net_settings"]["classes"]
                     if item["name"] == "Power")["nets"].remove("/p1")
                project.write_text(json.dumps(settings) + "\n")
                with self.assertRaisesRegex(ValueError, "Missing explicit netclass assignment: /p1 -> Power"):
                    validate.rules(board, output, manifest)
                # Modern pattern-based settings cannot fall back to stale legacy lists.
                next(item for item in settings["net_settings"]["classes"]
                     if item["name"] == "Power")["nets"].append("/p1")
                settings["net_settings"]["meta"]["version"] = 3
                settings["net_settings"]["netclass_patterns"] = []
                project.write_text(json.dumps(settings) + "\n")
                with self.assertRaisesRegex(ValueError, "Missing explicit netclass assignment: /p1 -> Power"):
                    validate.rules(board, output, manifest)

    def test_lowered_clearance_is_rejected_with_unchanged_net_assignments(self):
        manifest = json.loads((validate.ROOT / "ci/manifest.json").read_text())
        board = manifest["boards"]["rev2.2"]
        with tempfile.TemporaryDirectory(prefix="native-clearance-") as temporary:
            root = Path(temporary)
            source = validate.ROOT / "pcb/rev2.2/design"
            destination = root / "pcb/rev2.2/design"
            shutil.copytree(source, destination)
            output = root / "output"
            output.mkdir()
            with patch.object(validate, "ROOT", root):
                validate.rules(board, output, manifest)
                project = destination / "OnionStraws.kicad_pro"
                settings = json.loads(project.read_text())
                next(item for item in settings["net_settings"]["classes"]
                     if item["name"] == "Power")["clearance"] = 0.15
                project.write_text(json.dumps(settings) + "\n")
                with self.assertRaisesRegex(ValueError, "Intended Power clearance differs"):
                    validate.rules(board, output, manifest)


if __name__ == "__main__":
    unittest.main()
