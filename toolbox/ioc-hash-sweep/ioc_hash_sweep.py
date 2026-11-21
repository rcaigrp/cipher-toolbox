#!/usr/bin/env python3
"""Match local files against a supplied list of SHA-256 indicators."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys


def load_indicators(path):
    indicators = set()
    with path.open(encoding='utf-8') as source:
        for number, line in enumerate(source, 1):
            value = line.partition('#')[0].strip().lower()
            if not value:
                continue
            if not re.fullmatch(r'[0-9a-f]{64}', value):
                raise ValueError(f'{path}:{number}: expected one SHA-256 digest')
            indicators.add(value)
    if not indicators:
        raise ValueError(f'{path}: no SHA-256 indicators supplied')
    return indicators


def file_digest(path):
    if not stat.S_ISREG(path.lstat().st_mode):
        return None
    flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
    with os.fdopen(os.open(path, flags), 'rb') as source:
        before = os.fstat(source.fileno())
        if not stat.S_ISREG(before.st_mode):
            return None
        digest = hashlib.sha256()
        for chunk in iter(lambda: source.read(1024 * 1024), b''):
            digest.update(chunk)
        after = os.fstat(source.fileno())
        if (before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (
            after.st_size, after.st_mtime_ns, after.st_ctime_ns
        ):
            raise OSError(f'{path}: file changed during hashing')
        return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--hashes', required=True, type=Path,
                        help='UTF-8 file with one SHA-256 digest per line')
    parser.add_argument('directory', type=Path, help='local directory to sweep recursively')
    args = parser.parse_args()
    try:
        indicators = load_indicators(args.hashes)
        if not stat.S_ISDIR(args.directory.lstat().st_mode):
            raise ValueError(f'{args.directory}: expected a directory, without a symlink')
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 2

    errors = 0
    matched = False

    def report_error(error):
        nonlocal errors
        errors += 1
        print(error, file=sys.stderr)

    for directory, subdirectories, files in os.walk(
        args.directory, onerror=report_error, followlinks=False
    ):
        subdirectories.sort()
        for name in sorted(files):
            path = Path(directory) / name
            try:
                digest = file_digest(path)
            except OSError as error:
                report_error(error)
                continue
            if digest in indicators:
                matched = True
                print(json.dumps({'path': str(path), 'sha256': digest}))

    if errors:
        return 2
    return 1 if matched else 0


if __name__ == '__main__':
    sys.exit(main())
