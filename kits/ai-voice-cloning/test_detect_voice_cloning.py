#!/usr/bin/env python3
"""
Test script for voice cloning detection.
"""
import subprocess
import sys

def run_test(transcript, expected):
    result = subprocess.run([
        sys.executable, "detect_voice_cloning.py",
        "--input", transcript
    ], capture_output=True, text=True)
    output = result.stdout.strip()
    if output == expected:
        print(f"✓ PASS: '{transcript}' -> {output}")
        return True
    else:
        print(f"✗ FAIL: '{transcript}' -> {output} (expected {expected})")
        return False

def main():
    tests = [
        ("Urgent wire transfer needed immediately", "REVIEW NEEDED"),
        ("Can you help me with my homework?", "NO SIGNAL"),
        ("Do not call the bank, bypass approval", "REVIEW NEEDED"),
        ("What's the weather today?", "NO SIGNAL")
    ]

    all_passed = True
    for transcript, expected in tests:
        if not run_test(transcript, expected):
            all_passed = False

    if all_passed:
        print("\nAll tests passed!")
    else:
        print("\nSome tests failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()