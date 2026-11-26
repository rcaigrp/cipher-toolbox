# Template Injection Flaws in Web Applications

Template injection vulnerabilities occur when user input is directly embedded into templates without proper sanitization or escaping. These flaws can lead to remote code execution (RCE), information disclosure, or denial of service attacks, depending on the template engine and how it processes the injected content.

## Historical precedent and variant review

Template injection has been a recurring issue across various platforms and languages:
- **Classic examples**: The original vulnerability in Apache Struts (CVE-2017-5638) used Freemarker template injection to achieve RCE
- **Perl modules**: Several CVEs in PDF::API2, WWW-Form-UrlEncoded-XS, and Crypt-JWT relate to improper handling of untrusted input in templates or serialization
- **Modern frameworks**: Template engines like Jinja2 (Python), Handlebars (JavaScript), and Twig (PHP) have all had instances where improper escaping led to code execution

A key pattern is that template injection often occurs when:
1. User-provided content is rendered directly into templates without sanitization
2. Template engines support arbitrary expression evaluation or function calls
3. Input validation is bypassed or not enforced at the template level

## Why exposure can recur

Template injection vulnerabilities are challenging to prevent because:
- They often exist in dynamic rendering code paths that are complex and hard to audit
- Template engines frequently support powerful features (like variable substitution, function calls, or expression evaluation) that attackers can abuse
- The vulnerability surface expands with new template features or integrations
- Many applications use multiple template engines or have custom template logic

## Early warning signs

Monitor for:
- Reports of arbitrary code execution in web applications
- CVEs affecting template engines or applications using them
- Suspicious template processing or rendering logs
- Requests that include unusual characters or sequences used in template syntax
- Unusual file access patterns when templates are processed

## Prepare now

1. **Inventory**: Identify all applications and services that use template engines
2. **Hardening**: Enforce strict input validation and sanitization before template rendering
3. **Segmentation**: Isolate template processing components from other application functions
4. **Monitoring**: Implement logging of template processing activities with suspicious input detection
5. **Testing**: Regularly test for template injection vulnerabilities in your applications

## Class-wide detections

### Sigma rule

```yaml
title: Template Injection Detection
id: 00000000-0000-0000-0000-000000000000
status: experimental
description: Detects potential template injection attempts
author: Cipher
date: 2026-11-26
logsource:
    category: web_access
    product: web_server
detection:
    selection:
        url|endswith:
          - '.jsp'
          - '.php'
          - '.py'
          - '.pl'
          - '.html'
    condition: selection
fields:
  - remote_addr
  - user_agent
  - request_uri
  - http_method
  - response_status
falsepositives:
  - Legitimate template rendering operations (requires human validation)
level: high
```

### YARA rule

```yara
rule Template_Injection {
    meta:
        description = "Detects common template injection patterns"
        author = "Cipher"
        date = "2026-11-26"

    strings:
        $tpl_expr1 = "{{" nocase
        $tpl_expr2 = "${" nocase
        $tpl_expr3 = "<%" nocase
        $tpl_expr4 = "{%" nocase

    condition:
        any of them
}
```

### Suricata rule

```rules
alert http any any -> any any (msg:"Potential Template Injection Attempt"; uricontent:"{{"; sid:2000001; rev:1;)
alert http any any -> any any (msg:"Potential Template Injection Attempt"; uricontent:"${"; sid:2000002; rev:1;)
alert http any any -> any any (msg:"Potential Template Injection Attempt"; uricontent:"<%"; sid:2000003; rev:1;)
alert http any any -> any any (msg:"Potential Template Injection Attempt"; uricontent:"{%"; sid:2000004; rev:1;)
```

## Read-only check script

```bash
#!/bin/bash
# Check for potential template injection vulnerabilities in common web files

echo "Checking for potential template injection patterns..."

# Define common template injection indicators
INDICATORS=(
    "{{"
    "${"
    "<%"
    "{%"
)

# Check common web directories for these patterns
WEB_DIRS=(
    "/var/www/html"
    "/opt/app"
    "/usr/share/nginx/html"
)

for dir in "${WEB_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "Checking directory: $dir"
        for indicator in "${INDICATORS[@]}"; do
            grep -r "$indicator" "$dir" 2>/dev/null | head -5
        done
    fi
done

echo "Check complete."
```

See [HUNTS.md](HUNTS.md) for log fields, correlation guidance, and synthetic validation.