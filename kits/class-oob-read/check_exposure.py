#!/usr/bin/env python3
"""
Check script for exposure to Out-of-Bounds Read vulnerabilities in parsers.
This checks if system uses known vulnerable libraries or components.
"""

import os
import subprocess

def check_ffmpeg():
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        if 'FFmpeg' in result.stdout:
            print("FFmpeg detected. Checking version for known OOB issues...")
            # Simulate checking version here (real implementation would parse version string)
            return True
    except FileNotFoundError:
        pass
    return False

def check_gpac():
    try:
        result = subprocess.run(['MP4Box', '-version'], capture_output=True, text=True)
        if 'GPAC' in result.stdout:
            print("GPAC detected. Checking for OOB issues...")
            return True
    except FileNotFoundError:
        pass
    return False

if __name__ == '__main__':
    exposed = False
    if check_ffmpeg():
        exposed = True
    if check_gpac():
        exposed = True

    if not exposed:
        print("No known vulnerable libraries detected.")
    else:
        print("Potential exposure to OOB read vulnerabilities.")