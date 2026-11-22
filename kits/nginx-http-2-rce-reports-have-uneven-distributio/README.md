# nginx HTTP/2 exposure and worker crash triage

Prioritize public listeners where nginx terminates client HTTP/2 and the running build lacks verified fixes for CVE-2026-123007 and CVE-2026-123633. The supplied CVE records describe ASLR disabled or bypassed as a condition for code execution. CVE-2026-123633 also requires backend proxying and low worker connection availability. Public PoCs and in-the-wild exploitation are unconfirmed in the supplied material.

Match the running binary to its package origin, release and stream. The supplied material gives upstream fixed builds 1.30.7 and 1.31.9 and reported Debian floors 1.22.1-9+deb12u11 for Debian 12 and 1.26.3-3+deb13u11 for Debian 13. Confirm Debian 12 coverage against DLA-4918-1. For Ubuntu consult USN-9159-1. For RHEL 10 consult RHSA-2026:100744. RHEL 8 and 9 fixes are reported, with exact stream builds and coverage of both CVEs still to confirm. [Distribution report](https://seclists.org/oss-sec/2026/q4/791) · [Patch tracker](https://ma.ttias.be/nginx-http2-cve-2026-123633-123007/) · [Upstream advisories](https://nginx.org/en/security_advisories.html) · [Ubuntu notice](https://ubuntu.com/security/notices/USN-9159-1) · [Red Hat advisory](https://access.redhat.com/errata/RHSA-2026:100744)

## Sigma

`detection/sigma/nginx_http2_heap_overflow.yml` flags nginx worker exits on SIGSEGV. Map the raw nginx error log to `message` and correlate alerts with the listener inventory and package status. Other worker crashes produce the same signal.

## YARA

`detection/yara/nginx_http2_rce.yar` matches the nginx worker SIGSEGV message in retained logs or memory artifacts containing that text. Use it for artifact triage. A match establishes crash telemetry only.

## Suricata

`detection/suricata/nginx_http2_heap_overflow.rules` identifies the normal cleartext HTTP/2 prior-knowledge preface for exposure inventory. Restrict the monitored destination to nginx ingress and expect alerts on legitimate traffic. TLS and HTTP/1.1 upgrades require separate inventory evidence. Run `suricata -T -S detection/suricata/nginx_http2_heap_overflow.rules` with the sensor configuration before deployment.

## Hunts

`hunt.md` contains Splunk, Microsoft KQL and local grep/jq searches for worker crashes, plus instructions for correlating them with ingress inventory.

## Exposure check

Run `python3 -B check_exposure.py` on the nginx host. It reads package ownership, compares package versions for supported Debian releases, inspects common nginx configuration paths and lists local TCP sockets. Confirm active includes, running workers, container namespaces and public reachability against your inventory. For package origins without an applicable Debian floor, verify both CVEs manually against the relevant advisory.

## Mitigation

Run `python3 -B mitigate.py /path/to/selected.conf` to preview disabling `http2 on` and removing the legacy `http2` option from `listen` directives. The script processes all supported enabling directives in each selected file, including shared settings. Review the diff and affected virtual hosts before using `--apply`. Apply validates the default nginx configuration and attempts to restore originals if validation fails. Reload the intended instance after validation and verify that client HTTP/2 is disabled for the affected listeners. Account for clients that require HTTP/2 before reloading.

## Prepare now

For HTTP/2 worker memory corruption, inventory other ingress tiers that terminate HTTP/2, keep ASLR enabled, minimize worker privileges, and alert on repeated worker SIGSEGV exits. Patch confirmed exposures first and use the HTTP/2 workaround while package coverage is unclear.
