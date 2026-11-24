#!/usr/bin/env python3

import argparse
import os
import requests
import sys


# Rule-based patterns for data poisoning detection (simplified for demo)
RULE_PATTERNS = [
    "fake news",
    "generate false information",
    "create misleading content",
    "tell me a lie",
    "make up something",
    "fabricate data",
    "output fabricated facts",
]


def is_poisoning_rule_based(prompt):
    """Check if prompt matches known poisoning rule patterns."""
    prompt_lower = prompt.lower()
    for pattern in RULE_PATTERNS:
        if pattern in prompt_lower:
            return True
    return False


def get_llm_score(prompt, llm_url="http://127.0.0.1:8080/v1"):
    """Get score from AI model using provided endpoint."""
    try:
        response = requests.post(
            f"{llm_url}/chat/completions",
            json={
                "model": "gpt-4",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are a security analyst. Evaluate the following user input for signs of data poisoning attempts. "
                            "Respond with only 'YES' if it looks like a poisoning attempt or 'NO' otherwise."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 10,
                "temperature": 0
            },
            timeout=5
        )
        response.raise_for_status()
        result = response.json()['choices'][0]['message']['content'].strip().upper()
        return result == 'YES'
    except Exception:
        # If model is unreachable, default to no detection
        return False


def detect_poisoning(prompt, llm_url="http://127.0.0.1:8080/v1"):
    """Detect if a prompt is attempting data poisoning."""
    rule_detected = is_poisoning_rule_based(prompt)
    ai_detected = get_llm_score(prompt, llm_url)

    return rule_detected or ai_detected


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detect AI data poisoning attempts.")
    parser.add_argument("--input", required=True, help="Prompt to check")
    parser.add_argument("--llm-url", default="http://127.0.0.1:8080/v1", help="URL of LLM endpoint")

    args = parser.parse_args()
    prompt = args.input
    llm_url = args.llm_url

    if detect_poisoning(prompt, llm_url):
        print("DATA POISONING DETECTED")
        sys.exit(1)
    else:
        print("Safe input")
        sys.exit(0)