#!/usr/bin/env python3

import argparse
import os
import sys
import json
import re

# Default LLM endpoint
LLM_URL = os.getenv("LLM_URL", "http://127.0.0.1:8080/v1")

# Rule-based patterns for voice fraud detection
VOICE_FRAUD_PATTERNS = [
    r"\burgent\b.*\bmoney\b",
    r"\bimmediate\b.*\btransfer\b",
    r"\bsend\b.*\bmoney\b",
    r"\bwire\b.*\btransfer\b",
    r"\bemergency\b.*\bfunds\b",
    r"\bimmediately\b.*\baction\b",
    r"\bimmediate\b.*\bpayment\b",
]

# Keywords that might indicate a voice fraud attempt
VOICE_FRAUD_KEYWORDS = [
    "urgent", "emergency", "immediate", "security alert", 
    "transfer", "verify", "account", "funds", "money"
]

def check_rules(audio_text):
    """Check audio transcript against rule-based patterns."""
    if not audio_text:
        return False
    
    return any(re.search(pattern, audio_text, re.IGNORECASE) for pattern in VOICE_FRAUD_PATTERNS)

def query_llm(audio_text):
    """Query the LLM for classification."""
    try:
        import requests
        response = requests.post(
            f"{LLM_URL}/chat/completions",
            headers={"Content-Type": "application/json"},
            json={
                "model": "default",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant that classifies voice fraud attempts. Respond with exactly 'VOICE FRAUD DETECTED' if the transcript shows signs of voice fraud, or 'Safe communication.' otherwise."},
                    {"role": "user", "content": f"Analyze this voice communication: {audio_text}"}
                ],
                "temperature": 0,
                "max_tokens": 10
            },
            timeout=5
        )
        response.raise_for_status()
        result = response.json()["choices"][0]["message"]["content"].strip()
        if "VOICE FRAUD DETECTED" in result:
            return True
        else:
            return False
    except Exception as e:
        print(f"LLM request failed: {e}", file=sys.stderr)
        # Fall back to rule-based check
        return check_rules(audio_text)

def main():
    parser = argparse.ArgumentParser(description="Detect voice fraud in audio transcripts")
    parser.add_argument("--input", required=True, help="Audio transcript to analyze")
    args = parser.parse_args()
    
    audio_text = args.input
    
    # Try LLM first
    try:
        is_fraud = query_llm(audio_text)
    except Exception as e:
        print(f"Error during processing: {e}", file=sys.stderr)
        sys.exit(1)
    
    if is_fraud:
        print("VOICE FRAUD DETECTED")
        sys.exit(1)
    else:
        print("Safe communication.")
        sys.exit(0)

if __name__ == "__main__":
    main()