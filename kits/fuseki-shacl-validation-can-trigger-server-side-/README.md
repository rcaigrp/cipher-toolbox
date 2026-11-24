# Fuseki SHACL Validation SSRF Defense Kit

This kit defends against CVE-2026-86155, a server-side request forgery (SSRF) vulnerability in Apache Jena Fuseki.
The flaw allows remote attackers to trigger outbound requests during SHACL validation, potentially leading to
internal network enumeration or access to restricted resources.

## Who is exposed

Systems running Apache Jena Fuseki versions 6.2.0 and earlier, especially those exposed to untrusted input
or internet-facing deployments.

## Files in this kit

- `check_exposure.sh`: Checks if this machine is running an affected version of Fuseki.
- `mitigate.sh`: Applies hardening steps (restricting outbound access).
- `detection/`: Detection rules for logs, network, and memory.
  - `sigma/ssrf_shacl_validation.yml`: Sigma rule for log-based detection
  - `yara/ssrf_shacl_validation.yar`: YARA rule for file/memory scanning
  - `suricata/ssrf_shacl_validation.rules`: Suricata/Snort rule for network detection
- `hunt.md`: Hunting queries for Splunk, KQL, and grep/jq to find signs of exploitation.