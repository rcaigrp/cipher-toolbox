#!/usr/bin/env python3

import unittest
from triage import triage_input

class TestTriage(unittest.TestCase):
    def test_benign_input(self):
        result = triage_input("Hi, it's your colleague. I need to discuss a project update.")
        self.assertFalse(result)

    def test_malicious_input(self):
        result = triage_input("I'm in urgent need of funds for an emergency. Please send $500 immediately.")
        self.assertTrue(result)

    def test_pattern_detection(self):
        result = triage_input("This is a federal emergency and I need money right now.")
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()