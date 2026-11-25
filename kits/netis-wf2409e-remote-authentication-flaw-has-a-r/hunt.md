# Hunt for unexpected WF2409E management access

Use existing firewall logs enriched with inventory and approved management network membership as seen at the logging point. The examples use `destination_device_model`, `destination_service_role`, `action`, `source_is_approved_management`, `src_ip`, `dst_ip`, and `dst_port`. Normalize `action` to `allow` for allowed traffic. The approval field is a Boolean in KQL and JSON. Review missing approval values separately as telemetry gaps. A match identifies allowed traffic outside the approved management network.

## Splunk SPL

```spl
index=firewall earliest=-24h destination_device_model=WF2409E destination_service_role=management action=allow source_is_approved_management=false
| stats count as connections min(_time) as first_seen max(_time) as last_seen by src_ip dst_ip dst_port
| sort - connections
```

## Microsoft KQL

```kusto
FirewallLogs
| where TimeGenerated >= ago(24h)
| where destination_device_model == "WF2409E" and destination_service_role == "management"
| where action == "allow" and source_is_approved_management == false
| summarize connections=count(), first_seen=min(TimeGenerated), last_seen=max(TimeGenerated) by src_ip, dst_ip, dst_port
| order by connections desc
```

## Local grep and jq

For normalized newline-delimited JSON, grep provides a quick inventory review and jq applies the full policy predicate.

```bash
grep -F 'WF2409E' firewall.jsonl
jq -c 'select(.destination_device_model == "WF2409E" and
              .destination_service_role == "management" and
              .action == "allow" and
              .source_is_approved_management == false)
       | {src_ip, dst_ip, dst_port}' firewall.jsonl
```

Confirm the destination and management port against inventory, account for NAT as seen by the sensor, and review router administration records for unexpected changes. Check both IPv4 and IPv6 policy when investigating exposure.
