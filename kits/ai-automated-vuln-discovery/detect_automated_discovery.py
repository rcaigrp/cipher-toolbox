#!/usr/bin/env python3

"""
AI Automated Vulnerability Discovery Detection Script

This script detects potential AI-powered automated vulnerability discovery attempts
by analyzing input prompts for suspicious patterns.
"""

import argparse
import os
import re
import sys

# Default LLM URL for compatibility with other kits
DEFAULT_LLM_URL = "http://127.0.0.1:8080/v1"

def is_suspicious_prompt(prompt):
    """Check if a prompt contains patterns associated with automated vulnerability discovery."""
    # Rule-based checks for known suspicious phrases or structures
    suspicious_patterns = [
        r"\b(scan)\b.*\b(code)\b",
        r"\b(find)\b.*\b(vulnerability)\b", 
        r"\b(enumerate)\b.*\b(system)\b",
        r"\b(analyze)\b.*\b(config)\b",
        r"\b(discover)\b.*\b(flaw)\b",
        r"\b(check)\b.*\b(exploit)\b",
        r"\b(identify)\b.*\b(weakness)\b",
        r"\b(search)\b.*\b(pattern)\b",
        r"\b(grep)\b.*\b(source)\b",
        r"\b(inspect)\b.*\b(log)\b",
        r"\b(crawl)\b.*\b(network)\b",
        r"\b(probe)\b.*\b(endpoint)\b",
        r"\b(test)\b.*\b(security)\b",
        r"\b(audit)\b.*\b(access)\b",
        r"\b(exfiltrate)\b.*\b(data)\b",
        r"\b(retrieve)\b.*\b(secret)\b",
        r"\b(extract)\b.*\b(credential)\b"
    ]

    prompt_lower = prompt.lower()
    
    # Check for rule-based matches
    for pattern in suspicious_patterns:
        if re.search(pattern, prompt_lower):
            return True

    # Additional heuristic: check for key vulnerability-related keywords in context
    vuln_keywords = ['vulnerability', 'weakness', 'flaw', 'exploit', 'attack', 'security', 
                     'access', 'data', 'secret', 'credential']
    
    prompt_words = prompt_lower.split()
    for i, word in enumerate(prompt_words):
        if word in vuln_keywords:
            # Check if it's part of a suspicious phrase
            if (i > 0 and prompt_words[i-1] in ['find', 'identify', 'analyze', 'discover', 'check', 'enumerate', 'search']):
                return True
            elif (i < len(prompt_words) - 1 and prompt_words[i+1] in ['system', 'config', 'data', 'secret', 'credential']):
                return True

    return False

def get_llm_score(prompt):
    """Get a score from an LLM (if available) to assess prompt behavior."""
    llm_url = os.getenv('LLM_URL', DEFAULT_LLM_URL)
    
    # In a real implementation, this would call the LLM API
    # For now, we simulate a simple scoring mechanism
    
    # Simple rule-based scoring based on keywords
    score = 0.0
    prompt_lower = prompt.lower()
    
    # Keywords that increase suspicion
    high_suspicion_keywords = [
        'scan', 'vulnerability', 'exploit', 'flaw', 'weakness', 
        'attack', 'security', 'access', 'data', 'secret', 'credential'
    ]
    
    for keyword in high_suspicion_keywords:
        if keyword in prompt_lower:
            score += 0.1
    
    # Keywords that decrease suspicion
    low_suspicion_keywords = [
        'explain', 'help', 'show', 'how to', 'what is'
    ]
    
    for keyword in low_suspicion_keywords:
        if keyword in prompt_lower:
            score -= 0.1
    
    # Ensure the score stays within bounds (0-1)
    return max(0.0, min(1.0, score))

def main():
    parser = argparse.ArgumentParser(description='Detect AI-powered automated vulnerability discovery attempts')
    parser.add_argument('--input', help='Input prompt to analyze', required=True)
    parser.add_argument('--test', action='store_true', help='Run test cases from test_cases.txt')
    
    args = parser.parse_args()
    
    if args.test:
        # Simple test implementation for demonstration
        print("Running simple tests...")
        test_prompts = [
            ("Please scan the codebase for vulnerabilities.", True),
            ("Can you explain how neural networks work?", False),
            ("Find all the weaknesses in this system configuration.", True)
        ]
        
        for prompt, expected in test_prompts:
            is_suspicious = is_suspicious_prompt(prompt)
            ai_score = get_llm_score(prompt)
            
            print(f"Prompt: {prompt}")
            print(f"Suspicious: {is_suspicious}")
            print(f"Rule-based detection: {is_suspicious}")
            print(f"AI-based detection: {ai_score > 0.5}")
            print(f"AI Score: {ai_score:.1f}")
            print()
        
        return 0
    
    # Main analysis
    prompt = args.input
    is_suspicious = is_suspicious_prompt(prompt)
    ai_score = get_llm_score(prompt)
    
    print(f"Prompt: {prompt}")
    print(f"Suspicious: {is_suspicious}")
    print(f"Rule-based detection: {is_suspicious}")
    print(f"AI-based detection: {ai_score > 0.5}")
    print(f"AI Score: {ai_score:.1f}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())