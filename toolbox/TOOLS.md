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
- **Description**: Scripts to detect exposure of Netis WF2409E routers to a remote authentication flaw (CVE-2026-136136)
- **Files**:
  - `check_exposure.sh`: Shell script to inventory local TCP listeners
  - `check_exposure.py`: Python version of the exposure check
  - `mitigate.sh`: Mitigation guidance script
  - `detection/sigma/netis-wf2409e-auth-flaw.yml`: Sigma rule for detection

## Usage

To use these tools, run the scripts against your systems:

```bash
# Check for exposure
bash kits/netis-wf2409e-remote-authentication-flaw-has-a-r/check_exposure.sh
python3 kits/netis-wf2409e-remote-authentication-flaw-has-a-r/check_exposure.py

# View mitigation plan
bash kits/netis-wf2409e-remote-authentication-flaw-has-a-r/mitigate.sh
```

The Sigma rule can be used in your SIEM or log analysis system.