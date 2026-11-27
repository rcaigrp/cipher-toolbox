# Linux Hardening Checker

Review six Linux sysctl settings and the ownership and permissions of `/etc/passwd`, `/etc/group`, and `/etc/shadow`. The checker reads local sysctl values and file metadata without changing the host or reading account file contents.

## Installation

Use Python 3 on Linux. The checker uses only the standard library. Run it as your regular user.

## Usage

From the repository root, run:

```bash
cd toolbox/linux-hardening-checker
python3 linux_hardening_checker.py --help
python3 linux_hardening_checker.py
```

To check an existing local fixture tree containing `proc/sys` or `etc`, supply its path:

```bash
python3 linux_hardening_checker.py --root /path/to/local/fixture
```

- `PASS` means the observed value or metadata meets the check's criteria.
- `REVIEW` means the observed setting needs review against your host policy.
- `UNKNOWN` means the setting was missing, unreadable, or invalid.

The CLI prints one line per check. Review the reported statuses even when the command exits successfully.

## Tests

```bash
python3 -m unittest -v test_linux_hardening_checker
```

The tests use temporary local fixtures to cover accepted, unexpected, invalid, and missing sysctl values, file metadata and symlinks, and CLI output for a fixture root.
