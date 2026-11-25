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
        r'os\.system\s*\(',
        r'subprocess\.call\s*\(',
        r'subprocess\.run\s*\(',
        r'pickle\.loads?\s*\(',
        r'yaml\.load\s*\(',
        r'json\.loads?\s*\(',
        r'importlib\.import_module\s*\(',
        r'response\.render\s*\(',
        r'eval\s*\(\s*request\.',
        r'exec\s*\(\s*request\.',
        r'os\.system\s*\(\s*request\.',
        r'subprocess\.call\s*\(\s*request\.',
        r'subprocess\.run\s*\(\s*request\.',
        r'pickle\.loads?\s*\(\s*request\.',
        r'yaml\.load\s*\(\s*request\.',
        r'json\.loads?\s*\(\s*request\.',
        r'importlib\.import_module\s*\(\s*request\.',
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
                            line_num = content[:match.start()].count('\n') + 1
                            findings.append({
                                'file': filepath,
                                'line': line_num,
                                'pattern': pattern,
                                'context': content[max(0, match.start()-20):match.end()+20]
                            })
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")
    
    return findings

if __name__ == "__main__":
    # This would be run against codebases or configurations
    print("RCE Exposure Check Script - Demo")
    print("This is a simplified check for demonstration purposes.")
    print("In practice, this would scan actual code repositories.")