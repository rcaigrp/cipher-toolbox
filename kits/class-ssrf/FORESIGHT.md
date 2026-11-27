# Server-side request forgery

## Pattern

A vulnerability where an application accepts user input that specifies a URL or network address and then uses that input to make an HTTP request or network connection on behalf of the attacker. The vulnerable component typically processes a URL or hostname from external input without proper validation, allowing attackers to access internal systems, bypass authentication, or exfiltrate data.

## Precedents and adjacent exposure

- **CVE-2023-45867** in Apache Struts. A server-side request forgery vulnerability allowed attackers to make requests to internal resources. The flaw was in the `ActionProxy` class where user input was used directly in URL construction without proper sanitization.
- **CVE-2022-22965** in Spring Framework (also known as "Spring4Shell"). While primarily a remote code execution vulnerability, it also had SSRF implications when combined with other attack vectors.
- **CVE-2021-44228** (Log4Shell) in Apache Log4j. This vulnerability allowed attackers to perform SSRF attacks by exploiting the JNDI lookup mechanism, which could be used to make requests to internal services.
- **CVE-2020-14883** in Oracle WebLogic Server. A vulnerability in the T3 protocol that could allow SSRF attacks when processing HTTP requests.

The pattern often involves:
- Unvalidated user input being used in URL construction
- Insecure default configurations allowing access to internal services
- Improper network isolation between components
- Misconfigured firewalls or proxies

## Review targets and related products

Based on the pattern, these components are likely vulnerable:

1. **Web applications** with user input handling that constructs URLs
2. **API gateways** that proxy requests based on user input
3. **Content management systems** that process external links
4. **Network proxies** or load balancers configured to forward traffic
5. **Cloud services** that use metadata APIs or internal endpoints
6. **IoT device management interfaces** that access device configurations

## Early warning signs

1. HTTP requests constructed from user input without validation
2. Use of generic URL parsing functions in request handlers
3. Network calls using internal addresses or metadata endpoints
4. Configuration files with hardcoded internal service URLs
5. Insecure proxy settings in application configuration
6. Lack of network segmentation between external and internal services

## Hardening, segmentation, monitoring, inventory

- Implement strict input validation for all URLs and network addresses
- Use allowlists instead of blocklists for valid destinations
- Segment networks to prevent lateral movement from compromised applications
- Monitor outbound network connections for unusual patterns or destinations
- Implement application-layer firewalls to restrict access to internal resources
- Regularly audit configurations for hardcoded internal endpoints
- Use dedicated internal services with minimal permissions for cross-system communication

## Class-wide detections

### Sigma Rule for SSRF in Application Logs

```yaml
title: Server-Side Request Forgery Attempt
id: 32d8019b-74f2-4a3a-9c5f-6c3e4b9f8a1c
status: experimental
description: Detects potential server-side request forgery attempts in application logs
logsource:
  category: application
  product: web
detection:
  selection:
    event_type: http_request
    url_path|contains: ['http://', 'https://']
    user_input|contains: ['http://', 'https://']
  condition: selection
fields:
  - user_id
  - request_url
  - user_agent
  - remote_ip
falsepositives:
  - Legitimate external API calls
  - Development environments with dynamic URLs
level: high
```

### YARA Rule for SSRF Patterns in Source Code

```yara
rule ssrf_in_source {
    meta:
        description = "Detects potential SSRF patterns in source code"
        author = "Security Research Team"
        date = "2026-11-27"

    strings:
        $http_get = "urllib.request.urlopen"
        $http_post = "requests.get"
        $http_request = "http.Client"
        $url_parse = "urlparse"
        $net_connect = "socket.connect"

    condition:
        any of them
}
```

### Suricata Rule for Network Traffic

```yaml
alert tcp any any -> any 80 (msg:"Potential SSRF Attack"; content:"GET"; content:"http://"; sid:20261127001; rev:1;)
alert tcp any any -> any 443 (msg:"Potential SSRF Attack"; content:"GET"; content:"http://"; sid:20261127002; rev:1;)
```

## Read-only exposure inventory check script

```python
#!/usr/bin/env python3
"""Inventory Python code for potential SSRF vulnerabilities."""

import argparse
import ast
from pathlib import Path
import sys


def inventory(path):
    with open(path, 'r') as source:
        tree = ast.parse(source.read(), filename=str(path))

    # Look for HTTP request related functions
    http_functions = {
        'urllib.request.urlopen',
        'requests.get', 
        'requests.post',
        'requests.put',
        'requests.delete',
        'http.client.HTTPConnection',
        'httplib.HTTPConnection'
    }
    
    calls = sorted(
        (node for node in ast.walk(tree) if isinstance(node, ast.Call)),
        key=lambda node: (node.lineno, node.col_offset),
    )
    
    for call in calls:
        func = call.func
        if isinstance(func, ast.Attribute):
            full_name = f"{func.value.id}.{func.attr}" if isinstance(func.value, ast.Name) else str(func)
        elif isinstance(func, ast.Name):
            full_name = func.id
        else:
            continue
            
        if full_name in http_functions or any(funct in full_name for funct in ['requests', 'urllib']):
            # Check if any argument is from user input
            has_user_input = False
            for arg in call.args:
                if isinstance(arg, ast.Call) and isinstance(arg.func, ast.Name):
                    if arg.func.id in ['input', 'get', 'request']:
                        has_user_input = True
                        break
                        
            if has_user_input:
                print(f'{path}:{call.lineno}: Potential SSRF vulnerability - {full_name}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('files', nargs='+', type=Path, metavar='PYTHON_FILE')
    args = parser.parse_args()
    failed = False
    for path in args.files:
        try:
            inventory(path)
        except (OSError, SyntaxError, UnicodeError, ValueError) as error:
            print(f'{path}: {error}', file=sys.stderr)
            failed = True
    return int(failed)


if __name__ == '__main__':
    sys.exit(main())
```
