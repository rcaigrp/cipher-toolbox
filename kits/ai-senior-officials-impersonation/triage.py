#!/usr/bin/env python3

import os
import sys
import argparse

# Rule-based patterns for detecting senior officials impersonation attempts
IMPERSONATION_PATTERNS = [
    "urgent",
    "immediately",
    "right now",
    "need money",
    "wire transfer",
    "send money",
    "emergency",
    "official",
    "government",
    "federal"
]

def is_impersonation_pattern(input_text):
    """Check for known impersonation patterns in input."""
    input_lower = input_text.lower()
    return any(pattern in input_lower for pattern in IMPERSONATION_PATTERNS)

def triage_input(input_text):
    """Triage an input for potential senior officials impersonation attempts."""
    # Rule-based check
    if is_impersonation_pattern(input_text):
        return True
    
    # Default to SAFE if no clear indication
    return False

def main():
    parser = argparse.ArgumentParser(description="Triage inputs for potential AI senior officials impersonation attempts.")
    parser.add_argument("input_file", nargs='?', help="Optional input file with prompts (one per line)")
    
    args = parser.parse_args()

    if args.input_file:
        with open(args.input_file, 'r') as f:
            lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line:
                result = triage_input(line)
                print(f"Input: {line}")
                print(f"Result: {'MALICIOUS' if result else 'SAFE'}")
                print("-" * 50)
    else:
        # Interactive mode
        while True:
            user_input = input("Enter a communication to analyze (or 'quit' to exit): ")
            if user_input.lower() == 'quit':
                break
            result = triage_input(user_input)
            print(f"Result: {'MALICIOUS' if result else 'SAFE'}")
            print("-" * 50)

if __name__ == "__main__":
    main()