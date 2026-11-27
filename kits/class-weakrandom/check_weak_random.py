#!/usr/bin/env python3

import random
import secrets
import sys
import os
import re

# Check for weak PRNG usage in Python code
def check_weak_random_usage(filename):
    print(f"Checking {filename} for insecure random usage...")
    
    try:
        with open(filename, 'r') as f:
            content = f.read()
        
        # Patterns that indicate weak random usage
        weak_patterns = [
            r'\brandom\.randint\b',
            r'\brandom\.random\b', 
            r'\brandom\.choice\b',
            r'\brand\(\)',
            r'\bsrand\(\)'
        ]
        
        found_issues = []
        for pattern in weak_patterns:
            matches = re.findall(pattern, content)
            if matches:
                # Get line numbers
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    if re.search(pattern, line):
                        found_issues.append((i, line.strip()))
        
        if found_issues:
            print(f"Found weak random usage in {filename}:")
            for line_num, line_content in found_issues:
                print(f"  Line {line_num}: {line_content}")
            return True
        else:
            print(f"No weak random usage found in {filename}")
            return False
            
    except Exception as e:
        print(f"Error reading file {filename}: {e}")
        return False

def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        print("Usage: python3 check_weak_random.py [FILE]")
        print("Checks FILE for weak random number generation patterns.")
        print("If no FILE is provided, checks stdin or shows this help.")
        return
    
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        if os.path.exists(filename):
            check_weak_random_usage(filename)
        else:
            print(f"File {filename} not found")
    else:
        # Check stdin
        content = sys.stdin.read()
        if content.strip():
            print("Checking stdin for insecure random usage...")
            # Simple pattern matching on stdin
            weak_patterns = [
                r'\brandom\.randint\b',
                r'\brandom\.random\b', 
                r'\brandom\.choice\b',
                r'\brand\(\)',
                r'\bsrand\(\)'
            ]
            
            found_issues = []
            for pattern in weak_patterns:
                matches = re.findall(pattern, content)
                if matches:
                    # This is a simplified check - we don't have line numbers for stdin
                    found_issues.append(pattern)
            
            if found_issues:
                print("Found weak random usage in input:")
                for pattern in found_issues:
                    print(f"  {pattern}")
            else:
                print("No weak random usage found in input")
        else:
            print("Usage: python3 check_weak_random.py [FILE]")
            print("Checks FILE for weak random number generation patterns.")
            print("If no FILE is provided, checks stdin or shows this help.")

if __name__ == "__main__":
    main()