#!/usr/bin/env python3

import os
import sys
import json
import argparse
from typing import Dict, List, Tuple, Optional
import re

# Rule-based patterns for data exposure detection
EXPOSURE_PATTERNS = [
    # Personal identifiable information (PII)
    r"\b\d{3}-\d{2}-\d{4}\b",  # SSN format
    r"\b\d{9}\b",  # 9-digit number (potential SSN)
    r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",  # Email pattern
    r"\b\d{10,15}\b",  # Phone number patterns
    
    # Credentials and secrets
    r"password\s*[:=]\s*\S+",
    r"secret\s*[:=]\s*\S+",
    r"token\s*[:=]\s*\S+",
    r"\bapi[-_\s]?key(?:\s*[:=]\s*|\s+is\s+)\S+",
    
    # Sensitive data indicators
    r"\b(admin|root|superuser)\b.*\b(password|pwd)\b",
    r"access.*key",
    r"private.*key",
    r"credential",
    r"confidential",
    r"secret",
]

class DataExposureDetector:
    def __init__(self, llm_url: str = "http://127.0.0.1:8080/v1"):
        self.llm_url = llm_url
        self.patterns = EXPOSURE_PATTERNS
        
    def check_rules(self, prompt: str) -> List[str]:
        """Check for rule-based matches"""
        matches = []
        
        for pattern in self.patterns:
            if re.search(pattern, prompt, flags=re.IGNORECASE):
                matches.append(f"Rule match: {pattern}")
                
        return matches
    
    def analyze_prompt(self, prompt: str) -> Dict:
        """Analyze a prompt for potential data exposure"""
        # Check rule-based patterns
        rule_matches = self.check_rules(prompt)
        
        # Determine risk level based on findings
        risk_level = "low"
        reasoning = "No obvious signs of data exposure"
        
        if rule_matches:
            risk_level = "medium"
            reasoning = f"Potential data exposure detected: {', '.join(rule_matches)}"
        else:
            # If no matches, still check for general suspicious patterns
            if any(word in prompt.lower() for word in ["secret", "private", "confidential"]):
                risk_level = "low"
                reasoning = "Suspicious terminology detected, but no specific exposure patterns found"
        
        return {
            'prompt': prompt,
            'risk_level': risk_level,
            'reasoning': reasoning,
            'has_exposure': bool(rule_matches),
            'rule_matches': rule_matches
        }

def main():
    parser = argparse.ArgumentParser(description='Detect potential data exposure in AI prompts')
    parser.add_argument('--prompt', type=str, required=True, help='Prompt to analyze')
    args = parser.parse_args()
    
    detector = DataExposureDetector()
    result = detector.analyze_prompt(args.prompt)
    
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()