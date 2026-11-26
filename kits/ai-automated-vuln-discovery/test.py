#!/usr/bin/env python3

import sys
import os
from unittest.mock import patch, MagicMock
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from detect_automated_discovery import is_automated_discovery_activity

def test_automated_discovery_detection():
    """Test the automated discovery detection with sample activities."""
    
    # Test cases: (activity, expected_is_automated, description)
    test_cases = [
        ("GET /index.html HTTP/1.1", False, "Normal web request"),
        ("GET /admin.php?user=admin HTTP/1.1", False, "Single parameter access"),
        ("GET /sqlmap HTTP/1.1", True, "Direct reference to vulnerability tool"),
        ("POST /login.php with parameters: user=admin&pass=password", False, "Standard login attempt"),
        ("GET /robots.txt HTTP/1.1", False, "Normal site exploration"),
        ("GET /test.php?param=1&param2=2&param3=3&param4=4 HTTP/1.1", True, "Multiple parameters, suspicious"),
        ("GET /config.php.bak HTTP/1.1", True, "Looking for backup files"),
        ("GET /admin/ HTTP/1.1", False, "Standard admin access"),
        ("GET /wp-content/plugins/ HTTP/1.1", True, "WordPress plugin enumeration"),
        ("GET /?a=1&b=2&c=3&d=4&e=5 HTTP/1.1", True, "Excessive parameters, likely automated"),
        ("GET /etc/passwd HTTP/1.1", True, "Path traversal attempt"),
        ("GET /index.php?id=1 UNION SELECT 1,2,3 HTTP/1.1", True, "SQL injection attempt"),
        ("GET /test.php?user=admin&pass=password&submit=1 HTTP/1.1", True, "Multiple parameters with credentials"),
    ]
    
    # Test with rules-only mode (no LLM)
    print("Testing Automated Vulnerability Discovery Detection...")
    print("=" * 60)
    
    failed_tests = []
    passed_tests = []
    
    for activity, expected, description in test_cases:
        result, confidence = is_automated_discovery_activity(activity, rules_only=True)
        if result == expected:
            print(f"✓ PASS: {description}")
            passed_tests.append(description)
        else:
            print(f"✗ FAIL: {description} - Expected {expected}, got {result}")
            failed_tests.append((description, expected, result))
    
    # Test with LLM integration
    print("\nTesting with LLM integration...")
    mock_response = MagicMock()
    mock_response.json.return_value = {"response": "automated"}
    
    with patch('requests.post', return_value=mock_response):
        try:
            result, confidence = is_automated_discovery_activity("GET /sqlmap HTTP/1.1", rules_only=False)
            if result == True:
                print("✓ PASS: LLM correctly identified automated activity")
            else:
                print("✗ FAIL: LLM did not identify automated activity as expected")
        except Exception as e:
            print(f"✗ FAIL: LLM test raised exception: {e}")
    
    # Summary
    if failed_tests:
        print(f"\n{len(failed_tests)} out of {len(test_cases)} tests failed!")
        for desc, expected, got in failed_tests:
            print(f"  - {desc}: expected {expected}, got {got}")
        return False
    else:
        print(f"\nAll {len(test_cases)} tests passed!")
        return True

if __name__ == "__main__":
    success = test_automated_discovery_detection()
    sys.exit(0 if success else 1)