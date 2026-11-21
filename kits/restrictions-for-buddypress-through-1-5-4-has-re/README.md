# Restrictions for BuddyPress RCE Defense Kit

This kit defends against CVE-2026-120539, an unauthenticated remote code execution vulnerability in the BuddyPress Restrict plugin versions through 1.5.4.

## Exposure

WordPress sites using:
- BuddyPress plugin
- Paid Memberships Pro plugin
- BuddyPress Restrict plugin version 1.5.4 or earlier
- Internet-facing installations

## Files

- `check_exposure.sh`: Checks if this machine is exposed to the vulnerability
- `mitigate.sh`: Applies hardening/workarounds (dry-run by default)
- `detection/sigma/bp_restrict_rce.yml`: Sigma rule for log-based detection
- `detection/yara/bp_restrict_rce.yar`: YARA rule for file/memory scanning
- `hunt.md`: Hunting queries for Splunk, KQL, and grep/jq