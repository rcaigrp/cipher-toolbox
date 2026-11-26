# Hunt queries for GeoServer WMS RCE

## Log fields to correlate

- `request_uri` or `url` – identify the WMS endpoint, e.g., `/geoserver/wms`
- `user_agent` – identify bots or scanners
- `remote_addr` – track IP addresses that accessed WMS
- `http_method` – check for POST requests to WMS paths
- `response_status` – monitor for 200 OK responses from WMS endpoints (indicating successful access)
- `request_body` – inspect for parameters that might trigger RCE, e.g., `REQUEST`, `LAYERS`, or `STYLES`
- `timestamp` – correlate with other logs to find anomalous activity
- `server_name` – determine which host served the request if multiple are in use

## Correlation guidance

1. **WMS access outside normal hours**: Identify requests to WMS paths during non-business hours.
2. **WMS access with suspicious parameters**: Look for unusual or complex parameter values that could indicate an exploit attempt.
3. **WMS access followed by configuration changes**: If WMS modifies configuration files or database entries, look for those changes in logs.
4. **High-volume WMS requests**: Monitor for a large number of requests to the same endpoint, which may indicate scanning or exploitation.

## Synthetic validation

To validate if a GeoServer instance is vulnerable to WMS RCE:

1. **Direct HTTP call with malicious parameters**:
   ```bash
   curl -v "http://<target>/geoserver/wms?REQUEST=GetMap&LAYERS=test&STYLES=&FORMAT=image/png"
   ```
2. **Check for error messages or unexpected responses that could indicate exploitation**.

## Sigma rule

```yaml
title: GeoServer WMS RCE Attempt
id: 12345678-90ab-cdef-1234-567890abcdef
status: experimental
description: Detects attempts to exploit GeoServer WMS RCE vulnerability.
author: Cipher
date: 2026-11-26
logsource:
  category: web
  product: web_server
detection:
  selection:
    url|endswith:
      - '/geoserver/wms'
  condition: selection
fields:
  - remote_addr
  - user_agent
  - request_uri
  - http_method
  - response_status
falsepositives:
  - Legitimate WMS requests (requires human validation)
level: high
```

## YARA rule

```yara
rule GeoServer_WMS_RCE {
    meta:
        description = "Detects GeoServer WMS requests with suspicious parameters"
        author = "Cipher"
        date = "2026-11-26"

    strings:
        $wms_path = "/geoserver/wms"
        $request_param = "REQUEST="
        $layers_param = "LAYERS="

    condition:
        $wms_path and ($request_param or $layers_param)
}
```

## Suricata rule

```rules
alert http any any -> any any (msg:"GeoServer WMS RCE Attempt"; uricontent:"/geoserver/wms"; sid:1000004; rev:1;)
alert http any any -> any any (msg:"GeoServer WMS RCE Attempt"; content:"REQUEST="; sid:1000005; rev:1;)
alert http any any -> any any (msg:"GeoServer WMS RCE Attempt"; content:"LAYERS="; sid:1000006; rev:1;)
```