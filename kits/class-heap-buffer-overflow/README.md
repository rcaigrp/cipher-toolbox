# Heap Buffer Overflow Class Analysis

This kit analyzes heap buffer overflows in file parsing components.

## Files

- `FORESIGHT.md` contains the analysis and its implications.
- `check_exposure.py` inventories common file parser processes and executables.
- `detection_rules/` contains detection rules for this vulnerability class.

## Usage

From the kit directory, run the read-only inventory on Linux with Python 3 and `ps`.

```bash
python3 check_exposure.py
python3 check_exposure.py --verbose
python3 check_exposure.py --help
```

The default output shows the total number of matching processes, the PID and command name of up to five matches, and the names of known parser executables available on `PATH`.

- `-v` or `--verbose` shows every matching process and the path of each available parser executable.
- `-h` or `--help` shows usage and exits.

The process check matches exact command names from a list of common CAD, PDF, office, and image tools. A match indicates parser presence. The inventory does not determine whether a process is actively parsing a file or whether it is vulnerable. The script exits with status 0 after a successful scan, including a scan with no matches, and status 1 if it cannot inspect the process list.
