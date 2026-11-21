#!/usr/bin/env python3
"""Stage a scripting-denial override for a native systemd SurrealDB service."""

import argparse
import os
from pathlib import Path
import re
import shlex
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--unit', default='surrealdb.service')
    parser.add_argument('--apply', action='store_true', help='Install the override without restarting the service')
    args = parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_.-]+\.service', args.unit) or args.unit.startswith(('-', '.')):
        parser.error('Provide a concrete system service name.')
    try:
        result = subprocess.run(['systemctl', 'cat', '--', args.unit], capture_output=True, text=True, timeout=5, check=True)
    except (OSError, subprocess.SubprocessError):
        if args.apply:
            parser.exit(1, 'Could not inspect the selected service. No changes made.\n')
        print('Dry run: selected systemd service unavailable. No changes planned.')
        return

    # Accept simple units only. Refuse existing drop-ins and ambiguous command lines.
    lines = result.stdout.splitlines()
    definitions = [line.strip().partition('=')[2].strip() for line in lines if re.match(r'^\s*ExecStart\s*=', line)]
    if sum(line.startswith('# /') for line in lines) != 1 or len(definitions) != 1:
        parser.exit(1, 'Review the unit manually: expected one unit file and one ExecStart.\n')
    command = definitions[0]
    if not re.fullmatch(r'/[A-Za-z0-9_./+-]+(?: +[A-Za-z0-9_./,:@=+\[\]-]+)+', command):
        parser.exit(1, 'Review the unit manually: ExecStart uses unsupported syntax.\n')
    tokens = shlex.split(command)
    if Path(tokens[0]).name not in {'surreal', 'surrealdb'} or tokens[1] != 'start':
        parser.exit(1, 'ExecStart must launch a native SurrealDB server directly.\n')
    flags = {token.split('=', 1)[0] for token in tokens[2:]}
    if flags & {'--allow-all', '--allow-scripting', '--'}:
        parser.exit(1, 'Review the existing capability flags manually before disabling scripting.\n')
    if '--deny-scripting' in tokens[2:]:
        print('The unit already specifies --deny-scripting. Verify the running process after activation.')
        return
    if '--deny-scripting' in flags:
        parser.exit(1, 'Review the existing scripting flag manually.\n')
    try:
        help_output = subprocess.run([tokens[0], 'start', '--help'], capture_output=True, text=True, timeout=5, check=True).stdout
    except (OSError, subprocess.SubprocessError):
        parser.exit(1, 'Could not verify the installed binary supports --deny-scripting.\n')
    if not re.search(r'^\s*--deny-scripting\s{2,}\S', help_output, re.MULTILINE):
        parser.exit(1, 'The installed binary did not advertise --deny-scripting as a standalone flag.\n')

    path = Path('/etc/systemd/system') / (args.unit + '.d') / '90-deny-scripting.conf'
    override = f'[Service]\nExecStart=\nExecStart={command} --deny-scripting\n'
    if args.apply:
        try:
            path.parent.mkdir(mode=0o755, exist_ok=True)
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(fd, 'w') as output:
                output.write(override)
        except OSError as error:
            parser.exit(1, f'Could not install override: {error}\n')
        print(f'Installed {path}.')
    else:
        print(f'Dry run: would add --deny-scripting to ExecStart in {path}.')
    print(f'Activation requires systemctl daemon-reload and a planned restart of {args.unit}.')
    print('After restart, run check_exposure.py and confirm the effective scripting policy. Upgrade to the reported fixed release, 4.0.0.')


if __name__ == '__main__':
    main()
