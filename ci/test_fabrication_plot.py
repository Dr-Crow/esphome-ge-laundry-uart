"""Native CAM parity alone must not approve drill markers on stencil layers."""
import json
import re
import shutil
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

import validate


class FabricationPlotTest(unittest.TestCase):
    def test_native_source_matched_marker_cam_is_still_rejected(self):
        manifest = json.loads((validate.ROOT / "ci/manifest.json").read_text())
        current = manifest["boards"]["rev3c"]
        validate.tool("kicad-cli", manifest["tools"]["kicad"])
        with tempfile.TemporaryDirectory(prefix="fabrication-marker-regression-") as temporary:
            root = Path(temporary)
            for source in validate.sources(current):
                shutil.copy2(source, root / source.name)
            pcb = root / Path(current["source"]).with_suffix(".kicad_pcb").name
            board = {"source": pcb.stem, "archive": "review.zip", "fabrication_plot": {"drillshape": 0}}
            generated = root / "gerbers"
            generated.mkdir()
            with patch.object(validate, "ROOT", root):
                self.assertEqual(validate.fabrication_plot(board, root)["drillshape"], 0)
                original = pcb.read_text()
                changed, count = re.subn(r"\(drillshape\s+0\)", "(drillshape 1)", original)
                self.assertEqual(count, 1)
                pcb.write_text(changed)
                for name, args in (
                    ("gerbers", ["pcb", "export", "gerbers", "--board-plot-params"]),
                    ("drills", ["pcb", "export", "drill", "--excellon-separate-th"]),
                ):
                    self.assertEqual(validate.command(["kicad-cli", *args, "-o", str(generated) + "/", pcb],
                                                      root, name), 0)
                paste = [file.read_text() for file in generated.iterdir() if "Paste" in file.name]
                self.assertEqual(len(paste), 2)
                self.assertTrue(all(re.search(r"%ADD\d+C,0\.350000\*%", text) for text in paste))
                with zipfile.ZipFile(root / board["archive"], "w") as archive:
                    for file in generated.iterdir():
                        archive.write(file, file.name)
                # The regenerated marker-bearing CAM really matches its bad source.
                self.assertGreater(validate.matched_archive(board, generated), 0)
                with self.assertRaisesRegex(ValueError, "drillshape must be 0"):
                    validate.fabrication_plot(board, root)
                self.assertFalse((root / "fabrication-plot.json").exists())
                pcb.write_text(original)
                for declaration in (None, {"drillshape": 1}, {"drillshape": False}):
                    board["fabrication_plot"] = declaration
                    with self.subTest(declaration=declaration), self.assertRaisesRegex(ValueError, "plot policy"):
                        validate.fabrication_plot(board, root)


if __name__ == "__main__":
    unittest.main()
