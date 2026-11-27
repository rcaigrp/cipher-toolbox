# Hunt for Budibase public query filter erasure (CVE-2026-137498)

## Splunk SPL

```
index=main sourcetype=budibase 
| where operation IN ("find", "update", "delete")
| where isnull(filter) OR match(filter, "^\s*[{]\s*[}]\s*$")
| eval filter=coalesce(filter, "<missing>")
| stats count by query_id, operation, filter
```

## Microsoft KQL

```
budibase_logs
| where isempty(tostring(filter)) or replace_regex(tostring(filter), @"\s+", "") == "{}"
| where operation in ("find", "update", "delete")
| project timestamp, query_id, operation, filter
```

## Shell/Grep

```bash
# Hunt for unfiltered operations in log files
grep -rE '"operation"[[:space:]]*:[[:space:]]*"(find|update|delete)"' /var/log/budibase/ |
  grep -E '"filter"[[:space:]]*:[[:space:]]*("[{][[:space:]]*[}]"|[{][[:space:]]*[}]|null)'
```

## jq

```bash
# If logs are in JSON format
jq -c 'select(.operation == "find" or .operation == "update" or .operation == "delete")
  | select(.filter == {} or .filter == null or
      ((.filter | type) == "string" and (.filter | gsub("[[:space:]]"; "")) == "{}"))
  | {query_id, operation, filter}' /var/log/budibase/*.log
```

## Notes

- Map `operation`, `filter`, and `query_id` to telemetry for the effective MongoDB operation. Correlate query IDs with the public-query inventory and confirm that the query requires a filter. The grep example covers explicit empty or null filters in single-line JSON. The jq example also includes missing fields. Missing fields can reflect logging configuration.
- Filtered operations should have a non-empty filter field.
- Correlate with query IDs to determine if they are public and potentially exploitable.
- The presence of an empty filter alone does not confirm exploitation, but it is a suspicious indicator.
