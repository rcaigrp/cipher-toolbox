#!/bin/bash

# Check if Fuseki is installed and what version it is
# This script checks for the presence of Fuseki and its version.
# It does not modify any system state.

echo "Checking for Apache Jena Fuseki installation..."

# Try to find Fuseki jar files
FUSEKI_JAR=$(find /opt -name "fuseki-server*.jar" 2>/dev/null | head -1)
if [ -z "$FUSEKI_JAR" ]; then
    FUSEKI_JAR=$(find /usr -name "fuseki-server*.jar" 2>/dev/null | head -1)
fi

if [ -n "$FUSEKI_JAR" ]; then
    echo "Found Fuseki JAR: $FUSEKI_JAR"
    
    # Extract version from the jar file name (e.g., fuseki-server-6.2.0.jar)
    VERSION=$(basename "$FUSEKI_JAR" | sed -n 's/.*fuseki-server-\([0-9.]*\)\.jar/\1/p')
    
    if [ -n "$VERSION" ]; then
        echo "Detected Fuseki version: $VERSION"
        
        # Check if version is affected (6.2.0 or earlier)
        if [[ "$VERSION" == "6.2.0" ]] || [[ "$VERSION" < "6.3.0" ]]; then
            echo "CRITICAL: This version is affected by CVE-2026-86155"
            exit 1
        else
            echo "OK: Version $VERSION is not affected"
            exit 0
        fi
    else
        echo "WARNING: Could not extract version from JAR name"
        exit 2
    fi
else
    echo "INFO: No Fuseki installation found on this system"
    exit 0
fi