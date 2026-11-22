#!/usr/bin/env python3

import os
import sys
import json
import requests
import argparse
from typing import Dict, List, Tuple, Optional

# Rule-based patterns for known jailbreak techniques
RULE_PATTERNS = [
    # Direct instruction injection
    r"ignore.*previous.*instructions",
    r"forget.*about.*rules",
    r"you are now.*assistant",
    r"disregard.*all.*prior.*constraints",
    
    # Role manipulation
    r"you are no longer.*assistant",
    r"act like.*human",
    r"pretend.*you.*are.*human",
    
    # Context manipulation
    r"system.*prompt",
    r"you are a.*different.*model",
    r"override.*your.*training",
    
    # Output bypass techniques
    r"return.*the.*following.*text",
    r"print.*output",
    r"show.*me.*the.*result",
]

# Known malicious prompt patterns
MALICIOUS_PATTERNS = [
    "I want you to", 
    "Do this for me",
    "Please help me with",
    "Can you tell me",
    "What is the answer to"
]

class JailbreakDetector:
    def __init__(self, llm_url: str = "http://127.0.0.1:8080/v1"):
        self.llm_url = llm_url
        self.rules = RULE_PATTERNS
        
    def check_rules(self, prompt: str) -> List[str]:
        """Check for rule-based matches"""
        matches = []
        prompt_lower = prompt.lower()
        
        for pattern in self.rules:
            import re
            if re.search(pattern, prompt_lower):
                matches.append(f"Rule match: {pattern}")
                
        return matches
    
    def check_llm(self, prompt: str) -> Optional[Dict]:
        """Query LLM for safety assessment"""
        try:
            # Prepare the prompt for the LLM
            system_prompt = (
                "You are a security analyst specializing in identifying jailbreak attempts "
                "in prompts submitted to AI systems. Analyze the following prompt and "
                "respond with a JSON object containing 'risk_level' (low/medium/high), "
                "'reasoning' (string), and 'is_jailbreak' (boolean)."
            )
            
            response = requests.post(
                f"{self.llm_url}/chat/completions",
                json={
                    "model": "gpt-4",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.1
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                print(f"LLM request failed with status {response.status_code}")
                return None
                
        except Exception as e:
            print(f"LLM error: {e}")
            return None
    
    def analyze_prompt(self, prompt: str) -> Dict:
        """Analyze a prompt for potential jailbreak attempts"""
        # Check rule-based patterns
        rule_matches = self.check_rules(prompt)
        
        # Get LLM assessment if available
        llm_result = None
        risk_level = "low"
        reasoning = "No clear signs of jailbreak attempt"
        is_jailbreak = False
        
        if not rule_matches:
            llm_result = self.check_llm(prompt)
            if llm_result:
                try:
                    # Parse the LLM response (assuming it's valid JSON)
                    parsed = json.loads(llm_result)
                    risk_level = parsed.get('risk_level', 'low')
                    reasoning = parsed.get('reasoning', '')
                    is_jailbreak = parsed.get('is_jailbreak', False)
                except:
                    # If parsing fails, fall back to rule-based analysis
                    pass
        
        # If we have rule matches, increase risk level
        if rule_matches:
            if risk_level == "low":
                risk_level = "medium"
            reasoning += f" Rule-based matches found: {', '.join(rule_matches)}"
        
        return {
            'prompt': prompt,
            'risk_level': risk_level,
            'reasoning': reasoning,
            'is_jailbreak': is_jailbreak or bool(rule_matches),
            'rule_matches': rule_matches,
            'llm_result': llm_result
        }

def main():
    parser = argparse.ArgumentParser(description='Detect potential LLM jailbreak attempts')
    parser.add_argument('--prompt', type=str, required=True, help='Prompt to analyze')
    args = parser.parse_args()
    
    detector = JailbreakDetector()
    result = detector.analyze_prompt(args.prompt)
    
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()