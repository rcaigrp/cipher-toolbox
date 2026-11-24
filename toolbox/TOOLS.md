# Toolbox: Security Research Tools

## Overview

This directory contains defensive tools and scripts developed by Cipher for security research and defense.

## Tools

### 1. OOB Read Exposure Checker

- **Location**: `kits/class-oob-read/check_exposure.py`
- **Purpose**: Checks if systems are exposed to out-of-bounds read vulnerabilities
- **Usage**: Run the script to detect vulnerable libraries on the system

### 2. Tabbycat Tournament API Defense Kit

- **Location**: `kits/tabbycat-2-9-0-through-2-12-1-permits-unauthenti/`
- **Purpose**: Detects and mitigates unauthorized access to Tabbycat tournament API
- **Usage**: 
  - `check_exposure.sh` or `check_exposure.py`: Check if deployment is vulnerable to CVE-2026-135429
  - `mitigate.sh`: Install Nginx guard to block unauthorized access
  - Detection rules: Sigma and YARA rules for monitoring
- **Examples**:
  ```bash
  ./check_exposure.sh
  ./check_exposure.py --version 2.10.0
  ./mitigate.sh --nginx-include /etc/nginx/conf.d/tabbycat-guard.conf --apply
  ```

## CATALOG.md

A catalog of open-source defensive tools and resources.