#!/usr/bin/env python3
"""Audit a local inventory of server-side URL fetchers without network access."""

import argparse
import json
from pathlib import Path
import sys


CONTROLS = {
    "destination_allowlist": "Restrict destinations to approved hosts or services.",
    "http_https_only": "Restrict the fetcher to HTTP and HTTPS.",
    "connect_address_policy": "Enforce the destination address policy on the actual connection, including IPv6.",
    "redirect_policy": "Disable redirects or apply the full destination policy to each redirect.",
    "egress_isolation": "Enforce network egress restrictions independently of application validation.",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inventory", type=Path, help="local JSON file containing a list of fetcher records")
    args = parser.parse_args()

    try:
        records = json.loads(args.inventory.read_text(encoding="utf-8"))
        if not isinstance(records, list) or not records:
            raise ValueError("expected a nonempty list of fetcher records")
        names = set()
        for index, record in enumerate(records, start=1):
            if not isinstance(record, dict):
                raise ValueError(f"record {index} must be an object")
            name = record.get("name")
            if not isinstance(name, str) or not name.strip() or not name.isprintable():
                raise ValueError(f"record {index} requires a printable, nonempty name")
            if name in names:
                raise ValueError(f"record {index} repeats a fetcher name")
            names.add(name)
            unknown_fields = record.keys() - {"name", "untrusted_url", *CONTROLS}
            if unknown_fields:
                raise ValueError(f"record {index} has unknown fields: {sorted(unknown_fields)!r}")
            for field in ("untrusted_url", *CONTROLS):
                value = record.get(field)
                if value is not None and not isinstance(value, bool):
                    raise ValueError(f"record {index} field {field} must be true, false, or null")
    except (OSError, ValueError) as error:
        print(f"Inventory error: {error}", file=sys.stderr)
        return 2

    findings = 0
    for record in records:
        name = record["name"]
        untrusted = record.get("untrusted_url")
        if untrusted is False:
            print(f"{name}: inventory reports no untrusted URL input")
            continue
        if untrusted is None:
            print(f"{name}: unknown URL input trust; review callers and configuration sources")
            findings += 1
        for field, guidance in CONTROLS.items():
            value = record.get(field)
            if value is not True:
                state = "missing" if value is False else "unknown"
                print(f"{name}: {field} {state}. {guidance}")
                findings += 1

    print(f"{len(records)} fetcher(s) reviewed, {findings} finding(s). Results reflect the supplied inventory.")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
