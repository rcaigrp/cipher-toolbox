#!/usr/bin/env python3
"""Report selected Linux hardening settings from the local filesystem."""

import argparse
import stat
from pathlib import Path


SYSCTL_CHECKS = (
    ('kernel.kptr_restrict', {1, 2}, '1 or 2 to restrict kernel pointer exposure'),
    ('kernel.dmesg_restrict', {1}, '1 to restrict access to the kernel log'),
    ('kernel.randomize_va_space', {2}, '2 for full address space randomization'),
    ('fs.protected_hardlinks', {1}, '1 to restrict hardlink creation'),
    ('fs.protected_symlinks', {1}, '1 to restrict symlink following in sticky directories'),
    ('net.ipv4.conf.all.accept_source_route', {0}, '0 to disable IPv4 source routing globally'),
)


def audit(root):
    for name, accepted, expected in SYSCTL_CHECKS:
        path = root / 'proc/sys' / name.replace('.', '/')
        try:
            value = int(path.read_text(encoding='ascii').strip())
        except (OSError, ValueError) as error:
            yield 'UNKNOWN', name, str(error)
            continue
        status = 'PASS' if value in accepted else 'REVIEW'
        yield status, name, f'observed {value}, expected {expected}'

    for name in ('/etc/passwd', '/etc/group', '/etc/shadow'):
        path = root / name.lstrip('/')
        try:
            info = path.lstat()
        except OSError as error:
            yield 'UNKNOWN', name, str(error)
            continue
        if not stat.S_ISREG(info.st_mode):
            yield 'REVIEW', name, 'expected a regular file'
            continue
        mode = stat.S_IMODE(info.st_mode)
        forbidden = 0o027 if name == '/etc/shadow' else 0o022
        status = 'PASS' if info.st_uid == 0 and not mode & forbidden else 'REVIEW'
        yield status, name, f'owner UID {info.st_uid}, mode {mode:04o}; expected root ownership and no bits from {forbidden:04o}'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path('/'),
                        help='read checks under this directory (default: /)')
    args = parser.parse_args()
    if not args.root.is_dir():
        parser.error('--root must be an existing directory')
    for status, name, detail in audit(args.root):
        print(f'{status:7} {name}: {detail}')


if __name__ == '__main__':
    main()
