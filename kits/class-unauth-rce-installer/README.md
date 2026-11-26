# Class-Unauth-RCE-Installer Kit

This kit detects potential installer scripts that could lead to unauthenticated remote code execution vulnerabilities.

## Files

- `check_exposure.sh`: Script to check for common installer artifacts
- `detection_rules/`: Directory containing detection rules for various security tools
  - `yara_installer_rce.yar`
  - `suricata_installer_rce.rules`
  - `sigma_installer_rce.yml`
- `HUNTS.md`: Hunting guidelines
- `FORESIGHT.md`: Forensic guidance

## Usage

Run the check_exposure.sh script with a local web root as an argument to identify potential installer artifacts.