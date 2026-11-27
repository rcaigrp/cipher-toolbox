# XML External Entity (XXE) Vulnerability Defense Kit

## Pattern

An XXE vulnerability occurs when an application processes untrusted XML data without proper validation, allowing attackers to inject external entities that can access local files, perform server-side request forgery (SSRF), or execute arbitrary code.

## Precedents and adjacent exposure

- **CVE-2017-15715** in Apache Struts. This vulnerability allowed attackers to perform XXE attacks that could lead to remote code execution by leveraging the XML parsing capabilities of the framework.
- **CVE-2019-14287** in GitLab. A XXE vulnerability in the file upload functionality allowed attackers to read arbitrary files from the server.
- **CVE-2020-13942** in Apache OFBiz. This XXE vulnerability could be exploited to perform SSRF attacks and potentially lead to remote code execution.

## Key characteristics

The pattern typically involves:
- Processing XML data using vulnerable parsers (like SAX, DOM, or StAX in Java)
- Direct parsing of user-supplied XML without validation
- Use of external entity references like `<!ENTITY xxe SYSTEM "file:///etc/passwd">`
- Lack of proper input sanitization and validation

## Early warning signs

- Use of XML parsers that allow external entities by default (Java: SAXParser, DOMParser)
- Direct parsing of user input as XML without proper validation
- XML processing in APIs or web services that accept raw XML data
- Libraries that have known XXE vulnerabilities (e.g., older versions of Apache Commons Text)

## Mitigation strategies

1. **Disable external entities**: Configure XML parsers to disable external entity resolution
2. **Input validation**: Validate and sanitize all XML input before processing
3. **Use secure parsers**: Use parsers that are configured securely by default
4. **Alternative formats**: Consider using JSON or other formats instead of XML when possible

## Products at risk

- Web applications using XML parsing libraries
- APIs that accept XML input
- Enterprise software with XML configuration files
- Legacy systems using older XML processing libraries

## Variant analysis

This vulnerability class is particularly prevalent in:
- Web services using SOAP (XML-based)
- Applications processing configuration files in XML format
- Systems that allow user-provided XML content to be parsed directly

The same patterns are likely to appear in:
- XML parsers for other languages (Python, Ruby, etc.)
- Legacy enterprise systems still using XML as primary data format
- APIs accepting XML input without proper validation