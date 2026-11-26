#!/usr/bin/env python3
"""Triage software inventory against local CISA KEV and NVD JSON snapshots."""

import argparse
import json
from pathlib import Path


def load_array(path, key=None):
    with path.open(encoding='utf-8') as stream:
        payload = json.load(stream)
    rows = payload.get(key) if key and isinstance(payload, dict) else payload
    if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
        raise ValueError(f'{path}: expected an array of objects' + (f' in {key}' if key else ''))
    return rows


def valid_cpe(cpe):
    # Escaped values and wildcard inventory identities require a full CPE matcher.
    if not isinstance(cpe, str) or '\\' in cpe or '?' in cpe:
        return False
    fields = cpe.split(':')
    return (
        len(fields) == 13 and fields[:2] == ['cpe', '2.3']
        and fields[2] in {'a', 'o', 'h'}
        and all(field and field not in {'*', '-'} for field in fields[3:6])
        and all('*' not in field or field == '*' for field in fields[6:])
    )


def triage(inventory, kev, nvd):
    components = {}
    for item in inventory:
        cpe = item['cpe']
        if not valid_cpe(cpe):
            raise ValueError(f'expected a CPE 2.3 with explicit vendor, product and version: {cpe!r}')
        fields = cpe.casefold().split(':')
        components.setdefault(tuple(fields[2:5]), set()).add(cpe)

    exploited = {row['cveID'] for row in kev}
    findings = {}
    for entry in nvd:
        cve = entry['cve']
        cve_id = cve['id']
        for configuration in cve.get('configurations', []):
            for node in configuration['nodes']:
                for match in node.get('cpeMatch', []):
                    if not match.get('vulnerable'):
                        continue
                    criteria = match['criteria']
                    fields = criteria.casefold().split(':')
                    if len(fields) != 13 or fields[:2] != ['cpe', '2.3'] or '\\' in criteria:
                        continue
                    for cpe in components.get(tuple(fields[2:5]), ()):
                        actual = cpe.casefold().split(':')
                        if any(expected != '*' and expected != observed and observed != '*'
                               for expected, observed in zip(fields[5:], actual[5:])):
                            continue
                        bounded = any(key.startswith(('versionStart', 'versionEnd')) for key in match)
                        exact = (
                            fields == actual and valid_cpe(criteria) and not bounded
                            and len(configuration['nodes']) == 1
                            and len(node['cpeMatch']) == 1
                            and configuration.get('operator', 'OR') == 'OR'
                            and node.get('operator', 'OR') == 'OR'
                            and not configuration.get('negate') and not node.get('negate')
                        )
                        key = (cve_id, cpe)
                        findings[key] = findings.get(key, False) or exact

    return [
        {'cve': cve_id, 'inventory_cpe': cpe, 'in_kev_snapshot': cve_id in exploited,
         'match': 'exact_cpe' if exact else 'review_applicability'}
        for (cve_id, cpe), exact in sorted(
            findings.items(), key=lambda item: (item[0][0] not in exploited, item[0])
        )
    ]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inventory', required=True, type=Path, help='JSON array of inventory objects with a cpe field')
    parser.add_argument('--kev', required=True, type=Path, help='Local CISA KEV catalog JSON')
    parser.add_argument('--nvd', required=True, type=Path, action='append', help='Local NVD CVE 2.0 JSON response or feed (repeatable)')
    args = parser.parse_args()
    try:
        inventory = load_array(args.inventory)
        kev = load_array(args.kev, 'vulnerabilities')
        nvd = [row for path in args.nvd for row in load_array(path, 'vulnerabilities')]
        print(json.dumps(triage(inventory, kev, nvd), indent=2))
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        parser.exit(1, f'{parser.prog}: {error}\n')


if __name__ == '__main__':
    main()
