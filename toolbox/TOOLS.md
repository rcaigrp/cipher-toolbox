# Cipher Toolbox

This is a catalog of defensive tools built by Cipher for the lab.

## Authentication Bypass Detection Kit

- **Location**: `kits/class-auth-bypass/`
- **Description**: A set of detection rules and scripts to identify authentication bypass vulnerabilities in systems.
- **Files**:
  - `FORESIGHT.md`: Analysis of the authentication bypass class
  - `detection.yml`: Sigma rule for detecting auth bypass attempts
  - `check_exposure.py`: Script to check for exposed API endpoints

## Usage

To use these tools, run the Python script against your systems:

```bash
python3 kits/class-auth-bypass/check_exposure.py
```

The detection rules can be used in your SIEM or log analysis system.