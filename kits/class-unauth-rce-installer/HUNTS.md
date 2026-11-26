# Hunt queries for unauthenticated installer RCE

## Log fields to correlate

- `request_uri` or `url` – identify the setup endpoint, e.g., `/install.php`, `/setup`, `/admin/install`
- `user_agent` – identify bots or scanners
- `remote_addr` – track IP addresses that accessed setup
- `http_method` – check for POST requests to setup paths
- `response_status` – monitor for 200 OK responses from setup endpoints (indicating successful access)
- `request_body` – inspect for parameters that might trigger setup logic, e.g., `install`, `setup`, or `admin_user`
- `timestamp` – correlate with other logs to find anomalous activity
- `server_name` – determine which host served the request if multiple are in use

## Correlation guidance

1. **Setup access outside provisioning windows**: Identify requests to setup paths during normal operational hours, or from unusual IP addresses.
2. **Setup access with privileged user creation**: If setup creates users, correlate this with logs of new user creation, especially admin-level accounts.
3. **Setup access without prior authentication**: Confirm that no authentication tokens or cookies were present during the request.
4. **Setup access followed by configuration changes**: If setup writes configuration files or database entries, look for those changes in logs.

## Synthetic validation

To validate a setup path is exposed and accessible:

1. **Direct HTTP call**: Use `curl` to test the endpoint directly:
   ```bash
   curl -v http://<target>/install.php
   ```
2. **Check for setup-specific headers or content**:
   ```bash
   curl -s http://<target>/install.php | grep -i "setup\|install"
   ```

## Sigma rule

```yaml
title: Unauthenticated Web Installer Access
id: 12345678-90ab-cdef-1234-567890abcdef
status: experimental
description: Detects access to web application setup/installer paths without authentication.
author: Cipher
date: 2026-11-26
logsource:
  category: web
  product: web_server
detection:
  selection:
    url|endswith:
      - '/install.php'
      - '/setup'
      - '/admin/install'
  condition: selection
fields:
  - remote_addr
  - user_agent
  - request_uri
  - http_method
  - response_status
falsepositives:
  - Legitimate setup processes during provisioning (requires human validation)
level: high
```

## YARA rule

```yara
rule Unauth_Installer_Access {
    meta:
        description = "Detects access to common web installer paths"
        author = "Cipher"
        date = "2026-11-26"

    strings:
        $setup_path1 = "/install.php"
        $setup_path2 = "/setup"
        $setup_path3 = "/admin/install"

    condition:
        any of them
}
```

## Suricata rule

```rules
alert http any any -> any any (msg:"Unauthenticated Web Installer Access"; uricontent:"/install.php"; sid:1000001; rev:1;)
alert http any any -> any any (msg:"Unauthenticated Web Installer Access"; uricontent:"/setup"; sid:1000002; rev:1;)
alert http any any -> any any (msg:"Unauthenticated Web Installer Access"; uricontent:"/admin/install"; sid:1000003; rev:1;)
```