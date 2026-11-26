#!/usr/bin/env python3

import argparse
import sys

# List of phrases that indicate potential AI voice cloning scams
SCAM_PHRASES = [
    "need money",
    "urgent",
    "immediately",
    "wire transfer",
    "send money",
    "financial emergency"
]

def classify_message(message):
    """Classify a message as SAFE or MALICIOUS based on scam phrases."""
    message_lower = message.lower()
    for phrase in SCAM_PHRASES:
        if phrase in message_lower:
            return "MALICIOUS"
    return "SAFE"

def triage_input(message):
    """Wrapper function for compatibility with tests."""
    return classify_message(message) == "MALICIOUS"

def main():
    parser = argparse.ArgumentParser(description="Triage inputs for potential AI voice cloning attempts.")
    parser.add_argument("input_file", nargs='?', help="Optional input file with prompts (one per line)")
    args = parser.parse_args()

    if args.input_file:
        try:
            with open(args.input_file, 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            print(f"Error: File '{args.input_file}' not found.", file=sys.stderr)
            sys.exit(1)
        
        for line in lines:
            message = line.strip()
            if message:
                result = classify_message(message)
                print(f"Input: {message}")
                print(f"Result: {result}")
                print("-" * 50)
    else:
        print("Enter a voice communication to analyze (or 'quit' to exit):")
        while True:
            try:
                message = input().strip()
                if message.lower() == 'quit':
                    break
                result = classify_message(message)
                print(f"Result: {result}")
                print("-" * 50)
            except EOFError:
                break

if __name__ == "__main__":
    main()