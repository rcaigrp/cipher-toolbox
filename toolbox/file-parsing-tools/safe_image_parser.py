#!/usr/bin/env python3
"""Check a local PNG's input size, header, and pixel budget without decoding it."""

import argparse
import struct
import sys
import zlib

from buffer_safety import check_size, open_regular_file, positive_int


PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'
VALID_DEPTHS = {0: {1, 2, 4, 8, 16}, 2: {8, 16}, 3: {1, 2, 4, 8},
                4: {8, 16}, 6: {8, 16}}


def check_png_header(stream, max_pixels):
    header = stream.read(33)
    if len(header) != 33 or header[:8] != PNG_SIGNATURE:
        raise ValueError('expected a PNG signature and complete IHDR chunk')
    length, chunk_type = struct.unpack_from('>I4s', header, 8)
    if length != 13 or chunk_type != b'IHDR':
        raise ValueError('expected a 13-byte IHDR as the first chunk')
    expected_crc, = struct.unpack_from('>I', header, 29)
    if zlib.crc32(header[12:29]) != expected_crc:
        raise ValueError('IHDR checksum mismatch')
    width, height, depth, color, compression, filtering, interlace = struct.unpack_from(
        '>IIBBBBB', header, 16
    )
    if not (0 < width < 2**31 and 0 < height < 2**31):
        raise ValueError('invalid PNG dimensions')
    if width * height > max_pixels:
        raise ValueError(f'PNG dimensions exceed the {max_pixels}-pixel limit')
    if depth not in VALID_DEPTHS.get(color, ()):
        raise ValueError('invalid PNG color type or bit depth')
    if compression != 0 or filtering != 0 or interlace not in (0, 1):
        raise ValueError('invalid PNG compression, filtering, or interlace method')
    return width, height


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', help='local regular file containing a PNG')
    parser.add_argument('--max-bytes', type=positive_int, default=20 * 1024 * 1024,
                        help='maximum input size in bytes (default: 20971520)')
    parser.add_argument('--max-pixels', type=positive_int, default=25_000_000,
                        help='maximum declared pixel count (default: 25000000)')
    args = parser.parse_args()
    try:
        with open_regular_file(args.path) as stream:
            width, height = check_png_header(stream, args.max_pixels)
            stream.seek(0)
            check_size(stream, args.max_bytes)
    except (OSError, ValueError) as error:
        print(f'{args.path!r}: {error}', file=sys.stderr)
        return 1
    print(f'{args.path!r}: {width}x{height} PNG passed header and size checks')
    return 0


if __name__ == '__main__':
    sys.exit(main())
