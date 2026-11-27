#!/usr/bin/env python3

import subprocess
import sys
import os

def run_test():
    # Test 1: Help message
    print("Test 1: --help flag")
    result = subprocess.run([sys.executable, 'kits/class-weakrandom/check_weak_random.py', '--help'], 
                          capture_output=True, text=True)
    if '--help' in result.stdout:
        print("✅ Help works correctly")
    else:
        print("❌ Help doesn't work properly")
        return False
    
    # Test 2: No file provided
    print("\nTest 2: No file provided (should show help)")
    result = subprocess.run([sys.executable, 'kits/class-weakrandom/check_weak_random.py'], 
                          capture_output=True, text=True)
    if 'Usage:' in result.stdout:
        print("✅ No file handling works correctly")
    else:
        print("❌ No file handling doesn't work properly")
        return False
        
    # Test 3: File with weak random usage
    print("\nTest 3: File with weak random usage")
    test_content = '''import random
print(random.randint(1, 10))
x = random.random()
y = random.choice([1,2,3])'''
    
    with open('test_weak.py', 'w') as f:
        f.write(test_content)
        
    result = subprocess.run([sys.executable, 'kits/class-weakrandom/check_weak_random.py', 'test_weak.py'], 
                          capture_output=True, text=True)
    if 'Found weak random usage' in result.stdout and 'Line 2' in result.stdout:
        print("✅ Weak random detection works correctly")
    else:
        print("❌ Weak random detection doesn't work properly")
        print(f"Output: {result.stdout}")
        return False
    
    # Test 4: File with secure random usage
    print("\nTest 4: File with secure random usage")
    secure_content = '''import secrets
print(secrets.token_hex(16))'''
    
    with open('test_secure.py', 'w') as f:
        f.write(secure_content)
        
    result = subprocess.run([sys.executable, 'kits/class-weakrandom/check_weak_random.py', 'test_secure.py'], 
                          capture_output=True, text=True)
    if 'No weak random usage found' in result.stdout:
        print("✅ Secure random detection works correctly")
    else:
        print("❌ Secure random detection doesn't work properly")
        return False
        
    # Cleanup
    try:
        os.remove('test_weak.py')
        os.remove('test_secure.py')
    except:
        pass
    
    return True

if __name__ == "__main__":
    if run_test():
        print("\n✅ All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)