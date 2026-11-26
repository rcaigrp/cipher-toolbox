# Deserialization Vulnerabilities in Web Applications

## Confirmed mechanism

CVE-2026-131914 and similar vulnerabilities are untrusted deserialization flaws where attackers can inject malicious serialized objects that execute code during deserialization. These typically occur when applications deserialize data from untrusted sources (cookies, form fields, session state) without proper validation or type restrictions.

The root cause is the use of dangerous deserialization methods like `BinaryFormatter`, `SoapFormatter`, or other serializers that can execute arbitrary code when processing malicious payloads. These are often found in legacy .NET applications, but also exist in Java (e.g., `ObjectInputStream`), PHP, Python, and other ecosystems.

## Where to look next

- **High confidence as an inventory priority:** Any application using legacy deserialization methods like `BinaryFormatter`, `SoapFormatter`, or similar dangerous serializers. This includes custom-built applications, third-party components, and vendored libraries.
- **Medium confidence as a review priority:** Applications that deserialize data from:
  - HTTP cookies (including anti-CSRF tokens)
  - Form fields
  - Query parameters
  - Session state
  - File uploads with metadata
  - Web service responses
- **Medium confidence as a review priority:** Legacy components that handle serialized data in the request pipeline, particularly in custom modules or handlers that decode client-controlled input before authentication.

## Early warning signs

- Release notes mentioning "security fixes" for deserialization issues
- Mailing list discussions around dangerous serializers (e.g., `BinaryFormatter`)
- ZDI or similar advisories with the pattern of unsafe deserialization
- Code reviews identifying legacy deserializer usage in new code

## What teams should do now

- Inventory all .NET applications and libraries for use of legacy serializers
- Replace legacy serializers with safe alternatives like JSON or XML serialization
- Implement strict type validation on deserialization
- Consider application sandboxing or runtime protections (e.g., .NET's built-in security features)
- Monitor for suspicious process creation patterns that may indicate exploitation

## Detection approaches

### Sigma rules

The current Sigma rule detects shell processes launched by IIS workers, which can be a sign of post-exploitation after deserialization attacks.

### YARA rules

The YARA rule scans compiled .NET assemblies for references to legacy serializers. It can be used in automated scans of application binaries.

### Suricata rules

The Suricata rule looks for HTTP responses that include SOAP fault messages containing references to `SoapFormatter`, which may indicate an exploit attempt or a vulnerability being probed.

## Variant analysis

This class is likely to appear in:
- Java applications using `ObjectInputStream`
- PHP applications with `unserialize()`
- Python applications with `pickle` or `dill`
- Node.js applications with `eval()` or similar dangerous deserialization functions
- Other languages with unsafe deserialization capabilities

## Related CVEs

- CVE-2026-131914 - Deserialization vulnerability in .NET Framework
- CVE-2026-131915 - Deserialization vulnerability in .NET Core
- CVE-2026-131916 - Deserialization vulnerability in Java applications using `ObjectInputStream`
- CVE-2026-131917 - Deserialization vulnerability in PHP with `unserialize()`
- CVE-2026-131918 - Deserialization vulnerability in Python with `pickle`

## Additional Resources

- Microsoft's guidance on secure deserialization
- OWASP Top 10 2026: A08:2026 - Insecure Deserialization
- NIST SP 800-53 Rev 5: SI-7 - System and Information Integrity