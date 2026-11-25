#!/usr/bin/env bash
set -euo pipefail

if [[ $# -gt 0 ]]; then
    case "$1" in
        -h|--help) echo 'Usage: bash check_exposure.sh. Inventory local TCP listeners on HTTP(S) management ports without making network requests.'; exit 0 ;;
        *) echo 'Usage: bash check_exposure.sh' >&2; exit 2 ;;
    esac
fi

if ! command -v ss >/dev/null; then
    echo 'VERDICT: UNKNOWN. ss (iproute2) is required to inspect local listeners.' >&2
    exit 2
fi

if ! listeners=$(ss -H -ltn '( sport = :80 or sport = :443 or sport = :8080 or sport = :8443 )'); then
    echo 'VERDICT: UNKNOWN. Could not inspect local listeners.' >&2
    exit 2
fi

if [[ -z "$listeners" ]]; then
    echo 'VERDICT: NO MATCHING LOCAL TCP LISTENERS on ports 80, 443, 8080, or 8443.'
else
    printf '%s\n' "$listeners"
    if awk '$4 !~ /^(127\.|\[::1\]:)/ { found=1 } END { exit !found }' <<< "$listeners"; then
        echo 'VERDICT: REVIEW. At least one matching listener is bound beyond loopback. Verify its owner and firewall policy.'
    else
        echo 'VERDICT: Matching listeners bind only to loopback.'
    fi
fi

printf '%s\n' \
    'Router identity, WAN management, upstream forwarding, and internet reachability require separate verification from existing inventory or configuration records.' \
    'Firmware verdict: UNKNOWN. Record the exact model, hardware revision, and installed firmware from existing records. The supplied material identifies no verified fixed release for comparison.'
