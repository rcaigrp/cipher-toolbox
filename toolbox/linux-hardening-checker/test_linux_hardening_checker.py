import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from linux_hardening_checker import audit


class HardeningCheckerTests(unittest.TestCase):
    def test_sysctl_results(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            kernel = root / 'proc/sys/kernel'
            kernel.mkdir(parents=True)
            (kernel / 'kptr_restrict').write_text('2\n', encoding='ascii')
            (kernel / 'dmesg_restrict').write_text('0\n', encoding='ascii')
            (kernel / 'randomize_va_space').write_text('invalid\n', encoding='ascii')
            statuses = {name: status for status, name, _ in audit(root)}
            self.assertEqual(statuses['kernel.kptr_restrict'], 'PASS')
            self.assertEqual(statuses['kernel.dmesg_restrict'], 'REVIEW')
            self.assertEqual(statuses['kernel.randomize_va_space'], 'UNKNOWN')
            self.assertEqual(statuses['fs.protected_symlinks'], 'UNKNOWN')

    def test_file_metadata_results(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            etc = root / 'etc'
            etc.mkdir()
            passwd = etc / 'passwd'
            passwd.touch()
            passwd.chmod(0o644)
            (etc / 'group').symlink_to('passwd')
            shadow = etc / 'shadow'
            shadow.touch()
            shadow.chmod(0o644)
            real_lstat = Path.lstat

            def fixture_lstat(path):
                info = real_lstat(path)
                return type(info)((info.st_mode, info.st_ino, info.st_dev,
                                   info.st_nlink, 0, info.st_gid, info.st_size,
                                   info.st_atime, info.st_mtime, info.st_ctime))

            with patch.object(Path, 'lstat', fixture_lstat):
                results = {name: (status, detail) for status, name, detail in audit(root)}
            self.assertEqual(results['/etc/passwd'][0], 'PASS')
            self.assertEqual(results['/etc/group'], ('REVIEW', 'expected a regular file'))
            self.assertEqual(results['/etc/shadow'][0], 'REVIEW')

    def test_cli_reads_fixture_root(self):
        script = Path(__file__).with_name('linux_hardening_checker.py')
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [sys.executable, str(script), '--root', directory],
                check=True, capture_output=True, text=True,
            )
            self.assertIn('UNKNOWN kernel.kptr_restrict:', result.stdout)
            self.assertIn('UNKNOWN /etc/shadow:', result.stdout)
            self.assertEqual(len(result.stdout.splitlines()), 9)


if __name__ == '__main__':
    unittest.main()
