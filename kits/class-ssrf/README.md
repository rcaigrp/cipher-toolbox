# Server-Side Request Forgery (SSRF) defense kit

`FORESIGHT.md` documents the vulnerability class, review targets, early warning signs, hardening, and two Splunk hunts. `detection.yml` is an experimental Sigma rule for application telemetry that records potential SSRF attempts. `ssrf_check.py` is a read-only exposure inventory script for Python source code.

## Read-only exposure inventory

Run with Python 3 and pass the local Python source files to review:

```sh
python3 ssrf_check.py path/to/validator.py path/to/router.py
```

The checker parses source without importing it or making network requests. It identifies direct calls to HTTP request functions and checks if any arguments come from user input functions like `input()`, `get()`, or `request()` methods. For each potential SSRF vulnerability found, the script reports the file path, line number, and function name.

Exit status 1 means at least one file could not be read or parsed.

For the hunts, map the fields documented in `detection.yml`, set the application index, and establish per-route baselines. Correlate limit events with worker CPU, queue delay, and request errors to prioritize investigation.