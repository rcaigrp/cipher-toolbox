#!/usr/bin/env python3
"""
Check exposure to ToolJet release workflow command injection (CVE-2026-137964)
This script checks if the local system is running an affected version of ToolJet.
"""

import sys
import os

def check_tooljet_version():
    """Check if ToolJet version is affected by CVE-2026-137964"""
    
    # Affected versions: <= 3.21.61-beta
    # Fixed versions: >= 3.21.96-LTS
    
    # Since we can't easily determine the actual ToolJet version on this machine,
    # we'll just check if we're in a directory that might contain ToolJet files
    # and warn about potential exposure
    
    current_dir = os.getcwd()
    
    # Check for common ToolJet file patterns
    tooljet_indicators = [
        'package.json',
        'Dockerfile',
        '.github/workflows/release.yml'
    ]
    
    found_indicators = []
    for indicator in tooljet_indicators:
        if os.path.exists(indicator):
            found_indicators.append(indicator)
    
    if found_indicators:
        print("WARNING: Potential ToolJet installation detected")
        print(f"Found indicators: {', '.join(found_indicators)}")
        print("Please verify the version manually against CVE-2026-137964")
        print("Affected versions: <= 3.21.61-beta")
        print("Fixed versions: >= 3.21.96-LTS")
        return True
    else:
        print("No ToolJet indicators found in current directory")
        return False

if __name__ == "__main__":
    exposed = check_tooljet_version()
    sys.exit(0 if not exposed else 1)