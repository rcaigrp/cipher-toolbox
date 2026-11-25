#!/usr/bin/env python3
"""Stage an NGINX access restriction for an affected openIMIS deployment."""

import argparse
from pathlib import Path


CONFIG = "# Temporary access restriction for openIMIS CVE-2026-82489\ndeny all;\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path,
                        help='New NGINX snippet file to stage. Existing files are preserved.')
    parser.add_argument('--apply', action='store_true',
                        help='Write the snippet. The default only prints the proposed change.')
    args = parser.parse_args()

    if not args.apply:
        print(f'Dry run. Would create {args.output} with the following contents:')
        print(CONFIG, end='')
    else:
        try:
            with args.output.open('x', encoding='utf-8') as output:
                output.write(CONFIG)
        except OSError as error:
            parser.exit(1, f'Could not stage {args.output}: {error}\n')
        print(f'Staged {args.output}. NGINX has not been changed or reloaded.')

    print('This snippet denies all clients wherever it is included.')
    print('Review and explicitly include it in the affected openIMIS NGINX location.')
    print('Check that every route to the affected service is covered, including direct backend access.')
    print('Run nginx -t before reloading. Upgrade openIMIS to 2026-10 or later.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
