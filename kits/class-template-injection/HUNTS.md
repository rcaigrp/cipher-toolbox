# Hunting for Template Injection Vulnerabilities

## Log fields to correlate

When hunting for template injection vulnerabilities, look for these log fields:

- `request_uri` - Look for unusual patterns in URLs that might contain template syntax
- `http_method` - POST/PUT requests are more likely to carry injected content
- `user_agent` - Malicious user agents or tools often used in exploitation attempts
- `query_string` - Parameters containing template injection indicators
- `request_body` - Full request body for template syntax in POST data
- `response_status` - 500 errors might indicate template processing failures
- `remote_addr` - IP addresses making suspicious requests

## Correlation guidance

1. **High-risk patterns**: Requests containing `{{`, `${`, `<%`, or `{%` in query parameters or request bodies
2. **Suspicious combinations**: Template syntax with other indicators like `eval`, `exec`, `system`, or file access functions
3. **Frequent offenders**: Applications using Jinja2, Handlebars, Twig, Freemarker, or similar engines

## Synthetic validation

To validate the detection rules:
1. Create a test environment with a vulnerable application (e.g., a simple Flask app with Jinja2 templating)
2. Simulate requests with template injection payloads
3. Verify that the detection rules properly identify these requests
4. Test false positive scenarios to refine rule parameters

## Example hunt query for Splunk

```
index=web_logs 
[| inputlookup template_injection_indicators.csv] 
| stats count by request_uri, user_agent, remote_addr 
| where count > 1
```

This search identifies IPs or URIs that have multiple suspicious requests, which may indicate exploitation attempts.