#!/usr/bin/env python3
"""Check existing AddressSanitizer logs for out-of-bounds reads."""

import argparse
import re
import sys


REPORT = re.compile(
    r'\bERROR: AddressSanitizer: '
    r'(heap-buffer-overflow|stack-buffer-overflow|stack-buffer-underflow|'
    r'global-buffer-overflow|dynamic-stack-buffer-overflow)\b'
)
ACCESS = re.compile(r'\b(READ|WRITE) of size (\d+)\b')
REPORT_BOUNDARY = re.compile(r'\b(?:ERROR|SUMMARY): AddressSanitizer:')


def findings(lines):
    pending = None
    for line_number, line in enumerate(lines, 1):
        if REPORT_BOUNDARY.search(line):
            report = REPORT.search(line)
            pending = (line_number, report.group(1)) if report else None
        if pending is None:
            continue
        access = ACCESS.search(line)
        if access:
            if access.group(1) == 'READ':
                report_line, kind = pending
                yield report_line, kind, int(access.group(2))
            pending = None


def main():
    parser = argparse.ArgumentParser(
        description='Check existing AddressSanitizer logs for out-of-bounds reads.',
        epilog='Exit status: 0 no matching reports, 1 findings, 2 input error.',
    )
    parser.add_argument('log', nargs='+', help='Log path, or - for standard input')
    args = parser.parse_args()
    if args.log.count('-') > 1:
        parser.error('standard input can only be read once')

    found = False
    failed = False
    for path in args.log:
        try:
            if path == '-':
                for line_number, kind, size in findings(sys.stdin):
                    print(f'<stdin>:{line_number}: {kind}, read of {size} byte(s)')
                    found = True
            else:
                with open(path, encoding='utf-8', errors='replace') as log:
                    for line_number, kind, size in findings(log):
                        print(f'{path}:{line_number}: {kind}, read of {size} byte(s)')
                        found = True
        except OSError as error:
            print(f'{path}: {error.strerror}', file=sys.stderr)
            failed = True

    if failed:
        return 2
    if found:
        return 1
    print('No matching AddressSanitizer out-of-bounds read reports found.')
    return 0


if __name__ == '__main__':
    sys.exit(main())