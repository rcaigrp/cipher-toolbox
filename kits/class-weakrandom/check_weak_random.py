#!/usr/bin/env python3

import re
import sys
import argparse

def check_weak_random_usage(file_path):
    """Check for weak random number usage in a file."""
    # Patterns that detect weak random number generation functions
    weak_patterns = [
        r'\b(rand|random|srand|getrandom)\s*\(\s*\)',
        r'\brandom\s*\.\s*(randint|random|uniform)\b',
        r'\bMath\s*\.\s*(random)\b'
    ]

    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{file_path}': {e}")
        sys.exit(1)

    found_issues = []
    for pattern in weak_patterns:
        matches = re.finditer(pattern, content, re.IGNORECASE)
        for match in matches:
            line_num = content[:match.start()].count('\n') + 1
            found_issues.append(f"Line {line_num}: Found potential weak random usage: {match.group()}")

    return found_issues

def main():
    parser = argparse.ArgumentParser(
        description="Check for weak random number generation usage in source code",
        prog="check_weak_random.py"
    )
    parser.add_argument("file_path", help="Path to the source file to check")
    
    args = parser.parse_args()
    
    issues = check_weak_random_usage(args.file_path)
    if issues:
        for issue in issues:
            print(issue)
        sys.exit(1)
    else:
        print("No weak random usage detected.")

if __name__ == "__main__":
    main()