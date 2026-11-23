#!/bin/bash
# Simple check for dangerous system command patterns in scripts
echo "Checking for potential command injection patterns..."

# Find files with system command execution
find . -name "*.sh" -o -name "*.bash" 2>/dev/null | while read file; do
    if [ -n "$file" ] && [ -f "$file" ]; then
        echo "Checking $file"
        # Check for problematic patterns
        grep -n -E "(exec|system|sh -c|eval)" "$file" 2>/dev/null
    fi
done

# Check for string concatenation with variables in system context
find . -name "*.sh" -o -name "*.bash" 2>/dev/null | while read file; do
    if [ -n "$file" ] && [ -f "$file" ]; then
        echo "Checking variable interpolation in $file"
        grep -n '\$[a-zA-Z_][a-zA-Z0-9_]*' "$file" 2>/dev/null | head -5
    fi
done