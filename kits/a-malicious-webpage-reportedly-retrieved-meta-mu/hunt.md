# Hunt for sensitive assistant reads after browsing

Use normalized audit events emitted by the assistant gateway. Correlate the browsing context to the sensitive tool call using trusted runtime metadata. Normalize missing or unverifiable approval to `missing` or `unknown` before querying. The field names and values below define a local schema. Map your own telemetry to it before use. Keep raw chat and memory content out of hunt output.

## Splunk SPL

Replace `assistant_gateway` with your audit index.

```spl
index=assistant_gateway event_type=assistant_tool_access context_source=web_content outcome=allowed
| search resource_type IN (chat_history, saved_memory) approval_status IN (missing, denied, unknown)
| table _time session_id tool_call_id resource_type approval_status
```

## Microsoft KQL

Replace `AssistantGateway_CL` and the column names with your mapped schema.

```kusto
AssistantGateway_CL
| where event_type == "assistant_tool_access" and context_source == "web_content" and outcome == "allowed"
| where resource_type in ("chat_history", "saved_memory") and approval_status in ("missing", "denied", "unknown")
| project TimeGenerated, session_id, tool_call_id, resource_type, approval_status
```

## Local JSON Lines with jq

```sh
jq -c 'select(.event_type == "assistant_tool_access" and .context_source == "web_content" and .outcome == "allowed") | select(.resource_type == "chat_history" or .resource_type == "saved_memory") | select(.approval_status == "missing" or .approval_status == "denied" or .approval_status == "unknown") | {timestamp, session_id, tool_call_id, resource_type, approval_status}' assistant-audit.jsonl
```

## Triage

Look up the original approval decision using `tool_call_id` and `session_id`. Confirm that approval came from a trusted user interaction and covered that resource and operation. Check subsequent tool calls and outbound audit metadata for evidence of disclosure. An allowed read is evidence of access. Confirm disclosure separately. Prepare by verifying that your gateway denies web-influenced sensitive reads when scoped approval is absent and records denied attempts.
