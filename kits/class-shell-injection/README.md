# Shell Injection Class Kit

This kit provides defensive resources for identifying and mitigating shell injection vulnerabilities.

## Contents

- `FORESIGHT.md`: Analysis of the shell injection vulnerability class, including patterns, variant analysis, and early warning signs
- `check_exposure.sh`: A read-only script to identify potential shell injection patterns in bash scripts
- `detections/`: Detection rules for shell injection attempts:
  - Sigma rule for command-line pattern detection
  - YARA rule for shell injection pattern matching

## Usage

1. Run `check_exposure.sh` to scan for potential shell injection patterns in your codebase
2. Implement the recommendations from `FORESIGHT.md` to harden against shell injection
3. Deploy the detection rules to monitor for actual exploitation attempts

## Important Notes

This kit is for defensive purposes only. It does not contain exploit code or attempt to scan external systems.

## Scanner options

Run `./check_exposure.sh --help` for usage. Run `./check_exposure.sh [directory]` to scan shell scripts under the given directory, which defaults to the current directory. Findings show a file path and line number for review.

## Testing

Run `bash test_check_exposure.sh` from the kit directory. The test scans temporary sample files as text.
