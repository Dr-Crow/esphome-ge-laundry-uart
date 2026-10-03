"""Regression coverage for qualification evidence outside version control."""
import json
import tempfile
import unittest
from pathlib import Path

import validate


class ReleaseEvidenceTest(unittest.TestCase):
    def test_untracked_evidence_cannot_pass_readiness(self):
        manifest = json.loads((validate.ROOT / "ci/manifest.json").read_text())
        board = manifest["boards"]["rev2.2"]
        source_hashes = {str(p.relative_to(validate.ROOT)): validate.sha(p)
                         for p in validate.sources(board)}
        # Keep the fixture in the actual checkout so git, rather than a mock,
        # determines whether this otherwise valid qualification file is tracked.
        with tempfile.NamedTemporaryFile(dir=validate.ROOT, prefix="qualification-test-",
                                         suffix=".json") as temporary:
            evidence = Path(temporary.name)
            evidence.write_text('{"qualification": "test-only"}\n')
            board["readiness"] = {
                gate: {"state": "passed", "evidence": str(evidence.relative_to(validate.ROOT)),
                       "sha256": validate.sha(evidence), "source_sha256": source_hashes}
                for gate in ("power", "source", "physical")
            }
            with tempfile.TemporaryDirectory(prefix="qualification-result-") as output:
                with self.assertRaisesRegex(ValueError, "qualification evidence is not tracked in git"):
                    validate.release(board, Path(output), manifest)
                result = json.loads((Path(output) / "readiness.json").read_text())
                self.assertEqual(len(result["findings"]), 3)


if __name__ == "__main__":
    unittest.main()
