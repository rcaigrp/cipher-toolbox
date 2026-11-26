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

### LOKI IOC and YARA Scanner

- **Project** [LOKI](https://github.com/Neo23x0/Loki) is a local, on-demand scanner for YARA matches and known indicators such as suspicious filenames and hashes. It can help triage files collected during malware or supply-chain investigations.
- **License** GNU GPL v3 or later for LOKI. The upstream Signature Base rules carry Detection Rule License 1.1. [LOKI license](https://github.com/Neo23x0/Loki#license), [Signature Base license](https://github.com/Neo23x0/signature-base/blob/master/LICENSE)
- **Maintenance** The maintainer marks the Python project deprecated and in inactive maintenance mode. GitHub shows v0.51.0 as the latest release. The tested checkout was commit `7688421` from January 9, 2026 and reported version `0.51.1`. The issue tracker showed 15 open issues, including a user report of a YARA rule initialization error. [README](https://github.com/Neo23x0/Loki#readme), [Latest release](https://github.com/Neo23x0/Loki/releases/tag/v0.51.0), [Issues](https://github.com/Neo23x0/Loki/issues)
- **Install and use** Clone the project into `toolbox/try/Loki`. From that directory, run `python3 -m venv loki-venv` and `loki-venv/bin/python -m pip install colorama yara-python psutil rfc5424-logging-handler netaddr`. For a file-only sweep, run `loki-venv/bin/python loki.py -p ../test_scan --noprocscan --nolisten`. If its signature directory is missing, LOKI attempts to download public rule data on startup.
- **Local trial** `--help` and `--version` worked. An unprivileged scan of `toolbox/try/test_scan` initialized 1,066 YARA rules and reported zero alerts and zero warnings for the benign test directory. The scan log is `toolbox/try/Loki/loki_cipher_2026-11-26_20-45-09.log`. This run covered rule loading and the scan path. Detection of a known-positive fixture remains unverified.
- **Verdict** Suitable for occasional, controlled local IOC sweeps. For ongoing endpoint coverage, prioritize a maintained tool because the Python project is deprecated and users have reported rule compatibility issues.

## Vulnerability Scanners

### Nuclei
- **Name**: Nuclei
- **Link**: https://github.com/projectdiscovery/nuclei
- **Description**: Fast, customizable vulnerability scanner for applications, APIs, networks, DNS, and cloud configurations
- **License**: MIT
- **Maturity**: Mature (actively maintained)
- **Install & Use**: Download binary from releases page. Run with `./nuclei -u target-url`
- **What I saw when trying it**: Successfully displayed version and help information
- **Verdict**: Excellent tool for vulnerability scanning, widely adopted and actively maintained

### Grype
- **Name**: Grype
- **Link**: https://github.com/anchore/grype
- **Description**: Vulnerability scanner for container images, filesystems, and SBOMs
- **License**: Apache 2.0
- **Maturity**: Mature (actively maintained)
- **Install & Use**: Download binary from releases page. Run with `./grype <image|path>`
- **What I saw when trying it**: Successfully displayed version and help information, and could scan files with proper input format
- **Verdict**: Excellent tool for vulnerability scanning of software artifacts, widely adopted and actively maintained

## Usage

All tools are located in the `kits/` directory under their respective class names.