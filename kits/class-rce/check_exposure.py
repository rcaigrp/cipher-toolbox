#!/usr/bin/env python3
"""
Security script to check for RCE exposure patterns in code.
"""

import argparse
import os
import re

def find_unsafe_patterns(directory):
    """Find potential unsafe patterns that could lead to RCE."""
    unsafe_patterns = [
        r'eval\s*\(',
        r'exec\s*\(',
        r'(?<![\w.])system\s*\(',
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
    parser = argparse.ArgumentParser(description="Check source files for potential RCE exposure patterns.")
    parser.add_argument("directory", help="directory containing source files to scan")
    args = parser.parse_args()
    if not os.path.isdir(args.directory):
        parser.error(f"{args.directory!r} is not a directory")

    findings = find_unsafe_patterns(args.directory)
    if not findings:
        print("No potential RCE exposure patterns found.")
        return

    print("Potential RCE exposure patterns found:")
    for finding in findings:
        print(f"File: {finding['file']}, Line: {finding['line']}")
        print(f"Pattern: {finding['pattern']}")
        print(f"Match: {finding['match']}")
        print("---")


if __name__ == "__main__":
    main()
