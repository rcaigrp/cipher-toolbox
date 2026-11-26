#!/bin/bash

# Check for exposure to legacy ASP.NET authentication bypass vulnerabilities

echo "Checking for legacy ASP.NET authentication bypass exposure..."

# Check for vulnerable Idunno.AntiCsrf library usage
if grep -r "Idunno.AntiCsrf" . --include="*.csproj" --include="*.xml" 2>/dev/null; then
    echo "WARNING: Idunno.AntiCsrf library detected in project files"
    grep -r "Idunno.AntiCsrf" . --include="*.csproj" --include="*.xml" 2>/dev/null
fi

# Check for legacy ASP.NET WebForms usage
if find . -name "*.aspx" -o -name "*.ascx" | head -n 1 >/dev/null 2>&1; then
    echo "INFO: Legacy ASP.NET WebForms files detected"
    find . -name "*.aspx" -o -name "*.ascx" | head -n 5
fi

# Check for binary serialization usage in code
if grep -r "BinaryFormatter\|SoapFormatter" . --include="*.cs" 2>/dev/null; then
    echo "WARNING: Binary/SoapFormatter usage detected in source code"
    grep -r "BinaryFormatter\|SoapFormatter" . --include="*.cs" 2>/dev/null
fi

# Check for vulnerable session state configuration
if grep -r "cookieless" . --include="*.xml" --include="*.config" 2>/dev/null | grep -i "true"; then
    echo "INFO: Cookieless session state detected (potential risk)"
    grep -r "cookieless" . --include="*.xml" --include="*.config" 2>/dev/null | grep -i "true"
fi

echo "Check complete."