# Weak Random Number Generation (Weak RNG) Detection Kit

This kit provides detection and mitigation tools for weak random number generation vulnerabilities.

## Contents

- `FORESIGHT.md`: Analysis of the pattern and early warning signs
- `check_weak_random.py`: Python script to check for weak RNG usage in code
- `check_weak_rng.sh`: Bash script to check for weak RNG usage in binaries/libraries
- `detection.yml`: Sigma rule for detecting weak RNG patterns
- `hunt_query.json`: Elasticsearch query for hunting weak RNG usage
- `weak_rng_usage.yar`: YARA rule for detecting weak RNG usage
- `weak_rng_usage.yml`: Updated Sigma rule for weak RNG usage

## Usage

### Check Exposure

Run the check scripts to identify potential weak RNG usage in your systems:

```bash
# For binaries/libraries
./check_weak_rng.sh <binary_or_library>

# For Python code
python3 check_weak_random.py <source_file>
```

### Detection Rules

Use the Sigma, YARA, and Elasticsearch rules for monitoring and alerting on weak RNG usage.