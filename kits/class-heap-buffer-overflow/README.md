# Heap Buffer Overflow Exposure Checker

## Purpose

This tool detects potential heap buffer overflow vulnerabilities in software by scanning source code files for unsafe patterns that could lead to memory corruption.

## Usage

```bash
python3 check_heap_exposure.py [--apply] <directory>
```

- `--apply`: Apply actions (default is read-only)
- `<directory>`: Directory to scan (defaults to current directory)

## Features

- Scans C/C++ source files (.c, .cpp, .cc, .h, .hpp)
- Detects unsafe functions like `strcpy`, `memcpy`, `gets`, etc.
- Reports line numbers and matching patterns
- Safe by default; use `--apply` to take actions (logging/quarantining)

## Example

```bash
python3 check_heap_exposure.py /home/user/software
```

This will scan the `/home/user/software` directory for unsafe memory operations and report any findings.

## Test

The script was tested with a sample file containing known unsafe patterns and confirmed to correctly identify them.