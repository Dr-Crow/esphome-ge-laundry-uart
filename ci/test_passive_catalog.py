"""Source/BOM agreement must not hide independently wrong passive purchases."""
import copy
import json
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import validate


class PassiveCatalogTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.boards = json.loads(validate.path("ci/manifest.json").read_text())["boards"]

    def bom(self, revision):
        return validate.rows(validate.path(self.boards[revision]["bom"]), "Designator")

    def components(self, bom):
        return {ref: (row["Comment"], row["Footprint"],
                      dict(row, LCSC=row["LCSC Part #"])) for ref, row in bom.items()}

    def test_all_five_declared_supplier_boms_match_primary_passive_facts(self):
        revisions = [revision for revision, board in self.boards.items() if board.get("bom")]
        self.assertEqual(revisions, ["rev2.1", "rev2.2", "rev3a", "rev3b", "rev3c"])
        codes = set()
        for revision in revisions:
            with self.subTest(revision=revision):
                bom = self.bom(revision)
                result = validate.passive_catalog(bom, self.components(bom))
                self.assertEqual(set(result["references"]),
                                 {ref for ref in bom if re.fullmatch(r"[RCL]\d+", ref)})
                self.assertEqual(result["catalog_sha256"], validate.sha(validate.path("ci/passive-catalog.json")))
                codes.update(result["references"].values())
        self.assertEqual(len(codes), 23)

    def test_legacy_wrong_resistor_codes_fail_even_when_source_and_bom_agree(self):
        for revision in ("rev2.1", "rev2.2"):
            for ref, wrong_code in (("R18", "C17539"), ("R21", "C17539"), ("R22", "C17713")):
                with self.subTest(revision=revision, reference=ref):
                    row = copy.deepcopy(self.bom(revision)[ref])
                    row["LCSC Part #"] = wrong_code
                    bom = {ref: row}
                    components = self.components(bom)
                    self.assertEqual(row["LCSC Part #"], components[ref][2]["LCSC"])
                    with self.assertRaisesRegex(ValueError, f"Passive catalog value mismatch: {ref}: {wrong_code}"):
                        validate.passive_catalog(bom, components)

    def test_capacitor_value_package_voltage_and_dielectric_conflicts_fail(self):
        original = self.bom("rev3a")["C9"]
        for field, wrong, reason in (
            ("Comment", "1u 50V X7R", "value"),
            ("Footprint", "Capacitor_SMD:C_0805_2012Metric", "package"),
            ("Comment", "10u 25V X7R", "voltage"),
            ("Voltage", "25V", "voltage"),
            ("Comment", "10u 50V X5R", "dielectric"),
            ("Comment", "10u 50V Y5V", "dielectric"),
            ("Dielectric", "X5R", "dielectric"),
        ):
            with self.subTest(field=field, wrong=wrong):
                row = dict(original, **{field: wrong})
                bom = {"C9": row}
                with self.assertRaisesRegex(ValueError, f"Passive catalog {reason} mismatch: C9"):
                    validate.passive_catalog(bom, self.components(bom))

    def test_independent_native_rating_and_mpn_conflicts_fail(self):
        bom = {"C9": self.bom("rev3a")["C9"]}
        for field, wrong, reason in (("Voltage", "25V", "voltage"),
                                    ("Dielectric", "X5R", "dielectric"),
                                    ("MPN", "1206B106K250NT", "MPN")):
            with self.subTest(field=field):
                components = self.components(bom)
                components["C9"][2][field] = wrong
                with self.assertRaisesRegex(ValueError, f"Passive catalog {reason} mismatch: C9: C303950 \\(schematic\\)"):
                    validate.passive_catalog(bom, components)

    def test_unknown_or_missing_passive_code_fails_but_nonpassives_stay_outside_scope(self):
        original = self.bom("rev3c")["R18"]
        for code in ("C999999999", ""):
            with self.subTest(code=code), self.assertRaisesRegex(ValueError, "Unknown passive catalog code: R18"):
                validate.passive_catalog({"R18": dict(original, **{"LCSC Part #": code})})
        result = validate.passive_catalog({"U1": {"LCSC Part #": "unknown module"}})
        self.assertEqual(result["references"], {})
        self.assertIn("semiconductor/module", result["scope"])

    def test_exact_mpn_and_inductor_package_identity_are_checked(self):
        for ref, field, wrong, reason in (
            ("R18", "MPN", "0805W8F2003T5E", "MPN"),
            ("L1", "Comment", "3.3uH", "value"),
            ("L1", "Footprint", "Inductor_SMD:L_Panasonic_PCC-M0540M", "package"),
            ("L1", "MPN", "ETQP4M4R7YFP", "MPN"),
        ):
            row = dict(self.bom("rev3a")[ref], **{field: wrong})
            with self.subTest(reference=ref, field=field), self.assertRaisesRegex(
                    ValueError, f"Passive catalog {reason} mismatch: {ref}"):
                validate.passive_catalog({ref: row})

    def test_manufacturing_rejects_wrong_purchase_with_mocked_native_exports(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "ci").mkdir()
            (root / "ci/passive-catalog.json").write_bytes(validate.path("ci/passive-catalog.json").read_bytes())
            for extension in (".kicad_pro", ".kicad_sch", ".kicad_pcb"):
                (root / ("board" + extension)).write_text("(drillshape 0)\n")
            (root / "bom.csv").write_text(
                "Comment,Designator,Footprint,LCSC Part #\n220k,R18,Resistor_SMD:R_0805_2012Metric,C17539\n")
            (root / "cpl.csv").write_text("Designator,Mid X,Mid Y,Rotation,Layer\nR18,0,0,0,top\n")
            output = root / "output"
            output.mkdir()
            (output / "passive-catalog.json").write_text('{"stale":"passed"}\n')

            def native(args, output, name, cwd=None):
                if name == "netlist":
                    (output / "netlist.xml").write_text(
                        '<export><components><comp ref="R18"><value>220k</value>'
                        '<footprint>Resistor_SMD:R_0805_2012Metric</footprint>'
                        '<property name="LCSC" value="C17539"/></comp></components></export>')
                if name == "positions":
                    (output / "positions.csv").write_text(
                        "Ref,Val,Package,PosX,PosY,Rot,Side\nR18,220k,R_0805_2012Metric,0,0,0,top\n")
                return 0

            board = {"source": "board", "bom": "bom.csv", "cpl": "cpl.csv",
                     "archive": "review.zip", "fabrication_plot": {"drillshape": 0}}
            with patch.object(validate, "ROOT", root), patch.object(validate, "tool"), \
                    patch.object(validate, "command", side_effect=native), \
                    patch.object(validate, "matched_archive", return_value=1):
                with self.assertRaisesRegex(ValueError, "Passive catalog value mismatch: R18: C17539"):
                    validate.manufacturing(board, output, {"tools": {"kicad": "9.0.9"}})
                self.assertFalse((output / "passive-catalog.json").exists())


if __name__ == "__main__":
    unittest.main()
