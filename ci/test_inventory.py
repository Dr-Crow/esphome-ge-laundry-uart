"""Inventory must bind real profile dependencies and retain incomplete CAD evidence."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import validate


class FirmwareInventoryTest(unittest.TestCase):
    def fixture(self, root):
        firmware = root / 'firmware'
        (firmware / 'packages').mkdir(parents=True)
        (firmware / 'profile.yaml').write_text('packages:\n  common: !include packages/common.yaml\n')
        (firmware / 'packages/common.yaml').write_text('wifi:\n  ssid: !secret wifi_ssid\n')
        return {'firmware': ['firmware/profile.yaml']}

    def test_include_changes_are_in_recorded_profile_identity(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with patch.object(validate, 'ROOT', root):
                manifest = self.fixture(root)
                before = validate.firmware_inventory(root, manifest)
                (root / 'firmware/packages/common.yaml').write_text('logger:\n  baud_rate: 0\n')
                after = validate.firmware_inventory(root, manifest)
                self.assertEqual(before['firmware/profile.yaml']['source_sha256'],
                                 after['firmware/profile.yaml']['source_sha256'])
                self.assertNotEqual(before['firmware/profile.yaml']['input_sha256'],
                                    after['firmware/profile.yaml']['input_sha256'])

    def test_missing_include_and_duplicate_profile_fail(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with patch.object(validate, 'ROOT', root):
                manifest = self.fixture(root)
                (root / 'firmware/packages/common.yaml').unlink()
                with self.assertRaisesRegex(ValueError, 'MISSING: firmware/packages/common.yaml'):
                    validate.firmware_inventory(root, manifest)
                manifest['firmware'] *= 2
                with self.assertRaisesRegex(ValueError, 'Duplicate firmware compile profile'):
                    validate.firmware_inventory(root, manifest)

    def test_missing_board_assembly_does_not_hide_available_source_hashes(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for extension in ('.kicad_pro', '.kicad_sch', '.kicad_pcb'):
                (root / ('board' + extension)).write_text('native source\n')
            (root / 'review.zip').write_bytes(b'archive fixture')
            with patch.object(validate, 'ROOT', root):
                with self.assertRaisesRegex(ValueError, 'supplier BOM.*supplier CPL'):
                    validate.inventory({'source': 'board', 'archive': 'review.zip'}, root, {})
                recorded = json.loads((root / 'files.json').read_text())
                self.assertIn('board.kicad_pcb', recorded['files'])
                self.assertIn('review.zip', recorded['files'])


class NativeSourcePreservationTest(unittest.TestCase):
    def test_native_migration_stays_outside_committed_project(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            design = root / 'design'
            design.mkdir()
            for extension in ('.kicad_pro', '.kicad_sch', '.kicad_pcb'):
                (design / ('board' + extension)).write_text('original source\n')
            before = validate.sha(design / 'board.kicad_pro')
            output = root / 'output'
            output.mkdir()
            def native(args, output, name, cwd=None):
                source = Path(args[-1])
                source.with_suffix('.kicad_pro').write_text('native migrated metadata\n')
                Path(args[args.index('--output') + 1]).write_text('{}\n')
                return 5 if name == 'erc' else 0
            with patch.object(validate, 'ROOT', root), patch.object(validate, 'tool'), \
                    patch.object(validate, 'command', side_effect=native):
                with self.assertRaisesRegex(ValueError, "'erc': 5, 'drc': 0"):
                    validate.hardware({'source': 'design/board'}, output, {'tools': {'kicad': '9.0.9'}})
            self.assertEqual(before, validate.sha(design / 'board.kicad_pro'))
            self.assertEqual(json.loads((output / 'native-checks.json').read_text())['native_exit_codes'],
                             {'erc': 5, 'drc': 0})


if __name__ == '__main__':
    unittest.main()
