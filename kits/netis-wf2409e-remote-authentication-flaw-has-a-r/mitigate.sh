#!/usr/bin/env bash
set -euo pipefail

usage() {
    echo 'Usage: bash mitigate.sh [--apply | --help]'
}

if (( $# > 1 )); then
    usage >&2
    exit 2
fi

case "${1-}" in
    --help|-h) usage; exit 0 ;;
    --apply)
        echo 'No changes applied. The supplied material has no verified device-specific procedure, and this host has no confirmed router enforcement role.' >&2
        exit 2
        ;;
    '') echo 'Dry run. Planned changes for an authorized administrator at the router or its upstream enforcement point:' ;;
    *) usage >&2; exit 2 ;;
esac

printf '%s\n' \
    'Disable WAN management on each inventoried WF2409E.' \
    'Remove WAN port forwards and IPv6 firewall exceptions that expose its management interface.' \
    'Limit management access to the approved management network.' \
    'Verify the model, hardware revision, and firmware against vendor records. The supplied material establishes no fixed release.' \
    'Confirm the resulting WAN policy and preserve approved management access.'
