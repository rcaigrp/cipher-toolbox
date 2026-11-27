#!/usr/bin/env python3
"""Assess local Budibase exposure from deployment evidence and TCP listeners."""

import argparse
import ipaddress
import json
from pathlib import Path
import re
import subprocess


def report_version(path):
    if path is None:
        print('Version: unknown. Supply the deployed Budibase package manifest with --version-path.')
        return False
    try:
        version = json.loads(path.read_text())['version']
        match = re.fullmatch(r'(\d+)\.(\d+)\.(\d+)(-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?', version)
        if not match:
            raise ValueError('expected a semantic version')
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(f'Version: unknown ({exc}).')
        return False
    release = tuple(map(int, match.groups()[:3]))
    affected = release < (4, 0, 0) or (release == (4, 0, 0) and bool(match[4]))
    if affected:
        print(f'Version: {version} falls below the vendor-stated 4.0.0 fix.')
    else:
        print(f'Version: {version} meets the vendor-stated floor. The 4.1.0 report remains unresolved. Verify the deployed build before lifting restrictions.')
    return affected


def review_inventory(path):
    if path is None:
        print('Query inventory: unknown. Supply a reviewed local inventory with --config-path.')
        return None
    try:
        rows = json.loads(path.read_text())['publicQueries']
        if not isinstance(rows, list):
            raise ValueError('publicQueries must be a list')
        risky = []
        for row in rows:
            if not isinstance(row, dict) or not isinstance(row.get('id'), str) or type(row.get('callerControlledFilterFields')) is not bool:
                raise ValueError('each row needs a string id and a boolean callerControlledFilterFields')
            if row['callerControlledFilterFields'] or row.get('filter') in ({}, '{}'):
                risky.append(row['id'])
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(f'Query inventory: unknown ({exc}).')
        return None
    print(f'Public MongoDB queries inventoried: {len(rows)}. Queries requiring review: {json.dumps(risky)}.')
    return risky


def report_listeners(path, ports):
    try:
        lines = (path.read_text() if path else subprocess.run(
            ['ss', '-Hltn'], check=True, capture_output=True, text=True, timeout=10
        ).stdout).splitlines()
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f'Local listeners: unknown ({exc}).')
        return
    matched = set()
    for line in lines:
        fields = line.split()
        if len(fields) < 5 or fields[0] != 'LISTEN':
            continue
        endpoint = fields[3]
        host, _, port = endpoint.rpartition(':')
        if not port.isdecimal() or int(port) not in ports:
            continue
        address = host.strip('[]').split('%', 1)[0]
        try:
            ip = ipaddress.ip_address(address)
            loopback = ip.is_loopback or bool(getattr(ip, 'ipv4_mapped', None) and ip.ipv4_mapped.is_loopback)
        except ValueError:
            loopback = False
        matched.add((endpoint, 'loopback' if loopback else 'non-loopback or wildcard'))
    for endpoint, scope in sorted(matched):
        print(f'Candidate TCP listener: {endpoint} ({scope}).')
    if not matched:
        print(f'No TCP listeners found on candidate ports {sorted(ports)}.')
    print('Listener scope alone cannot establish application identity or external reachability.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version-path', type=Path, help='Local package.json for the deployed Budibase build')
    parser.add_argument('--ports-path', type=Path, help='Saved local ss -Hltn output')
    parser.add_argument('--port', type=int, action='append', help='Candidate listener port, repeatable (defaults: 3000 and 8080)')
    parser.add_argument('--config-path', type=Path, help='Reviewed local JSON inventory of public MongoDB queries')
    args = parser.parse_args()
    ports = set(args.port or [3000, 8080])
    if any(not 1 <= port <= 65535 for port in ports):
        parser.error('--port must be between 1 and 65535')
    affected = report_version(args.version_path)
    risky = review_inventory(args.config_path)
    report_listeners(args.ports_path, ports)
    if risky:
        print('Verdict: potential exposure. Restrict the flagged public queries and verify the deployed build.')
    elif risky is None:
        print('Verdict: exposure unknown. Inventory public MongoDB queries and restrict affected routes.')
    elif affected:
        print('Verdict: affected version. No risky queries identified in the supplied inventory. Upgrade and verify inventory coverage.')
    else:
        print('Verdict: no risky queries identified in the supplied inventory. Verify inventory coverage and patch status independently.')


if __name__ == '__main__':
    main()
