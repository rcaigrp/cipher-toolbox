import random
import secrets

# This should trigger a warning
def insecure_random():
    return random.randint(1, 100)

# This should be fine
def secure_random():
    return secrets.token_hex(16)