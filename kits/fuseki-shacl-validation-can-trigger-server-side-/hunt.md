# Hunt Queries for Fuseki SHACL SSRF (CVE-2026-86155)

## Splunk SPL

```
index=your_fuseki_logs sourcetype=fuseki "shacl" "http://" OR "https://"
| stats count by src_ip, dest_ip, url
```

## Microsoft KQL (Log Analytics)

```
FusekiLogs
| where Url contains "/shacl" and (Url contains "http://" or Url contains "https://")
| summarize count() by SrcIp, DestIp, Url
```

## grep/jq for log files

```bash
# Example for JSON logs
grep -E '"/shacl".*(http|https)://' /var/log/fuseki.log | jq '.src_ip, .dest_ip'
```