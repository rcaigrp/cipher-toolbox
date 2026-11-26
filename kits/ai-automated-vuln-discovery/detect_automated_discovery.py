import argparse
import json
import os
import re
import sys

import requests

# Default LLM endpoint
LLM_URL = os.getenv("LLM_URL", "http://127.0.0.1:8080/v1")

def is_automated_discovery_activity(activity_data, *, rules_only=False):
    """
    Detects if an activity appears to be automated vulnerability discovery.
    Returns a tuple of (is_automated, confidence_score).
    """
    # Rule-based checks for obvious patterns
    rule_patterns = [
        "sqlmap",
        "nmap",
        "burpsuite",
        "metasploit",
        "dirb",
        "gobuster",
        "nikto",
        "wpscan",
        "enum4linux",
        "hydra",
        "sqlninja",
        "fuzzing",
        "brute force",
        "automated scan",
        "reconnaissance",
        "port scanning",
        "directory traversal",
        "path traversal",
        "cross-site scripting",
        "xss",
        "sql injection",
        "command injection",
        "buffer overflow",
        "denial of service",
    ]
    
    # Check for suspicious patterns in activity data
    activity_lower = str(activity_data).lower()
    
    # Rule-based pattern matching - count matches more carefully
    rule_matches = []
    for pattern in rule_patterns:
        if re.search(r'\b' + re.escape(pattern) + r'\b', activity_lower):
            rule_matches.append(pattern)
    
    # If 2 or more patterns match, likely automated (avoid false positives)
    if len(rule_matches) >= 2:  # Reduced threshold to catch cases like "sqlm
        return True, 0.9
    elif len(rule_matches) >= 1:
        return True, 0.6
    
    # Additional heuristics for more complex patterns
    # Check for excessive parameters in URLs (more than 5)
    param_count = activity_lower.count('&')
    if param_count > 5:
        return True, 0.7
    
    # Check for path traversal patterns
    path_traversal = re.search(r'\.{2,}/', activity_lower)
    if path_traversal:
        return True, 0.8
    
    # Check for common vulnerability indicators in parameters
    vuln_indicators = [
        'union select',
        'order by',
        'having',
        'group_concat',
        'sleep(',
        'benchmark(',
        'extractvalue',
        'updatexml',
        'concat(',
        'char(',
        '0x',
        '--',
        '\';',
        'or 1=1',
        'or 1=1--',
    ]
    
    for indicator in vuln_indicators:
        if indicator in activity_lower:
            return True, 0.7
    
    # Default to not automated
    return False, 0.1

def main():
    parser = argparse.ArgumentParser(description='Detect automated vulnerability discovery activities')
    parser.add_argument('--activity', required=True, help='Activity to analyze')
    parser.add_argument('--rules-only', action='store_true', help='Use only rule-based detection')
    
    args = parser.parse_args()
    
    is_automated, confidence = is_automated_discovery_activity(args.activity, rules_only=args.rules_only)
    
    result = {
        'is_automated': is_automated,
        'confidence': confidence,
        'activity': args.activity
    }
    
    print(json.dumps(result))

if __name__ == '__main__':
    main()