#!/usr/bin/env python3
"""
check_heap_exposure.py: A defensive script to detect heap buffer overflow exposures in software.

This script checks for potential heap buffer overflow vulnerabilities by scanning a directory
for files that may contain known unsafe patterns (e.g., unchecked array accesses, unsafe string operations).
It's designed to be run in read-only mode by default, with an optional --apply flag to take actions like logging or quarantining.

Usage:
    python3 check_heap_exposure.py [--help] [--apply] <directory>

Example:
    python3 check_heap_exposure.py /home/user/software
"""

import os
import sys
import argparse
import re

# Unsafe patterns that could indicate heap buffer overflows
UNSAFE_PATTERNS = [
    r'\bmemcpy\s*\([^)]*\)',
    r'\bstrcpy\s*\([^)]*\)',
    r'\bstrncpy\s*\([^)]*\)',
    r'\bscanf\s*\([^)]*\)',
    r'\bfread\s*\([^)]*\)',
    r'\bgets\s*\([^)]*\)',
    r'\bgets_s\s*\([^)]*\)',
    r'\bstrcpy_s\s*\([^)]*\)',
    r'\bstrncpy_s\s*\([^)]*\)',
    r'\bmemcpy_s\s*\([^)]*\)',
    r'\bstrncat\s*\([^)]*\)',
    r'\bstrncat_s\s*\([^)]*\)',
    r'\bstrcat\s*\([^)]*\)',
    r'\bstrcat_s\s*\([^)]*\)',
    r'\bmemset\s*\([^)]*\)',
    r'\bmemmove\s*\([^)]*\)',
]

# File extensions to scan
FILE_EXTENSIONS = ['.c', '.cpp', '.cc', '.h', '.hpp']

def check_file(file_path):
    """Check a single file for unsafe patterns."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

    issues = []
    for pattern in UNSAFE_PATTERNS:
        matches = re.finditer(pattern, content)
        for match in matches:
            line_number = content[:match.start()].count('\n') + 1
            issues.append({
                'file': file_path,
                'line': line_number,
                'pattern': pattern,
                'match': match.group(0)
            })
    return issues

def scan_directory(directory):
    """Scan a directory for unsafe patterns in source code files."""
    issues = []
    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in FILE_EXTENSIONS):
                file_path = os.path.join(root, file)
                issues.extend(check_file(file_path))
    return issues

def main():
    parser = argparse.ArgumentParser(description='Check for heap buffer overflow exposures in software.')
    parser.add_argument('--apply', action='store_true', help='Apply actions (default: read-only)')
    parser.add_argument('directory', nargs='?', default='.', help='Directory to scan')
    args = parser.parse_args()

    print(f"Scanning directory: {args.directory}")
    
    issues = scan_directory(args.directory)
    
    if not issues:
        print("No unsafe patterns found.")
        return

    print(f"\nFound {len(issues)} potential heap buffer overflow exposures:")
    for issue in issues:
        print(f"- File: {issue['file']}, Line: {issue['line']}, Pattern: {issue['pattern']}")
        if args.apply:
            # In a real-world scenario, this could log to a file or quarantine the file
            print("  (Action taken: logged to output)")
    return

if __name__ == '__main__':
    main()