#!/usr/bin/env python3
"""Inventory common file parsers on Linux without opening any input files."""

import argparse
import shutil
import subprocess
import sys


PARSER_NAMES = (
    'autocad', 'dwg2dxf', 'dwgread', 'pdfinfo', 'pdftotext', 'pdftoppm',
    'pdftocairo', 'mutool', 'gs', 'evince', 'okular', 'libreoffice',
    'soffice', 'soffice.bin', 'inkscape', 'gimp', 'gimp-2.10', 'gimp-3.0',
    'magick', 'convert', 'convert-im6', 'convert-im6.q16', 'identify',
    'identify-im6', 'identify-im6.q16',
)


def find_file_parsing_processes():
    """Return PID and command name for each matching running process."""
    result = subprocess.run(
        ['ps', '-ww', '-eo', 'pid=,stat=,comm='],
        capture_output=True,
        text=True,
        errors='replace',
        check=True,
        timeout=10,
    )
    processes = []
    for line in result.stdout.splitlines():
        fields = line.split(maxsplit=2)
        if len(fields) != 3:
            continue
        pid, state, command = fields
        if not state.startswith('Z') and command.casefold() in PARSER_NAMES:
            processes.append((int(pid), command))
    return processes


def main():
    parser = argparse.ArgumentParser(
        description='List common file parsing processes and tools on Linux.',
        epilog='Matches indicate parser presence. Vulnerability status is outside the scope of this inventory.',
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='Show every matching process and the PATH location of each available parser. By default, show the first five matching processes and list available parsers by name.',
    )
    args = parser.parse_args()

    try:
        processes = find_file_parsing_processes()
    except (OSError, subprocess.SubprocessError) as error:
        print(f'Could not inspect running processes: {error}', file=sys.stderr)
        return 1

    if processes:
        print(f'Found {len(processes)} running process(es) with known parser names:')
        visible_processes = processes if args.verbose else processes[:5]
        for pid, command in visible_processes:
            print(f'  {pid:>7}  {command}')
        if len(visible_processes) < len(processes):
            print(f'  ... and {len(processes) - len(visible_processes)} more (use --verbose)')
    else:
        print('No running processes matched the known parser names.')

    available = {}
    for name in PARSER_NAMES:
        path = shutil.which(name)
        if path:
            available[name] = path
    if available and args.verbose:
        print('Parser executables on PATH:')
        for name, path in available.items():
            print(f'  {name}: {path}')
    elif available:
        print(f'Parser executables on PATH: {", ".join(available)}')
    else:
        print('No known parser executables found on PATH.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
