#!/usr/bin/env python3
"""Assess an openIMIS deployment using local release and socket evidence."""

import argparse
import ipaddress
import re
import subprocess
from pathlib import Path


RELEASE = re.compile(r'([0-9]{4})[-.](0[1-9]|1[0-2])')
FIXED = (2026, 10)


def local_listeners(port):
    result = subprocess.run(['ss', '-Hltn'], check=True, capture_output=True,
                            text=True, timeout=10)
    for line in result.stdout.splitlines():
        fields = line.split()
        if len(fields) < 5:
            raise ValueError('Unexpected ss output')
        address, _, local_port = fields[3].rpartition(':')
        if local_port == str(port):
            yield address.strip('[]')


def binding_scope(address):
    if address == '*':
        return 'wildcard'
    ip = ipaddress.ip_address(address.split('%', 1)[0])
    if ip.version == 6 and ip.ipv4_mapped:
        ip = ip.ipv4_mapped
    if ip.is_loopback:
        return 'loopback'
    return 'wildcard' if ip.is_unspecified else 'non-loopback'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    release = parser.add_mutually_exclusive_group()
    release.add_argument('--release', help='Verified installed openIMIS suite release, YYYY-MM')
    release.add_argument('--release-file', type=Path,
                         help='Local deployment file containing only its suite release')
    parser.add_argument('--port', type=int, choices=None,
                        help='Verified local TCP port for this deployment')
    parser.add_argument('--preview-access', choices=('untrusted', 'restricted', 'unknown'),
                        default='unknown', help='Operator-verified preview ingress policy')
    args = parser.parse_args()
    if args.port is not None and not 1 <= args.port <= 65535:
        parser.error('--port must be between 1 and 65535')

    version = args.release or ''
    if args.release_file:
        try:
            with args.release_file.open(encoding='utf-8') as source:
                version = source.read(65).strip()
        except (OSError, UnicodeError) as error:
            print(f'Could not read release file: {error}')
    match = RELEASE.fullmatch(version)
    if match:
        installed = tuple(map(int, match.groups()))
        print(f'Installed suite release: {installed[0]}-{installed[1]:02d}')
    else:
        installed = None
        print('Installed suite release could not be established.')

    print(f'Operator-reported preview ingress: {args.preview_access}')
    if args.port is None:
        print('Local listener assessment requires the deployment TCP port.')
    else:
        try:
            bindings = [(address, binding_scope(address))
                        for address in local_listeners(args.port)]
            for address, scope in bindings:
                print(f'TCP port {args.port} binds to {address} ({scope}).')
            if not bindings:
                print(f'No TCP listener for port {args.port} in this network namespace.')
        except (OSError, ValueError, subprocess.SubprocessError) as error:
            print(f'Local listener check unavailable: {error}')
        print('Check proxy and container ingress separately. Socket bindings alone cannot establish access policy.')

    if installed is None:
        print('VERDICT: UNKNOWN. Verify the installed suite release.')
        return 2
    if installed >= FIXED:
        print('VERDICT: FIXED RELEASE for this CVE, based on the supplied release evidence.')
        return 0
    print(f'VERDICT: AFFECTED RELEASE. Preview access is {args.preview_access} based on operator input.')
    print('Block untrusted access and upgrade to 2026-10 or later.')
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
