# Hunting for Fuseki SHACL SSRF (CVE-2026-86155)

This document contains hunting queries to detect vulnerable configurations or past exploitation attempts.

## Splunk SPL

```
index=your_fuseki_logs 
  | where 'SHACL validation request to' OR 'Fetching remote resource during SHACL'
  | stats count by user, ip, url
  | where count > 10
```

## Microsoft KQL (Log Analytics)

```
FusekiLogs
| where Message contains "SHACL validation request to" or Message contains "Fetching remote resource during SHACL"
| summarize Count = count() by User, Ip, Url
| where Count > 10
```

## Bash/grep/jq

```bash
# Check logs for patterns (adjust path as needed)
grep -r "SHACL validation request to" /var/log/fuseki/ 2>/dev/null || echo "No SHACL requests found"
grep -r "Fetching remote resource during SHACL" /var/log/fuseki/ 2>/dev/null || echo "No remote fetches found"
```

## Configuration Check

Check for Fuseki configurations that allow remote resources:

```bash
# Find fuseki config files (common locations)
find /etc -name "*fuseki*" -type f 2>/dev/null
find /opt -name "*fuseki*" -type d 2>/dev/null
```

## Version Check

Check if Fuseki is installed and what version:

```bash
# Check version if fuseki-server is available
fuseki-server --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+'
```