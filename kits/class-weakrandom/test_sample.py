import random
import secrets

# Weak random usage
def weak_random_func():
    return random.random()

def another_weak_func():
    return random.randint(1, 10)

# Secure random usage
def secure_random_func():
    return secrets.token_hex(16)