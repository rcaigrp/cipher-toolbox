# Command Injection Detection Kit

This kit provides tools and techniques for detecting command injection vulnerabilities in systems.

## Contents

- `FORESIGHT.md`: Analysis of the command injection vulnerability class
- `check_exposure.sh`: Script to check for exposure to command injection patterns
- `detections/`: Detection rules for Sigma and YARA

## Usage

1. Run `check_exposure.sh` to identify potential command injection patterns in your codebase
2. Implement the detection rules in your security infrastructure
3. Review `FORESIGHT.md` for understanding of the vulnerability class and mitigation strategies

## Scanner options

Run `./check_exposure.sh --help` for usage. Run `./check_exposure.sh [directory]` to scan shell scripts under the given directory, which defaults to the current directory. Findings show a file path and line number for review.

## Testing

Run `bash test_check_exposure.sh` from the kit directory. The test scans temporary sample files as text.
