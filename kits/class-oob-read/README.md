# Out-of-Bounds Read Vulnerability Class Kit

This kit contains resources for detecting and defending against Out-of-Bounds Read vulnerabilities, a common class of memory safety issues in parsers.

## Contents

- `FORESIGHT.md`: Detailed analysis of the vulnerability class and its implications
- `check_exposure.py`: Read-only script to identify exposure to this vulnerability class
- `detection_rules/`: Detection rules for monitoring and hunting

## Usage

1. Run the exposure check script to identify vulnerable components:
   ```bash
   python3 check_exposure.py
   ```

2. Deploy the detection rules in your security infrastructure:
   - Sigma rules for SIEM systems
   - YARA rules for malware analysis
   - Hunt queries for endpoint detection

## Key Findings

This vulnerability class is prevalent in media processing libraries and document parsers, with many affected components identified on this system.

## References

- CVE-2026-130632: GPAC/MP4Box OOB Read
- CVE-2026-130634: GPAC/MP4Box Heap Buffer Overflow  
- CVE-2026-130793: GPAC/MP4Box Stack Buffer Overflow
- Re: CVE-2026-123633, CVE-2026-123007: nginx RCE via HTTP/2