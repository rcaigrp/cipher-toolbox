#!/bin/bash
# Check script for weak random number generation in shell scripts.
# This is a read-only check and does not make any changes to the system.

echo "Checking for weak random number generation in shell scripts..."

# Look for common insecure patterns
grep -r "rand\|RANDOM" . --include="*.sh" | grep -v "#.*rand\|#.*RANDOM" || echo "No insecure patterns found."

echo "Check complete."