# Fuseki SHACL Validation SSRF Defensive Kit

This kit defends against CVE-2026-86155, a server-side request forgery (SSRF) vulnerability in Apache Jena Fuseki.
The flaw allows untrusted input during SHACL validation to trigger outbound requests from the server,
potentially leading to internal network reconnaissance or exploitation of other services.

## Files

- `check_exposure.sh`: Checks if this machine is running vulnerable Fuseki versions or has risky configurations
- `mitigate.sh`: Applies hardening/workaround steps, such as restricting outbound access
- `detection/sigma/ssrf_shacl_validation.yml`: Sigma rules for detecting SSRF attempts in logs
- `detection/yara/ssrf_shacl_validation.yar`: YARA rules for detecting malicious patterns in memory/files
- `detection/suricata/ssrf_shacl_validation.rules`: Suricata/Snort network rules to detect SSRF traffic
- `hunt.md`: Hunting queries for identifying vulnerable configurations or past exploitation attempts

## Who is exposed?

Systems running Apache Jena Fuseki versions 6.2.0 and earlier, especially those exposed to untrusted input or
accessible from the internet.

## How to use

Run `check_exposure.sh` to see if this system is vulnerable.
Run `mitigate.sh` with `--apply` to apply hardening steps.
Use detection rules in your SIEM/IDS/IPS for monitoring.
Use hunt queries to look for past exploitation or misconfigurations.