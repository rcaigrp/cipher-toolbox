#!/bin/bash
# File parsing exposure check

echo "Checking for vulnerable file parsing libraries..."

# Check if ImageMagick is installed (commonly vulnerable)
if command -v identify &> /dev/null; then
    echo "ImageMagick identified"
    # Check version
    identify -version | grep -i "version"
fi

# Check for known vulnerable library files in common paths
for lib_path in "/usr/lib" "/usr/local/lib" "/opt"; do
    if [ -d "$lib_path" ]; then
        find "$lib_path" -name "*jpeg*" -o -name "*tiff*" -o -name "*png*" 2>/dev/null | head -5
    fi
done

echo "Check complete. Review results for any vulnerable libraries."