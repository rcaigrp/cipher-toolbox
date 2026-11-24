#!/usr/bin/env python3
"""Compare a local software inventory with CISA KEV and NVD 2.0 JSON."""

import argparse
import json
import re
from pathlib import Path


def load_records(path, key):
    with path.open(encoding='utf-8') as source:
        data = json.load(source)
    if not isinstance(data, dict) or not isinstance(data.get(key), list):
        raise ValueError(f'{path}: expected a JSON object with a {key} array')
    return data[key]


def read_inventory(path):
    with path.open(encoding='utf-8') as source:
        for number, line in enumerate(source, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            fields = [field.strip() for field in line.split(':')]
            if len(fields) not in (2, 3) or not all(fields):
                raise ValueError(f'{path}:{number}: expected [vendor:]product:version')
            yield (None, *fields) if len(fields) == 2 else tuple(fields)


def normalize(name):
    return re.sub(r'[\s_-]+', '_', name.casefold())


def numeric_version(version):
    if not re.fullmatch(r'[0-9]+(?:\.[0-9]+)*', version):
        return None
    return tuple(int(part) for part in version.split('.'))


def version_status(version, criterion, match):
    if criterion == '-':
        return 'review'
    if criterion != '*' and criterion.casefold() != version.casefold():
        return 'review' if re.search(r'[\\?*]', criterion) else None
    comparisons = {
        'versionStartIncluding': lambda value, bound: value >= bound,
        'versionStartExcluding': lambda value, bound: value > bound,
        'versionEndIncluding': lambda value, bound: value <= bound,
        'versionEndExcluding': lambda value, bound: value < bound,
    }
    current = numeric_version(version)
    status = 'matches'
    for key, compare in comparisons.items():
        if key not in match:
            continue
        bound_text = match[key]
        bound = numeric_version(bound_text)
        if version == bound_text:
            if not compare(0, 0):
                return None
        elif current is None or bound is None or len(current) != len(bound):
            status = 'review'
        elif not compare(current, bound):
            return None
    return status


def cpe_candidates(record):
    for configuration in record.get('configurations', []):
        nodes = configuration.get('nodes', [])
        for node in nodes:
            if configuration.get('negate') or node.get('negate'):
                continue
            conditional = configuration.get('operator') == 'AND' or node.get('operator') == 'AND'
            for match in node.get('cpeMatch', []):
                if not match.get('vulnerable'):
                    continue
                fields = re.split(r'(?<!\\):', match.get('criteria', ''))
                if len(fields) == 13 and fields[:2] == ['cpe', '2.3']:
                    vendor, product, version = fields[3:6]
                    constrained = conditional or any(field != '*' for field in fields[6:])
                    yield vendor, product, version, match, constrained


def build_report(inventory, kev_records, nvd_records):
    kev_ids = {entry['cveID'] for entry in kev_records}
    nvd_by_product = {}
    for entry in nvd_records:
        record = entry['cve']
        cve_id = record['id']
        if record.get('vulnStatus') == 'Rejected':
            continue
        metrics = record.get('metrics', {})
        scores = [
            metric['cvssData']['baseScore']
            for key in ('cvssMetricV40', 'cvssMetricV31', 'cvssMetricV30', 'cvssMetricV2')
            for metric in metrics.get(key, [])
        ]
        score = max(scores, default=None)
        if cve_id not in kev_ids and (score is None or score < 7):
            continue
        for vendor, product, criterion, match, constrained in cpe_candidates(record):
            nvd_by_product.setdefault(normalize(product), []).append(
                (vendor, criterion, match, constrained, cve_id, score)
            )

    report = []
    for vendor, product, version in inventory:
        matches = {}
        for cpe_vendor, criterion, match, constrained, cve_id, score in nvd_by_product.get(normalize(product), []):
            if vendor and cpe_vendor != '*' and normalize(vendor) != normalize(cpe_vendor):
                continue
            status = version_status(version, criterion, match)
            if status is None:
                continue
            if constrained or not vendor or cpe_vendor == '*':
                status = 'review'
            if cve_id not in matches or status == 'matches':
                matches[cve_id] = {
                    'cve_id': cve_id,
                    'in_kev': cve_id in kev_ids,
                    'cvss_max': score,
                    'inventory_match': status,
                }
        report.append({'vendor': vendor, 'product': product, 'version': version,
                       'candidates': [matches[key] for key in sorted(matches)]})
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inventory', type=Path, required=True, help='Text file with [vendor:]product:version rows')
    parser.add_argument('--kev', type=Path, required=True, help='Local CISA KEV catalog JSON')
    parser.add_argument('--nvd', type=Path, required=True, help='Local NVD 2.0 feed or API response JSON')
    args = parser.parse_args()
    try:
        report = build_report(list(read_inventory(args.inventory)),
                              load_records(args.kev, 'vulnerabilities'),
                              load_records(args.nvd, 'vulnerabilities'))
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        parser.exit(1, f'error: {error}\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
