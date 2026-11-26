# SSRF Defense Kit

This kit provides tools and guidance to defend against Server-Side Request Forgery (SSRF) vulnerabilities.

## Contents

- `FORESIGHT.md`: Analysis of the SSRF vulnerability class and its implications
- `detection.yml`: Sigma rule for detecting SSRF attempts
- `ssrf_check.py`: Script to check URLs for potential SSRF risks

## Usage

### Check URL Safety

```bash
python3 ssrf_check.py <url>
```

The script will return exit code 0 if the URL appears safe, or 1 if it detects a potential SSRF risk.

## Recommendations

- Implement strict egress filtering to restrict outbound traffic
- Validate and sanitize all user-supplied URLs
- Use allowlists for allowed domains/URLs
- Monitor logs and network traffic for unusual patterns
- Isolate internal services from untrusted networks