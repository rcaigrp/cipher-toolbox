# Budibase public MongoDB query filter erasure

CVE-2026-137498 concerns a public Budibase MongoDB query losing its filter, potentially widening a read, update, or delete to the entire collection. Prioritize apps with public MongoDB queries that accept caller-controlled filter fields. Budibase lists releases below 4.0.0 as affected and 4.0.0 as patched. VulnCheck lists 3.39.18 through versions before 4.0.0. AnonHaven reports that 4.1.0 retains associated code. Exploitability in 4.1.0 and exploitation in the wild remain unconfirmed. [Vendor advisory](https://github.com/Budibase/budibase/security/advisories/GHSA-x4w8-596q-fmh7) · [VulnCheck](https://www.vulncheck.com/advisories/budibase-server-3.39.18-before-4.0.0-mongodb-filter-erasure-via-proto-keys) · [AnonHaven](https://anonhaven.com/en/budibase-mongodb-filter-erasure-proto-cve-2026-137498/) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-137498)

## check_exposure.py

Run `python3 check_exposure.py --help`. Check version and query configuration using local deployment evidence, and review local listeners. Treat missing inventory as unknown. A listening socket alone cannot establish public query access, and a 4.x version alone cannot resolve the 4.1.0 report.

## mitigate.py

Run `python3 mitigate.py --help`. Preview the restriction for a confirmed query route and review application impact before applying it. Restrict affected queries through every ingress, including direct access to the app listener. Upgrade according to vendor guidance when possible.

## Detection rules

Sigma rules (*.yml) for logs, YARA rules (*.yar) for files/memory, Suricata/Snort rules (*.rules) for network, hunt queries (Splunk SPL, Microsoft KQL, plain grep/jq) in hunt.md.

## hunt.md

Hunt queries for identifying public MongoDB queries with caller-controlled filter fields.