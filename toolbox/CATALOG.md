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
