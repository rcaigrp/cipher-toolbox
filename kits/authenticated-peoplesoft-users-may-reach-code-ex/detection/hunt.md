# PeopleSoft registration activity hunt

Scope to PeopleSoft management logs. Map the request path, source, method and status fields to your schema. Replace `/register` with the locally verified route. The advisory names the operation and leaves the HTTP mapping unknown. Review route hits against approved peers and change windows, then correlate by host and time with service-account process launches, changes to deployed web files and unexpected peer connections. Route hits include routine traffic. Avoid collecting request bodies or credentials.

## Splunk SPL

```spl
index=peoplesoft_management
| where uri_path="/register" OR like(uri_path,"/register/%")
| bin _time span=15m
| stats count values(http_method) AS methods values(status) AS statuses by _time host src_ip uri_path
```

## Microsoft KQL

```kql
PeopleSoftManagement_CL
| where UriPath == "/register" or UriPath startswith_cs "/register/"
| summarize Requests=count(), Methods=make_set(HttpMethod), Statuses=make_set(Status) by bin(TimeGenerated, 15m), Computer, SourceIp, UriPath
```

## Local logs

For combined-format access logs and normalized newline-delimited JSON respectively:

```bash
grep -E '"[A-Z]+ /register([/?][^ ]*)? HTTP/[0-9.]+' -- access.log
jq -c 'select((.uri_path // "") | . == "/register" or startswith("/register/")) | {timestamp, host, src_ip, method, uri_path, status}' -- access.jsonl
```
