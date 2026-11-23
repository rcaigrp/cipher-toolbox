# Hunt for tournament API writes

Scope these searches to Tabbycat access logs. Use a normalized path with the query string removed. A match shows a write request. Correlate its time, request ID, status, and source with authenticated identity and tournament audit records. Prioritize unexplained 2xx responses and verify whether tournament, team, or speaker records changed. Preserve blocked requests for timeline review. The supplied investigation contains no incident indicators or memory signatures.

## Splunk SPL

Replace the index and field names with your access log mappings.

```spl
index=web_logs sourcetype=tabbycat_access http_method IN ("POST","PUT","PATCH","DELETE")
| where uri_path="/api/v1/tournaments" OR like(uri_path,"/api/v1/tournaments/%")
| table _time request_id clientip http_method uri_path status authenticated_user
```

## Microsoft KQL

Replace the example custom table and columns with your workspace mappings.

```kusto
TabbycatAccess_CL
| where HttpMethod in ("POST", "PUT", "PATCH", "DELETE")
| where UriPath == "/api/v1/tournaments" or UriPath startswith_cs "/api/v1/tournaments/"
| project TimeGenerated, RequestId, ClientIp, HttpMethod, UriPath, Status, AuthenticatedUser
```

## Local logs

Use grep for combined-format logs and jq for JSON Lines logs. Substitute the local file paths and JSON field names as needed.

```sh
grep -E '"(POST|PUT|PATCH|DELETE) /api/v1/tournaments([/?][^" ]*)? HTTP/[0-9.]+" [1-5][0-9]{2} ' access.log
jq -c 'select(((.method // "" | ascii_upcase) | IN("POST", "PUT", "PATCH", "DELETE")) and ((.uri // "") | test("^/api/v1/tournaments([/?]|$)")))' access.json
```
