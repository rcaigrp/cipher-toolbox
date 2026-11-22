#!/usr/bin/env python3
"""Inventory local parser exposure without connecting to services."""
import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess


def command(*args):
    try:
        result = subprocess.run(args, capture_output=True, text=True, timeout=5, check=True)
        return result.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return None


def version(text):
    match = re.fullmatch(r'v?(\d+)\.(\d+)\.(\d+)(?:\+[^\s]+)?', text)
    return tuple(map(int, match.groups())) if match else None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', action='append', type=Path, help='Local Composer project, repeatable. Defaults to the current directory.')
    parser.add_argument('--unit', action='append', default=[], help='Local systemd parser service to inspect, repeatable.')
    args = parser.parse_args()
    findings = set()

    def report(status, message):
        findings.add(status)
        print(f'[{status}] {message}')

    for root in args.project or [Path.cwd()]:
        metadata = root / 'vendor/composer/installed.json'
        try:
            data = json.loads(metadata.read_text())
            packages = data if isinstance(data, list) else data['packages']
            package = next((item for item in packages if item['name'] == 'zbateson/mail-mime-parser'), None)
            if package is None:
                report('INFO', f'{root}: MIME parser absent from installed Composer metadata')
                continue
            raw = package['version']
            parsed = version(raw)
            if parsed is None:
                status = 'UNKNOWN'
            elif (2, 0, 0) <= parsed < (3, 0, 6) or (4, 0, 0) <= parsed < (4, 0, 2):
                status = 'AFFECTED'
            else:
                status = 'INFO'
            report(status, f'{root}: zbateson/mail-mime-parser {raw}')
        except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
            report('UNKNOWN', f'{metadata}: {error}')

    mailpit = shutil.which('mailpit')
    if mailpit:
        output = command(mailpit, '--version') or ''
        match = re.search(r'(?im)^\s*(?:mailpit\s+(?:version\s+)?)?(v?\d+\.\d+\.\d+(?:[-+][^\s]+)?)(?=\s|$)', output)
        parsed = version(match[1]) if match else None
        status = 'UNKNOWN' if parsed is None else 'AFFECTED' if parsed < (1, 30, 4) else 'INFO'
        report(status, f'Mailpit on PATH at {mailpit}: {match[1] if match else "version unavailable"}')
    else:
        report('UNKNOWN', 'Mailpit absent from PATH. Check service deployments and container images separately.')

    props = ('LoadState', 'User', 'DynamicUser', 'NoNewPrivileges', 'PrivateNetwork', 'IPAddressDeny', 'IPAddressAllow', 'CPUQuotaPerSecUSec', 'MemoryMax', 'TasksMax')
    if not args.unit:
        report('UNKNOWN', 'No parser service specified. Supply --unit for each systemd worker.')
    for unit in args.unit:
        output = command('systemctl', 'show', '--property=' + ','.join(props), '--', unit)
        settings = dict(line.split('=', 1) for line in (output or '').splitlines() if '=' in line)
        if settings.get('LoadState') != 'loaded':
            report('UNKNOWN', f'{unit}: unable to read a loaded system service')
            continue
        print(f'{unit}: ' + ', '.join(f'{key}={settings.get(key, "unavailable")}' for key in props[1:]))
        if settings.get('User') in ('', 'root', '0', None) and settings.get('DynamicUser') != 'yes':
            report('REVIEW', f'{unit}: no non-root service identity confirmed')
        if settings.get('PrivateNetwork') != 'yes':
            report('REVIEW', f'{unit}: verify effective default-deny egress and any exceptions')
        for key in ('CPUQuotaPerSecUSec', 'MemoryMax', 'TasksMax'):
            if settings.get(key) in (None, '', 'infinity', '[not set]', '18446744073709551615'):
                report('REVIEW', f'{unit}: no finite {key} visible')

    listeners = command('ss', '-H', '-lntup')
    if listeners is None:
        report('UNKNOWN', 'Local socket inventory unavailable')
    else:
        for line in listeners.splitlines():
            columns = line.split()
            if len(columns) < 5:
                continue
            address = columns[4]
            host, _, port = address.rpartition(':')
            if 'mailpit' in line.lower() or port in {'1025', '8025'}:
                loopback = host.startswith('127.') or host in ('[::1]', '::1')
                report('INFO' if loopback else 'REVIEW', f'Candidate Mailpit listener: {line}')
        print('Socket coverage: current network namespace, Mailpit process names and candidate ports 1025/8025. Process ownership may require elevated visibility.')

    if 'AFFECTED' in findings:
        print('Verdict: affected version detected.')
        return 1
    if findings & {'UNKNOWN', 'REVIEW'}:
        print('Verdict: exposure unresolved or configuration needs review.')
        return 2
    print('Verdict: no affected version found in inspected scope.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
