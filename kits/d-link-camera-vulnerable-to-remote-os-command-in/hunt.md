# Hunt Queries for D-Link DCS-935L Command Injection

## Splunk SPL

```
index=web_logs 
  [ search index=web_logs uri="/cgi-bin/localrecording/setconf.cgi" 
    earliest=-24h 
    | stats count by client_ip, user_agent, request_body 
    | where count > 1 ]
  | stats count by client_ip, user_agent, request_body
```

## Microsoft KQL (Log Analytics)

```
WebLogs
| where UriPath == "/cgi-bin/localrecording/setconf.cgi"
| summarize count() by ClientIP, UserAgent, RequestBody
| where count_ > 1
```

## grep/jq for log files

```bash
# For text logs
grep "/cgi-bin/localrecording/setconf.cgi" /var/log/nginx/access.log | grep -E "(;|&|\|\||\|)" 

# For JSON logs with jq
jq '.uri == "/cgi-bin/localrecording/setconf.cgi" and (.request_body | contains(";") or .request_body | contains("&"))' access.json
```

## Example query for finding repeated patterns

```bash
grep -E "(;|&|\|\||\|)" /var/log/nginx/access.log | grep "/cgi-bin/localrecording/setconf.cgi"
```