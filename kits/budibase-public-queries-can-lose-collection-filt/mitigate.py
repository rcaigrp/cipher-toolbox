#!/usr/bin/env python3
"""Stage a deny rule for an inventoried Budibase route in Nginx."""

import argparse
import os
from pathlib import Path
import re
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--query-path', help='Operator-confirmed literal URL path')
    parser.add_argument('--output', type=Path, help='New local file to stage for inclusion in the relevant Nginx server block')
    parser.add_argument('--apply', action='store_true', help='Create the staged file without overwriting an existing path')
    args = parser.parse_args()
    if args.query_path is None and args.output is None and not args.apply:
        print('DRY RUN: Supply --query-path and --output to preview the exact route restriction.')
        return
    if args.query_path is None or args.output is None:
        parser.error('--query-path and --output are required together')
    route = args.query_path
    if not re.fullmatch(r'/(?:[A-Za-z0-9._~-]+/)*[A-Za-z0-9._~-]+/?', route) or any(
        part in {'.', '..'} for part in route.split('/')
    ):
        parser.error('--query-path must be a literal non-root path with no dot segments')
    snippet = f'# CVE-2026-137498\nlocation = {route} {{\n    return 403;\n}}\n'
    if not args.apply:
        print(f'DRY RUN: Would create {args.output}')
        print(snippet, end='')
        return
    try:
        with tempfile.TemporaryDirectory(dir=args.output.parent) as temp_dir:
            staged = Path(temp_dir) / 'restriction.conf'
            staged.write_text(snippet, encoding='ascii')
            os.link(staged, args.output)
    except OSError as exc:
        parser.exit(1, f'Could not stage the restriction: {exc}\n')
    print(f'Staged {args.output}. Include it in the relevant Nginx server block, run nginx -t, then reload.')
    print('Review every route variant and ingress, including direct access to the application listener.')
    print('To roll back, remove the include directive, run nginx -t, and reload.')


if __name__ == '__main__':
    main()
