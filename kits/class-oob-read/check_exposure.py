#!/usr/bin/env python3
"""
Check for exposure to Out-of-Bounds Read vulnerabilities in parsers.
This script tests the current system for known vulnerable components.
"""

import subprocess
import sys

def check_parser_exposure():
    """Check if any known vulnerable parser libraries are installed."""
    vulnerable_libs = [
        "libgpac", 
        "ffmpeg",
        "nginx",
        "ghostscript"
    ]
    
    found_vulnerable = []
    
    for lib in vulnerable_libs:
        try:
            result = subprocess.run(["dpkg", "-l", lib], capture_output=True, text=True)
            if result.returncode == 0 and "ii" in result.stdout:
                found_vulnerable.append(lib)
        except Exception:
            pass
    
    return found_vulnerable

if __name__ == "__main__":
    vulnerable = check_parser_exposure()
    
    if vulnerable:
        print("WARNING: Found potentially vulnerable parser libraries:")
        for lib in vulnerable:
            print(f"  - {lib}")
        sys.exit(1)
    else:
        print("No known vulnerable parser libraries detected.")
        sys.exit(0)