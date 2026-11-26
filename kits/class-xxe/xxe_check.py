#!/usr/bin/env python3
"""
Check for exposure to XXE vulnerabilities in XML processing.

This script checks if a system might be vulnerable by scanning for common
XXE patterns that can lead to insecure XML parsing.
"""

import re
import sys

def check_xxe_safety(xml_content):
    """
    Check if XML content contains XXE patterns.

    Args:
        xml_content (str): The XML content to validate.

    Returns:
        bool: True if the XML appears safe, False otherwise.
    """
    # Check for common XXE patterns
    xxe_patterns = [
        re.compile(r'<!ENTITY.*SYSTEM', re.IGNORECASE),
        re.compile(r'<!ENTITY.*PUBLIC', re.IGNORECASE),
        re.compile(r'file://\/etc\/passwd', re.IGNORECASE),
        re.compile(r'http:\/\/', re.IGNORECASE)
    ]

    for pattern in xxe_patterns:
        if pattern.search(xml_content):
            return False

    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 xxe_check.py <xml_file>")
        sys.exit(1)

    xml_file = sys.argv[1]
    try:
        with open(xml_file, 'r') as f:
            content = f.read()
        
        is_safe = check_xxe_safety(content)
        if not is_safe:
            print(f"Potential XXE vulnerability detected in XML file: {xml_file}")
            sys.exit(1)
        else:
            print(f"XML file appears safe: {xml_file}")
    except Exception as e:
        print(f"Error reading XML file: {e}")
        sys.exit(1)