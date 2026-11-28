#!/usr/bin/env python3
"""
Comprehensive test for the check_weak_random.py script.
Tests various scenarios of weak random usage.
"""

import random
import secrets

# Weak random usage - should be detected
def weak_random_func():
    return random.random()

def another_weak_func():
    return random.randint(1, 10)

def yet_another_weak_func():
    return random.uniform(1.0, 10.0)

# Secure random usage - should not be detected
def secure_random_func():
    return secrets.token_hex(16)

def another_secure_func():
    return secrets.randbelow(100)