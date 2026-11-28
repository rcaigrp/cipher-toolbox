#!/usr/bin/env python3

import re
import sys

def check_weak_random_usage(file_path):
    """Check for weak random number usage in a file."""
    weak_patterns = [
        r'\b(rand|random)\s*\(\s*\)',
        r'\bgetrandom\b',
        r'\bsrand\b'
    ]

    with open(file_path, 'r') as f:
        content = f.read()

    found_issues = []
    for pattern in weak_patterns:
        matches = re.finditer(pattern, content)
        for match in matches:
            line_num = content[:match.start()].count('\n') + 1
            found_issues.append(f"Line {line_num}: Found potential weak random usage: {match.group()}")

    return found_issues

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_weak_random.py <file_path>")
        sys.exit(1)

    issues = check_weak_random_usage(sys.argv[1])
    if issues:
        for issue in issues:
            print(issue)
        sys.exit(1)
    else:
        print("No weak random usage detected.")