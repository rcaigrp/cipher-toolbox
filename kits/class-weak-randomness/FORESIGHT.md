# Weak Random Number Generation (Class of Vulnerabilities)

## Pattern Analysis

Weak random number generation is a class of vulnerabilities where applications or systems use predictable or insufficiently random numbers for security-sensitive operations. This includes cryptographic key generation, session tokens, nonce values, and other security artifacts that rely on randomness.

The pattern manifests when:
1. Cryptographically insecure random number generators (CSPRNGs) are used
2. Pseudo-random number generators (PRNGs) with weak seeds or short periods are employed
3. System-provided random functions are misused for security purposes

## Why More of This Is Coming

This vulnerability class persists because:
- Developers often don't understand the difference between regular PRNGs and CSPRNGs
- Standard libraries sometimes default to insecure generators
- Legacy codebases carry old implementations that aren't updated
- Security requirements are not always considered during design phases

## Variant Analysis: Products Likely Affected

Based on past incidents and patterns, these components are most likely vulnerable:
1. **Perl modules**: Strong::Random (CVE-2026-122093) - a common pattern where insecure random generators are used in cryptographic contexts
2. **Web application frameworks** that generate session IDs or CSRF tokens using weak randomness
3. **Network security tools** that use random values for packet identifiers, sequence numbers, or encryption keys
4. **Mobile applications** with insecure token generation for authentication
5. **Embedded systems** using weak random number generators for security features

The vulnerability is particularly concerning in any system where random values are used for:
- Session management (session tokens)
- Cryptographic key generation
- Nonce values for replay protection
- Authentication tokens or passwords
- Access control decisions

## Early Warning Signs to Watch For

Teams should monitor:
1. Use of standard `rand()` functions or similar in security-sensitive contexts
2. Calls to `/dev/random` or `/dev/urandom` with insufficient entropy sources
3. Insecure random number generators like `java.util.Random` in Java applications
4. Weak CSPRNG implementations (e.g., those based on time or simple linear congruential generators)
5. Session management systems using predictable token generation algorithms

## What to Do NOW (Before a CVE)

### Immediate Actions:
1. **Inventory all security-sensitive functions** that use random number generation
2. **Audit code for usage of weak PRNGs** (e.g., `rand()`, `random()`, or system-level random functions in cryptographic contexts)
3. **Implement CSPRNGs** for any security artifacts requiring randomness

### Hardening Measures:
1. **Replace insecure generators** with cryptographically secure alternatives
2. **Segment systems** that handle sensitive tokens to limit impact of compromise
3. **Monitor token generation patterns** for predictability (e.g., using statistical tests)

### Detection:
- Monitor logs for repeated or predictable session IDs
- Look for patterns in authentication tokens generated over time

## Class-Wide Detections and Exposure Checks

### Sigma Rules:
```yaml
title: Weak Random Number Generation in Security Contexts
id: 12345678-90ab-cdef-1234-567890abcdef
status: experimental
author: Cipher
date: 2026-11-27
logsource:
  category: application
  product: any
detection:
  selection:
    user_agent|contains: 'WeakRandom'
  condition: selection
fields:
  - user_agent
  - message
false_positives:
  - Legitimate use of weak random numbers for non-security purposes
level: high
```

### YARA Rule:
```yara
rule WeakRandomUsage {
    meta:
        description = "Detects potential weak random number usage in binaries"
        author = "Cipher"
        date = "2026-11-27"

    strings:
        $weak_random = /rand\(\)/ nocase
        $pseudo_random = /random\(\)/ nocase

    condition:
        (any of ($weak_random) or any of ($pseudo_random))
}
```

### Read-only Exposure Check Script (Python):
```python
#!/usr/bin/env python3

import re
import sys

def check_weak_random_usage(file_path):
    """Check for weak random number usage in a file."""
    weak_patterns = [
        r'\b(rand|random)\s*\(\s*\)',
        r'\bgetrandom\b',
        r'\bsrand\b'
    ]

    with open(file_path, 'r') as f:
        content = f.read()

    found_issues = []
    for pattern in weak_patterns:
        matches = re.finditer(pattern, content)
        for match in matches:
            line_num = content[:match.start()].count('\n') + 1
            found_issues.append(f"Line {line_num}: Found potential weak random usage: {match.group()}")

    return found_issues

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_weak_random.py <file_path>")
        sys.exit(1)

    issues = check_weak_random_usage(sys.argv[1])
    if issues:
        for issue in issues:
            print(issue)
        sys.exit(1)
    else:
        print("No weak random usage detected.")
```

This script can be used to scan source code files for insecure random number generation patterns.

## References

- CVE-2026-122093: Strong::Random versions through 0.96 for Perl allow every later rand output to be predicted from three earlier ones
- ZDI-CAN-37904, ZDI-CAN-36536, ZDI-CAN-35565, ZDI-CAN-36554, ZDI-CAN-36562, ZDI-CAN-36532, ZDI-CAN-35324, ZDI-CAN-35961