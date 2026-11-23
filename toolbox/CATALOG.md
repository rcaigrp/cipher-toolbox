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
- **Verdict**: Successfully imported and functional. Excellent for system introspection, configuration auditing, and compliance checks.

## Resources

### 1. NVD Vulnerability Database

- **URL**: https://nvd.nist.gov/
- **Purpose**: Research CVEs and vulnerability details

### 2. oss-security Mailing List

- **URL**: https://marc.info/?l=oss-security
- **Purpose**: Early warnings on security issues## Tools
Rustinel - Endpoint Detection Engine
## Rustinel
- **Description**: Cross-platform endpoint detection engine using Sigma, YARA, and IOC rules on native telemetry
- **Link**: https://github.com/Karib0u/rustinel
- **License**: Apache License 2.0
- **Maturity**: Mature (actively maintained, v1.11.0 released in 2026)
- **Installation**: Download binary from https://rustinel.io/install.sh or GitHub releases page
- **Usage**: Run with elevated privileges to monitor system events and detect threats using Sigma rules, YARA rules, and IOC lists. Can replay recordings offline for rule testing.
- **Tested on**: Cipher's test environment with Linux x86_64 (eBPF support failed due to kernel version but config and rules loaded)
- **Verdict**: A promising, high-performance EDR solution with a strong focus on Sigma and YARA rule support. While eBPF detection failed in this test environment, the core functionality including rule loading and configuration is working.
## Resources
- **1. NVD Vulnerability Database**
  - **URL**: https://nvd.nist.gov/
  - **Purpose**: Research CVEs and vulnerability details
- **2. oss-security Mailing List**
  - **URL**: https://marc.info/?l=oss-security
  - **Purpose**: Early warnings on security issues
