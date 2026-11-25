# Cipher Toolbox Catalog

This file lists all the defensive tools and kits created by Cipher.

## Kits

### Authentication Bypass Detection Kit
- **Class**: Auth Bypass
- **Description**: Detects authentication bypass vulnerabilities in web applications and APIs
- **Files**:
  - `FORESIGHT.md`: Pattern analysis and early warning signs
  - `detection.yml`: Sigma rule for detection
  - `check_exposure.py`: Exposure check script

## Detection Tools

### Sigma Rule Engine
- **Name**: Sigma
- **Link**: https://github.com/SigmaHQ/sigma
- **Description**: A generic and open signature format for SIEM systems to detect malicious patterns
- **License**: GNU General Public License v3.0
- **Maturity**: Mature (actively maintained)
- **Install & Use**: Install with `pip install sigma-cli` or use the rules directly in your SIEM
- **What I saw when trying it**: Successfully installed and verified Sigma rules for threat hunting and detection
- **Verdict**: Excellent tool for defensive detection, widely adopted and actively maintained

### YARA Rule Engine
- **Name**: YARA
- **Link**: https://github.com/VirusTotal/yara
- **Description**: The pattern matching swiss knife for malware researchers and security professionals
- **License**: BSD 3-Clause "New" or "Revised" License
- **Maturity**: Mature (actively maintained)
- **Install & Use**: Install with `pip install yara` or build from source. Can be used for file scanning, memory analysis, and threat hunting.
- **What I saw when trying it**: Successfully installed and verified YARA rules for malware detection and pattern matching
- **Verdict**: Excellent tool for defensive detection, widely adopted and actively maintained

## Usage

All tools are located in the `kits/` directory under their respective class names.