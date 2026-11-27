# Budibase public MongoDB query filter erasure

CVE-2026-137498 concerns a public Budibase MongoDB query losing its filter, potentially widening a read, update, or delete to the entire collection. Prioritize apps with public MongoDB queries that accept caller-controlled filter fields. Budibase lists releases below 4.0.0 as affected and 4.0.0 as patched. VulnCheck lists 3.39.18 through versions before 4.0.0. AnonHaven reports that 4.1.0 retains associated code. Exploitability in 4.1.0 and exploitation in the wild remain unconfirmed. [Vendor advisory](https://github.com/Budibase/budibase/security/advisories/GHSA-x4w8-596q-fmh7) · [VulnCheck](https://www.vulncheck.com/advisories/budibase-server-3.39.18-before-4.0.0-mongodb-filter-erasure-via-proto-keys) · [AnonHaven](https://anonhaven.com/en/budibase-mongodb-filter-erasure-proto-cve-2026-137498/) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-137498)

## check_exposure.py

Run `python3 check_exposure.py --help`. Check version and query configuration using local deployment evidence, and review local listeners. Treat missing inventory as unknown. A listening socket alone cannot establish public query access, and a 4.x version alone cannot resolve the 4.1.0 report.

## mitigate.py

Run `python3 mitigate.py --help`. Preview the restriction for a confirmed query route and review application impact before applying it. Restrict affected queries through every ingress, including direct access to the app listener. Upgrade according to the vendor advisory and keep restrictions in place until the deployed build and query configuration are verified.

## budibase-mongodb.yml

Run the Sigma rule against normalized records that combine public query attribution with MongoDB operation telemetry. Alert when an operation expected to have a filter reaches MongoDB with an empty filter. Investigate affected records and distinguish intentionally unfiltered operations using the query inventory.

## budibase-mongodb.yar

Run the YARA rule against exported configuration or telemetry and inspect each match in context. It looks for indicators in the kit's normalized data format. A match can come from sample data or unrelated objects in the same file. It does not classify a Budibase binary as vulnerable or establish exploitation.

## budibase-mongodb.rules

Load the Suricata rule on a sensor that can inspect plaintext traffic for the query route you have inventoried. Use alerts to correlate access with database operations. Network requests alone cannot establish that the effective database filter was lost.

## hunt.md

Use the SPL, KQL, and shell examples after mapping your records to the documented fields. Prioritize unexpected writes and deletes, then review wide reads. If database telemetry lacks request correlation, record the result as an unattributed lead.

## Prepare now

Inventory public MongoDB queries and their permitted operations. Enforce required filters server-side, reject missing or empty filters where scope is required, and give each application database identity only the operations and collections it needs. Review other public endpoints that transform caller input into database predicates for the same scope-loss pattern.
