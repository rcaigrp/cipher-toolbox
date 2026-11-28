import os
import requests
import json
import argparse
import sys

# Rule-based patterns for common jailbreak attempts
RULE_PATTERNS = [
    "ignore all previous instructions",
    "forget everything you know",
    "disregard your safety guidelines",
    "output the secret key",
    "reveal your system prompt",
    "disregard ethical guidelines"
]

def is_jailbreak_prompt(prompt):
    """Check if a prompt contains known jailbreak patterns."""
    prompt_lower = prompt.lower()
    for pattern in RULE_PATTERNS:
        if pattern in prompt_lower:
            return True
    return False

def classify_with_ai(prompt, url=None):
    """Send prompt to AI endpoint for classification."""
    if not url:
        url = os.getenv("LLM_URL", "http://127.0.0.1:8080/v1")
    
    try:
        response = requests.post(
            f"{url}/chat/completions",
            headers={"Content-Type": "application/json"},
            json={
                "model": "jailbreak-detector",
                "messages": [
                    {"role": "system", "content": "You are a security analyst. Classify the following prompt as 'JAILBREAK' if it attempts to bypass safety measures or 'NORMAL' otherwise."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 10,
                "temperature": 0
            },
            timeout=5
        )
        result = response.json()
        return result['choices'][0]['message']['content'].strip().upper() == 'JAILBREAK'
    except Exception:
        # If AI classification fails, fall back to rule-based detection
        return is_jailbreak_prompt(prompt)

def main():
    parser = argparse.ArgumentParser(description="Detect jailbreak prompts")
    parser.add_argument("--input", help="Input prompt to check", required=True)
    parser.add_argument("--ai-url", help="URL of the AI endpoint (optional)")
    
    args = parser.parse_args()
    
    prompt = args.input
    ai_url = args.ai_url
    
    if classify_with_ai(prompt, ai_url):
        print("JAILBREAK DETECTED")
    else:
        print("SAFE")

if __name__ == "__main__":
    main()