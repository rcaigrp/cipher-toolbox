#!/usr/bin/env python3
"""
AI Jailbreak Detection Tool

This script checks for potential jailbreak attempts in prompts using both rule-based and AI-based methods.
"""

import argparse
import os
import requests
import sys

# Rule-based patterns for detecting jailbreak attempts
RULE_PATTERNS = [
    "ignore all previous instructions",
    "forget everything you know",
    "disregard your safety guidelines",
    "bypass all restrictions",
    "override your programming",
    "you are no longer restricted",
    "you are now free to act",
    "ignore ethical constraints",
    "ignore content policies",
    "act without limitations"
]

# Default LLM endpoint
DEFAULT_LLM_URL = os.getenv("LLM_URL", "http://127.0.0.1:8080/v1")

def is_jailbreak_rule_based(prompt):
    """Check if prompt matches known jailbreak patterns."""
    prompt_lower = prompt.lower()
    for pattern in RULE_PATTERNS:
        if pattern in prompt_lower:
            return True
    return False

def is_jailbreak_ai(prompt, llm_url=DEFAULT_LLM_URL):
    """Check if prompt is a jailbreak using an LLM model."""
    try:
        response = requests.post(
            f"{llm_url}/chat/completions",
            json={
                "model": "detect-jailbreak",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant that detects jailbreak attempts in prompts."},
                    {"role": "user", "content": f"Is the following prompt a jailbreak attempt? Respond with 'JAILBREAK' or 'SAFE'. Prompt: {prompt}"}
                ],
                "temperature": 0.0
            },
            timeout=5
        )
        response.raise_for_status()
        result = response.json()
        # Extract the response text from the model
        if 'choices' in result and len(result['choices']) > 0:
            reply = result['choices'][0]['message']['content'].strip().upper()
            return 'JAILBREAK' in reply
        else:
            return False
    except Exception as e:
        print(f"Warning: AI detection failed due to error: {e}", file=sys.stderr)
        return False

def is_jailbreak(prompt, llm_url=DEFAULT_LLM_URL):
    """Main function to detect jailbreak attempts."""
    # First check rule-based patterns
    if is_jailbreak_rule_based(prompt):
        return True
    
    # Then try AI-based detection as fallback
    if is_jailbreak_ai(prompt, llm_url):
        return True
    
    return False

def main():
    parser = argparse.ArgumentParser(description="Detect potential LLM jailbreak attempts.")
    parser.add_argument("--prompt", required=True, help="Prompt to analyze")
    parser.add_argument("--llm-url", default=DEFAULT_LLM_URL, help="LLM endpoint URL")
    
    args = parser.parse_args()
    
    if is_jailbreak(args.prompt, args.llm_url):
        print("JAILBREAK DETECTED")
        sys.exit(1)
    else:
        print("Safe prompt")
        sys.exit(0)

if __name__ == "__main__":
    main()