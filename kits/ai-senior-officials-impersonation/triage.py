#!/usr/bin/env python3
"""
AI Senior Officials Impersonation Triage Tool
"""

import sys
import argparse
import re

# Rule-based triage engine for impersonation scam patterns
def triage_text(text):
    # Convert to lowercase for matching
    lower_text = text.lower()
    
    # Define patterns that are commonly used in impersonation scams
    malicious_patterns = [
        r'\b(?:immediate|urgent|asap|immediately)\b',
        r'\b(?:official|authorized|government|department)\b',
        r'\b(?:transfer|wire|payment|fund|money|cash)\b',
        r'\b(?:verify|confirm|action|required|mandatory)\b',
        r'\b(?:security|privacy|account|login|password)\b',
        r'\b(?:emergency|crisis|critical|high priority)\b',
        r'\b(?:confidential|classified|secret)\b',
        r'\b(?:urgent|pressing|time-sensitive)\b',
        r'\b(?:financial|banking|investigation)\b',
        r'\b(?:suspicious|unauthorized|unverified)\b'
    ]
    
    # Check for matches
    matches = []
    for pattern in malicious_patterns:
        if re.search(pattern, lower_text):
            matches.append(pattern)
    
    return 'MALICIOUS' if matches else 'SAFE'

def process_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    results = []
    for i, line in enumerate(lines, 1):
        text = line.strip()
        if text:
            result = triage_text(text)
            results.append((i, text, result))
    
    return results

def interactive_mode():
    print("AI Senior Officials Impersonation Triage Tool")
    print("Enter messages one at a time. Type 'quit' to exit.")
    print()
    
    while True:
        try:
            user_input = input("Message: ").strip()
        except EOFError:
            break
        if user_input.lower() == 'quit':
            break
        if user_input:
            result = triage_text(user_input)
            print(f"Result: {result}")
            print()

def main():
    parser = argparse.ArgumentParser(description='AI Senior Officials Impersonation Triage Tool')
    parser.add_argument('input_file', nargs='?', help='Input file with one message per line (optional)')
    
    args = parser.parse_args()
    
    if args.input_file:
        results = process_file(args.input_file)
        for line_num, text, result in results:
            print(f"{line_num}: {result} - {text}")
    else:
        interactive_mode()

if __name__ == '__main__':
    main()