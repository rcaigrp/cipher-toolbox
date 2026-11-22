#!/usr/bin/env python3
"""
Check script for exposure to Out-of-Bounds Read vulnerabilities in parsers.
This script identifies potential exposure by checking for usage of known vulnerable libraries.
"""

import subprocess
import sys
import os

def check_vulnerable_libraries():
    """Check if system has known vulnerable parser libraries installed."""
    
    # Common vulnerable library patterns (this is a simplified example)
    vulnerable_libs = [
        'libxml2',
        'libxslt',
        'libjson-c',
        'libyaml',
        'ghostscript',
        'gpac'
    ]
    
    found_vulnerable = []
    
    try:
        # Check installed packages
        result = subprocess.run(['dpkg', '-l'], capture_output=True, text=True)
        
        for lib in vulnerable_libs:
            if lib in result.stdout:
                found_vulnerable.append(lib)
                
    except Exception as e:
        print(f"Error checking packages: {e}")
        return []
    
    return found_vulnerable

if __name__ == "__main__":
    print("Checking for Out-of-Bounds Read vulnerability exposure...")
    
    vulnerable_libs = check_vulnerable_libraries()
    
    if vulnerable_libs:
        print(f"Found potentially vulnerable libraries: {', '.join(vulnerable_libs)}")
        sys.exit(1)  # Exit with error code to indicate exposure
    else:
        print("No known vulnerable parser libraries detected.")
        sys.exit(0)