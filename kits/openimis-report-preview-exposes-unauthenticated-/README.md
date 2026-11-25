# openIMIS report preview defensive kit

CVE-2026-82489 affects openIMIS suite releases before 2026-10. The report preview can allow unauthenticated remote code execution and arbitrary file read. Prioritize deployments that let untrusted clients reach preview through a proxy, ingress, or direct backend route. Block untrusted access and upgrade to 2026-10 or later. Public proof-of-concept availability and active exploitation remain unconfirmed. [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-82489) · [VulnCheck](https://www.vulncheck.com/advisories/openimis-2026-10-report-module-unauthenticated-rce-via-reportbro-preview)

## check_exposure.py

Run `python3 check_exposure.py --release YYYY-MM --port PORT --preview-access unknown` on the deployment host, replacing `YYYY-MM` and `PORT` with verified local values. Use `--release-file PATH` in place of `--release` to read a local file containing the suite release. Set `--preview-access` to `restricted` or `untrusted` if you have verified the policy. The script reads local TCP listener state with `ss` in its own network namespace. Review proxy, container ingress, and direct backend access to establish reachability. Exit codes are `0` for a fixed release, `1` for an affected release, and `2` for unknown release evidence or invalid arguments.

## mitigate.py

Run `python3 mitigate.py --output ./openimis-preview-deny.conf` to preview an NGINX `deny all` snippet. Add `--apply` to stage it at a new path. Include the snippet in the affected openIMIS NGINX location. This snippet denies all clients wherever it is included.

## Detection

Sigma rules for webserver logs, YARA rules for files/memory, and Suricata/Snort rules for network traffic. Hunt queries are provided for Splunk and Microsoft Sentinel.

- `detection/sigma/openimis_rce_file_read.yml`: Sigma rule for detecting unauthenticated access to the report preview endpoint
- `detection/yara/openimis_reportbro_preview.yar`: YARA rule for identifying openIMIS ReportBro preview context in files or memory
- `detection/suricata/openimis_preview.rules`: Suricata rule for detecting requests to the preview endpoint
- `detection/splunk/openimis_rce_file_read.yml`: Splunk-specific Sigma rule variant (converted from main rule)

## Hunt

Queries to search logs for unauthenticated access to the report preview endpoint:
- `hunt.md`: Examples for Splunk SPL, Microsoft Sentinel KQL, and local JSON log parsing