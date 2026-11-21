import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name('kev_nvd_checker.py')
KEV_ID = 'TEST-KEV'
HIGH_ID = 'TEST-HIGH'


def nvd_record(identifier, criterion, score, **bounds):
    return {'cve': {
        'id': identifier,
        'metrics': {'cvssMetricV31': [{'cvssData': {'baseScore': score}}]},
        'configurations': [{'nodes': [{'operator': 'OR', 'cpeMatch': [
            {'vulnerable': True, 'criteria': criterion, **bounds},
        ]}]}],
    }}


class CheckerTest(unittest.TestCase):
    def test_cli_matches_local_catalogs(self):
        base = 'cpe:2.3:a:example:widget:'
        suffix = ':*:*:*:*:*:*:*'
        records = [
            nvd_record(KEV_ID, base + '*' + suffix, 5.0,
                       versionStartIncluding='1.0', versionEndExcluding='2.0'),
            nvd_record(HIGH_ID, base + '2.0' + suffix, 8.0),
            nvd_record('TEST-LOW', base + '*' + suffix, 5.0),
        ]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            inventory = root / 'inventory.txt'
            kev = root / 'kev.json'
            nvd = root / 'nvd.json'
            inventory.write_text(
                '# Synthetic inventory\nexample:widget:1.0\nexample:widget:2.0\n'
                'other:widget:1.0\nwidget:1.5\nexample:widget:1.5-beta\n',
                encoding='utf-8',
            )
            kev.write_text(json.dumps({'vulnerabilities': [{'cveID': KEV_ID}]}), encoding='utf-8')
            nvd.write_text(json.dumps({'vulnerabilities': records}), encoding='utf-8')
            result = subprocess.run(
                [sys.executable, str(SCRIPT), '--inventory', str(inventory),
                 '--kev', str(kev), '--nvd', str(nvd)],
                check=True, capture_output=True, text=True,
            )
        report = json.loads(result.stdout)
        self.assertEqual([row['version'] for row in report], ['1.0', '2.0', '1.0', '1.5', '1.5-beta'])
        self.assertEqual([row['candidates'] for row in report], [
            [{'cve_id': KEV_ID, 'in_kev': True, 'cvss_max': 5.0, 'inventory_match': 'matches'}],
            [{'cve_id': HIGH_ID, 'in_kev': False, 'cvss_max': 8.0, 'inventory_match': 'matches'}],
            [],
            [{'cve_id': KEV_ID, 'in_kev': True, 'cvss_max': 5.0, 'inventory_match': 'review'}],
            [{'cve_id': KEV_ID, 'in_kev': True, 'cvss_max': 5.0, 'inventory_match': 'review'}],
        ])


if __name__ == '__main__':
    unittest.main()
