# D-Link DCS-935L Command Injection Defense Kit

This kit provides defensive measures against CVE-2026-133680, a critical remote OS command injection vulnerability in D-Link DCS-935L cameras.

## What This Kit Contains

- **Detection rules** for logs, network traffic, and memory/files
- **Hunt queries** to find evidence of exploitation attempts
- **Exposure check script** to verify if this system is exposed to the vulnerability
- **Mitigation script** with hardening steps (dry-run by default)

## Who Is Exposed

Systems running D-Link DCS-935L firmware version 1.10.01 or earlier, especially those with internet-exposed web management interfaces.

## How to Use

1. Run `check_exposure.sh` to see if your system is affected
2. Use detection rules in your SIEM for monitoring
3. Run `mitigate.sh` with `--apply` flag to apply mitigations (dry-run by default)
4. Search logs using hunt queries for signs of exploitation attempts
