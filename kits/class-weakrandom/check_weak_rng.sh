#!/bin/bash

# This script checks for weak random number generation in binaries and libraries
# It's designed to be run on your own computer (not a target system)
# Usage: ./check_weak_rng.sh <binary_or_library>

if [ $# -eq 0 ]; then
    echo "Usage: $0 <binary_or_library>"
    exit 1
fi

TARGET="$1"

echo "Checking for weak random number generation in: $TARGET"
echo "========================================================"

# Check for common insecure RNG function calls
echo "1. Checking for insecure RNG calls:"
strings "$TARGET" | grep -E "(rand|random|srand)" | sort -u

# Check for usage of /dev/random instead of /dev/urandom (which is often problematic)
echo -e "\n2. Checking for device random access:"
if [ -e "$TARGET" ]; then
    ldd "$TARGET" 2>/dev/null | grep -v "not a dynamic executable" | grep -E "(lib.*random|lib.*crypto)" || echo "No crypto libraries found"
fi

# Check for common weak RNG patterns in source code (if available)
echo -e "\n3. Checking for common weak RNG usage patterns in source:"
find "$TARGET" -name "*.c" -o -name "*.cpp" -o -name "*.h" 2>/dev/null | head -5 | while read file; do
    if [ -f "$file" ]; then
        echo "Source file: $file"
        grep -n -E "(rand\(|srand\(|random\()" "$file" 2>/dev/null || echo "No insecure RNG found in this file"
    fi
done

echo -e "\nCheck complete. Review the results to identify potential weak RNG usage."