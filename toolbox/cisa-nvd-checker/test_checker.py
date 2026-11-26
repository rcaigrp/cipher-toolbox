import json
import subprocess
import sys
import unittest
from pathlib import Path


class CheckerTest(unittest.TestCase):
    def run_checker(self, *args):
        return subprocess.run(
            [sys.executable, 'cisa_nvd_checker.py', *args],
            cwd=Path(__file__).resolve().parent,
            capture_output=True,
            text=True,
        )

    def test_sample_inventory(self):
        result = self.run_checker('--inventory', 'test_inventory.json',
                                  '--kev', 'test_kev.json', '--nvd', 'test_nvd.json')
        self.assertEqual(result.returncode, 0, result.stderr)
        findings = json.loads(result.stdout)
        self.assertEqual(
            [(row['cve'], row['in_kev_snapshot'], row['match']) for row in findings],
            [('TEST-ADVISORY-EXACT', True, 'exact_cpe'),
             ('TEST-ADVISORY-RANGE', False, 'review_applicability')],
        )
        self.assertIn(':example_editor:4.15.2:', findings[0]['inventory_cpe'])
        self.assertIn(':example_portal:3.1.4:', findings[1]['inventory_cpe'])

    def test_missing_snapshot_fails(self):
        result = self.run_checker('--inventory', 'test_inventory.json',
                                  '--kev', 'missing-snapshot.json', '--nvd', 'test_nvd.json')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, '')
        self.assertIn('missing-snapshot.json', result.stderr)

    def test_help(self):
        result = self.run_checker('--help')
        self.assertEqual(result.returncode, 0, result.stderr)
        for option in ('--inventory', '--kev', '--nvd'):
            self.assertIn(option, result.stdout)


if __name__ == '__main__':
    unittest.main()
