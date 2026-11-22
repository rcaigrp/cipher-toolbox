#!/usr/bin/env python3
"""
Read-only check script for OOB read vulnerability exposure.
This script identifies systems with parser libraries that may be vulnerable.
"""

import os
import subprocess
import sys

def check_parser_libraries():
    """Check for known parser libraries that might be vulnerable."""
    # Common vulnerable library patterns
    vulnerable_libs = [
        'libavformat',
        'libmp4',
        'ffmpeg',
        'gstreamer',
        'libreoffice',
        'pdfbox'
    ]
    
    found_vulnerable = []
    
    # Check for presence of vulnerable libraries
    try:
        result = subprocess.run(['ldd', '/usr/bin/ffmpeg'], capture_output=True, text=True)
        if result.returncode == 0:
            for lib in vulnerable_libs:
                if lib in result.stdout:
                    found_vulnerable.append(lib)
    except Exception as e:
        print(f"Error checking libraries: {e}")
    
    return found_vulnerable

def main():
    print("Checking for OOB read vulnerability exposure...")
    vulnerable = check_parser_libraries()
    
    if vulnerable:
        print(f"Found potentially vulnerable parser libraries: {', '.join(vulnerable)}")
        print("Recommendation: Review these libraries for known OOB read vulnerabilities.")
        return 1
    else:
        print("No vulnerable parser libraries detected in current system.")
        return 0

if __name__ == "__main__":
    sys.exit(main())