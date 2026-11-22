#!/usr/bin/env python3
"""Review local TCP listeners against operator-supplied NCIC gateway ports."""

import argparse
from pathlib import Path
import subprocess


def tcp_port(value):
    try:
        port = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError('expected a port number') from exc
    if not 1 <= port <= 65535:
        raise argparse.ArgumentTypeError('port must be between 1 and 65535')
    return port


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--gateway-port', type=tcp_port, action='append', default=[],
                        help='known local NCIC gateway TCP port from your inventory; repeat as needed')
    parser.add_argument('--auth-log', type=Path, help='local authentication log path to check')
    parser.add_argument('--query-log', type=Path, help='local query audit log path to check')
    args = parser.parse_args()

    print('Fixed-version comparison: unavailable in the supplied incident reporting.')
    for label, path in [('Authentication log', args.auth_log), ('Query audit log', args.query_log)]:
        if path is None:
            print(f'{label}: path unspecified')
            continue
        try:
            path.stat()
        except OSError as exc:
            print(f'{label}: metadata unavailable ({exc})')
        else:
            print(f'{label}: path exists ({path}); verify coverage and retention separately')

    try:
        listeners = subprocess.run(['ss', '-H', '-ltn'], capture_output=True,
                                   text=True, check=True, timeout=10).stdout
    except (OSError, subprocess.SubprocessError) as exc:
        print(f'VERDICT: Local listener check incomplete ({exc}). Incident exposure unknown.')
        return 2

    if not args.gateway_port:
        print('VERDICT: Incident exposure unknown. Supply inventoried gateway ports to assess local bindings.')
        return 2

    found = False
    for line in listeners.splitlines():
        columns = line.split()
        if len(columns) < 5:
            continue
        local = columns[3]
        address, _, port = local.rpartition(':')
        if port.isdecimal() and int(port) in args.gateway_port:
            found = True
            scope = 'wildcard binding' if address in {'*', '0.0.0.0', '[::]'} else 'specific address binding'
            print(f'Local TCP listener {local} ({scope})')

    if found:
        print('VERDICT: Review gateway bindings and confirm reachability against approved access paths. Incident exposure unknown.')
        return 1
    print('VERDICT: No TCP listeners found on the supplied ports in this network namespace. Incident exposure unknown.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
