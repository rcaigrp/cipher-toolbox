#!/usr/bin/env python3
"""Plan or apply the local Nexter Blocks Pro disablement workaround."""

import argparse
from pathlib import Path

from check_exposure import FIXED_VERSION, plugin_version


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plugin-dir', required=True, type=Path,
                        help='Exact local directory containing Nexter Blocks Pro')
    parser.add_argument('--apply', action='store_true',
                        help='Move the affected plugin out of the WordPress plugins directory')
    args = parser.parse_args()
    plugin_dir = args.plugin_dir.absolute()
    if plugin_dir.parent.name != 'plugins' or plugin_dir.is_symlink():
        parser.error('Supply a real plugin directory directly under a local plugins directory.')
    destination = plugin_dir.parent.parent / (plugin_dir.name + '.disabled-cve-2026-125294')

    try:
        if not plugin_dir.exists() and destination.is_dir() and not destination.is_symlink():
            if (version := plugin_version(destination)) is not None and version < FIXED_VERSION:
                print(f'Affected plugin already moved to {destination}. Verify site behavior.')
                return 0
        version = plugin_version(plugin_dir)
        if version is None:
            print('Could not verify the Nexter Blocks Pro version. Confirm the directory and installed version.')
            return 2
        if version >= FIXED_VERSION:
            print('Installed version meets the reported 5.0.11 fix threshold.')
            return 0
        if destination.exists() or destination.is_symlink():
            print(f'Destination already exists: {destination}')
            return 2

        print('Preferred remediation is updating to 5.0.11 or a newer patched release. Audit administrator changes across the exposure window.')
        if not args.apply:
            print(f'DRY RUN: Would move {plugin_dir} to {destination}. Nexter features may stop working on sites that share this installation.')
            return 0
        plugin_dir.rename(destination)
    except OSError as error:
        print(f'Could not complete mitigation: {error}')
        return 2

    print(f'Moved {plugin_dir} to {destination}. Verify WordPress no longer loads the plugin and check affected pages.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
