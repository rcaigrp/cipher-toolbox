# Hunting Queries for NCIC Breach

## Splunk SPL Query
```
index=main sourcetype=authentication Service="ncic_gateway" Outcome="success" SourceApproved=false
| stats count by Account, SourceIp, Gateway
```

## Microsoft KQL Query
```
SecurityEvent
| where EventID == 4624 and Service contains "ncic_gateway" and Outcome == "success"
| summarize count() by Account, IpAddress, Service
```

## Plain grep/jq Query
```bash
# Check for NCIC-related log entries with successful access
grep -i 'ncic_gateway' /var/log/auth.log | grep -i 'success'
```