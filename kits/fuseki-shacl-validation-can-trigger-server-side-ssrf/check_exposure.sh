#!/bin/bash

# Check exposure to CVE-2026-86155: Fuseki SHACL validation SSRF

echo "Checking for Apache Jena Fuseki exposure..."

# Check if fuseki is installed (simple check)
if command -v fuseki-server &> /dev/null; then
    echo "Found fuseki-server command."

    # Try to get version, if available
    VERSION=$(fuseki-server --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
    if [ -n "$VERSION" ]; then
        echo "Fuseki version: $VERSION"

        # Check if version is vulnerable (6.2.0 or earlier)
        IFS='.' read -r major minor patch <<< "$VERSION"
        if [ "$major" -lt 6 ] || ([ "$major" -eq 6 ] && [ "$minor" -lt 3 ]); then
            echo "VULNERABLE: Fuseki version $VERSION is affected by CVE-2026-86155"
            exit 1
        else
            echo "NOT VULNERABLE: Fuseki version $VERSION is patched"
        fi
    else
        echo "Could not determine Fuseki version."
        # Assume vulnerable if installed but version unknown
        echo "UNKNOWN: Could not determine version, assuming vulnerable"
        exit 1
    fi
else
    echo "NOT INSTALLED: Fuseki is not installed on this system"
fi

# Check for common Fuseki listening ports (if running)
if ss -tuln | grep -qE ':(8080|3030)'; then
    echo "RUNNING: Fuseki appears to be running (listening on port 8080 or 3030)"
else
    echo "NOT RUNNING: No Fuseki service detected listening on common ports"
fi

exit 0