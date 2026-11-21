# Hunt Queries for CVE-2026-133949

This file contains detection rules and queries for identifying exposure to the compromised eMudhra certificates in pip installations.

## Sigma Rules

### pip_compromised_ca_sigma.yml
```yaml
title: Pip Installation with Compromised eMudhra Certificate
id: 12345678-1234-1234-1234-123456789012
status: experimental
description: Detects pip installations that may be using compromised eMudhra certificates
author: Cipher
date: 2026-11-20
logsource:
    category: pip
    product: python
detection:
    pip_version:
        - "pip < 26.2.2"
    condition: pip_version
fields:
    - pip_version
falsepositives:
    - Legitimate use of older pip versions in controlled environments
level: critical
```

## YARA Rules

### pip_compromised_ca.yar
```yara
rule pip_compromised_ca {
    meta:
        description = "Detects pip installations with compromised eMudhra certificates"
        author = "Cipher"
        date = "2026-11-20"
        reference = "https://seclists.org/oss-sec/2026/q4/803"

    strings:
        $compromised_cert = "emSign ECC Root CA - G3" ascii wide nocase

    condition:
        $compromised_cert
}
```

## Hunt Queries

### Splunk SPL
```spl
| rest /servicesNS/nobody/search/saved/searches
| where search like "*pip*" AND search like "*version*"
| stats count by search
```

### KQL (Microsoft)
```kql
DeviceProcessEvents
| where ProcessCommandLine contains "pip" and ProcessCommandLine contains "install"
| project Timestamp, DeviceName, ProcessCommandLine
```

### grep/jq
```bash
# Check for pip version in logs or system files
grep -r "pip.*< 26.2.2" /var/log/ || echo "No vulnerable pip versions found"
```