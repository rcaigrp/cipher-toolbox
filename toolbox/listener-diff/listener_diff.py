#!/usr/bin/env python3
"""Compare local TCP listeners and bound UDP sockets using ss snapshots."""

import argparse
import ipaddress
from pathlib import Path
import subprocess
import sys


def parse_snapshot(snapshot, source):
    endpoints = set()
    for line_number, line in enumerate(snapshot.splitlines(), 1):
        if not line.strip():
            continue
        fields = line.split()
        if len(fields) != 6 or fields[0] not in {'tcp', 'udp'}:
            raise ValueError(f'{source}:{line_number}: expected ss -H -lntu output')
        protocol, state, _, _, local, _ = fields
        host, separator, port = local.rpartition(':')
        if not separator or not host or not port.isascii() or not port.isdecimal() or len(port) > 5 or not 0 <= int(port) <= 65535:
            raise ValueError(f'{source}:{line_number}: invalid local endpoint {local!r}')
        if host.startswith('[') and host.endswith(']'):
            host = host[1:-1]
        if host != '*':
            try:
                host = str(ipaddress.ip_address(host))
            except ValueError as exc:
                raise ValueError(f'{source}:{line_number}: invalid local address {host!r}') from exc
        if (protocol, state) not in {('tcp', 'LISTEN'), ('udp', 'UNCONN')}:
            raise ValueError(f'{source}:{line_number}: unexpected socket state {state!r}')
        endpoints.add((protocol, host, int(port)))
    return endpoints


def print_changes(label, endpoints):
    for protocol, host, port in sorted(endpoints):
        address = f'[{host}]' if ':' in host else host
        print(f'{label} {protocol} {address}:{port}')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('baseline', type=Path, help='baseline captured with ss -H -lntu')
    parser.add_argument('current', type=Path, nargs='?', help='second snapshot (default: read live local sockets)')
    args = parser.parse_args(argv)
    try:
        baseline = parse_snapshot(args.baseline.read_text(encoding='utf-8'), args.baseline)
        if args.current is None:
            command = ['ss', '-H', '-lntu']
            snapshot = subprocess.run(command, check=True, capture_output=True, text=True).stdout
            current = parse_snapshot(snapshot, 'live ss')
        else:
            current = parse_snapshot(args.current.read_text(encoding='utf-8'), args.current)
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(f'listener-diff: {exc}', file=sys.stderr)
        return 2
    if baseline == current:
        print('No listener changes.')
        return 0
    print_changes('ADDED', current - baseline)
    print_changes('REMOVED', baseline - current)
    return 1


if __name__ == '__main__':
    sys.exit(main())
