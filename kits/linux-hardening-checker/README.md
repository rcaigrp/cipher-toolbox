# Linux Hardening Checker

This tool performs a basic check of common Linux system hardening configurations. It verifies settings that help protect against common attack vectors and security misconfigurations.

## Usage

```bash
python3 linux_hardening_checker.py --help
python3 linux_hardening_checker.py
```

The script will check various system configurations and report any issues found. It runs in read-only mode by default, with no changes made to the system.

## Features

- Checks for proper sysctl settings
- Verifies file permissions and ownership
- Reviews SSH configuration
- Validates kernel parameters
- Checks for unnecessary services
- Reviews network configurations

## Installation

This tool requires Python 3 and standard library modules only.

## How It Works

The checker examines system configurations against security best practices. It performs checks without making changes to the system, providing a report of any issues found.

## Testing

Run `python3 linux_hardening_checker.py` with no arguments to perform a basic check.