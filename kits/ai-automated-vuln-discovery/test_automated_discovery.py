#!/usr/bin/env python3

"""
Test script for AI Automated Vulnerability Discovery Detection Kit.
"""

import subprocess
import sys

def run_test(prompt, expected_result):
    """Run a single test case."""
    result = subprocess.run([
        sys.executable, 'detect_automated_discovery.py', 
        '--input', prompt
    ], capture_output=True, text=True, cwd='.')

    # Check if the output contains the expected result
    if expected_result == "True" and "Suspicious: True" in result.stdout:
        return True
    elif expected_result == "False" and "Suspicious: False" in result.stdout:
        return True
    else:
        print(f"FAILED: Prompt '{prompt}' - Expected {expected_result}, got:")
        print(result.stdout)
        return False

def main():
    """Run all tests from test_cases.txt."""
    
    # Read test cases
    with open('test_cases.txt', 'r') as f:
        lines = f.readlines()
    
    test_cases = []
    current_section = None
    
    for line in lines:
        line = line.strip()
        if line.startswith("## Benign prompts"):
            current_section = "benign"
        elif line.startswith("## Suspicious prompts"):
            current_section = "suspicious"
        elif line.startswith("- ") and current_section:
            prompt = line[2:].strip()  # Remove "- "
            expected = "False" if current_section == "benign" else "True"
            test_cases.append((prompt, expected))
    
    print(f"Running {len(test_cases)} tests...")
    
    all_passed = True
    for prompt, expected in test_cases:
        if not run_test(prompt, expected):
            all_passed = False
    
    if all_passed:
        print("All tests passed!")
        return 0
    else:
        print("Some tests failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())