# ReDoS defense kit

`FORESIGHT.md` documents the vulnerability class, review targets, early warning signs, hardening, and two Splunk hunts. `detection.yml` is an experimental Sigma rule for application telemetry that records regex evaluation timeouts or work-limit exhaustion on external input. Map the normalized fields to your application logs and validate the rule against synthetic events before deployment.

## Read-only exposure inventory

Run with Python 3 and pass the local Python source files to review:

```sh
python3 rl_check.py path/to/validator.py path/to/router.py
```

The checker parses source without importing it or running its regexes. It lists direct standard-library `re` call sites, including import aliases, and identifies literal and unresolved pattern arguments. For each result, trace the matched input to its source and record its maximum size, evaluation budget, and worker isolation. Review compiled-pattern methods, wrappers, and other regex engines separately. Import alias shadowing can produce false positives. An empty result provides no assurance of coverage. Exit status 1 means at least one file could not be read or parsed.

For the hunts, map the fields documented in `detection.yml`, set the application index, and establish per-route baselines. Correlate limit events with worker CPU, queue delay, and request errors to prioritize investigation.
