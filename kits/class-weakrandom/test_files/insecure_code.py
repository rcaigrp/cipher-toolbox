import random

# Insecure usage of randomness (should be detected)
x = random.randint(1, 100)
y = random.random()
z = random.randrange(10)