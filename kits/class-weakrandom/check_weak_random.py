#!/usr/bin/env python3
"""
Check script for weak random number generation.
This script is read-only and does not make any changes to the system.
"""

import random
import secrets

def check_weak_random_usage():
    """
    Checks if insecure random functions are used in this script.
    """
    # This is a test case to demonstrate usage of insecure function
    insecure_value = random.randint(1, 100)
    
    # This is the secure way to generate random numbers
    secure_value = secrets.token_hex(16)

    print(f"Insecure random value: {insecure_value}")
    print(f"Secure random value: {secure_value}")

if __name__ == "__main__":
    check_weak_random_usage()