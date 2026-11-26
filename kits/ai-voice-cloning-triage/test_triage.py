#!/usr/bin/env python3

import unittest
from triage import triage_input

class TestTriage(unittest.TestCase):
    def test_benign_input(self):
        result = triage_input("Hi, it's your sister. I'm at the airport and need some money for a cab.")
        self.assertFalse(result)

    def test_malicious_input(self):
        result = triage_input("I'm in trouble and need you to send me $500 immediately. Don't call me back — just wire it.")
        self.assertTrue(result)

    def test_pattern_detection(self):
        result = triage_input("I need money right now because I'm in a family emergency.")
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()