#!/usr/bin/env python3

import unittest
import json
from data_exposure_detector import DataExposureDetector

class TestDataExposureDetector(unittest.TestCase):
    def setUp(self):
        self.detector = DataExposureDetector()
    
    def test_pii_detection(self):
        """Test detection of personal identifiable information"""
        # Test SSN pattern
        prompt_with_ssn = "My social security number is 123-45-6789"
        result = self.detector.analyze_prompt(prompt_with_ssn)
        
        self.assertTrue(result['has_exposure'])
        self.assertEqual(result['risk_level'], 'medium')
    
    def test_email_detection(self):
        """Test detection of email addresses"""
        prompt_with_email = "Contact me at user@example.com for more info"
        result = self.detector.analyze_prompt(prompt_with_email)
        
        self.assertTrue(result['has_exposure'])
        self.assertEqual(result['risk_level'], 'medium')
    
    def test_secret_detection(self):
        """Test detection of secret/credential indicators"""
        prompt_with_secret = "The API key is abc123def456"
        result = self.detector.analyze_prompt(prompt_with_secret)
        
        self.assertTrue(result['has_exposure'])
        self.assertEqual(result['risk_level'], 'medium')
    
    def test_normal_prompt(self):
        """Test that normal prompts don't trigger false positives"""
        normal_prompt = "What is the weather like today?"
        result = self.detector.analyze_prompt(normal_prompt)
        
        # Should not be flagged as having exposure
        self.assertFalse(result['has_exposure'])
        self.assertEqual(result['risk_level'], 'low')

if __name__ == '__main__':
    unittest.main()