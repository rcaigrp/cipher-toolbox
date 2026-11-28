import random

def test_function():
    # This should be detected as weak random usage
    x = random.random()
    y = random.randint(1, 10)
    
    # This should also be detected
    z = rand()
    
    return x, y, z