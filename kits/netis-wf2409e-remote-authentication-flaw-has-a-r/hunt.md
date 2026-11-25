# Hunt for Netis WF2409E management exposure

Use firewall logs to find allowed connections to inventoried WF2409E management endpoints from outside approved management networks. This identifies management access that needs review. Router identity, firmware status, and internet reachability require separate verification from existing records.

## Splunk example

Replace the documentation addresses and CIDRs with your inventory and allowlist. Map `action`, `src_ip`, `dst_ip`, and `dst_port` to your firewall fields. Use destination addresses as recorded at the point where the firewall logs the connection, accounting for address translation.

```spl
index=network action=allow dst_ip IN ("192.0.2.10", "2001:db8::10") dst_port IN (80, 443, 8080, 8443)
| where isnotnull(src_ip) AND NOT (cidrmatch("198.51.100.0/24", src_ip) OR cidrmatch("2001:db8:1::/48", src_ip))
| stats count min(_time) AS first_seen max(_time) AS last_seen BY src_ip dst_ip dst_port
```

The Sigma template in `detection/sigma/netis-wf2409e-auth-flaw.yml` uses the same example inventory and allowlist. Before deployment, replay sample events for allowed traffic from an unapproved source, allowed traffic from an approved source, denied traffic, and traffic to an unrelated destination. Only the first case should match. Exercise IPv4 and IPv6 and check how your backend handles missing source addresses.

For each match, review the firewall zone, forwarding policy, and approved management paths. Confirm the hardware revision and firmware from existing records. Run `./mitigate.sh` to review the isolation plan.
