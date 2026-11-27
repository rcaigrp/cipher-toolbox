#!/usr/bin/env python3

import random
import secrets

# This file contains various patterns of weak random usage for testing

def test_insecure_random():
    # These should be detected as insecure
    x = random.randint(1, 10)
    y = random.random()
    z = random.choice(['a', 'b', 'c'])
    a = random.randrange(100)
    b = random.uniform(1.0, 10.0)
    
    # This is secure
    secure_random = secrets.token_hex(16)
    
    # This should also be detected as insecure (even though it's not a direct call)
    random.seed(42)  # Predictable seeding
    
    return x, y, z, a, b, secure_random

if __name__ == "__main__":
    test_insecure_random()