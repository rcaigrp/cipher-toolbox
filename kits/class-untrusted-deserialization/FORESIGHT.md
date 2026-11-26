# Untrusted Deserialization in .NET Applications

## Confirmed mechanism

CVE-2026-131914 is an untrusted deserialization flaw in Idunno.AntiCsrf through 0.9.1 Beta. NVD describes unauthenticated remote code execution through object injection during double-submit cookie and form-field validation. Tuskira reports observed exploitation, CISA KEV listing, and no available patch. The scope to prioritize is ASP.NET WebForms deployments that load the module and accept unauthenticated form submissions.

This pattern represents a broader class of vulnerabilities in .NET applications where untrusted input is deserialized into objects without proper validation or type restrictions. This can occur in various contexts including:

- Session state serialization
- Cookie deserialization
- Form field decoding
- Web service request parsing
- File upload handling with metadata

The root cause is the use of dangerous deserialization methods like `BinaryFormatter`, `SoapFormatter`, or other serializers that can execute arbitrary code when processing malicious payloads.

## Where to look next

- **High confidence as an inventory priority:** Any .NET application using legacy serializers such as `BinaryFormatter` or `SoapFormatter`. This includes custom-built applications, third-party components, and vendored libraries.
- **Medium confidence as a review priority:** Applications that deserialize data from:
  - HTTP cookies (including anti-CSRF tokens)
  - Form fields
  - Query parameters
  - Session state
  - File uploads with metadata
  - Web service responses
- **Medium confidence as a review priority:** Legacy components that handle serialized data in the request pipeline, particularly in custom modules or handlers that decode client-controlled input before authentication.

## Early warning

Look for:
- ZDI upcoming notices related to .NET deserialization vulnerabilities
- oss-security and Full Disclosure mailing list posts about .NET serialization flaws
- Vendor security release notes mentioning removal of legacy serializers or introduction of safer alternatives
- Conference talks or blog posts discussing .NET deserialization patterns in the wild

## Prepare now

- Inventory all .NET applications that might deserialize untrusted input, particularly those using legacy serializers
- Review application configurations for any use of `BinaryFormatter`, `SoapFormatter`, or similar dangerous serializers
- Replace legacy serializers with safer alternatives like `System.Text.Json` or `Newtonsoft.Json` with proper type restrictions
- Implement strict type whitelisting for deserialization operations
- Use data-only schemas at request boundaries and avoid deserializing user input into complex object graphs
- Monitor for unusual outbound connections from application workers, unexpected file writes, or process spawning

## Kit status

This kit will include:
1. Detection rules (Sigma/YARA/Suricata) for patterns of dangerous deserialization
2. A read-only exposure check script to identify potential vulnerable components
3. Hunt queries for anomalous behavior in logs that might indicate exploitation attempts

The existing Idunno.AntiCsrf kit provides a starting point, but this new class is broader and more fundamental.