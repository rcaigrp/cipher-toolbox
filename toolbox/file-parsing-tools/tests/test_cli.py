import os
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest
import zlib


TOOL_DIR = Path(__file__).resolve().parents[1]


def png_chunk(kind, data):
    payload = kind + data
    return struct.pack('>I', len(data)) + payload + struct.pack('>I', zlib.crc32(payload))


class FileParsingTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        self.text = self.directory / 'sample.txt'
        self.text.write_bytes(b'hello')
        self.png = self.directory / 'sample.png'
        self.png.write_bytes(
            b'\x89PNG\r\n\x1a\n'
            + png_chunk(b'IHDR', struct.pack('>IIBBBBB', 2, 1, 8, 0, 0, 0, 0))
            + png_chunk(b'IDAT', zlib.compress(b'\x00\x00\xff'))
            + png_chunk(b'IEND', b'')
        )

    def run_cli(self, script, *args, status=0, message=None):
        result = subprocess.run(
            [sys.executable, '-B', str(TOOL_DIR / script), *map(str, args)],
            capture_output=True, text=True, timeout=5,
        )
        self.assertEqual(result.returncode, status, result.stdout + result.stderr)
        if message is not None:
            self.assertIn(message, result.stdout + result.stderr)

    def test_size_boundary(self):
        self.run_cli('buffer_safety.py', self.text, '--max-bytes', 5)
        self.run_cli('buffer_safety.py', self.text, '--max-bytes', 4,
                     status=1, message='exceeds the 4-byte limit')

    def test_rejects_symlink_and_fifo(self):
        link = self.directory / 'link.txt'
        link.symlink_to(self.text)
        fifo = self.directory / 'fifo.txt'
        os.mkfifo(fifo)
        self.run_cli('buffer_safety.py', link, status=1)
        self.run_cli('buffer_safety.py', fifo, status=1, message='regular file')

    def test_extension_policy(self):
        self.run_cli('file_validation.py', self.text)
        self.run_cli('file_validation.py', self.text, '--allow-extension', '.pdf',
                     status=1, message='outside the allowed list')
        self.run_cli('file_validation.py', self.text, '--allow-extension', '.TXT')

    def test_png_header_and_pixel_limit(self):
        self.run_cli('safe_image_parser.py', self.png, message='2x1 PNG')
        self.run_cli('safe_image_parser.py', self.png, '--max-pixels', 1,
                     status=1, message='exceed the 1-pixel limit')
        self.run_cli('safe_image_parser.py', self.text, status=1, message='PNG signature')

    def test_png_checksum(self):
        damaged = bytearray(self.png.read_bytes())
        damaged[32] ^= 1
        self.png.write_bytes(damaged)
        self.run_cli('safe_image_parser.py', self.png, status=1, message='checksum mismatch')

    def test_help(self):
        for script in ('buffer_safety.py', 'file_validation.py', 'safe_image_parser.py'):
            with self.subTest(script=script):
                self.run_cli(script, '--help', message='usage:')


if __name__ == '__main__':
    unittest.main()
