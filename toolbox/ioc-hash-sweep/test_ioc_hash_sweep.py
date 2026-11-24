import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).with_name('ioc_hash_sweep.py')


class HashSweepTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        self.directory = root / 'sweep'
        self.directory.mkdir()
        self.indicators = root / 'indicators.txt'
        self.sample = b'Synthetic sweep fixture\n'
        self.digest = hashlib.sha256(self.sample).hexdigest()
        self.indicators.write_text(f'# sample\n{self.digest.upper()} # fixture\n', encoding='utf-8')

    def sweep(self, directory=None):
        return subprocess.run(
            [sys.executable, str(SCRIPT), '--hashes', str(self.indicators),
             str(self.directory if directory is None else directory)],
            capture_output=True, text=True, timeout=5,
        )

    def test_reports_nested_match(self):
        nested = self.directory / 'nested'
        nested.mkdir()
        match = nested / 'sample.txt'
        match.write_bytes(self.sample)
        (self.directory / 'clean.txt').write_bytes(b'Different content')
        result = self.sweep()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual([json.loads(line) for line in result.stdout.splitlines()],
                         [{'path': str(match), 'sha256': self.digest}])
        self.assertEqual(match.read_bytes(), self.sample)

    def test_skips_file_and_directory_symlinks(self):
        outside = self.directory.parent / 'outside'
        outside.mkdir()
        match = outside / 'sample.txt'
        match.write_bytes(self.sample)
        (self.directory / 'file-link').symlink_to(match)
        (self.directory / 'directory-link').symlink_to(outside, target_is_directory=True)
        result = self.sweep()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, '')

    def test_rejects_malformed_indicator(self):
        self.indicators.write_text('invalid_hash\n', encoding='utf-8')
        result = self.sweep()
        self.assertEqual(result.returncode, 2)
        self.assertIn('expected one SHA-256 digest', result.stderr)

    def test_reports_missing_directory(self):
        result = self.sweep(self.directory / 'missing')
        self.assertEqual(result.returncode, 2)
        self.assertIn('missing', result.stderr)


if __name__ == '__main__':
    unittest.main()
