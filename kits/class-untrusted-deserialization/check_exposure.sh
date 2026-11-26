#!/bin/bash

# Check for untrusted deserialization exposure in .NET applications
# This script identifies potential vulnerable components by looking for
# usage of dangerous serializers in .NET assemblies and configuration files

echo "Checking for untrusted deserialization exposure..."

# Find .NET assemblies that might contain dangerous deserialization code
find . -name "*.dll" -o -name "*.exe" | while read -r file; do
    if [[ -f "$file" ]]; then
        # Check for use of BinaryFormatter or SoapFormatter in assembly metadata
        if strings "$file" | grep -q -i "System\.Runtime\.Serialization\.Formatters\.BinaryFormatter\|System\.Runtime\.Serialization\.Formatters\.SoapFormatter"; then
            echo "Potential dangerous serializer found in: $file"
        fi
    fi
done

# Check for configuration files that might contain unsafe deserialization settings
find . -name "web.config" -o -name "app.config" | while read -r config_file; do
    if [[ -f "$config_file" ]]; then
        # Look for legacy serialization settings
        if grep -q -i "BinaryFormatter\|SoapFormatter\|formatter" "$config_file"; then
            echo "Potential unsafe deserialization configuration found in: $config_file"
        fi
    fi
done

# Check for usage of dangerous deserialization methods in source code (C#)
find . -name "*.cs" | while read -r source_file; do
    if [[ -f "$source_file" ]]; then
        # Look for BinaryFormatter or SoapFormatter usage
        if grep -q -i "BinaryFormatter\|SoapFormatter" "$source_file"; then
            echo "Potential dangerous deserialization method found in: $source_file"
        fi
        
        # Look for unsafe serialization patterns that could lead to deserialization
        if grep -q -E "(Deserialize|ReadObject)" "$source_file" && grep -q -i "request\|cookie\|form\|session" "$source_file"; then
            echo "Potential untrusted deserialization pattern found in: $source_file"
        fi
    fi
done

echo "Check complete."