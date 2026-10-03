"""Reviewed centroid conventions must not authorize stale or uncommitted data."""
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import validate


class PlacementOriginTest(unittest.TestCase):
    def fixture(self, root):
        for suffix in (".kicad_pro", ".kicad_sch", ".kicad_pcb"):
            (root / ("board" + suffix)).write_text("reviewed source\n")
        board = {"source": "board"}
        review = {
            "source_sha256": {p.name: validate.sha(p) for p in validate.design_inputs(board)},
            "references": {"J1": {
                "footprint": "Library:RJ45", "native_anchor_xy_mm": [122.425, -99.2825],
                "pad_bbox_center_xy_mm": [124.755, -94.8375],
                "native_pad_bbox_xy_mm": [119.135, -102.1525, 130.375, -87.5225],
                "rotation_degrees": 90.0}}
        }
        evidence = root / "centroid.json"
        evidence.write_text(json.dumps(review) + "\n")
        board["cpl_centroid_policy"] = {"evidence": evidence.name, "sha256": validate.sha(evidence)}
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "-c", "user.name=Dr-Crow", "-c",
                        "user.email=9339757+Dr-Crow@users.noreply.github.com",
                        "commit", "-qm", "test: reviewed centroid fixture"], cwd=root, check=True)
        positions = {"J1": {"Package": "RJ45", "PosX": "122.425", "PosY": "-99.2825", "Rot": "90"}}
        return board, positions

    def test_source_change_invalidates_reviewed_origin(self):
        with tempfile.TemporaryDirectory(prefix="centroid-source-") as temporary:
            root = Path(temporary)
            with patch.object(validate, "ROOT", root):
                board, positions = self.fixture(root)
                origins = validate.reviewed_placement_origins(board, validate.design_inputs(board), positions, root)
                self.assertEqual(origins["J1"], {"PosX": 124.755, "PosY": -94.8375})
                (root / "board.kicad_pcb").write_text("changed geometry\n")
                with self.assertRaisesRegex(ValueError, "does not match current source hashes"):
                    validate.reviewed_placement_origins(board, validate.design_inputs(board), positions, root)

    def test_changed_native_anchor_is_rejected(self):
        with tempfile.TemporaryDirectory(prefix="centroid-anchor-") as temporary:
            root = Path(temporary)
            with patch.object(validate, "ROOT", root):
                board, positions = self.fixture(root)
                positions["J1"]["PosX"] = "125"
                with self.assertRaisesRegex(ValueError, "Placement-origin geometry differs"):
                    validate.reviewed_placement_origins(board, validate.design_inputs(board), positions, root)

    def test_uncommitted_replacement_cannot_authorize_offsets(self):
        with tempfile.TemporaryDirectory(prefix="centroid-commit-") as temporary:
            root = Path(temporary)
            with patch.object(validate, "ROOT", root):
                board, positions = self.fixture(root)
                evidence = root / "centroid.json"
                evidence.write_text(evidence.read_text() + " ")
                board["cpl_centroid_policy"]["sha256"] = validate.sha(evidence)
                with self.assertRaisesRegex(ValueError, "not committed at HEAD"):
                    validate.reviewed_placement_origins(board, validate.design_inputs(board), positions, root)


if __name__ == "__main__":
    unittest.main()
