# Linux Hardening Checker

This read-only tool reports selected Linux hardening settings. It requires Python 3 and uses only the standard library.

## Usage

```bash
python3 linux_hardening_checker.py --help
python3 linux_hardening_checker.py
```

By default, the checker reads settings from the local system. Use `--root ROOT` to read from a fixture directory with the same layout.

## Checks

- Selected sysctl values for kernel pointer exposure, kernel log access, address space randomization, hardlink and symlink protections, and IPv4 source routing.
- File type, root ownership, and permission bits for `/etc/passwd`, `/etc/group`, and `/etc/shadow`.

Each check reports `PASS` when the observed setting meets the check, `REVIEW` when it differs, or `UNKNOWN` when the setting cannot be read or interpreted.

## Testing

```bash
python3 test_linux_hardening_checker.py
```

The test builds a temporary sample filesystem and runs the checker with `--root` to verify `PASS`, `REVIEW`, and `UNKNOWN` results.
