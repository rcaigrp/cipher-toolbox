# File Parsing Vulnerability Class

This kit contains detection rules, check scripts, and analysis for the file parsing vulnerability class that affects image processing software.

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

- ZDI-26-1014: Krita TIFF File Parsing Out-Of-Bounds Write
- ZDI-26-1013: Krita PSB File Parsing Integer Overflow
- ZDI-26-1012: Krita ASL File Parsing Integer Overflow
- ZDI-26-1011: Krita ABR File Parsing Heap-based Buffer Overflow
- ZDI-26-1010: Krita JC2 File Parsing Heap-based Buffer Overflow