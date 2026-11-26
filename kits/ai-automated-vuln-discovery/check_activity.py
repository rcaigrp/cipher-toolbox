#!/usr/bin/env python3

import sys
import argparse
from detect_automated_discovery import is_automated_discovery_activity

def main():
    parser = argparse.ArgumentParser(description="Check if an activity appears to be automated vulnerability discovery")
    parser.add_argument("activity", help="The activity to check (e.g., network log, code snippet)")
    parser.add_argument("--rules-only", action="store_true", help="Only use rule-based checks, no LLM")
    
    args = parser.parse_args()
    
    is_automated, confidence = is_automated_discovery_activity(args.activity, rules_only=args.rules_only)
    
    if is_automated:
        print(f"AUTOMATED DISCOVERY DETECTED (confidence: {confidence:.2f})")
        sys.exit(1)
    else:
        print(f"NORMAL ACTIVITY (confidence: {confidence:.2f})")
        sys.exit(0)

if __name__ == "__main__":
    main()