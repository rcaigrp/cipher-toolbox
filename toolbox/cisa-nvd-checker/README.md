# CISA NVD Checker

Triage software inventory against local NVD CVE 2.0 JSON snapshots and flag findings listed in a local CISA Known Exploited Vulnerabilities (KEV) snapshot. The checker reads local files and writes JSON to standard output. It makes no network requests.

## Install

Use Python 3. No third-party packages are required.

## Usage

From `toolbox/cisa-nvd-checker/`, run:

```bash
python3 cisa_nvd_checker.py --help
python3 cisa_nvd_checker.py --inventory inventory.json --kev kev.json --nvd nvd.json
```

Repeat `--nvd` to include additional snapshots. Each snapshot must contain a top-level `vulnerabilities` array. The inventory must be a JSON array of objects with a `cpe` field. Supply a CPE 2.3 with an explicit vendor, product, and version for each component. For example:

```json
[
  {"cpe": "cpe:2.3:a:example_vendor:example_editor:4.15.2:*:*:*:*:*:*:*"}
]
```

## Interpret the results

- `exact_cpe` means the inventory CPE equals a single, unbounded vulnerable criterion in a simple NVD configuration.
- `review_applicability` means the tool found a candidate criterion. Review version bounds, platform details, and configuration conditions against the advisory before acting.
- `in_kev_snapshot` records whether the CVE ID appears in the supplied KEV snapshot. KEV entries need a matching NVD criterion to appear in the results. Findings listed in KEV sort first.

Coverage depends on the snapshots and inventory. The checker skips escaped CPE criteria and does not fully evaluate CPE wildcards, version ranges, or Boolean applicability conditions. An empty result does not establish that a component is safe.

## Example and tests

The included fixtures use synthetic advisory IDs and component names.

```bash
python3 cisa_nvd_checker.py --inventory test_inventory.json --kev test_kev.json --nvd test_nvd.json
python3 test_checker.py
```

The tests cover exact and review-needed findings, KEV membership, an unmatched component, a missing snapshot, and `--help`.
