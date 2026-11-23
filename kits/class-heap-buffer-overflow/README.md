# Heap Buffer Overflow

This folder contains resources related to heap buffer overflow vulnerabilities, a persistent class of memory safety issues.

## Files

- `FORESIGHT.md`: Overview of the vulnerability pattern and analysis.
- `check_exposure.sh`: Script to inventory tools that may parse untrusted data.
- `detection_rules/`: Sigma, YARA, and Suricata rules for detecting heap buffer overflow behavior.

## Testing

Run the exposure check script:

```bash
./check_exposure.sh
```

This will list tools on the PATH and installed Debian packages related to heap parsing.