# IOC Hash Sweep

## Purpose

This tool scans a local directory recursively for files whose SHA-256 hashes match a provided list of indicators of compromise (IOCs). It's designed to be run in read-only mode by default, with no actions taken beyond reporting matches.

## Usage

```bash
python3 ioc_hash_sweep.py --hashes <indicators_file> <directory>
```

- `--hashes`: Path to a UTF-8 file containing one SHA-256 hash per line (comments allowed after #)
- `<directory>`: Local directory to scan recursively

## Features

- Recursively scans directories
- Reports matching files with their full paths and hashes
- Safe by default; no modifications or actions taken
- Handles errors gracefully and reports them

## Example

```bash
python3 ioc_hash_sweep.py --hashes /path/to/iocs.txt /home/user/software
```

This will scan `/home/user/software` for files matching any hash in `/path/to/iocs.txt`.

## Test

The tool was tested with a sample file and indicators list, confirming it correctly identifies matches.