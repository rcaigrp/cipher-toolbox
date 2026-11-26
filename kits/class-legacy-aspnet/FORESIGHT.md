# Legacy ASP.NET Authentication Bypass

## Confirmed mechanism

CVE-2026-131914 is an untrusted deserialization flaw in Idunno.AntiCsrf through 0.9.1 Beta. NVD describes unauthenticated remote code execution through object injection during double-submit cookie and form-field validation. Tuskira reports observed exploitation, CISA KEV listing, and no available patch. The scope to prioritize is ASP.NET WebForms deployments that load the module and accept unauthenticated form submissions.

This pattern represents a broader class of vulnerabilities in legacy ASP.NET applications where authentication mechanisms are bypassed through insecure deserialization or improper validation of client-controlled data. These flaws typically manifest in:

- Authentication state manipulation via serialized cookies
- Session hijacking through deserialized session tokens
- Form field tampering that bypasses anti-CSRF protections
- Custom module handling that improperly validates request data

## Where to look next

- **High confidence as an inventory priority:** Legacy ASP.NET WebForms applications using Idunno.AntiCsrf or similar anti-CSRF libraries. Any application that accepts unauthenticated form submissions and uses the library.
- **Medium confidence as a review priority:** Custom authentication modules, especially those handling:
  - Session state serialization
  - Anti-CSRF token validation
  - Form field decoding before authentication
  - Cookie management in legacy ASP.NET applications
- **Medium confidence as a review priority:** Legacy components that handle serialized data in the request pipeline. This includes older versions of ASP.NET and related libraries that may have similar patterns.

## Early warning

Look for:
- ZDI upcoming notices related to ASP.NET authentication bypasses
- oss-security and Full Disclosure mailing list posts about .NET serialization flaws in legacy ASP.NET
- Vendor security release notes mentioning removal of legacy serializers or introduction of safer alternatives in ASP.NET frameworks
- Conference talks or blog posts discussing ASP.NET authentication bypass patterns in the wild

## Prepare now

- Inventory all legacy ASP.NET WebForms applications, particularly those using anti-CSRF libraries
- Review application configurations for use of vulnerable libraries like Idunno.AntiCsrf
- Replace vulnerable components with modern alternatives that don't rely on insecure deserialization
- Implement strict input validation at request boundaries
- Monitor for unusual authentication behavior or session management anomalies in logs
- Ensure proper separation between authentication and data handling components

## Kit status

This kit will include:
1. Detection rules (Sigma/YARA/Suricata) for patterns of legacy ASP.NET authentication bypasses
2. A read-only exposure check script to identify potential vulnerable components
3. Hunt queries for anomalous behavior in logs that might indicate exploitation attempts