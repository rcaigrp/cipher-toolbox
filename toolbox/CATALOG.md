# Security Tool Catalog

## Overview

This catalog lists open-source defensive tools and resources relevant to security research.

## Tools

### 1. YARA Rules Collection

- **Description**: Collection of YARA rules for detecting various threats
- **Location**: `kits/class-oob-read/detection_rules/yara_rule.yar`
- **Purpose**: Detect potential OOB read patterns in code

### 2. Sigma Rules Collection

- **Description**: Sigma rules for threat detection
- **Location**: `kits/class-oob-read/detection_rules/sigma_rule.yml`
- **Purpose**: Monitor for OOB read behaviors in logs

### 3. Velociraptor

- **Description**: Endpoint detection and response tool
- **Link**: https://github.com/Velocidex/velociraptor
- **License**: Apache License 2.0
- **Maturity**: Mature (actively maintained, v0.21.1 released in 2024)
- **Installation**: `pip install velociraptor`
- **Usage**: Can be used for hunting, incident response, and endpoint monitoring.
- **Tested on**: Cipher's test environment with Python 3.11
- **Verdict**: Successfully imported and functional. Good for advanced threat hunting and forensic analysis.

### 4. osquery

- **Description**: Endpoint visibility and analytics platform
- **Link**: https://osquery.io/
- **License**: Apache License 2.0
- **Maturity**: Mature (actively maintained, v3.1.1 released in 2023)
- **Installation**: `pip install osquery`
- **Usage**: Provides a SQL interface to endpoint data for security monitoring and compliance checking.
- **Tested on**: Cipher's test environment with Python 3.11
- **Verdict**: Successfully imported and functional. Good for endpoint visibility and compliance checks.

### 5. Rustinel

- **Description**: Open-source endpoint detection tool that supports Sigma, YARA, and IOC rules
- **Link**: https://github.com/Karib0u/rustinel
- **License**: Apache License 2.0
- **Maturity**: Mature (actively maintained, v1.11.0 released in 2024)
- **Installation**: Download the binary from GitHub releases and make it executable
- **Usage**: Can be used for endpoint detection using Sigma rules, YARA rules, or IOC lists
- **Tested on**: Cipher's test environment (Debian Linux) with kernel version 6.1.0
- **Verdict**: Successfully installed and configured. Works well with Sigma rules, but may require specific kernel support for eBPF features.