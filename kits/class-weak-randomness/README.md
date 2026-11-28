# Weak Random Number Generation Detection Kit

This kit provides tools and guidance for detecting weak random number generation vulnerabilities in systems.

## Files

- `FORESIGHT.md`: Analysis of the weak randomness vulnerability class
- `detect.yml`: Sigma rule for detecting weak random usage
- `check_weak_random.py`: Script to scan source code for weak random patterns

## Usage

1. Review the FORESIGHT.md document for analysis and recommendations
2. Use the Sigma rule to detect weak random usage in logs
3. Run the check script on source code to identify insecure random number usage:

```bash
python3 check_weak_random.py <source_file>
```

## Detection

The kit provides both behavioral detection (Sigma rules) and static analysis (check script) for identifying weak random number generation vulnerabilities.