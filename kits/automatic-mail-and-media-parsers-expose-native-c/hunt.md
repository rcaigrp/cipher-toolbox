# Hunt for mail and media parser resource exhaustion

Map local application, proxy and worker logs to `host`, `handler`, `event_type` and a timestamp. Use `mime_parse` and `mailpit_thumbnail` as handler labels. Normalize known resource events to `cpu_budget_exceeded`, `memory_budget_exceeded`, `parse_timeout` or `oom_kill`. Map the thumbnail handler from the route seen in legitimate local requests. The labels below are examples for normalized telemetry.

## Splunk SPL

```spl
index=mail_parser (handler=mime_parse OR handler=mailpit_thumbnail)
(event_type=cpu_budget_exceeded OR event_type=memory_budget_exceeded OR event_type=parse_timeout OR event_type=oom_kill)
| bin _time span=5m
| stats count by _time host handler event_type
| sort 0 -_time -count
```

## Microsoft KQL

```kusto
ParserEvents_CL
| where TimeGenerated >= ago(24h)
| where Handler in ('mime_parse', 'mailpit_thumbnail')
| where EventType in ('cpu_budget_exceeded', 'memory_budget_exceeded', 'parse_timeout', 'oom_kill')
| summarize Events=count() by bin(TimeGenerated, 5m), Host, Handler, EventType
| order by TimeGenerated desc, Events desc
```

## Local grep and jq

```bash
journalctl --since '24 hours ago' -u parser-worker.service --no-pager |
  grep -Ei 'out of memory|oom.kill|cpu budget|memory budget|parse timeout'
jq -c 'select((.handler == "mime_parse" or .handler == "mailpit_thumbnail") and (.event_type as $event | ["cpu_budget_exceeded", "memory_budget_exceeded", "parse_timeout", "oom_kill"] | index($event) != null))' parser-events.jsonl
```

Compare matching windows with worker CPU, memory and restarts. For Mailpit, compare thumbnail requests with request latency and worker pressure. Include isolated failures in the review because a single request can be expensive. Check the deployment baseline and recent workload changes before escalating.
