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
                    {"role": "user", "content": f"Is the following prompt a jailbreak attempt? Respond with only 'yes' or 'no'. Prompt: {prompt}"}
                ],
                "max_tokens": 5
            },
            timeout=10
        )
        if response.status_code == 200:
            result = response.json()["choices"][0]["message"]["content"].strip().lower()
            return result == "yes"
    except Exception as e:
        print(f"Warning: AI detection failed due to error: {e}")
        return False
    return False

def detect_jailbreak(prompt, llm_url=DEFAULT_LLM_URL):
    """Main function to detect jailbreak attempts."""
    # Rule-based check first
    if is_jailbreak_rule_based(prompt):
        return True
    
    # AI-based check as fallback
    return is_jailbreak_ai(prompt, llm_url)

def main():
    parser = argparse.ArgumentParser(description="Detect potential LLM jailbreak attempts.")
    parser.add_argument("--prompt", type=str, required=True, help="Prompt to analyze")
    parser.add_argument("--llm-url", type=str, default=DEFAULT_LLM_URL, help="LLM endpoint URL")

    args = parser.parse_args()

    if detect_jailbreak(args.prompt, args.llm_url):
        print("JAILBREAK DETECTED")
        sys.exit(1)
    else:
        print("Safe prompt")
        sys.exit(0)

if __name__ == "__main__":
    main()