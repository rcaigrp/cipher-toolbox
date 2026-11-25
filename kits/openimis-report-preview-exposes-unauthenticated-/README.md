# openIMIS Report Preview RCE and File Read - Defensive Kit

This kit defends against CVE-2026-82489, a critical vulnerability in openIMIS that allows unauthenticated remote code execution (RCE) and arbitrary file read through the report preview module.

## Files

### Detection Rules
- `detection/sigma/openimis_rce_file_read.yml`: Sigma rule for web server logs
- `detection/yara/openimis_reportbro_preview.yar`: YARA rule for triage of artifacts
- `detection/suricata/openimis_preview.rules`: Suricata rule for network traffic
- `detection/splunk/openimis_rce_file_read.yml`: Splunk SPL query for access logs

### Hunt Queries
- `hunt.md`: Hunting queries for SIEM platforms

### Exposure Check
- `check_exposure.py`: Script to verify local deployment status

### Mitigation
- `mitigate.py`: Script to harden affected deployments with NGINX restrictions

## Usage

1. **Check exposure**: Run `check_exposure.py` on the target system to identify vulnerable deployments
2. **Deploy detection rules**: Load the Sigma, YARA, Suricata, and Splunk rules into your security infrastructure
3. **Hunt**: Use queries in `hunt.md` to search for past exploitation attempts
4. **Mitigate**: Run `mitigate.py` with `--apply` flag to create NGINX restrictions on affected services

## Important Notes

- All files must be customized with the actual preview path used in your deployment
- The Suricata rule requires replacing `$OPENIMIS_HTTP_SERVERS` and `$OPENIMIS_HTTP_PORTS`
- The Sigma and Splunk rules require replacing `OPENIMIS_PREVIEW_PATH` with the actual route
- The NGINX restriction is temporary and should be replaced by proper authentication once deployed

## Verification

All files have been tested:
- Sigma rule syntax validated
- YARA rule syntax confirmed valid
- Python scripts execute without error in dry-run mode