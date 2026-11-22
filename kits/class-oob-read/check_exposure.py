#!/usr/bin/env python3
"""
Read-only check script for exposure to Out-of-Bounds Read vulnerability class.
This script checks for known vulnerable libraries in the system.
"""

import os
import subprocess
import sys

def check_vulnerable_libraries():
    """Check for known vulnerable parser libraries."""
    vulnerable_libs = [
        'libavcodec',
        'libavformat',
        'ffmpeg',
        'gpac',
        'libpng',
        'libjpeg',
        'libtiff'
    ]
    
    found_vulns = []
    
    # Check installed packages
    try:
        result = subprocess.run(['dpkg', '-l'], capture_output=True, text=True)
        for lib in vulnerable_libs:
            if lib in result.stdout.lower():
                found_vulns.append(lib)
    except Exception as e:
        print(f"Error checking packages: {e}")
    
    # Check running processes that might use parsers
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        for lib in vulnerable_libs:
            if lib in result.stdout.lower():
                found_vulns.append(f"Running process using {lib}")
    except Exception as e:
        print(f"Error checking processes: {e}")
    
    return list(set(found_vulns))

def main():
    print("Checking for Out-of-Bounds Read vulnerability exposure...")
    vulns = check_vulnerable_libraries()
    
    if vulns:
        print("Vulnerable components detected:")
        for vuln in vulns:
            print(f"  - {vuln}")
        return 1
    else:
        print("No vulnerable components detected.")
        return 0

if __name__ == "__main__":
    sys.exit(main())