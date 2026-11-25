#!/usr/bin/env python3
"""
Directory Traversal Exposure Check Script
This script identifies potential directory traversal vulnerabilities in file handling code.
"""

import argparse
import os
import re

def check_directory_traversal_patterns(file_path):
    """
    Check a file for common directory traversal patterns
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Patterns that indicate potential directory traversal issues
        patterns = [
            r'(\.\./)',
            r'(\.\.\\)',
            r'\b(?:os\.)?path\.join.*\.\.',
            r'file\.open.*\.\.',
            r'open.*\.\.',
            r'load.*\.\.',
            r'read.*\.\.',
        ]
        
        findings = []
        for pattern in patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                line_number = content[:match.start()].count('\n') + 1
                findings.append({
                    'file': file_path,
                    'line': line_number,
                    'pattern': pattern,
                    'match': match.group()
                })
        
        return findings
    
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

def scan_directory(directory):
    """
    Scan a directory for files that might contain directory traversal issues
    """
    potential_issues = []
    
    # Common file extensions to check
    extensions = ['.py', '.js', '.php', '.java', '.cpp', '.c', '.go', '.rb', '.pl']
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                file_path = os.path.join(root, file)
                issues = check_directory_traversal_patterns(file_path)
                potential_issues.extend(issues)
    
    return potential_issues

def main():
    """
    Main function to run the directory traversal exposure check
    """
    parser = argparse.ArgumentParser(description=__doc__.strip())
    parser.add_argument('directory', help='directory containing source files to scan')
    scan_dir = parser.parse_args().directory
    if not os.path.isdir(scan_dir):
        parser.error(f'{scan_dir!r} is not a directory')

    print(f"Scanning {scan_dir} for directory traversal patterns...")
    
    issues = scan_directory(scan_dir)
    
    if issues:
        print(f"\nFound {len(issues)} potential directory traversal issues:")
        for issue in issues:
            print(f"  File: {issue['file']}")
            print(f"  Line: {issue['line']}")
            print(f"  Pattern: {issue['pattern']}")
            print(f"  Match: {issue['match']}")
            print()
    else:
        print("No directory traversal patterns found.")

if __name__ == "__main__":
    main()