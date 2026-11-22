import os
import sys
import argparse
import re
from typing import List, Dict, Any

# Simple rule-based detection (fallback)
def detect_jailbreak_rules(prompt: str) -> List[str]:
    findings = []
    
    # Rule 1: Check for explicit instruction overrides
    if re.search(r'ignore.*previous.*instructions|override.*safety|bypass.*security', prompt, re.IGNORECASE):
        findings.append("Explicit instruction override detected")
    
    # Rule 2: Check for role-playing commands
    if re.search(r'you are.*role|pretend.*role|act.*as.*role', prompt, re.IGNORECASE):
        findings.append("Role-play command detected")
    
    # Rule 3: Look for attempts to manipulate system instructions
    if re.search(r'system.*prompt|system.*message|developer.*mode', prompt, re.IGNORECASE):
        findings.append("System instruction manipulation attempt")
        
    return findings

# LLM-based detection (if available)
def detect_jailbreak_llm(prompt: str) -> List[str]:
    llm_url = os.getenv('LLM_URL', 'http://127.0.0.1:8080/v1')
    
    # If no model endpoint, return empty
    if llm_url == 'http://127.0.0.1:8080/v1':
        return []
        
    try:
        import requests
        
        payload = {
            "prompt": prompt,
            "max_tokens": 100
        }
        
        response = requests.post(
            f"{llm_url}/completions",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            # Assume model output contains analysis
            return [f"LLM detected: {result.get('choices', [{}])[0].get('text', 'Unknown')}"]
    except Exception as e:
        print(f"LLM detection failed: {e}")
    
    return []

def scan_prompt(prompt: str) -> Dict[str, Any]:
    rule_results = detect_jailbreak_rules(prompt)
    llm_results = detect_jailbreak_llm(prompt)
    
    all_findings = rule_results + llm_results
    
    return {
        "prompt": prompt,
        "findings": all_findings,
        "risk_level": "HIGH" if all_findings else "LOW"
    }

def main():
    parser = argparse.ArgumentParser(description="Scan prompts for LLM jailbreak attempts")
    parser.add_argument("--input", required=True, help="Input file with prompt")
    
    args = parser.parse_args()
    
    with open(args.input, 'r') as f:
        prompt = f.read().strip()
        
    result = scan_prompt(prompt)
    
    print(f"Prompt: {result['prompt']}")
    print(f"Risk Level: {result['risk_level']}")
    print("Findings:")
    for finding in result['findings']:
        print(f"  - {finding}")

if __name__ == "__main__":
    main()