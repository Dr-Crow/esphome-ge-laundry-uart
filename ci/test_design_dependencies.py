"""Real-git release receipts must invalidate on local dependency mutations."""
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import validate


class DesignDependencyTest(unittest.TestCase):
    def fixture(self, root):
        design = root / 'design'
        for directory in ('symbols', 'footprints/Local.pretty', 'models'):
            (design / directory).mkdir(parents=True, exist_ok=True)
        (design / 'board.kicad_pro').write_text('{}\n')
        (design / 'board.kicad_sch').write_text('(kicad_sch (property "Sheetfile" "child.kicad_sch"))\n')
        (design / 'child.kicad_sch').write_text('(kicad_sch)\n')
        (design / 'board.kicad_pcb').write_text('(kicad_pcb (footprint "Local:part" (model "${KIPRJMOD}/models/part.step")))\n')
        (design / 'fp-lib-table').write_text('(fp_lib_table (lib (name "Local")(type "KiCad")(uri "${KIPRJMOD}/footprints/Local.pretty")))\n')
        (design / 'sym-lib-table').write_text('(sym_lib_table (lib (name "Local")(type "KiCad")(uri "${KIPRJMOD}/symbols/local.kicad_sym")))\n')
        (design / 'symbols/local.kicad_sym').write_text('(kicad_symbol_lib)\n')
        (design / 'footprints/Local.pretty/part.kicad_mod').write_text('(footprint "part" (model "${KIPRJMOD}/models/part.step"))\n')
        (design / 'models/part.step').write_text('local model fixture\n')
        # Same basename elsewhere must retain a distinct checkout-relative identity.
        (design / 'symbols/other').mkdir()
        (design / 'symbols/other/local.kicad_sym').write_text('(kicad_symbol_lib other)\n')
        (root / 'qualification.json').write_text('{"qualification":"test-only"}\n')
        return {'source': 'design/board', 'library_tables': ['design/fp-lib-table', 'design/sym-lib-table']}

    def commit(self, root):
        subprocess.run(['git', 'init', '-q', str(root)], check=True)
        subprocess.run(['git', 'add', '.'], cwd=root, check=True)
        subprocess.run(['git', '-c', 'user.name=Dr-Crow', '-c',
                        'user.email=9339757+Dr-Crow@users.noreply.github.com',
                        'commit', '-qm', 'test: local dependency qualification fixture'], cwd=root, check=True)

    def qualify(self, root, board, manifest):
        identity = validate.source_identity(board)
        board['readiness'] = {
            gate: {'state': 'passed', 'evidence': 'qualification.json',
                   'sha256': validate.sha(root / 'qualification.json'),
                   'source_sha256': identity, 'external_kicad': validate.external_identity(board, manifest)}
            for gate in ('power', 'source', 'physical')}
        return identity

    def test_edits_and_deletions_cannot_reuse_committed_passed_receipt(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            board = self.fixture(root)
            self.commit(root)
            output = root / 'output'
            output.mkdir()
            with patch.object(validate, 'ROOT', root):
                identity = self.qualify(root, board, {})
                self.assertIn('design/symbols/local.kicad_sym', identity)
                self.assertIn('design/symbols/other/local.kicad_sym', identity)
                self.assertEqual(validate.release(board, output, {})['readiness'], 'passed')
                for name in ('symbols/local.kicad_sym', 'footprints/Local.pretty/part.kicad_mod',
                             'models/part.step', 'fp-lib-table', 'sym-lib-table', 'child.kicad_sch'):
                    file = root / 'design' / name
                    original = file.read_bytes()
                    with self.subTest(dependency=name, mutation='edit'):
                        file.write_bytes(original + b'\n# changed dependency\n')
                        with self.assertRaisesRegex(ValueError, 'qualification does not match current source hashes'):
                            validate.release(board, output, {})
                        file.write_bytes(original)
                    with self.subTest(dependency=name, mutation='delete'):
                        file.unlink()
                        with self.assertRaisesRegex(ValueError, 'MISSING:'):
                            validate.release(board, output, {})
                        file.write_bytes(original)
                self.assertEqual(validate.source_identity(board), identity)

    def test_stock_references_are_named_and_separately_pin_qualified(self):
        manifest = json.loads((validate.ROOT / 'ci/manifest.json').read_text())
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            board = self.fixture(root)
            pcb = root / 'design/board.kicad_pcb'
            pcb.write_text(pcb.read_text() + '(model "${KICAD9_3DMODEL_DIR}/Package.3dshapes/stock.step")\n')
            self.commit(root)
            output = root / 'output'
            output.mkdir()
            with patch.object(validate, 'ROOT', root):
                identity = self.qualify(root, board, manifest)
                external = validate.external_identity(board, manifest)
                self.assertEqual(external['references'], ['${KICAD9_3DMODEL_DIR}/Package.3dshapes/stock.step'])
                self.assertFalse(any('stock.step' in name for name in identity))
                self.assertEqual(validate.release(board, output, manifest)['readiness'], 'passed')
                manifest['external_kicad']['models_commit'] = '0' * 40
                with self.assertRaisesRegex(ValueError, 'pinned external KiCad dependencies'):
                    validate.release(board, output, manifest)


if __name__ == '__main__':
    unittest.main()
