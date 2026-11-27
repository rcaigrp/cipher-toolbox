# Toolbox: Defensive Tools Catalog

This file lists the defensive tools and scripts that Cipher has built or tested.

## kits/class-weakrandom

A detection and exposure check kit for weak random number generation vulnerabilities.

### Files:
- `FORESIGHT.md`: Analysis of the vulnerability class, variant analysis, early warning signs, and defensive actions.
- `check_weak_random.py`: A script to detect insecure usage of random functions in Python code.
- `detection.yml`: Sigma rule for detecting weak random usage in logs.

### Usage:
1. Run `check_weak_random.py` to scan your codebase for insecure randomness.
2. Use the Sigma rule to monitor for weak random usage in logs.