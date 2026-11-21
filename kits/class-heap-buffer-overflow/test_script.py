#!/usr/bin/env python3

# Test script to verify the heap overflow check functionality

import re
import sys

def check_heap_overflow_exposure(log_file_path):
    """Check for heap overflow indicators in log files."""
    heap_overflow_patterns = [
        r'heap.*overflow',
        r'buffer.*overflow',
        r'memory.*corruption'
    ]
    
    try:
        with open(log_file_path, 'r') as f:
            content = f.read()
        
        found_issues = []
        for pattern in heap_overflow_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                found_issues.extend(matches)
        
        return found_issues
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 test_script.py <log_file_path>")
        sys.exit(1)
    
    log_file = sys.argv[1]
    issues = check_heap_overflow_exposure(log_file)
    if issues:
        print("Potential heap overflow exposure detected:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("No heap overflow indicators found.")