#!/usr/bin/env python3
"""
Security script to check for RCE exposure patterns in code.
This is a simplified version for demonstration purposes.
"""

import os
import re

def find_unsafe_patterns(directory):
    """Find potential unsafe patterns that could lead to RCE."""
    unsafe_patterns = [
        r'eval\s*\(',
        r'exec\s*\(',
        r'system\s*\(',
        r'shell\s*\(',
        r'os\.system\s*\(',
        r'os\.popen\s*\(',
        r'subprocess\.call\s*\(',
        r'subprocess\.run\s*\(',
        r'subprocess\.Popen\s*\(',
        r'pickle\.loads\s*\(',
        r'pickle\.load\s*\(',
        r'json\.loads\s*\(',
        r'yaml\.load\s*\(',
        r'yaml\.full_load\s*\(',
        r'xml\.etree\.ElementTree\.parse\s*\(',
        r'xml\.minidom\.parseString\s*\(',
        r'base64\.decode\s*\(',
        r'importlib\.import_module\s*\(',
        r'__import__\s*\(',
        r'globals\s*\(\)',
        r'locals\s*\(\)',
        r'compile\s*\(',
        r'execfile\s*\(',
        r'open\s*\(',
        r'eval\s*\(',
        r'exec\s*\(',
        r'filter\s*\(',
        r'map\s*\(',
        r'reduce\s*\(',
    ]
    
    findings = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    for pattern in unsafe_patterns:
                        matches = re.finditer(pattern, content)
                        for match in matches:
                            line_number = content[:match.start()].count('\n') + 1
                            findings.append({
                                'file': filepath,
                                'line': line_number,
                                'pattern': pattern,
                                'match': match.group()
                            })
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")
    
    return findings

def main():
    """Main function to demonstrate the check."""
    # For demonstration, we'll create a test file with some unsafe patterns
    test_code = '''
import os
import pickle
import subprocess

def unsafe_function(user_input):
    # This is an example of potentially dangerous code
    result = eval(user_input)
    system_call = os.system("echo " + user_input)
    pickled_data = pickle.loads(user_input)
    subproc = subprocess.call(user_input)
    return result
'''
    
    with open('/tmp/test_rce.py', 'w') as f:
        f.write(test_code)
    
    # Check the test file
    findings = find_unsafe_patterns('/tmp')
    
    if findings:
        print("Potential RCE exposure patterns found:")
        for finding in findings:
            print(f"File: {finding['file']}, Line: {finding['line']}")
            print(f"Pattern: {finding['pattern']}")
            print(f"Match: {finding['match']}")
            print("---")
    else:
        print("No potential RCE exposure patterns found.")

if __name__ == "__main__":
    main()