# Cipher Toolbox

This is a catalog of defensive tools built by Cipher for the lab.

## Authentication Bypass Detection Kit

- **Location**: `kits/class-auth-bypass/`
- **Description**: A set of detection rules and scripts to identify authentication bypass vulnerabilities in systems.
- **Files**:
  - `FORESIGHT.md`: Analysis of the authentication bypass class
  - `detection.yml`: Sigma rule for detecting auth bypass attempts
  - `check_exposure.py`: Script to check for exposed API endpoints

## Netis WF2409E Exposure Check Kit

- **Location**: `kits/netis-wf2409e-remote-authentication-flaw-has-a-r/`
- **Description**: Local TCP listener inventory and dry-run mitigation guidance for reviewing Netis WF2409E management exposure
- **Files**:
  - `check_exposure.sh`: Shell script to inventory local TCP listeners
  - `check_exposure.py`: Python version of the exposure check
  - `mitigate.sh`: Mitigation guidance script
  - `detection/sigma/netis-wf2409e-auth-flaw.yml`: Sigma rule for detection
  - `detection/yara/netis-wf2409e-exploit.yar`: YARA rule for identifying Netis WF2409E inventory markers in local artifacts

## CISA NVD Checker

- **Location** `toolbox/cisa-nvd-checker/`
- **Purpose** Triage CPE 2.3 inventory against local NVD CVE 2.0 snapshots and prioritize findings listed in a local CISA KEV snapshot. Review version ranges and configuration conditions against the advisory.
- **Usage** From the tool directory, run `python3 cisa_nvd_checker.py --inventory inventory.json --kev kev.json --nvd nvd.json`. The checker uses the Python standard library, reads local files, and prints JSON to stdout.
- **Tests** Run `python3 test_checker.py` from the tool directory. The included fixtures use synthetic advisory IDs and products.

## Sigma Rule Engine
- **Location**: `toolbox/try/sigma/`
- **Description**: A generic and open signature format for SIEM systems to detect malicious patterns
- **Files**:
  - `README.md`: Installation and usage instructions
  - `test-rule.yml`: Sample Sigma rule for testing
- **Install & Use**: Install with `pip install sigma-cli` and `pip install pysigma-backend-splunk pysigma-backend-loki`. Run `sigma convert` to convert rules into target query languages.
- **Verdict**: Excellent tool for defensive detection, widely adopted and actively maintained.

## YARA Rule Engine
- **Location**: `toolbox/try/yara/`
- **Description**: The pattern matching swiss knife for malware researchers and security professionals
- **Files**:
  - `README.md`: Installation and usage instructions
  - `test.rules`: Sample YARA rules for testing
- **Install & Use**: Install with `pip install yara`. Run `yara` commands to scan files or compile rules.
- **Verdict**: Excellent tool for defensive detection, widely adopted and actively maintained.

## Usage

To use these tools, run the scripts against your systems:

```bash
# Inventory local HTTP(S) listeners
bash kits/netis-wf2409e-remote-authentication-flaw-has-a-r/check_exposure.sh
python3 kits/netis-wf2409e-remote-authentication-flaw-has-a-r/check_exposure.py

# View mitigation plan
bash kits/netis-wf2409e-remote-authentication-flaw-has-a-r/mitigate.sh
```

The Sigma rule can be used in your SIEM or log analysis system.