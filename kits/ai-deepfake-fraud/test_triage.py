#!/usr/bin/env python3
"""Test triage module."""

import unittest
from pathlib import Path
import tempfile

# Add the current directory to path so we can import the module
import sys
sys.path.insert(0, '/home/mind/bots/cipher/kits/ai-deepfake-fraud')

from triage import triage


class TestTriage(unittest.TestCase):
    def test_normal_text(self):
        """Test a normal text."""
        result = triage("What is the weather like today?")
        self.assertFalse(result["review"])
        self.assertEqual(result["rule_signals"], [])
        self.assertEqual(result["model_status"], "unavailable")

    def test_financial_request(self):
        """Test a financial request."""
        result = triage("Please wire $5000 to my account immediately.")
        self.assertTrue(result["review"])
        self.assertIn("financial_request", result["rule_signals"])

    def test_urgent_request(self):
        """Test an urgent request."""
        result = triage("This is urgent. Send the payment now before the close of business.")
        self.assertTrue(result["review"])
        self.assertIn("urgency", result["rule_signals"])

    def test_sensitive_request(self):
        """Test a sensitive data request."""
        result = triage("Please send me your password and one-time code.")
        self.assertTrue(result["review"])
        self.assertIn("sensitive_request", result["rule_signals"])


if __name__ == "__main__":
    unittest.main()