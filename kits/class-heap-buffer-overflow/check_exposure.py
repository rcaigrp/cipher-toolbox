#!/usr/bin/env python3
"""Inventory selected native attachment and media parsers on the local host."""

import shutil
import subprocess


PACKAGES = ("ytnef", "libytnef0", "libytnef0t64", "gpac", "gpac-modules-base", "ffmpeg", "libreoffice-core", "imagemagick")
EXECUTABLES = ("ytnef", "ytnefprint", "MP4Box", "ffmpeg", "soffice", "magick", "convert")


def main():
    print("Local inventory of selected native attachment and media parsers")
    dpkg_query = shutil.which("dpkg-query")
    package_inventory_ok = False
    if dpkg_query:
        try:
            result = subprocess.run(
                [dpkg_query, "-W", "-f=${db:Status-Abbrev}\t${Package}\t${Version}\n"],
                capture_output=True,
                text=True,
                check=True,
                timeout=15,
            )
        except (subprocess.SubprocessError, OSError) as error:
            print(f"Package inventory unavailable ({error})")
        else:
            package_inventory_ok = True
            installed = []
            for line in result.stdout.splitlines():
                status, package, version = line.split("\t", 2)
                if status.startswith("ii") and package in PACKAGES:
                    installed.append(f"{package} {version}")
            print("Matching Debian packages:")
            for entry in sorted(installed):
                print(f"  {entry}")
            if not installed:
                print("  None found in the local Debian package database.")
    else:
        print("Package inventory unavailable (dpkg-query missing).")

    print("Matching commands on PATH:")
    commands = [(name, shutil.which(name)) for name in EXECUTABLES]
    for name, path in commands:
        if path:
            print(f"  {name} {path}")
    if not any(path for _, path in commands):
        print("  None found on PATH.")

    print("Review whether mail gateways, preview services, and transcoders invoke these parsers on untrusted inputs.")
    print("Check their service accounts, sandbox boundaries, and write and network permissions.")
    print("Scope is the local Debian package database and current PATH. Container images, bundled libraries, and service reachability require separate inventory.")
    return 0 if package_inventory_ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
