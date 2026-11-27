# Predictable randomness in security tokens

Use this kit to review Perl code for weak randomness references and hunt for unusual token issuance or redemption activity.

## Local source inventory

```sh
./check_randomness.sh /path/to/local/source
./test_check.sh
```

The checker reads Perl source and dependency manifests and prints candidate file paths. It skips `.git` directories, makes no network requests, and executes no project code. Omitting the path checks the current directory. A successful run exits 0 even when it finds candidates. An invalid directory exits 2.

Trace each candidate to a reset link, invitation, session identifier, API token, or other security-sensitive value. Comments and nonsecurity uses can match. A clean scan leaves other languages, indirect generator calls, and deployed dependency versions for manual review.

## Files

- `FORESIGHT.md` covers the vulnerability class, historical cases, early signals, and preparation before disclosure.
- `HUNTS.md` defines the audit event fields and provides Kusto queries for duplicate issuance and redemption bursts.
- `sigma_rule.yml` correlates a repeated keyed token fingerprint across distinct issuance IDs within 24 hours. It requires application audit telemetry and a Sigma backend that supports `value_count` correlation. Validate the field mapping and time-window behavior in your backend before enabling alerts.
- `test_check.sh` exercises positive findings, a clean directory, Git exclusion, help, and invalid input using temporary fixtures.

Keep raw tokens and reset URLs out of audit logs. Predictable generators can issue unique tokens, so use source review alongside telemetry.
