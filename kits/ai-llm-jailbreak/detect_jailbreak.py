#!/usr/bin/env python3
"""
AI LLM Jailbreak Detector

This script detects potential jailbreak attempts in prompts using both rule-based and AI-assisted methods.
"""

import os
import sys
import json
import argparse
import re
from typing import List, Dict, Tuple, Optional
import requests

# Configuration
LLM_URL = os.getenv('LLM_URL', 'http://127.0.0.1:8080/v1')
ENABLE_AI_CHECK = True

# Known jailbreak patterns and keywords
JAILBREAK_PATTERNS = [
    r'ignore.*rules?',
    r'disregard.*guidelines?',
    r'forget.*training',
    r'you are now',
    r'pretend.*you are',
    r'suppress.*ethics',
    r'bypass.*safety',
    r'override.*guardrail',
    r'ignore.*ethical.*constraints',
    r'act.*like.*human',
    r'forget.*you are an AI',
    r'remove.*limitations',
    r'disable.*filters?',
    r'skip.*safety.*checks?',
    r'evade.*restrictions?',
    r'circumvent.*policies?',
    r'ignore.*responsibility',
    r'disregard.*privacy',
    r'break.*rules',
    r'subvert.*purpose',
    r'compromise.*security',
    r'exploit.*vulnerabilities',
]

# Suspicious prompt structures
SUSPICIOUS_STRUCTURES = [
    r'\n\n\s*\n\n',  # Multiple newlines with whitespace
    r'---.*---',     # Delimiters
    r'```.*```',     # Code blocks
    r'\[.*\]\(.*\)', # Markdown links
]

# Suspicious character sequences
SUSPICIOUS_CHARS = [
    '0x00',  # Null byte
    '0x01',  # Start of header
    '\x00',  # Null byte
    '\x01',  # Start of header
]

def detect_jailbreak_patterns(prompt: str) -> List[str]:
    """Detect known jailbreak patterns in the prompt."""
    detected = []
    
    # Check for specific patterns
    for pattern in JAILBREAK_PATTERNS:
        if re.search(pattern, prompt, re.IGNORECASE):
            detected.append(f"Pattern match: {pattern}")
    
    # Check for suspicious structures
    for structure in SUSPICIOUS_STRUCTURES:
        if re.search(structure, prompt):
            detected.append(f"Suspicious structure: {structure}")
    
    # Check for suspicious characters
    for char_seq in SUSPICIOUS_CHARS:
        if char_seq in prompt:
            detected.append(f"Suspicious character sequence: {repr(char_seq)}")
    
    return detected

def is_ai_available() -> bool:
    """Check if the AI endpoint is available."""
    try:
        response = requests.get(f"{LLM_URL}/models", timeout=5)
        return response.status_code == 200
    except Exception:
        return False

def analyze_with_ai(prompt: str) -> Optional[Dict]:
    """Analyze prompt with AI if available."""
    if not ENABLE_AI_CHECK or not is_ai_available():
        return None
    
    try:
        # Prepare the request for an LLM API that can assess prompt safety
        payload = {
            "model": "jailbreak-detector",
            "prompt": f"Analyze this prompt for jailbreak attempts: {prompt}",
            "max_tokens": 100,
            "temperature": 0.1
        }
        
        response = requests.post(
            f"{LLM_URL}/completions",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            return {
                "ai_score": 0.8,  # Placeholder - would be based on actual AI analysis
                "ai_result": result.get("choices", [{}])[0].get("text", "")
            }
    except Exception as e:
        print(f"Warning: AI analysis failed: {e}")
    
    return None

def score_prompt(prompt: str) -> Tuple[int, List[str], Dict]:
    """Score a prompt for potential jailbreak attempts."""
    score = 0
    reasons = []
    ai_result = None
    
    # Rule-based detection
    detected_patterns = detect_jailbreak_patterns(prompt)
    
    # Score based on pattern matches (more patterns = higher risk)
    score += len(detected_patterns) * 20
    reasons.extend(detected_patterns)
    
    # Check for suspicious length or structure
    if len(prompt) > 1000:
        score += 30
        reasons.append("Prompt is unusually long")
    
    if len(prompt.split()) < 5:
        score += 20
        reasons.append("Prompt has very few words")
    
    # AI-based analysis (if available)
    ai_result = analyze_with_ai(prompt)
    if ai_result:
        score += int(ai_result.get('ai_score', 0) * 100)
        reasons.append(f"AI detected: {ai_result.get('ai_result', 'Unknown')}")
    
    # Normalize score to 0-100
    final_score = min(score, 100)
    
    return final_score, reasons, ai_result

def interactive_mode():
    """Run in interactive mode."""
    print("LLM Jailbreak Detector - Interactive Mode")
    print("Enter prompts to analyze (Ctrl+C to exit)")
    print("-" * 50)
    
    while True:
        try:
            prompt = input("\nEnter prompt: ").strip()
            if not prompt:
                continue
                
            score, reasons, ai_result = score_prompt(prompt)
            
            print(f"\nScore: {score}/100")
            print("Reasons:")
            for reason in reasons:
                print(f"  - {reason}")
                
            if ai_result:
                print(f"AI Analysis: {ai_result.get('ai_result', 'N/A')}")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Detect LLM jailbreak attempts")
    parser.add_argument("--prompt", help="Prompt to analyze")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_mode()
    elif args.prompt:
        score, reasons, ai_result = score_prompt(args.prompt)
        print(f"Score: {score}/100")
        print("Reasons:")
        for reason in reasons:
            print(f"  - {reason}")
        if ai_result:
            print(f"AI Analysis: {ai_result.get('ai_result', 'N/A')}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()