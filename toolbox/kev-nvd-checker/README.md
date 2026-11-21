# KEV-NVD Checker

Triage a local software inventory using the CISA Known Exploited Vulnerabilities (KEV) catalog and NVD 2.0 applicability data. The checker reports candidates listed in KEV or with a maximum published CVSS base score of at least 7.0.

## Installation

Use Python 3.7 or later. The checker uses the standard library and needs no installation. Provide local, uncompressed copies of the KEV catalog and an NVD 2.0 feed or API response. The checker reads these files and prints JSON to stdout. It makes no network requests.

## Usage

From `toolbox/kev-nvd-checker`, run `python3 kev_nvd_checker.py --help` for options. Put one component per line in `inventory.txt` using `vendor:product:version` or `product:version`. Use NVD CPE vendor and product names for the best results. Blank lines and lines starting with `#` are ignored.

```text
example:widget:1.0
```

```bash
python3 kev_nvd_checker.py --inventory inventory.txt --kev kev.json --nvd nvd.json
```

The report lists each component with its candidate CVEs, KEV membership, maximum CVSS base score, and inventory match status. `matches` indicates that the checker matched the available inventory fields to a supported CPE criterion. `review` flags uncertainty such as an omitted vendor, an unsupported version comparison, or additional applicability conditions. Confirm candidates against vendor advisories before taking action. An empty candidate list means the checker found no matches in the supplied data. Coverage depends on the NVD files you supply, including all relevant API pages or feed years. KEV entries without matching NVD applicability data cannot be evaluated. Package aliases, backported fixes, and complex CPE conditions can require manual review.

## Tests

Run `python3 test.py`. The test runs the CLI with generated local fixtures and checks KEV membership, CVSS filtering, exact versions, an exclusive upper bound, vendor mismatches, and cases that require review.
