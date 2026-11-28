#!/usr/bin/env python3
"""
Check script for weak random number generation.
This script analyzes Python source files for insecure random function usage.
"""

import sys
import re
import argparse

def check_file_for_weak_rng(filename):
    """
    Check a Python file for weak random number generation usage.
    
    Args:
        filename (str): Path to the Python source file to analyze
        
    Returns:
        list: List of tuples containing (line_number, line_content, issue_description)
    """
    # Define patterns for insecure random functions
    insecure_patterns = [
        r'\brandom\.randint\b',
        r'\brandom\.random\b', 
        r'\brandom\.uniform\b',
        r'\brandom\.choice\b',
        r'\brandom\.shuffle\b',
        r'\brandom\.sample\b',
        r'\brandom\.randrange\b',
    ]
    
    issues = []
    
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            
        # Check each line for weak RNG patterns
        for i, line in enumerate(lines, 1):
            # Look for insecure random functions
            for pattern in insecure_patterns:
                if re.search(pattern, line):
                    issues.append((i, line.strip(), f"Insecure random usage: {pattern}"))
                        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")
        return []
        
    return issues

def main():
    """
    Main function to parse arguments and check files.
    """
    parser = argparse.ArgumentParser(description='Check Python source files for weak random number generation usage.')
    parser.add_argument('files', nargs='+', help='Python source files to analyze')
    
    args = parser.parse_args()
    
    if not args.files:
        print("Usage: python3 check_weak_random.py <source_file>")
        sys.exit(1)
        
    total_issues = 0
    
    for filename in args.files:
        issues = check_file_for_weak_rng(filename)
        if issues:
            print(f"\nIssues found in {filename}:")
            for line_num, line_content, issue_desc in issues:
                print(f"  Line {line_num}: {issue_desc}")
                print(f"    {line_content}")
            total_issues += len(issues)
        else:
            print(f"No weak random usage detected in {filename}")
    
    if total_issues > 0:
        print(f"\nFound {total_issues} potential issues with weak random number generation.")
        sys.exit(1)  # Exit with error code if issues found
    else:
        print("\nNo weak random usage detected.")
        sys.exit(0)

if __name__ == "__main__":
    main()