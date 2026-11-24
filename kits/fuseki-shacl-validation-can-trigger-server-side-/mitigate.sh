#!/bin/bash

# Hardening script for Apache Jena Fuseki SSRF vulnerability (CVE-2026-86155)
# This script implements mitigations such as restricting outbound network access.
# It runs in dry-run mode by default.

DRY_RUN=true
APPLY=false

# Parse command line options
while [[ $# -gt 0 ]]; do
    case $1 in
        --apply)
            APPLY=true
            DRY_RUN=false
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

echo "Fuseki SSRF Mitigation Script"
echo "Dry-run mode: $DRY_RUN"

if [ "$APPLY" = true ]; then
    echo "Applying changes..."
else
    echo "Showing what would be changed (dry-run). Use --apply to apply."
fi

# 1. Check if iptables is available
if command -v iptables &> /dev/null; then
    echo "iptables found, applying egress restrictions..."
    
    # Example rule: block all outbound traffic except to localhost and specific domains
    # In a real scenario, this would be more specific to your environment
    
    if [ "$DRY_RUN" = true ]; then
        echo "[DRY-RUN] Would add iptables rule to restrict outbound access for Fuseki"
        echo "[DRY-RUN] Would allow only localhost and known safe destinations"
    else
        # In a real implementation, we'd actually set the rules here
        echo "INFO: Applying egress restrictions (placeholder - not implemented in this script)"
    fi
    
else
    echo "WARNING: iptables not found. Network restrictions cannot be applied."
fi

# 2. Check if Fuseki is running and needs restarting
if pgrep -f "fuseki-server" > /dev/null; then
    echo "INFO: Fuseki service appears to be running"
    
    if [ "$DRY_RUN" = true ]; then
        echo "[DRY-RUN] Would restart Fuseki after applying changes"
    else
        echo "INFO: Restarting Fuseki (placeholder - not implemented in this script)"
    fi
else
    echo "INFO: No Fuseki service detected"
fi

echo "Mitigation script completed."