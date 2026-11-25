#!/usr/bin/env python3
"""
Security script to check for SSRF exposure patterns in code.
This is a simplified version for demonstration purposes.
"""

import os
import re

def find_unsafe_patterns(directory):
    """Find potential unsafe patterns that could lead to SSRF."""
    unsafe_patterns = [
        r'requests\.get\s*\(',
        r'urllib\.request\.urlopen\s*\(',
        r'httpx\.get\s*\(',
        r'socket\.create_connection\s*\(',
        r'urllib3\.PoolManager\s*\(',
        r'httplib\.HTTPConnection\s*\(',
        r'requests\.post\s*\(',
        r'httpx\.post\s*\(',
        r'urllib\.request\.Request\s*\(',
        r'urllib3\.make_headers\s*\(',
        r'requests\.request\s*\(',
        r'httpx\.request\s*\(',
        r'urllib3\.ConnectionPool\s*\(',
        r'socket\.socket\s*\(',
        r'urllib\.parse\.urljoin\s*\(',
        r'urllib\.parse\.urlparse\s*\(',
        r'requests\.Session\s*\(',
        r'httpx\.Client\s*\(',
        r'urllib3\.connection_from_url\s*\(',
        r'urllib\.request\.build_opener\s*\(',
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
                except (UnicodeDecodeError, PermissionError):
                    # Skip files that can't be read
                    continue
    
    return findings

def find_url_handling_patterns(directory):
    """Find patterns related to URL handling that might be vulnerable to SSRF."""
    url_patterns = [
        r'urllib\.parse\.urljoin\s*\(',
        r'urllib\.parse\.urlparse\s*\(',
        r'requests\.get\s*\(\s*.*url.*\)',
        r'httpx\.get\s*\(\s*.*url.*\)',
        r'urllib3\.make_headers\s*\(',
        r'urllib3\.connection_from_url\s*\(',
        r'requests\.request\s*\(\s*.*url.*\)',
        r'httpx\.request\s*\(\s*.*url.*\)',
    ]
    
    findings = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    for pattern in url_patterns:
                        matches = re.finditer(pattern, content)
                        for match in matches:
                            line_number = content[:match.start()].count('\n') + 1
                            findings.append({
                                'file': filepath,
                                'line': line_number,
                                'pattern': pattern,
                                'match': match.group()
                            })
                except (UnicodeDecodeError, PermissionError):
                    # Skip files that can't be read
                    continue
    
    return findings

def main():
    """Main function to check for SSRF exposure patterns."""
    print("Checking for potential SSRF exposure patterns...")
    
    # Check current directory
    current_dir = "."
    unsafe_findings = find_unsafe_patterns(current_dir)
    url_findings = find_url_handling_patterns(current_dir)
    
    all_findings = unsafe_findings + url_findings
    
    if not all_findings:
        print("No potential SSRF exposure patterns found.")
        return 0
    else:
        print(f"Found {len(all_findings)} potential SSRF exposure patterns:")
        for finding in all_findings:
            print(f"File: {finding['file']}, Line: {finding['line']}")
            print(f"Pattern: {finding['pattern']}")
            print(f"Match: {finding['match']}")
            print("-" * 50)
        return len(all_findings)

if __name__ == "__main__":
    main()