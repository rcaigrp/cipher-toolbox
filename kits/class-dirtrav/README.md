# Directory Traversal Vulnerability Class

This kit provides resources for detecting and defending against directory traversal vulnerabilities.

## Files

- `FORESIGHT.md`: Analysis of the directory traversal vulnerability class
- `detect.yml`: Sigma rule for detecting directory traversal attempts
- `check_exposure.py`: Script to check code for potential directory traversal issues

## Usage

1. **Detection**: Use the Sigma rule in your SIEM to detect directory traversal attempts
2. **Exposure Check**: Run the Python script to scan code for potential directory traversal patterns:
   ```bash
   python check_exposure.py /path/to/scan
   ```

## Related CVEs and ZDIs

- ZDI-26-1099: NVIDIA AIStore Object Rename Directory Traversal
- ZDI-26-1097: NVIDIA AIStore ht Server-Side Request Forgery
- ZDI-26-1093 to ZDI-26-1087: Bosch Rexroth IndraWorks directory traversal issues
- ZDI-26-1104: NVIDIA Megatron Bridge Weight Map Directory Traversal
- ZDI-26-1094: NVIDIA NeMo Framework nemo File Parsing Directory Traversal
- CVE-2026-132165: Critical Drupal installer flaw