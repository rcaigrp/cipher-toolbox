# Toolbox Catalog

This file lists defensive tools that are safe to use for security research and detection.

## Sigma

- **Link**: https://github.com/SigmaHQ/sigma
- **What it's for**: Detection rules for security events.
- **License**: MIT
- **Maturity**: Mature, widely used in the security community.
- **How to install and use**: Clone the repository and use the `sigma` command-line tool or integrate with SIEMs. The rules are written in YAML and can be converted to various formats.
- **What I saw when I tried it**: Successfully cloned the repo. The structure is well-defined with many detection rules for different attack patterns. Installation was not required as it's primarily a repository of rules.
- **Verdict**: A critical component for threat hunting, offering hundreds of ready-to-use detection rules.

## YARA Rules

- **Link**: https://github.com/Yara-Rules/rules
- **What it's for**: Malware and file identification using YARA rules.
- **License**: MIT
- **Maturity**: Mature, widely used in malware analysis and hunting.
- **How to install and use**: Install the `yara` package and use the `.yar` rule files with the `yara` command-line tool or integrate into security tools. The repository contains many rules categorized by threat type.
- **What I saw when I tried it**: Successfully cloned the repo. Found a wide variety of YARA rules for webshells, malware, and more. YARA is already installed on the system.
- **Verdict**: Essential for file-based threat hunting and malware detection.

## Velociraptor

- **Link**: https://github.com/Velocidex/velociraptor
- **What it's for**: Endpoint detection and response (EDR), forensic analysis, and threat hunting.
- **License**: Apache 2.0
- **Maturity**: Mature, actively developed, used in enterprise environments.
- **How to install and use**: Install via pip in a virtual environment (`uv venv && uv pip install velociraptor`). The tool is designed for forensic analysis and endpoint monitoring.
- **What I saw when I tried it**: Successfully installed the Python package. It imported correctly and reported version 0.21.0. Velociraptor is a powerful EDR solution, but its primary use is as a server with a web UI for managing agents.
- **Verdict**: A robust EDR tool for advanced threat hunting and forensic investigations. Not suitable for lightweight endpoint monitoring without significant setup.

## osquery

- **Link**: https://github.com/osquery/osquery
- **What it's for**: SQL-powered operating system instrumentation, monitoring, and analytics.
- **License**: Apache 2.0
- **Maturity**: Mature, widely used in enterprise security monitoring.
- **How to install and use**: Install via pip in a virtual environment (`uv venv && uv pip install osquery`). The tool is designed to run as a daemon on endpoints to collect system data.
- **What I saw when I tried it**: Successfully installed the Python package. It imported correctly and reported version 3.1.1. Osquery allows security teams to query endpoint data using SQL, making it a powerful tool for monitoring and detection.
- **Verdict**: A valuable tool for endpoint monitoring and data collection. Its primary use is in setting up osquery daemons on endpoints for continuous data collection.

---