# Toolbox Tools

This file lists the defensive tools that are part of the toolbox.

## Sigma

- **Description**: Detection rules for security events.
- **Location**: `toolbox/try/sigma`
- **Usage**: Clone the repository and use the `sigma` command-line tool or integrate with SIEMs. The rules are written in YAML and can be converted to various formats.

## YARA Rules

- **Description**: Malware and file identification using YARA rules.
- **Location**: `toolbox/try/yara`
- **Usage**: Install the `yara` package and use the `.yar` rule files with the `yara` command-line tool or integrate into security tools. The repository contains many rules categorized by threat type.
