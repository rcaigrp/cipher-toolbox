# SurrealDB scripting policy hunts

Search SurrealDB application and audit logs for messages mentioning scripting alongside a capability or permission decision. Map the examples to your ingestion fields. Review individual events and baseline expected startup messages and routine denials by host. A match is a triage lead. The supplied advisories establish no confirmed indicators or vendor log formats.

## Splunk SPL

```spl
index=surrealdb_logs
| eval policy_text=lower(coalesce(message, _raw))
| where like(policy_text, "%scripting%") AND (like(policy_text, "%capability%") OR like(policy_text, "%permission%") OR like(policy_text, "%denied%") OR like(policy_text, "%disabled%"))
| table _time host policy_text
```

## Microsoft KQL

```kql
SurrealDBLogs
| where tostring(Message) contains "scripting"
| where tostring(Message) contains "capability" or tostring(Message) contains "permission" or tostring(Message) contains "denied" or tostring(Message) contains "disabled"
```

## Plain text and JSON logs

```bash
grep -iF 'scripting' surrealdb.log | grep -Ei 'capability|permission|denied|disabled'
jq -c 'objects | select((.message // "" | tostring) | test("scripting"; "i") and test("capability|permission|denied|disabled"; "i"))' surrealdb.jsonl
```

Correlate unexpected decisions with deployment versions, scripting policy changes, and application request logs where available. Retain the original event and timestamp for investigation.
