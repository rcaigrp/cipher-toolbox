#!/usr/bin/env python3
"""Inspect native SurrealDB executables, running servers, and local TCP listeners."""

import re
import shutil
import subprocess
from pathlib import Path

FIXED = (4, 0, 0)
FIRST_AFFECTED = (1, 0, 0)
STABLE_VERSION = re.compile(r'(?<!\S)v?(\d+)\.(\d+)\.(\d+)(?:\+[0-9A-Za-z.-]+)?(?=\s|$)')


def local_command(*command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, errors='replace', timeout=5)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return result.stdout if result.returncode == 0 else None


def version_verdict(executable):
    output = local_command(executable, '--version') or local_command(executable, 'version') or ''
    match = STABLE_VERSION.search(output)
    if match is None:
        return 'unknown stable version', 'manual review'
    version = tuple(map(int, match.groups()))
    label = '.'.join(map(str, version))
    if version >= FIXED:
        return label, 'at or above the reported fixed release'
    if version >= FIRST_AFFECTED:
        return label, 'in the reported affected range'
    return label, 'outside the reported range; verify support and exposure'


def scripting_policy(arguments):
    flags = {argument.split('=', 1)[0] for argument in arguments if argument.startswith('--')}
    allow = bool(flags & {'--allow-scripting', '--allow-all'})
    deny = bool(flags & {'--deny-scripting', '--deny-all'})
    if allow and deny:
        return 'conflicting capability flags; verify effective policy'
    if allow:
        return 'scripting allow flag present; prioritize review'
    if deny:
        return 'scripting deny flag present; verify effective policy'
    return 'unknown; verify service environment and deployment configuration'


def main():
    print('Local SurrealDB exposure check for CVE-2026-134292')
    executable = shutil.which('surreal')
    if executable:
        version, verdict = version_verdict(executable)
        print(f'PATH executable: {version} ({verdict})')
    else:
        print('No surreal executable found on PATH.')

    listeners = local_command('ss', '-H', '-ltnp')
    if listeners is None:
        print('Local TCP listener inspection unavailable.')
    servers = 0
    incomplete = False
    for process in Path('/proc').iterdir():
        if not process.name.isdecimal():
            continue
        try:
            if (process / 'comm').read_text(errors='replace').strip() not in {'surreal', 'surrealdb'}:
                continue
            args = (process / 'cmdline').read_bytes().decode(errors='replace').split('\0')
        except PermissionError:
            incomplete = True
            continue
        except OSError:
            continue
        if 'start' not in args[1:]:
            continue
        servers += 1
        print(f'Native server PID {process.name}')
        # Resolve the installed executable without reading or printing process environment values.
        try:
            running_executable = str((process / 'exe').resolve(strict=True))
        except OSError:
            running_executable = None
        version, verdict = version_verdict(running_executable) if running_executable else ('unknown version', 'manual review')
        print(f'  Version: {version} ({verdict})')
        print(f'  Scripting: {scripting_policy(args[1:])}')
        endpoints = []
        for line in (listeners or '').splitlines():
            fields = line.split()
            if len(fields) >= 5 and re.search(rf'\bpid={process.name}(?:,|\))', line):
                endpoints.append(fields[3])
        print(f'  Local TCP listeners: {", ".join(endpoints) or "none attributable with current visibility"}')
        if verdict == 'in the reported affected range':
            print('  Action: verify scripting policy and prioritize the 4.0.0 upgrade.')

    if not servers:
        print('Verdict: no native SurrealDB server identified in visible processes.')
    if incomplete:
        print('Process visibility was incomplete.')
    print('Coverage: PATH and visible native processes only. Review containers, embedded deployments, and effective configuration separately. A local listener does not establish remote reachability.')


if __name__ == '__main__':
    main()
