import random

# Test cases for weak random usage
x = random.random()  # Should be detected
y = random.randint(1, 10)  # Should be detected
z = random.uniform(1.0, 10.0)  # Should be detected

import os
# This should be detected (srand)
os.system("srand")

# Test other patterns
a = rand()  # Should be detected
b = srand()  # Should be detected
c = getrandom()  # Should be detected

# Math.random() - should be detected
d = Math.random()

# More complex patterns
def some_function():
    return random.choice([1, 2, 3])  # Should be detected

# This should NOT be detected (secure random)
import secrets
secure_random = secrets.token_hex(16)  # Secure random - should not be flagged