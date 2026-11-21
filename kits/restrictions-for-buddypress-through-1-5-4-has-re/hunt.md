# Hunting Queries for BuddyPress Restrict RCE

## Splunk SPL

```
index=wordpress_logs 
  | search "bp-restrict" 
  | where method="GET" AND url LIKE "%eval%" OR url LIKE "%assert%" OR url LIKE "%exec%" OR url LIKE "%system%" OR url LIKE "%passthru%"
  | stats count by client_ip, url, user_agent
```

## Microsoft KQL (Azure Sentinel)

```
WorkloadLogs
| where OperationName == "WebAppFirewall"
| where UriPath contains "bp-restrict"
| where RequestBody contains_any("eval", "assert", "exec", "system", "passthru")
| summarize count() by ClientIP, UriPath, UserAgent
```

## Grep/JQ for log files

```bash
# For Apache/Nginx logs
grep -i 'bp-restrict' /var/log/apache2/access.log | grep -E '(eval|assert|exec|system|passthru)'

# For WordPress debug logs (if enabled)
jq '.[] | select(.message | contains("bp-restrict")) | select(.message | contains("eval") or contains("assert") or contains("exec") or contains("system") or contains("passthru"))' /var/log/wordpress/debug.log
```

## Network-level hunting (Suricata/Snort)

```
alert tcp any any -> any 80 (msg:"Potential BuddyPress Restrict RCE Exploitation"; flow:established,to_server; content:"/wp-content/plugins/bp-restrict/"; nocase; content:"eval("; nocase; sid:2026120539; rev:1;)
```

## WordPress-specific hunting

```bash
# Check for vulnerable plugin versions in WordPress installation
wp plugin list --field=Name,Version | grep -E "(bp-restrict|buddypress)"
```