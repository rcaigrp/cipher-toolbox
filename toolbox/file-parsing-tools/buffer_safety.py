#!/usr/bin/env python3
"""Enforce an input size limit before handing a file to a parser."""

import argparse
from contextlib import contextmanager
import os
import stat
import sys


@contextmanager
def open_regular_file(path):
    """Open a local regular file without following a final symlink or blocking on a FIFO."""
    with open(path, 'rb', opener=_open_nonblocking) as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
            raise ValueError('input must be a regular file')
        yield stream


def _open_nonblocking(path, flags):
    return os.open(path, flags | os.O_NOFOLLOW | os.O_NONBLOCK)


def check_size(stream, max_bytes):
    """Check both the reported size and the bytes readable from the open file."""
    if os.fstat(stream.fileno()).st_size > max_bytes:
        raise ValueError(f'input exceeds the {max_bytes}-byte limit')
    remaining = max_bytes
    while remaining:
        chunk = stream.read(min(remaining, 64 * 1024))
        if not chunk:
            break
        remaining -= len(chunk)
    if stream.read(1):
        raise ValueError(f'input exceeds the {max_bytes}-byte limit')


def positive_int(value):
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError('must be a positive integer')
    return number


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', help='local regular file to check')
    parser.add_argument('--max-bytes', type=positive_int, default=10 * 1024 * 1024,
                        help='maximum input size in bytes (default: 10485760)')
    args = parser.parse_args()
    try:
        with open_regular_file(args.path) as stream:
            check_size(stream, args.max_bytes)
    except (OSError, ValueError) as error:
        print(f'{args.path!r}: {error}', file=sys.stderr)
        return 1
    print(f'{args.path!r}: passed the {args.max_bytes}-byte size check')
    return 0


if __name__ == '__main__':
    sys.exit(main())
