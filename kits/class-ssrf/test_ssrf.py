#!/usr/bin/env python3
"""Test script for SSRF checker"""

import tempfile
import os
import subprocess

def test_ssrf_check():
    # Create a temporary Python file with potential SSRF vulnerability
    test_code = '''
import requests
def test():
    user_input = input("Enter URL: ")
    response = requests.get(user_input)
    return response
'''

    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        fname = f.name

    try:
        # Run the SSRF check on the test file
        result = subprocess.run(['python3', 'kits/class-ssrf/ssrf_check.py', fname], 
                               capture_output=True, text=True, cwd='.')
        
        print(f'Return code: {result.returncode}')
        print(f'Stdout lines: {result.stdout.splitlines()}')
        print(f'Stderr: {result.stderr}')
        
        # The script should detect the SSRF vulnerability
        if result.returncode == 1 and 'Potential SSRF vulnerability' in result.stdout:
            print("✓ SSRF detection working correctly")
            return True
        else:
            print("✗ SSRF detection not working as expected")
            return False
            
    finally:
        os.unlink(fname)

if __name__ == '__main__':
    test_ssrf_check()