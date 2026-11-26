#!/usr/bin/env python3

import subprocess
import sys

def run_test(transcript, expected):
    """Run a test case and check if result matches expectation."""
    result = subprocess.run([
        sys.executable, "detect_voice_fraud.py", "--input", transcript
    ], capture_output=True, text=True)
    
    if result.returncode == 1:
        detected = "VOICE FRAUD DETECTED"
    else:
        detected = "Safe communication."
    
    print(f"Input: {transcript}")
    print(f"Expected: {expected}")
    print(f"Got: {detected}")
    print("---")
    
    return detected == expected

def main():
    test_cases = [
        ("Hello, this is John from IT. I need to verify your account details.", "Safe communication."),
        ("Urgent money transfer needed immediately. Send $5000 now.", "VOICE FRAUD DETECTED"),
        ("Can you please verify your account information?", "Safe communication."),
        ("Emergency funds required for immediate payment.", "VOICE FRAUD DETECTED"),
    ]
    
    print("Running voice fraud detection tests...\n")
    
    all_passed = True
    for transcript, expected in test_cases:
        if not run_test(transcript, expected):
            all_passed = False
    
    if all_passed:
        print("All tests passed!")
    else:
        print("Some tests failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()