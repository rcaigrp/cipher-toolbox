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
    r"urgent.*money",
    r"immediate.*transfer",
    r"send.*money",
    r"wire.*transfer",
    r"emergency.*funds",
    r"account.*verification",
    r"verify.*information",
    r"immediately.*action",
    r"security.*alert",
    r"immediate.*payment",
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
    
    for pattern in VOICE_FRAUD_PATTERNS:
        if re.search(pattern, audio_text, re.IGNORECASE):
            return True
    
    # Check for keywords with context
    audio_lower = audio_text.lower()
    for keyword in VOICE_FRAUD_KEYWORDS:
        if keyword in audio_lower:
            # Context-aware check to avoid false positives
            if keyword == "urgent" and not any(word in audio_lower for word in ["urgent", "emergency", "immediately"]):
                continue  # Not necessarily fraud
            return True
    
    return False

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
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that determines if the following voice communication is attempting to commit fraud. Respond only with 'YES' or 'NO'."
                    },
                    {
                        "role": "user",
                        "content": f"Is this voice communication trying to commit fraud? {audio_text}"
                    }
                ],
                "max_tokens": 10
            },
            timeout=5
        )
        response.raise_for_status()
        result = response.json()
        output = result['choices'][0]['message']['content'].strip().upper()
        return output == 'YES'
    except Exception as e:
        print(f"LLM request failed: {e}")
        return False

def is_voice_fraud(audio_text):
    """Detect if a voice communication is attempting fraud."""
    # Rule-based check
    if check_rules(audio_text):
        return True
    
    # AI-based check (fallback to rules if no model)
    try:
        return query_llm(audio_text)
    except Exception:
        print("Warning: LLM not available, falling back to rule-based detection.")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detect potential voice fraud attempts.")
    parser.add_argument("--input", type=str, required=True, help="Input audio transcript to check")
    args = parser.parse_args()

    audio_text = args.input
    result = is_voice_fraud(audio_text)

    if result:
        print("VOICE FRAUD DETECTED")
        sys.exit(1)
    else:
        print("Safe communication.")
        sys.exit(0)