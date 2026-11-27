#!/usr/bin/env python3

import random
import secrets

# This file contains secure random usage patterns

def test_secure_random():
    # These are secure
    secure_token = secrets.token_hex(16)
    secure_bytes = secrets.token_bytes(32)
    secure_urlsafe = secrets.token_urlsafe(32)
    
    # This is also secure (SystemRandom)
    sys_random = random.SystemRandom()
    secure_choice = sys_random.choice(['a', 'b', 'c'])
    
    return secure_token, secure_bytes, secure_urlsafe, secure_choice

if __name__ == "__main__":
    test_secure_random()