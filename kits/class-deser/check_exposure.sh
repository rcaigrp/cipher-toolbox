#!/usr/bin/env bash
set -eu

exec python3 - "$@" <<'PY'
import argparse
import os
import re
import sys
from pathlib import Path

parser = argparse.ArgumentParser(description='Inventory legacy .NET serializer references in local source, configuration, and assemblies.')
parser.add_argument('root', nargs='?', default='.', type=Path, help='local directory to inspect (default: current directory)')
args = parser.parse_args()
if not args.root.is_dir() or args.root.is_symlink():
    parser.error('root must be a local directory and not a symbolic link')

serializer = re.compile(rb'\b(?:BinaryFormatter|SoapFormatter|ObjectStateFormatter|LosFormatter|NetDataContractSerializer)\b', re.IGNORECASE)
findings = 0
errors = []

for directory, _, filenames in os.walk(args.root, followlinks=False, onerror=errors.append):
    for filename in sorted(filenames):
        path = Path(directory) / filename
        is_assembly = path.suffix.lower() == '.dll'
        is_text = path.suffix.lower() in {'.cs', '.vb', '.fs'} or filename.lower() in {'app.config', 'web.config'}
        if not (is_assembly or is_text) or path.is_symlink() or not path.is_file():
            continue
        try:
            data = path.read_bytes()
            if is_text and data.startswith((b'\xff\xfe', b'\xfe\xff')):
                data = data.decode('utf-16').encode('utf-8')
        except (OSError, UnicodeError) as error:
            errors.append(f'{str(path)!r}: {error}')
            continue
        matches = sorted({match.group().decode('ascii').lower() for match in serializer.finditer(data)})
        if matches:
            findings += 1
            print(f'Serializer reference: {str(path)!r} ({", ".join(matches)})')

for error in errors:
    print(f'Check incomplete: {error}', file=sys.stderr)
print(f'Files with serializer references: {findings}')
sys.exit(2 if errors else 0)
PY
