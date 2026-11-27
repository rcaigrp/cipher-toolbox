import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


CHECKER = Path(__file__).resolve().with_name('linux_hardening_checker.py')


class HardeningCheckerTest(unittest.TestCase):
    def test_fixture_root(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            kernel = root / 'proc/sys/kernel'
            kernel.mkdir(parents=True)
            (kernel / 'kptr_restrict').write_text('2\n', encoding='ascii')
            (kernel / 'dmesg_restrict').write_text('0\n', encoding='ascii')
            (kernel / 'randomize_va_space').write_text('invalid\n', encoding='ascii')

            etc = root / 'etc'
            etc.mkdir()
            (etc / 'passwd').mkdir()
            group = etc / 'group'
            group.touch()
            group.chmod(0o666)

            result = subprocess.run(
                [sys.executable, str(CHECKER), '--root', str(root)],
                check=True,
                capture_output=True,
                text=True,
            )

        self.assertEqual(result.stderr, '')
        statuses = {}
        for line in result.stdout.splitlines():
            status, report = line.split(maxsplit=1)
            name, _, _ = report.partition(':')
            self.assertNotIn(name, statuses)
            statuses[name] = status
        self.assertEqual(statuses, {
            'kernel.kptr_restrict': 'PASS',
            'kernel.dmesg_restrict': 'REVIEW',
            'kernel.randomize_va_space': 'UNKNOWN',
            'fs.protected_hardlinks': 'UNKNOWN',
            'fs.protected_symlinks': 'UNKNOWN',
            'net.ipv4.conf.all.accept_source_route': 'UNKNOWN',
            '/etc/passwd': 'REVIEW',
            '/etc/group': 'REVIEW',
            '/etc/shadow': 'UNKNOWN',
        })


if __name__ == '__main__':
    unittest.main()
