#!/usr/bin/env python3
"""Inventory local document conversion tools without running them or accessing the network."""

import json
import os
import shutil
import subprocess
from pathlib import Path


BINARIES = ('gs', 'magick', 'convert', 'pdftoppm', 'pdftocairo', 'mutool', 'soffice', 'unoconv')
PACKAGE_PATTERNS = ('ghostscript', 'libgs[0-9]*', 'imagemagick*', 'poppler-utils', 'mupdf-tools', 'libreoffice-core*', 'unoconv')
POLICY_PATHS = (
    '/etc/ImageMagick-6/policy.xml',
    '/etc/ImageMagick-7/policy.xml',
    '/usr/local/etc/ImageMagick-6/policy.xml',
    '/usr/local/etc/ImageMagick-7/policy.xml',
)


def main():
    binaries = {name: shutil.which(name) for name in BINARIES}
    packages = []
    errors = []
    dpkg_query = shutil.which('dpkg-query')
    if dpkg_query:
        try:
            result = subprocess.run(
                [dpkg_query, '-W', '-f=${db:Status-Status}\t${binary:Package}\t${Version}\n', *PACKAGE_PATTERNS],
                capture_output=True, text=True, timeout=10, env={**os.environ, 'LC_ALL': 'C'},
            )
            for line in result.stdout.splitlines():
                fields = line.split('\t')
                if len(fields) == 3 and fields[0] == 'installed':
                    packages.append({'name': fields[1], 'version': fields[2]})
            for line in result.stderr.splitlines():
                if not line.startswith('dpkg-query: no packages found matching '):
                    errors.append(line)
            if result.returncode and not result.stderr:
                errors.append(f'dpkg-query exited with status {result.returncode}')
        except (OSError, subprocess.TimeoutExpired) as exc:
            errors.append(str(exc))
    else:
        errors.append('dpkg-query unavailable; package inventory skipped')

    print(json.dumps({
        'binaries_on_path': {name: path for name, path in binaries.items() if path},
        'installed_packages': packages,
        'policy_files_at_common_paths': [path for path in POLICY_PATHS if Path(path).is_file()],
        'magick_configure_path': os.environ.get('MAGICK_CONFIGURE_PATH'),
        'inventory_errors': errors,
        'scope': 'Current environment only. Run within each conversion worker environment to inventory its tools.',
        'review': 'Confirm which untrusted inputs reach these tools and verify the worker identity, mounts, secrets, and outbound access in the deployment configuration.',
    }, indent=2))
    return int(bool(errors))


if __name__ == '__main__':
    raise SystemExit(main())
