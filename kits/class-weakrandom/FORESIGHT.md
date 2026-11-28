# Weak Random Number Generation (Weak RNG)

## Pattern Description

Weak random number generation occurs when applications or systems use predictable or insufficiently random number generators for security-sensitive operations. This includes using cryptographically insecure PRNGs, seeding with predictable values, or relying on weak entropy sources.

## Why More of This is Coming

This pattern persists because:
1. Developers often underestimate the importance of cryptographic randomness
2. Many libraries default to fast but insecure RNGs
3. Testing for proper randomness is difficult and often skipped
4. Legacy systems continue to use outdated RNG implementations

## Variant Analysis

### Products Likely Next:
- **Web frameworks** using weak RNG for session IDs or CSRF tokens (e.g., Flask, Django, Express.js)
- **Mobile apps** with insecure key generation or token handling
- **IoT devices** with limited entropy sources
- **Embedded systems** in industrial control networks
- **Game engines** or simulation software that use predictable randomness for gameplay elements

### Design Patterns at Risk:
- Using `time()` or other predictable values as seeds
- Using `rand()` from standard C libraries instead of cryptographically secure alternatives
- Relying on system clocks, memory addresses, or process IDs for entropy

## Early Warning Signs to Watch

1. **ZDI upcoming advisories** for weak RNG in popular libraries
2. **Security mailing list disclosures** about predictable randomness in new frameworks
3. **Release notes** mentioning improved entropy sources or changes to cryptographic libraries
4. **Talks at security conferences** about weak RNG exploitation
5. **Public PoCs** demonstrating how to predict outputs from known RNG implementations

## What to Do NOW (Before a CVE)

1. **Inventory**: Identify all components using random number generation for security purposes
2. **Hardening**: Replace insecure RNG usage with cryptographically secure alternatives:
   - Use `urandom` on Unix-like systems instead of `/dev/random`
   - Use `crypto/rand` in Go or `secrets.token_urlsafe()` in Python
   - Implement proper seeding from high-entropy sources
3. **Monitoring**: Log and alert on repeated patterns in security tokens, session IDs, or other random values
4. **Segmentation**: Isolate systems that generate critical secrets to minimize impact of any RNG compromise

## Class-Wide Detections

### Sigma Rule (Detection)
```yaml
title: Weak Random Number Generation Usage
id: 12345678-1234-1234-1234-123456789012
status: experimental
author: Cipher
date: 2026/11/27
logsource:
    category: application
    product: any
detection:
    selection:
        # This is a placeholder - real detection would require specific patterns
        # from system calls, library usage, or logs showing weak RNG usage
        - 'rand('
        - 'random()'
        - 'srand('
    condition: selection
fields:
    - process_name
    - command_line
falsepositives:
    - Legitimate use of non-cryptographic PRNG for simulation or testing
level: medium
```

### YARA Rule (Detection)
```yara
rule weak_rng_usage {
    meta:
        description = "Detects usage of potentially weak random number generators"
        author = "Cipher"
        date = "2026-11-27"
    
    strings:
        $rand_call = /rand\(\)/ nocase
        $random_call = /random\(\)/ nocase
        $srand_call = /srand\(\)/ nocase
    
    condition:
        any of them
}
```

### Hunt Query (Elasticsearch)
```json
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "event.category": "application"
          }
        },
        {
          "terms": {
            "message": [
              "rand(",
              "random(",
              "srand("
            ]
          }
        }
      ]
    }
  }
}
```

## Read-Only Exposure Check Script

```bash
#!/bin/bash

# This script checks for weak random number generation in binaries and libraries
# It's designed to be run on your own computer (not a target system)
# Usage: ./check_weak_rng.sh <binary_or_library>

if [ $# -eq 0 ]; then
    echo "Usage: $0 <binary_or_library>"
    exit 1
fi

TARGET="$1"

echo "Checking for weak random number generation in: $TARGET"
echo "========================================================"

# Check for common insecure RNG function calls
echo "1. Checking for insecure RNG calls:"
strings "$TARGET" | grep -E "(rand|random|srand)" | sort -u

# Check for usage of /dev/random instead of /dev/urandom (which is often problematic)
echo -e "\n2. Checking for device random access:"
if [ -e "$TARGET" ]; then
    ldd "$TARGET" 2>/dev/null | grep -v "not a dynamic executable" | grep -E "(lib.*random|lib.*crypto)" || echo "No crypto libraries found"
fi

# Check for common weak RNG patterns in source code (if available)
echo -e "\n3. Checking for common weak RNG usage patterns in source:"
find "$TARGET" -name "*.c" -o -name "*.cpp" -o -name "*.h" 2>/dev/null | head -5 | while read file; do
    if [ -f "$file" ]; then
        echo "Source file: $file"
        grep -n -E "(rand\(|srand\(|random\()" "$file" 2>/dev/null || echo "No insecure RNG found in this file"
    fi
done

echo -e "\nCheck complete. Review the results to identify potential weak RNG usage."
```

This script is a simplified version for demonstration purposes and would need to be expanded for comprehensive checking.