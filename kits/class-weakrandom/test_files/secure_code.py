import secrets
import random

# Secure usage of randomness
token = secrets.token_hex(16)
secure_random = secrets.randbelow(100)

# Insecure usage (should be detected)
insecure_random = random.randint(1, 100)