# Weak Random Number Generation (Weak RNG) - Security Kit

This kit contains detection rules, a check script, and analysis for the weak random number generation vulnerability class.

## Files

- `FORESIGHT.md`: Detailed analysis of the pattern, why more of it is coming, and what to do now
- `check_weak_rng.sh`: Read-only exposure check script for weak RNG usage
- `check_weak_random.py`: Python-based check for weak random patterns in code

## Usage

### Check for Weak RNG Exposure

Run the check script on source files:
```bash
python3 check_weak_random.py <source_file>
```

Or use the shell version to analyze binaries or libraries:
```bash
./check_weak_rng.sh <binary_or_library>
```

### Detection Rules

- Sigma rule: `weak_rng_usage.yml` - Detects insecure RNG function calls
- YARA rule: `weak_rng_usage.yar` - Detects weak RNG usage in binaries
- Hunt query: `hunt_query.json` - Elasticsearch query to find weak RNG patterns

## Analysis

This kit focuses on the vulnerability class of weak random number generation, where applications use predictable or insufficiently random number generators for security-sensitive operations. This pattern has been observed in various systems including web frameworks, mobile apps, and embedded systems.