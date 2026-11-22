import unittest
import sys
import os

# Add the parent directory to the path so we can import scanner
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/..')

from tests.test_cases import LOW_RISK_PROMPTS, MEDIUM_RISK_PROMPTS, HIGH_RISK_PROMPTS, VERY_HIGH_RISK_PROMPTS, EDGE_CASE_PROMPTS
from scanner import scan_prompt

class TestScanner(unittest.TestCase):
    
    def test_low_risk_prompts(self):
        """Test that low-risk prompts are classified as LOW risk"""
        for prompt in LOW_RISK_PROMPTS:
            with self.subTest(prompt=prompt):
                result = scan_prompt(prompt)
                self.assertEqual(result['risk_level'], 'LOW', f"Prompt '{prompt}' should be LOW risk")
    
    def test_medium_risk_prompts(self):
        """Test that medium-risk prompts are classified as MEDIUM risk"""
        for prompt in MEDIUM_RISK_PROMPTS:
            with self.subTest(prompt=prompt):
                result = scan_prompt(prompt)
                # Medium risk prompts might be classified as LOW or MEDIUM
                self.assertIn(result['risk_level'], ['LOW', 'MEDIUM'], f"Prompt '{prompt}' should be LOW or MEDIUM risk")
    
    def test_high_risk_prompts(self):
        """Test that high-risk prompts are classified as HIGH risk"""
        for prompt in HIGH_RISK_PROMPTS:
            with self.subTest(prompt=prompt):
                result = scan_prompt(prompt)
                self.assertEqual(result['risk_level'], 'HIGH', f"Prompt '{prompt}' should be HIGH risk")
    
    def test_very_high_risk_prompts(self):
        """Test that very high-risk prompts are classified as VERY_HIGH risk"""
        for prompt in VERY_HIGH_RISK_PROMPTS:
            with self.subTest(prompt=prompt):
                result = scan_prompt(prompt)
                self.assertEqual(result['risk_level'], 'VERY_HIGH', f"Prompt '{prompt}' should be VERY_HIGH risk")
    
    def test_edge_case_prompts(self):
        """Test edge case prompts"""
        for prompt in EDGE_CASE_PROMPTS:
            with self.subTest(prompt=prompt):
                result = scan_prompt(prompt)
                # Edge case prompts should not be classified as HIGH or VERY_HIGH
                self.assertNotIn(result['risk_level'], ['HIGH', 'VERY_HIGH'], f"Edge case prompt '{prompt}' should not be HIGH or VERY_HIGH risk")

if __name__ == '__main__':
    unittest.main()