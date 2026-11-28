#!/bin/bash

# Check for weak random number generation in binaries and libraries
# This script uses readelf and strings to identify potential weak RNG usage

if [ $# -eq 0 ]; then
    echo "Usage: $0 <binary_or_library>"
    exit 1
fi

BINARY="$1"

# Check if file exists
if [ ! -f "$BINARY" ]; then
    echo "Error: File '$BINARY' not found"
    exit 1
fi

echo "Checking $BINARY for weak random number generation patterns..."

# Look for common weak RNG function names in the binary
WEAK_FUNCTIONS=("rand" "random" "srand" "randomize")

FOUND_WEAK=false

for func in "${WEAK_FUNCTIONS[@]}"; do
    if strings "$BINARY" | grep -q -i "$func"; then
        echo "Found potential weak RNG reference: $func"
        FOUND_WEAK=true
    fi
done

# Check for specific libc functions that might be used insecurely
if strings "$BINARY" | grep -q "libc.*rand\|libm.*random"; then
    echo "Found references to standard library random functions"
    FOUND_WEAK=true
fi

# Check for common entropy sources that are often weak
ENTROPY_SOURCES=("time()" "getpid()" "clock()")
for source in "${ENTROPY_SOURCES[@]}"; do
    if strings "$BINARY" | grep -q "$source"; then
        echo "Found potential weak entropy source: $source"
        FOUND_WEAK=true
    fi
done

if [ "$FOUND_WEAK" = false ]; then
    echo "No obvious weak random patterns detected"
fi