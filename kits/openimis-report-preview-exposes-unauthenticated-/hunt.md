# Hunt for openIMIS report preview access

Scope the hunt to logs for the affected deployment. Replace `OPENIMIS_PREVIEW_PATH` with the exact normalized path recorded by your own ingress. The examples assume the path excludes the query string. Map the example fields to your log schema. Use the authentication result recorded by trusted ingress, and treat missing authentication data as unknown.

## Splunk SPL

```spl
index=web_logs earliest=-24h uri_path="OPENIMIS_PREVIEW_PATH"
| eval auth_state=coalesce(auth_state,"unknown")
| where auth_state="unauthenticated" OR auth_state="unknown"
| fillnull value=unknown src_ip status
| stats count min(_time) AS first_seen max(_time) AS last_seen BY src_ip auth_state status
| sort - count
```

## Microsoft Sentinel KQL

Replace `WebEvents` and the column names with the table and fields used by your connector.

```kusto
WebEvents
| where TimeGenerated >= ago(24h)
| where UriPath == "OPENIMIS_PREVIEW_PATH"
| extend AuthResult = iff(isempty(AuthState), "unknown", AuthState)
| where AuthResult in ("unauthenticated", "unknown")
| summarize Requests=count(), FirstSeen=min(TimeGenerated), LastSeen=max(TimeGenerated) by SrcIp, AuthResult, StatusCode
| order by Requests desc
```

## Local logs

For JSON Lines logs, set `preview_path` to the verified path and adjust the field names as needed.

```bash
preview_path='OPENIMIS_PREVIEW_PATH'
jq -c --arg path "$preview_path" '
  select(.uri_path == $path)
  | .auth_state |= (if . == null or . == "" then "unknown" else . end)
  | select(.auth_state == "unauthenticated" or .auth_state == "unknown")
  | {timestamp, src_ip, auth_state, status, request_id}
' access.jsonl
```

For text logs, use a fixed-string search to find candidate lines, then verify the request path and authentication result against the log format.

```bash
grep -Fn -- "$preview_path" access.log
```

## Triage and preparation

Review individual requests as well as bursts. Prioritize requests that ingress forwarded upstream, including requests that returned errors. Correlate request IDs and timestamps with application logs and host telemetry. Look for unexpected child processes of the report service and file access outside its expected report and template directories where telemetry is available. A preview request or a successful HTTP response alone does not establish exploitation.

Prepare now by recording the verified preview route and ingress authentication outcome, retaining request IDs across the proxy and backend, and identifying every ingress path to the deployment. Block untrusted access and upgrade affected deployments to 2026-10 or later. Review other report-rendering services for anonymous access and constrain their filesystem permissions and process privileges.
