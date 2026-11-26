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
- Template engines frequently support powerful features (like variable interpolation, expression evaluation) that can be abused
- Security teams may overlook these in favor of more obvious issues like SQL injection or XSS

## Early warning signs

Look for these patterns in code:
1. Direct user input passed to template rendering functions
2. Template compilation from strings without proper sanitization
3. Dynamic template loading with user-controlled paths
4. Lack of input validation at the template level

## Mitigation and detection

Teams should:
1. **Inventory** all template rendering functions in their codebase
2. **Audit** how user input reaches these functions
3. **Implement strict** input sanitization for templates
4. **Use** detection rules to monitor logs for suspicious patterns

## Class-wide detections

These rules can catch behavior without relying on specific CVEs:
- Sigma: `event_type == "web_request" AND (request_uri contains "{{" OR request_uri contains "${" OR request_body contains "{{" OR request_body contains "${")`
- YARA: `rule template_injection { condition: (pe.imports("template_engine") or pe.imports("jinja2")) and (pe.sections[0].data contains "{{" or pe.sections[0].data contains "${") }`
- Suricata: `alert http any any -> any any (msg:"Template Injection Attempt"; content:"{{"; content:"}}"; sid:1000001;)`

## Check script

Run `check_exposure.sh SOURCE_DIRECTORY` to find files that may compile templates at runtime.

## Files in this kit

- `FORESIGHT.md`: This document
- `HUNTS.md`: Hunting guidance for template injection
- `check_exposure.sh`: Script to inventory template compilation sites
- `detection_rules/`: Sigma, YARA, and Suricata rules for detection