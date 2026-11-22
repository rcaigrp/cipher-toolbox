#!/usr/bin/env python3
"""Inventory native parser packages and locally discoverable tools on Debian."""

import shutil
import subprocess
import sys

PACKAGE_FAMILIES = ('gpac', 'libgpac', 'ffmpeg', 'libavformat', 'ytnef', 'libytnef', 'claws-mail-tnef')
TOOLS = ('MP4Box', 'ffmpeg', 'ytnef')


def main():
    try:
        result = subprocess.run(
            ['dpkg-query', '-W', '-f=${Package}\t${Version}\t${db:Status-Status}\n'],
            capture_output=True, text=True, check=True,
        )
    except (OSError, subprocess.CalledProcessError) as error:
        print(f'Package inventory unavailable ({error})', file=sys.stderr)
        return 1

    matches = []
    for line in result.stdout.splitlines():
        package, version, status = line.split('\t')
        if status == 'installed' and package.startswith(PACKAGE_FAMILIES):
            matches.append(f'{package}\t{version}')

    print('Installed parser packages and versions')
    print('\n'.join(sorted(matches)) or 'No matching installed packages found.')
    print('\nParser tools on PATH')
    paths = [(tool, shutil.which(tool)) for tool in TOOLS]
    print('\n'.join(f'{tool}\t{path}' for tool, path in paths if path)
          or 'No matching tools found on PATH.')
    print('\nFor each match, verify downstream patch status and whether an automatic worker parses external input.')
    print('Coverage is limited to the local Debian package database and current PATH. Check containers, bundled libraries, and worker configuration separately.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
