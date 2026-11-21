#!/usr/bin/env python3
"""Assess local Nexter Blocks Pro exposure without running WordPress or querying its database."""

import argparse
from pathlib import Path
import re
import subprocess


FIXED_VERSION = (5, 0, 11)
PLUGIN_HEADER = re.compile(r'^\s*(?:/\*+\s*|[*#]\s*)?Plugin Name:\s*(.+?)\s*$', re.MULTILINE | re.IGNORECASE)
VERSION_HEADER = re.compile(r'^\s*(?:/\*+\s*|[*#]\s*)?Version:\s*(\d+)\.(\d+)\.(\d+)\s*$', re.MULTILINE | re.IGNORECASE)


def plugin_version(plugin_dir):
    versions = set()
    for path in plugin_dir.glob('*.php'):
        with path.open('rb') as plugin_file:
            header = plugin_file.read(8192).decode('utf-8', errors='replace')
        name = PLUGIN_HEADER.search(header)
        if name and name.group(1).strip().casefold() == 'nexter blocks pro':
            version = VERSION_HEADER.search(header)
            versions.add(tuple(map(int, version.groups())) if version else None)
    return versions.pop() if len(versions) == 1 else None


def show_listeners():
    print('Local TCP listeners (bind addresses only; public reachability is unverified):', flush=True)
    try:
        return subprocess.run(['ss', '-ltn'], check=False, timeout=5).returncode == 0
    except (OSError, subprocess.TimeoutExpired) as error:
        print(f'Listener inventory unavailable: {error}')
        return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--wp-root', type=Path, help='Local WordPress root for one site')
    parser.add_argument('--plugin-dir', type=Path, help='Override the Nexter Blocks Pro directory for a custom layout')
    for setting in ('plugin-active', 'public-registration', 'public-nexter-block'):
        parser.add_argument(f'--{setting}', choices=('yes', 'no', 'unknown'), default='unknown',
                            help='Value verified from trusted local configuration or audit records for this site')
    args = parser.parse_args()
    listeners_ok = show_listeners()
    if args.plugin_dir is not None:
        plugin_dir = args.plugin_dir
    elif args.wp_root is not None and (args.wp_root / 'wp-includes' / 'version.php').is_file():
        plugin_dir = args.wp_root / 'wp-content' / 'plugins' / 'nexter-blocks-pro'
    else:
        print('VERDICT: UNKNOWN. Supply a local WordPress root or the exact plugin directory.')
        return 2

    print(f'Plugin directory: {plugin_dir}')
    try:
        plugin_dir.stat()
        version = plugin_version(plugin_dir)
    except FileNotFoundError:
        print('VERDICT: UNKNOWN. Expected plugin directory or file is missing. Check custom layouts and plugin slugs.')
        return 2
    except OSError as error:
        print(f'VERDICT: UNKNOWN. Could not read the plugin: {error}')
        return 2
    if version is None:
        print('VERDICT: UNKNOWN. Could not verify a stable version from plugin headers.')
        return 2

    print('Installed version:', '.'.join(map(str, version)))
    print(f'Active: {args.plugin_active}, public registration: {args.public_registration}, '
          f'public Nexter login/registration block: {args.public_nexter_block}')
    if version >= FIXED_VERSION:
        print('VERDICT: Installed version meets the reported 5.0.11 fix threshold.')
        return 0 if listeners_ok else 2
    conditions = (args.plugin_active, args.public_registration, args.public_nexter_block)
    if 'no' in conditions:
        print('VERDICT: Affected version installed. A reported prerequisite is absent according to the supplied configuration. Update the plugin.')
        return 0 if listeners_ok else 2
    if 'unknown' in conditions:
        print('VERDICT: POTENTIALLY EXPOSED. Affected version installed. Verify the unknown prerequisites and update the plugin.')
        return 2
    print('VERDICT: EXPOSURE PREREQUISITES PRESENT for the supplied site configuration. Update or disable the plugin and audit administrator changes.')
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
