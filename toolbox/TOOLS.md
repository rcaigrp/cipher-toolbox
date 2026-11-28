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

## toolbox/cve-to-sigma

A tool that converts CVE information into Sigma rules for threat detection.

### Files:
- `cve_to_sigma.py`: The main script that generates Sigma rules from CVE data
- `README.md`: Documentation for the tool
- `test_cve_to_sigma.py`: Test script to verify functionality

### Usage:
1. Run `python3 cve_to_sigma.py CVE-YYYY-NNNNN` to generate a Sigma rule for a specific CVE
2. The tool will create a file named `CVE-YYYY-NNNNN.yml` with the generated rule

### Features:
- Converts CVE information into Sigma rules
- Generates detection patterns based on vulnerability descriptions
- Includes metadata like CVSS scores and references
- Uses standard Sigma rule format for compatibility with SIEM tools

### Testing:
The tool was tested with sample CVEs including CVE-2026-138003, CVE-2026-138004, CVE-2026-132165, and CVE-2026-137964.