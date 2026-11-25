import os
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
import unittest


ROOT = Path(__file__).resolve().parents[1]


class KitTests(unittest.TestCase):
    def run_cli(self, *args, **kwargs):
        return subprocess.run(args, cwd=ROOT, capture_output=True, text=True, **kwargs)

    def test_exposure_with_sample_listeners(self):
        with TemporaryDirectory() as directory:
            ss = Path(directory) / 'ss'
            ss.write_text('#!/bin/sh\nprintf "%s" "$SAMPLE_LISTENERS"\n')
            ss.chmod(0o755)
            cases = [
                ('', 'NO MATCHING LOCAL TCP LISTENERS'),
                ('LISTEN 0 128 127.0.0.1:80 0.0.0.0:*\nLISTEN 0 128 [::1]:443 [::]:*\n', 'bind only to loopback'),
                ('LISTEN 0 128 0.0.0.0:8080 0.0.0.0:*\n', 'VERDICT: REVIEW'),
            ]
            for sample, expected in cases:
                with self.subTest(sample=sample):
                    env = dict(os.environ, PATH=f'{directory}:{os.environ["PATH"]}', SAMPLE_LISTENERS=sample)
                    result = self.run_cli('./check_exposure.sh', env=env, check=True)
                    self.assertIn(expected, result.stdout)

    def test_help_and_mitigation(self):
        for script in ('./check_exposure.sh', './mitigate.sh'):
            with self.subTest(script=script):
                self.assertIn('Usage:', self.run_cli(script, '--help', check=True).stdout)
        self.assertIn('Dry run.', self.run_cli('./mitigate.sh', check=True).stdout)
        result = self.run_cli('./mitigate.sh', '--apply')
        self.assertEqual(result.returncode, 2)
        self.assertIn('No changes applied.', result.stderr)

    def test_yara_inventory_marker(self):
        rule = 'detection/yara/netis-wf2409e-exploit.yar'
        with TemporaryDirectory() as directory:
            sample = Path(directory) / 'inventory.txt'
            for text, expected in [('Netis WF2409E\n', True), ('Netis WF2409\n', False), ('Other vendor WF2409E\n', False)]:
                with self.subTest(text=text):
                    sample.write_text(text)
                    result = self.run_cli('yara', rule, str(sample), check=True)
                    self.assertEqual('netis_wf2409e_inventory_marker' in result.stdout, expected)
