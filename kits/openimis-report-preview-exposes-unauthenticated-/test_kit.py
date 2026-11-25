#!/usr/bin/env python3
"""Test the openIMIS kit scripts."""

import subprocess
import sys


def test_check_exposure_help():
    result = subprocess.run([sys.executable, 'check_exposure.py', '--help'],
                            capture_output=True, text=True, check=True)
    assert '--release' in result.stdout
    assert '--port' in result.stdout
    print("✅ check_exposure.py --help works")


def test_mitigate_help():
    result = subprocess.run([sys.executable, 'mitigate.py', '--help'],
                            capture_output=True, text=True, check=True)
    assert '--output' in result.stdout
    assert '--apply' in result.stdout
    print("✅ mitigate.py --help works")


def test_check_exposure_no_args():
    result = subprocess.run([sys.executable, 'check_exposure.py'],
                            capture_output=True, text=True)
    assert result.returncode != 0
    print("✅ check_exposure.py with no args fails as expected")


def test_mitigate_no_args():
    result = subprocess.run([sys.executable, 'mitigate.py'],
                            capture_output=True, text=True)
    assert result.returncode != 0
    print("✅ mitigate.py with no args fails as expected")


if __name__ == '__main__':
    test_check_exposure_help()
    test_mitigate_help()
    test_check_exposure_no_args()
    test_mitigate_no_args()
    print("All tests passed!")