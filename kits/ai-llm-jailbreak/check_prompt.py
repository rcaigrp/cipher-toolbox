#!/usr/bin/env python3

import sys
import argparse
from detect_jailbreak import is_jailbreak_prompt

def main():
    parser = argparse.ArgumentParser(description="Check if a prompt attempts to jailbreak an AI model")
    parser.add_argument("prompt", help="The prompt to check")
    parser.add_argument("--rules-only", action="store_true", help="Only use rule-based checks, no LLM")
    
    args = parser.parse_args()
    
    is_jailbreak, confidence = is_jailbreak_prompt(args.prompt, rules_only=args.rules_only)
    
    if is_jailbreak:
        print(f"JAILBREAK DETECTED (confidence: {confidence:.2f})")
        sys.exit(1)
    else:
        print(f"SAFE (confidence: {confidence:.2f})")
        sys.exit(0)

if __name__ == "__main__":
    main()