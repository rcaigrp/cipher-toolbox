# Hunt for nginx worker crashes at HTTP/2 ingress

Filter to hosts in the existing ingress inventory where nginx handles client HTTP/2. Run the hunt over your relevant exposure window and review individual crashes and clusters. These events indicate worker failure. Correlate with active listener configuration, running package or image provenance, and fix coverage for both CVEs. Review reverse proxying and worker connection pressure for CVE-2026-123633.

## Splunk SPL

Replace the index and sourcetype with the ones used for nginx error logs.

```spl
index=nginx sourcetype=nginx:error "worker process" "exited on signal 11"
| regex _raw="worker process [0-9]+ exited on signal 11([^0-9]|$)"
| bin _time span=15m
| stats count AS worker_crashes by host _time
| sort - _time
```

## Microsoft KQL

This example assumes nginx error logs arrive in `Syslog`. Adapt the table and raw-message column to your connector.

```kusto
Syslog
| where SyslogMessage matches regex @"worker process [0-9]+ exited on signal 11([^0-9]|$)"
| summarize WorkerCrashes=count() by Computer, bin(TimeGenerated, 15m)
| order by TimeGenerated desc
```

## Local grep and jq

```bash
grep -En 'worker process [0-9]+ exited on signal 11([^0-9]|$)' /var/log/nginx/error.log
journalctl -u nginx --since '2026-11-19' -o json --no-pager |
  jq -r 'select((.MESSAGE // "") | strings | test("worker process [0-9]+ exited on signal 11([^0-9]|$)")) | [.__REALTIME_TIMESTAMP, ._HOSTNAME, .MESSAGE] | @tsv'
```

Review rotated error logs and configured log destinations when the current file or journal has incomplete coverage. Use `check_exposure.py` for local configuration candidates and socket inventory. Confirm which configuration is loaded and which listeners are publicly reachable using existing ingress records.
