import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from linux_hardening_checker import audit


class HardeningCheckerTest(unittest.TestCase):
    def setUp(self):
        fixture = tempfile.TemporaryDirectory()
        self.addCleanup(fixture.cleanup)
        self.root = Path(fixture.name)

    def write_sysctl(self, name, value):
        path = self.root / 'proc/sys' / name.replace('.', '/')
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value + '\n', encoding='ascii')

    def test_cli_with_sample_tree(self):
        samples = {
            'kernel.kptr_restrict': ('2', 'PASS'),
            'kernel.dmesg_restrict': ('0', 'REVIEW'),
            'kernel.randomize_va_space': ('invalid', 'UNKNOWN'),
            'fs.protected_hardlinks': ('1', 'PASS'),
            'fs.protected_symlinks': (None, 'UNKNOWN'),
            'net.ipv4.conf.all.accept_source_route': ('0', 'PASS'),
        }
        for name, (value, _) in samples.items():
            if value is not None:
                self.write_sysctl(name, value)

        etc = self.root / 'etc'
        etc.mkdir()
        (etc / 'passwd').symlink_to('missing-target')
        (etc / 'group').mkdir()

        script = Path(__file__).with_name('linux_hardening_checker.py')
        result = subprocess.run(
            [sys.executable, str(script), '--root', str(self.root)],
            check=True,
            capture_output=True,
            text=True,
        )
        expected = [f'{status} {name}' for name, (_, status) in samples.items()]
        expected.extend(['REVIEW /etc/passwd', 'REVIEW /etc/group', 'UNKNOWN /etc/shadow'])
        observed = [' '.join(line.split(':', 1)[0].split()) for line in result.stdout.splitlines()]
        self.assertEqual(observed, expected)
        self.assertIn('/etc/passwd: expected a regular file', result.stdout)

    def test_account_file_ownership_and_modes(self):
        cases = (
            ((0, 0o644, 'PASS'), (0, 0o644, 'PASS'), (0, 0o640, 'PASS')),
            ((1000, 0o644, 'REVIEW'), (0, 0o664, 'REVIEW'), (0, 0o644, 'REVIEW')),
        )
        names = ('/etc/passwd', '/etc/group', '/etc/shadow')
        for records in cases:
            with self.subTest(records=records):
                metadata = [SimpleNamespace(st_uid=uid, st_mode=stat.S_IFREG | mode)
                            for uid, mode, _ in records]
                with patch.object(Path, 'lstat', side_effect=metadata):
                    result = [(name, status) for status, name, _ in audit(self.root)
                              if name.startswith('/etc/')]
                self.assertEqual(result, list(zip(names, (status for _, _, status in records))))
