# Hunt for allocator errors in unattended OpenPGP receivers

Identify the services that use GPGME to process external keys or signed data. Include queue workers and mail processors. Substitute the actual service and log source in each query. Collect receiver stderr. The examples search for the same two allocator diagnostics as the Sigma rule.

## Splunk SPL

Use the index that collects receiver logs. Replace `receiver.service` with the value in your service field.

```spl
index=receiver_logs service="receiver.service"
| regex _raw="(?i)double[ -]free"
| table _time host service _raw
```

## Microsoft Sentinel KQL

For Linux systems forwarding receiver diagnostics to the `Syslog` table, substitute the receiver's syslog process name.

```kql
Syslog
| where TimeGenerated >= ago(7d)
| where ProcessName =~ "receiver"
| where SyslogMessage contains "double free" or SyslogMessage contains "double-free"
| project TimeGenerated, Computer, ProcessName, SyslogMessage
```

## Local journal with grep

```bash
journalctl -u receiver.service --since '7 days ago' --no-pager -o short-iso | grep -Ei 'double[ -]free'
```

## Triage

For each hit, match the host, service, timestamp and any request or queue ID against the receiver's import and verification logs. Record which library the worker loaded and whether the distributor confirms the fix for that build. A double-free message alone cannot establish the cause or demonstrate data disclosure. A receiver may expose data without logging an allocator error.

If the receiver already records OpenPGP user ID lengths, compare unusual values with that receiver's own history. The advisory supplies no cutoff. Use existing length metadata and preserve the original input under restricted access. Avoid sending suspect input through a production parser again.
