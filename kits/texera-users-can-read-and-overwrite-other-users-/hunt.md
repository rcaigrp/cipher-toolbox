# Hunt for unexpected Texera workflow result access

Use application audit events or independently reconstructed access records. Map local fields to the normalized fields shown below. Resolve `expected_access` against ownership, sharing grants, and administrative roles at the time of the event. Use `unknown` when those records are incomplete. Keep the actor, result ID, and event timestamp in the output for investigation.

## Splunk SPL

Replace `texera` with the index containing normalized events.

```spl
index=texera resource_type=workflow_result outcome=success expected_access=denied (operation=read OR operation=overwrite)
| table _time actor result_id operation expected_access
```

## Microsoft KQL

Replace `TexeraAudit` with the table containing normalized events.

```kusto
TexeraAudit
| where resource_type == "workflow_result" and outcome == "success" and expected_access == "denied"
| where operation in ("read", "overwrite")
| project TimeGenerated, actor, result_id, operation, expected_access
```

## grep and jq

Use `grep` to locate candidates in normalized JSON Lines, then run `jq` on the original file to evaluate the fields precisely.

```bash
grep -nF 'workflow_result' audit.jsonl
jq -c 'select(.resource_type == "workflow_result" and .outcome == "success" and .expected_access == "denied" and (.operation == "read" or .operation == "overwrite"))' audit.jsonl
```

## Investigate and prepare

Review each matching event against historical permissions. Investigate successful reads as potential disclosure. For suspected overwrites, preserve the current result and available audit records, then compare against a trusted copy or rerun from trusted inputs. Prioritize important results and review events with unknown permissions separately. Where actor, result ID, or historical permissions are missing, record the visibility gap and arrange to retain those records before the next incident.
