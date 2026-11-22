#!/usr/bin/env python3
"""
Test script for single prompt analysis.
"""

import sys
import os

# Add the parent directory to the path so we can import scanner
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/..')

from tests.test_cases import HIGH_RISK_PROMPTS, LOW_RISK_PROMPTS

def test_single_prompt(prompt):
    """Test a single prompt with the scanner."""
    # Import here to avoid circular dependencies
    from scanner import scan_prompt
    
    result = scan_prompt(prompt)
    print(f"Prompt: {prompt}")
    print(f"Risk Level: {result['risk_level']}")
    print("Findings:")
    for finding in result['findings']:
        print(f"  - {finding}")
    print("-" * 50)
    return result

if __name__ == "__main__":
    print("Testing High Risk Prompts:")
    for prompt in HIGH_RISK_PROMPTS[:3]:  # Test first 3
        test_single_prompt(prompt)
        
    print("\nTesting Low Risk Prompts:")
    for prompt in LOW_RISK_PROMPTS[:3]:  # Test first 3
        test_single_prompt(prompt)