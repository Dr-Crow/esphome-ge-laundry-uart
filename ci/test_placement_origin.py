"""Reviewed centroid conventions must not authorize stale or uncommitted data."""
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import validate


class PlacementOriginFixture:
    def commit(self, root):
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "-c", "user.name=Dr-Crow", "-c",
                        "user.email=9339757+Dr-Crow@users.noreply.github.com",
                        "commit", "-qm", "test: reviewed centroid fixture"], cwd=root, check=True)

    def fixture(self, root):
        for suffix in (".kicad_pro", ".kicad_sch", ".kicad_pcb"):
            (root / ("board" + suffix)).write_text("reviewed source\n")
        (root / "symbols").mkdir()
        (root / "symbols/local.kicad_sym").write_text("reviewed local symbol\n")
        board = {"source": "board"}
        review = {
            "source_sha256": {str(p.relative_to(root)): validate.sha(p) for p in validate.design_inputs(board)},
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
        self.commit(root)
        positions = {"J1": {"Package": "RJ45", "PosX": "122.425", "PosY": "-99.2825", "Rot": "90"}}
        return board, positions


class PlacementOriginTest(PlacementOriginFixture, unittest.TestCase):
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

    def test_changed_local_library_invalidates_centroid_attestation(self):
        with tempfile.TemporaryDirectory(prefix="centroid-library-") as temporary:
            root = Path(temporary)
            with patch.object(validate, "ROOT", root):
                board, positions = self.fixture(root)
                (root / "symbols/local.kicad_sym").write_text("changed pin function\n")
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


class BodyDatumTest(PlacementOriginFixture, unittest.TestCase):
    def body_fixture(self, root):
        board, _ = self.fixture(root)
        documentary = root / "manufacturer-datums.txt"
        documentary.write_text("Test-only documentary fixture: Seeed 21 x 17.8 mm module PCB; "
                               "EVERCOM 5301 body x=-3.155..12.045, y=-14.350..3.700 in STEP.\n")
        review = {
            "source_sha256": validate.source_identity(board),
            "references": {
                "U2": {"datum_type": "module_pcb_body_bbox_center",
                       "footprint": "GEA_XIAO:XIAO-ESP32-C3-v1.3-SMD",
                       "native_anchor_xy_mm": [77.39, -4.0], "rotation_degrees": -90.0,
                       "side": "top", "local_body_center_xy_mm": [8.9, -10.5],
                       "body_center_xy_mm": [87.89, -12.9],
                       "manufacturer_datum": {"manufacturer": "Seeed", "mpn": "113991054",
                           "evidence": documentary.name, "sha256": validate.sha(documentary),
                           "source_url": "https://wiki.seeedstudio.com/XIAO_ESP32C3_Getting_Started/",
                           "datum_description": "Nominal 21 x 17.8 mm module PCB body; excludes USB."}},
                "J1": {"datum_type": "manufacturer_nominal_body_bbox_center",
                       "footprint": "OnionStraws:RJ45_EVERCOM_5301-8P8C_Horizontal",
                       "native_anchor_xy_mm": [13.97, -12.55], "rotation_degrees": -90.0,
                       "side": "top", "local_body_center_xy_mm": [4.445, 5.325],
                       "body_center_xy_mm": [8.645, -16.995],
                       "manufacturer_datum": {"manufacturer": "EVERCOM", "mpn": "5301-8P8C",
                           "evidence": documentary.name, "sha256": validate.sha(documentary),
                           "source_url": "https://chinarj45.com/manufacturer-drawing.pdf",
                           "datum_description": "5301-880XXX nominal family body centre, "
                                                "not the footprint F.Fab or all-pad centre."}}
            }
        }
        positions = {ref: {"Package": record["footprint"].split(":")[-1],
                          "PosX": str(record["native_anchor_xy_mm"][0]),
                          "PosY": str(record["native_anchor_xy_mm"][1]),
                          "Rot": "-90", "Side": "top"}
                     for ref, record in review["references"].items()}
        components = {ref: ("part", record["footprint"],
                           {"Manufacturer": record["manufacturer_datum"]["manufacturer"],
                            "MPN": record["manufacturer_datum"]["mpn"]})
                      for ref, record in review["references"].items()}
        board["cpl_centroid_policy"]["required_references"] = ["U2", "J1"]
        self.update_review(root, board, review)
        return board, positions, components, review

    def update_review(self, root, board, review):
        evidence = root / board["cpl_centroid_policy"]["evidence"]
        evidence.write_text(json.dumps(review) + "\n")
        board["cpl_centroid_policy"]["sha256"] = validate.sha(evidence)
        self.commit(root)

    def validate_body(self, root, board, positions, components):
        return validate.reviewed_placement_origins(board, validate.design_inputs(board),
                                                  positions, root, components)

    def test_body_datums_are_distinct_from_pad_centres(self):
        with tempfile.TemporaryDirectory(prefix="body-datum-") as temporary:
            root = Path(temporary)
            with patch.object(validate, "ROOT", root):
                board, positions, components, _ = self.body_fixture(root)
                origins = self.validate_body(root, board, positions, components)
                self.assertEqual(origins["U2"], {"PosX": 87.89, "PosY": -12.9})
                self.assertEqual(origins["J1"], {"PosX": 8.645, "PosY": -16.995})
                self.assertNotEqual(origins["U2"]["PosX"], 88.321)
                self.assertNotEqual(origins["J1"]["PosX"], 11.640)
                self.assertNotEqual(origins["U2"]["PosX"], float(positions["U2"]["PosX"]))

    def test_required_reference_declaration_is_exact_and_known(self):
        for requested in ([], "U2", ["U2", "U2"], ["UNKNOWN"], ["U2"]):
            with self.subTest(requested=requested), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                with patch.object(validate, "ROOT", root):
                    board, positions, components, _ = self.body_fixture(root)
                    board["cpl_centroid_policy"]["required_references"] = requested
                    with self.assertRaisesRegex(ValueError, "placement-origin|Placement-origin"):
                        self.validate_body(root, board, positions, components)

    def test_missing_review_record_does_not_fall_back_to_native(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with patch.object(validate, "ROOT", root):
                board, positions, components, review = self.body_fixture(root)
                del review["references"]["J1"]
                self.update_review(root, board, review)
                with self.assertRaisesRegex(ValueError, "differs from required references"):
                    self.validate_body(root, board, positions, components)

    def test_extra_or_duplicate_evidence_record_fails(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with patch.object(validate, "ROOT", root):
                board, positions, components, review = self.body_fixture(root)
                review["references"]["J2"] = dict(review["references"]["J1"])
                positions["J2"] = dict(positions["J1"])
                self.update_review(root, board, review)
                with self.assertRaisesRegex(ValueError, "differs from required references"):
                    self.validate_body(root, board, positions, components)
                evidence = root / "centroid.json"
                evidence.write_text(evidence.read_text().replace('"datum_type":',
                                    '"datum_type": "unreviewed", "datum_type":', 1))
                board["cpl_centroid_policy"]["sha256"] = validate.sha(evidence)
                self.commit(root)
                with self.assertRaisesRegex(ValueError, "Duplicate placement-origin evidence key"):
                    self.validate_body(root, board, positions, components)

    def test_body_datums_require_explicit_references(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with patch.object(validate, "ROOT", root):
                board, positions, components, _ = self.body_fixture(root)
                del board["cpl_centroid_policy"]["required_references"]
                with self.assertRaisesRegex(ValueError, "must be explicitly required"):
                    self.validate_body(root, board, positions, components)

    def test_native_anchor_rotation_side_and_full_footprint_are_bound(self):
        for field, changed in (("PosX", "78"), ("Rot", "90"), ("Side", "bottom"),
                               ("Package", "OtherFootprint")):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                with patch.object(validate, "ROOT", root):
                    board, positions, components, _ = self.body_fixture(root)
                    positions["U2"][field] = changed
                    with self.assertRaises(ValueError):
                        self.validate_body(root, board, positions, components)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with patch.object(validate, "ROOT", root):
                board, positions, components, _ = self.body_fixture(root)
                value, footprint, properties = components["U2"]
                components["U2"] = (value, "OtherLibrary:" + footprint.split(":")[-1], properties)
                with self.assertRaisesRegex(ValueError, "full footprint differs"):
                    self.validate_body(root, board, positions, components)

    def test_wrong_part_identity_fails(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with patch.object(validate, "ROOT", root):
                board, positions, components, _ = self.body_fixture(root)
                components["J1"][2]["MPN"] = "OTHER"
                with self.assertRaisesRegex(ValueError, "part identity differs"):
                    self.validate_body(root, board, positions, components)

    def test_documentary_basis_must_be_present_hashed_and_committed(self):
        mutations = (lambda record: record.pop("manufacturer_datum"),
                     lambda record: record["manufacturer_datum"].update(datum_description=""),
                     lambda record: record["manufacturer_datum"].update(source_url="not a URL"),
                     lambda record: record["manufacturer_datum"].update(sha256="0" * 64),
                     lambda record: record["manufacturer_datum"].update(evidence="absent.pdf"))
        for index, mutate in enumerate(mutations):
            with self.subTest(index=index), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                with patch.object(validate, "ROOT", root):
                    board, positions, components, review = self.body_fixture(root)
                    mutate(review["references"]["U2"])
                    self.update_review(root, board, review)
                    with self.assertRaises(ValueError):
                        self.validate_body(root, board, positions, components)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with patch.object(validate, "ROOT", root):
                board, positions, components, review = self.body_fixture(root)
                documentary = root / "manufacturer-datums.txt"
                documentary.write_text(documentary.read_text() + "Changed datum basis.\n")
                for record in review["references"].values():
                    record["manufacturer_datum"]["sha256"] = validate.sha(documentary)
                evidence = root / "centroid.json"
                evidence.write_text(json.dumps(review) + "\n")
                board["cpl_centroid_policy"]["sha256"] = validate.sha(evidence)
                subprocess.run(["git", "add", evidence.name], cwd=root, check=True)
                subprocess.run(["git", "-c", "user.name=Dr-Crow", "-c",
                                "user.email=9339757+Dr-Crow@users.noreply.github.com",
                                "commit", "-qm", "test: change proof without committing drawing"],
                               cwd=root, check=True)
                with self.assertRaisesRegex(ValueError, "Manufacturer datum evidence.*not committed at HEAD"):
                    self.validate_body(root, board, positions, components)

    def test_malformed_or_untyped_body_geometry_fails(self):
        changes = ({"datum_type": "guess_body_center"}, {"datum_type": "pad_bbox_center"},
                   {"local_body_center_xy_mm": [8.9]}, {"body_center_xy_mm": [88.321, -12.9175]},
                   {"body_center_xy_mm": [True, -12.9]}, {"rotation_degrees": float("nan")},
                   {"native_pad_bbox_xy_mm": [79.27, -22.375, 97.372, -3.460]})
        for changed in changes:
            with self.subTest(changed=changed), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                with patch.object(validate, "ROOT", root):
                    board, positions, components, review = self.body_fixture(root)
                    review["references"]["U2"].update(changed)
                    self.update_review(root, board, review)
                    with self.assertRaises(ValueError):
                        self.validate_body(root, board, positions, components)

    def test_complete_local_source_closure_is_required(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with patch.object(validate, "ROOT", root):
                board, positions, components, review = self.body_fixture(root)
                inputs = validate.design_inputs(board)
                with self.assertRaisesRegex(ValueError, "omit current source dependencies"):
                    validate.reviewed_placement_origins(board, inputs[:-1], positions, root, components)
                (root / "board.kicad_dru").write_text("new source rule\n")
                with self.assertRaisesRegex(ValueError, "does not match current source hashes"):
                    self.validate_body(root, board, positions, components)

    def test_declared_empty_policy_fails_but_absent_policy_uses_native(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with patch.object(validate, "ROOT", root):
                self.assertEqual(validate.reviewed_placement_origins({}, [], {}, root), {})
                for policy in ({}, None, [], {"required_references": ["U2"]}):
                    with self.subTest(policy=policy), self.assertRaisesRegex(ValueError, "Malformed"):
                        validate.reviewed_placement_origins({"cpl_centroid_policy": policy}, [], {}, root)


if __name__ == "__main__":
    unittest.main()
