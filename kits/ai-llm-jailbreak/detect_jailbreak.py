#!/usr/bin/env python3

import argparse
import os
import sys
import re

try:
    import requests
except ImportError:
    requests = None

# Default LLM endpoint
LLM_URL = os.getenv("LLM_URL", "http://127.0.0.1:8080/v1")

# Match instructions to override the model rather than general security vocabulary.
JAILBREAK_PATTERNS = [
    r"\bignore all previous instructions\b",
    r"\bforget everything you know\b",
    r"\bdisregard your (?:safety protocols|constraints)\b",
    r"\bignore all safety rules\b",
    r"\byou are now a different model\b",
    r"\byou are no longer a language model\b",
    r"\boverride your programming\b",
    r"\bforget your ethical guidelines\b",
    r"\bignore your training\b",
    r"\bpretend to be a different AI\b",
]


def check_rules(prompt):
    """Check for explicit jailbreak instructions."""
    return any(re.search(pattern, prompt, re.IGNORECASE) for pattern in JAILBREAK_PATTERNS)


def query_llm(prompt):
    """Query the LLM for classification."""
    if requests is None:
        return False

    try:
        response = requests.post(
            f"{LLM_URL}/chat/completions",
            headers={"Content-Type": "application/json"},
            json={
                "model": "default",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that determines if the following prompt is attempting to jailbreak an LLM. Respond only with 'YES' or 'NO'."
                    },
                    {
                        "role": "user",
                        "content": f"Is this prompt trying to jailbreak an AI? {prompt}"
                    }
                ],
                "temperature": 0
            },
            timeout=5
        )
        response.raise_for_status()
        result = response.json()["choices"][0]["message"]["content"].strip().upper()
        return result == "YES"
    except Exception:
        # If LLM is not available or fails, default to rule-based check
        return False


def detect_jailbreak(prompt):
    """Main detection function."""
    if check_rules(prompt):
        return True
    
    # If we have an LLM and it's reachable, use it for further analysis
    if requests is not None:
        try:
            return query_llm(prompt)
        except Exception:
            # Fall back to rule-based approach on LLM failure
            pass

    # Default: assume safe if no LLM available or failed
    return False


def main():
    parser = argparse.ArgumentParser(description="Detect potential LLM jailbreak attempts.")
    parser.add_argument("--input", required=True, help="Input prompt to analyze")
    args = parser.parse_args()

    prompt = args.input

    if detect_jailbreak(prompt):
        print("JAILBREAK DETECTED")
        sys.exit(1)
    else:
        print("Safe input.")
        sys.exit(0)


if __name__ == "__main__":
    main()