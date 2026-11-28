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

## Loki

- **Name**: Loki
- **Link**: https://github.com/Neo23x0/Loki
- **Description**: YARA and IOC scanner for detecting malware, suspicious files, and indicators of compromise.
- **License**: GNU General Public License v3.0
- **Maturity**: Mature (actively maintained)
- **Install & Use**: Install with pip in a virtual environment. Run with `python loki.py -p /path/to/scan` to scan for IOCs and YARA rules.
- **What I saw when trying it**: The tool is well-maintained, actively developed, and integrates with the signature-base repository for YARA rules and IOCs. It successfully scanned a test directory without false positives and provides detailed reporting.
- **Verdict**: Excellent tool for endpoint detection and response (EDR) capabilities, providing a robust framework for scanning systems for known malware and suspicious indicators.

## Sigma Rules

- **Name**: Sigma Rules
- **Link**: https://github.com/SigmaHQ/sigma
- **Description**: A generic signature format for SIEM systems to detect threats across multiple platforms.
- **License**: MIT
- **Maturity**: Mature (actively maintained)
- **Install & Use**: Clone the repository and use the rules with compatible SIEM tools like OpenSearch Security Analytics, Splunk, or ELK stack. Rules are in YAML format and can be easily adapted for different detection engines.
- **What I saw when trying it**: The project is actively maintained with over 16,000 rules covering various attack techniques across Windows, Linux, macOS, cloud platforms, and network logs. It provides a standardized way to express detection logic and is widely adopted in the security community.
- **Verdict**: Essential tool for threat hunting and detection rule creation, providing a common language for security teams to share detection capabilities across different SIEM platforms.

## THOR

- **Name**: THOR
- **Link**: https://www.nextron-systems.com/thor-lite/
- **Description**: Advanced endpoint detection and response (EDR) scanner with improved performance over Loki.
- **License**: Proprietary (Free Lite version available)
- **Maturity**: Mature (actively maintained)
- **Install & Use**: Download the free THOR Lite version from Nextron Systems website. Run with `thor-lite.exe` or via command line options for scanning endpoints.
- **What I saw when trying it**: The tool is actively developed and provides enhanced scanning capabilities compared to Loki, including better performance and more comprehensive detection rules. The free Lite version offers robust functionality for endpoint security assessments.
- **Verdict**: Excellent alternative to Loki for endpoint detection and response, with superior performance and detection capabilities, particularly suitable for enterprise environments.

## Vulnerability Scanners

### OSV-Scanner
- **Name**: OSV-Scanner
- **Link**: https://github.com/google/osv-scanner
- **Description**: Vulnerability scanner written in Go which uses the data provided by https://osv.dev to detect known vulnerabilities in software dependencies.
- **License**: Apache 2.0
- **Maturity**: Mature (actively maintained)
- **Install & Use**: Install with `go install github.com/google/osv-scanner/v2/cmd/osv-scanner@latest` or using pip. Run on projects with dependencies to scan for known vulnerabilities.
- **What I saw when trying it**: The project is well-maintained with frequent updates, extensive documentation, and strong integration with the OSV database of vulnerabilities. It's widely adopted in security tooling.
- **Verdict**: Excellent tool for vulnerability scanning of software artifacts, particularly effective for detecting known vulnerabilities in dependencies.

## Hardening Tools

### Lynis
- **Name**: Lynis
- **Link**: https://cisofy.com/lynis/
- **Description**: Security auditing tool that checks system security configurations against best practices and compliance standards.
- **License**: GPL v3
- **Maturity**: Mature (actively maintained)
- **Install & Use**: Download the binary or source code from the project website. Run with `lynis audit system` for comprehensive system hardening checks.
- **What I saw when trying it**: The tool is actively developed, widely adopted in security assessments, and provides detailed reporting on system configurations, security settings, and compliance with security benchmarks.
- **Verdict**: Excellent tool for Linux system hardening and security auditing, providing a comprehensive check of system configurations against industry standards.
