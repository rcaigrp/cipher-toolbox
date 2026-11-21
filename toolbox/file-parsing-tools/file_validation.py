#!/usr/bin/env python3
"""Check a local file against a filename extension and input size policy."""

import argparse
from pathlib import Path
import sys

from buffer_safety import check_size, open_regular_file, positive_int


DEFAULT_EXTENSIONS = ('.txt', '.pdf', '.log', '.xml', '.json')


def extension(value):
    if not value.startswith('.') or len(value) < 2 or any(
        character in value[1:] for character in './\\'
    ):
        raise argparse.ArgumentTypeError('expected a single extension such as .txt')
    return value.lower()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', type=Path, help='local regular file to check')
    parser.add_argument('--max-bytes', type=positive_int, default=50 * 1024 * 1024,
                        help='maximum input size in bytes (default 52428800)')
    parser.add_argument('--allow-extension', action='append', type=extension,
                        help='override the default list (.txt, .pdf, .log, .xml, .json); repeat to allow multiple extensions')
    args = parser.parse_args()
    allowed_extensions = args.allow_extension or DEFAULT_EXTENSIONS
    suffix = args.path.suffix.lower()
    try:
        if suffix not in allowed_extensions:
            raise ValueError(f'extension {suffix!r} is outside the allowed list')
        with open_regular_file(args.path) as stream:
            check_size(stream, args.max_bytes)
    except (OSError, ValueError) as error:
        print(f'{str(args.path)!r}: {error}', file=sys.stderr)
        return 1
    print(f'{str(args.path)!r}: passed the extension and size checks')
    return 0


if __name__ == '__main__':
    sys.exit(main())
