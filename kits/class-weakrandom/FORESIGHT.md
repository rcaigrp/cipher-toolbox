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
2. **Security mailing list disclosures** about predictable randomness in widely-used components
3. **Release notes** mentioning fixes for weak RNG issues (especially in crypto libraries)
4. **Public PoCs** demonstrating how weak RNG can be exploited to predict future outputs

## What to Do Now

1. **Inventory**: Audit all systems and libraries for weak RNG usage
2. **Hardening**: Replace insecure RNGs with cryptographically secure alternatives
3. **Monitoring**: Implement detection rules to monitor for weak RNG patterns in logs
4. **Testing**: Add randomness quality checks to your CI/CD pipeline
5. **Segmentation**: Isolate systems using weak RNG from sensitive operations

## Class-Wide Detections

### Sigma Rules:
- `detection.yml`: Detects patterns indicative of weak RNG usage

### YARA Rules:
- `weak_rng_usage.yar`: Identifies code or binaries that use known weak RNG functions

### Hunt Queries:
- `hunt_query.json`: Elasticsearch queries for identifying weak RNG usage in logs