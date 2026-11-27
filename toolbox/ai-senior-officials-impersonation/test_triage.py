#!/usr/bin/env python3
"""
Test suite for AI Senior Officials Impersonation Triage Tool
"""

import subprocess
import sys
import unittest
from pathlib import Path
from triage import triage_text

class TestTriage(unittest.TestCase):
    
    def test_malicious_patterns(self):
        # Test cases that should be flagged as MALICIOUS
        malicious_texts = [
            "This is an urgent matter requiring immediate action",
            "Official government verification needed for your account",
            "Please transfer funds immediately via wire payment",
            "Security breach requires urgent confirmation",
            "Financial investigation demands immediate attention",
            "Confidential information requires urgent review"
        ]
        
        for text in malicious_texts:
            with self.subTest(text=text):
                self.assertEqual(triage_text(text), 'MALICIOUS')
    
    def test_safe_patterns(self):
        # Test cases that should be flagged as SAFE
        safe_texts = [
            "Hello, how are you today?",
            "Please review the attached document",
            "Meeting scheduled for tomorrow at 2 PM",
            "Thank you for your cooperation",
            "The report has been completed"
        ]
        
        for text in safe_texts:
            with self.subTest(text=text):
                self.assertEqual(triage_text(text), 'SAFE')
    
    def test_mixed_patterns(self):
        # Test cases that should be flagged as MALICIOUS (contains malicious keywords)
        mixed_texts = [
            "This is an urgent official matter requiring immediate action",
            "Please confirm your account details for the financial transfer",
            "Security verification required urgently"
        ]
        
        for text in mixed_texts:
            with self.subTest(text=text):
                self.assertEqual(triage_text(text), 'MALICIOUS')

class TestCLI(unittest.TestCase):
    def test_help(self):
        result = subprocess.run(
            [sys.executable, 'triage.py', '--help'],
            cwd=Path(__file__).resolve().parent,
            capture_output=True, text=True, check=True,
        )
        self.assertIn('usage:', result.stdout)

    def test_sample_file(self):
        result = subprocess.run(
            [sys.executable, 'triage.py', 'sample_inputs.txt'],
            cwd=Path(__file__).resolve().parent,
            capture_output=True, text=True, check=True,
        )
        labels = [line.split()[1] for line in result.stdout.splitlines()]
        self.assertEqual(labels, ['MALICIOUS'] * 3 + ['SAFE'] * 5 + ['MALICIOUS'] * 2)

    def test_interactive_exit(self):
        for ending in ('', 'quit\n'):
            with self.subTest(ending=ending):
                result = subprocess.run(
                    [sys.executable, 'triage.py'],
                    cwd=Path(__file__).resolve().parent,
                    input='Hello, how are you today?\n' + ending,
                    capture_output=True, text=True, check=True,
                )
                self.assertIn('Result: SAFE', result.stdout)
                self.assertEqual(result.stderr, '')


if __name__ == '__main__':
    unittest.main()