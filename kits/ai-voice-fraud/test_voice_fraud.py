#!/usr/bin/env python3

import unittest
import subprocess
import os

class TestVoiceFraudDetection(unittest.TestCase):
    def test_script_exists(self):
        self.assertTrue(os.path.exists('kits/ai-voice-fraud/detect_voice_fraud.py'))

if __name__ == '__main__':
    unittest.main()