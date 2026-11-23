#!/usr/bin/env python3

import os
import subprocess

def check_vulnerable_libraries():
    # List of known vulnerable libraries (this would be expanded)
    vulnerable_libs = [
        'libytnef',
        'libmp4v2',
        'ffmpeg',
        'gstreamer'
    ]

    installed_libs = []
    
    # Check if libraries are installed
    for lib in vulnerable_libs:
        try:
            result = subprocess.run(['dpkg', '-l', lib], capture_output=True, text=True)
            if 'ii' in result.stdout:
                installed_libs.append(lib)
        except Exception as e:
            print(f"Error checking {lib}: {e}")

    return installed_libs

def main():
    exposed_libs = check_vulnerable_libraries()
    if exposed_libs:
        print("Exposed to OOB read class via libraries:", ", ".join(exposed_libs))
    else:
        print("No known vulnerable libraries detected.")

if __name__ == "__main__":
    main()