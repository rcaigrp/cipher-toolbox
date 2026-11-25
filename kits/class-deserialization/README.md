# Deserialization Vulnerability Class

This kit contains detection rules, check scripts, and analysis for the deserialization vulnerability class that affects software components that deserialize untrusted data.

## Files

- `FORESIGHT.md`: Analysis of the vulnerability pattern and affected products
- `check_exposure.py`: Read-only script to check exposure to this class
- Detection rules:
  - Sigma rules for process monitoring
  - YARA rules for binary signature matching
  - Hunt queries for log analysis

## Usage

1. Run `check_exposure.py` to scan your system for exposure
2. Implement the detection rules in your security tools
3. Review the FORESIGHT.md for variant analysis and hardening recommendations

## References

- ZDI-26-1100: NVIDIA Megatron Dataset Cache Deserialization of Untrusted Data Remote Code Execution Vulnerability
- ZDI-26-1091: Bosch Rexroth IndraWorks MTX XIWP File Parsing Deserialization of Untrusted Data Remote Code Execution Vulnerability
- ZDI-26-1090: Bosch Rexroth IndraWorks MTX XIWP File Parsing Deserialization of Untrusted Data Remote Code Execution Vulnerability
- ZDI-26-1089: Bosch Rexroth IndraWorks MTX IWZ File Parsing Deserialization of Untrusted Data Remote Code Execution Vulnerability
- ZDI-26-1088: Bosch Rexroth IndraWorks XIWP File Parsing Deserialization Of Untrusted Data Remote Code Execution Vulnerability
- ZDI-26-1087: Bosch Rexroth IndraWorks XML Print Settings File Parsing Deserialization Of Untrusted Data Remote Code Execution Vulnerability
- ZDI-26-1086: Bosch Rexroth IndraWorks XIWP File Parsing Deserialization Of Untrusted Data Remote Code Execution Vulnerability