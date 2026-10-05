"""Clean ERC/DRC must still fail when the current native review set is absent."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import validate


PDF = b'%PDF-1.5\n1 0 obj\n<< /Type /Page >>\nendobj\n%%EOF\n'
SVG = b'<svg xmlns="http://www.w3.org/2000/svg"><path d="M0 0L1 1"/></svg>\n'


class ReviewExportTest(unittest.TestCase):
    def fixture(self, root):
        design = root / 'design'
        design.mkdir()
        for extension in ('.kicad_pro', '.kicad_sch', '.kicad_pcb'):
            (design / ('board' + extension)).write_text('original source\n')
        (design / 'board.kicad_sch').write_text('(property "Sheetfile" "child.kicad_sch")\n')
        (design / 'child.kicad_sch').write_text('original child\n')
        output = root / 'output'
        output.mkdir()
        return {'source': 'design/board'}, output

    def native(self, calls, bad=None, behavior=None, drc=0):
        def run(args, output, name, cwd=None):
            calls.append(args)
            source = Path(args[-1])
            # Native migration/export is allowed to write only the isolated copy.
            source.with_suffix('.kicad_pro').write_text('migrated metadata\n')
            self.assertTrue((source.parent / 'child.kicad_sch').is_file())
            target = Path(args[args.index('--output') + 1])
            if name in ('erc', 'drc'):
                target.write_text('{}\n')
                return drc if name == 'drc' else 0
            if target.name == bad:
                if behavior == 'nonzero':
                    return 3
                if behavior == 'missing':
                    return 0
                target.write_bytes({'empty': b'', 'wrong-kind': b'{}\n',
                                    'malformed-svg': b'<svg',
                                    'empty-svg': b'<svg xmlns="http://www.w3.org/2000/svg"/>'}[behavior])
            else:
                target.write_bytes(PDF if target.suffix == '.pdf' else SVG)
            return 0
        return run

    def test_current_files_hashes_views_and_source_copy(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            board, output = self.fixture(root)
            calls = []
            with patch.object(validate, 'ROOT', root), patch.object(validate, 'tool', return_value='9.0.9'), \
                    patch.object(validate, 'command', side_effect=self.native(calls)):
                identity = validate.source_identity(board)
                result = validate.hardware(board, output, {'tools': {'kicad': '9.0.9'}})
                self.assertEqual(identity, validate.source_identity(board))
            self.assertEqual(len(calls), 5)
            self.assertEqual(calls[0][-1], calls[2][-1])
            self.assertEqual(calls[1][-1], calls[3][-1])
            self.assertEqual(calls[1][-1], calls[4][-1])
            self.assertFalse(Path(calls[0][-1]).is_relative_to(root))
            self.assertFalse(Path(calls[0][-1]).exists())
            self.assertIn('--schematic-parity', calls[1])
            self.assertIn('--all-track-errors', calls[1])
            self.assertEqual(calls[3][calls[3].index('--layers') + 1], 'F.Cu,F.SilkS,Edge.Cuts')
            self.assertNotIn('--mirror', calls[3])
            self.assertEqual(calls[4][calls[4].index('--layers') + 1], 'B.Cu,B.SilkS,Edge.Cuts')
            self.assertIn('--mirror', calls[4])
            receipt = json.loads((output / 'review-exports.json').read_text())
            self.assertEqual(receipt, result['review_exports'])
            self.assertEqual(receipt['status'], 'passed')
            self.assertEqual(receipt['source_sha256'], identity)
            self.assertEqual(receipt['kicad_version'], '9.0.9')
            self.assertIn('mirrored', receipt['files']['review/board-bottom-mirrored.svg']['view'])
            for name, record in receipt['files'].items():
                self.assertEqual(record['sha256'], validate.sha(output / name))
                self.assertEqual(record['bytes'], (output / name).stat().st_size)

    def test_failed_or_missing_or_bad_output_stays_red_after_clean_checks(self):
        cases = [('schematic.pdf', 'nonzero'), ('board-top.svg', 'missing'),
                 ('board-bottom-mirrored.svg', 'empty'), ('schematic.pdf', 'wrong-kind'),
                 ('board-top.svg', 'wrong-kind'), ('board-top.svg', 'malformed-svg'),
                 ('board-bottom-mirrored.svg', 'empty-svg')]
        for name, behavior in cases:
            with self.subTest(file=name, behavior=behavior), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                board, output = self.fixture(root)
                # Stale success files must never mask a missing fresh output.
                (output / 'review').mkdir()
                (output / 'review' / name).write_bytes(PDF if name.endswith('.pdf') else SVG)
                (output / 'review-exports.json').write_text('{"status":"passed"}\n')
                with patch.object(validate, 'ROOT', root), patch.object(validate, 'tool', return_value='9.0.9'), \
                        patch.object(validate, 'command', side_effect=self.native([], name, behavior)):
                    with self.assertRaisesRegex(ValueError, 'Review export infrastructure/output problem'):
                        validate.hardware(board, output, {'tools': {'kicad': '9.0.9'}})
                self.assertEqual(json.loads((output / 'native-checks.json').read_text())['native_exit_codes'],
                                 {'erc': 0, 'drc': 0})
                receipt = json.loads((output / 'review-exports.json').read_text())
                self.assertEqual(receipt['status'], 'failed')
                self.assertTrue(receipt['findings'])
                self.assertNotIn('sha256', receipt['files']['review/' + name])

    def test_native_failure_keeps_diagnostics_and_skips_exports(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            board, output = self.fixture(root)
            (output / 'review').mkdir()
            (output / 'review/schematic.pdf').write_bytes(PDF)
            (output / 'review-exports.json').write_text('{"status":"passed"}\n')
            calls = []
            with patch.object(validate, 'ROOT', root), patch.object(validate, 'tool'), \
                    patch.object(validate, 'command', side_effect=self.native(calls, drc=5)):
                with self.assertRaisesRegex(ValueError, "'erc': 0, 'drc': 5"):
                    validate.hardware(board, output, {'tools': {'kicad': '9.0.9'}})
            self.assertEqual(len(calls), 2)
            self.assertTrue((output / 'erc.json').is_file())
            self.assertTrue((output / 'drc.json').is_file())
            self.assertTrue((output / 'native-checks.json').is_file())
            self.assertFalse((output / 'review').exists())
            self.assertFalse((output / 'review-exports.json').exists())


if __name__ == '__main__':
    unittest.main()
