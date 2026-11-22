#!/usr/bin/env python3
"""Preserve local authentication and query audit logs for incident review."""

import argparse
import os
from pathlib import Path
import shutil
import stat
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--auth-log', type=Path, help='local authentication log or rotated export')
    parser.add_argument('--query-log', type=Path, help='local query audit log or rotated export')
    parser.add_argument('--output-dir', type=Path, help='new directory under an existing evidence directory')
    parser.add_argument('--apply', action='store_true', help='create the private evidence directory and copy the logs')
    args = parser.parse_args()

    print('Confirm incident scope through the FBI or your state CJIS contact.')
    print('The supplied reporting identifies no product-specific configuration workaround.')
    sources = {'authentication.log': args.auth_log, 'query-audit.log': args.query_log}
    if not all(sources.values()) or args.output_dir is None:
        if args.apply:
            parser.error('--apply requires --auth-log, --query-log, and --output-dir')
        print('DRY RUN: Supply both local log paths and a new evidence directory to preview the copies.')
        return 0

    output_dir = args.output_dir
    try:
        for source in sources.values():
            if not stat.S_ISREG(source.lstat().st_mode):
                raise ValueError(f'expected a regular file, without a final symlink: {source}')
        if not output_dir.parent.is_dir():
            raise ValueError(f'evidence parent directory does not exist: {output_dir.parent}')
        if output_dir.exists() or output_dir.is_symlink():
            raise ValueError(f'evidence directory already exists: {output_dir}')
        for name, source in sources.items():
            print(f'{"Preserve" if args.apply else "DRY RUN: Would copy"} {source} to {output_dir / name}')
        if not args.apply:
            return 0

        output_dir.mkdir(mode=0o700)
        for name, source in sources.items():
            with source.open('rb') as original, (output_dir / name).open('xb') as copy:
                os.fchmod(copy.fileno(), 0o600)
                shutil.copyfileobj(original, copy)
        print(f'Both logs copied to {output_dir}. Use rotated logs or stable exports for a consistent capture.')
        return 0
    except (OSError, ValueError) as exc:
        print(f'Preservation failed: {exc}', file=sys.stderr)
        if args.apply:
            print('If this run created the evidence directory, treat its contents as potentially incomplete.', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
