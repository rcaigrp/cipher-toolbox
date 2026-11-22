#!/usr/bin/env bash
set -euo pipefail

if (( $# != 0 )); then
    echo 'Usage: check_exposure.sh' >&2
    exit 2
fi

printf '%s\n' 'Meta Muse and browser-enabled assistant exposure check' \
    'Verdict: UNKNOWN for Meta Muse. The supplied material gives no affected or fixed version and no documented local product identifier.' \
    'Approval policy: UNVERIFIED. Confirm that a trusted gateway requires user approval scoped to the resource and operation before a browsing assistant can read chat history or saved memories.' \
    'Local TCP/UDP listeners (inventory only):'

if command -v ss >/dev/null 2>&1; then
    if ! ss -lntu; then
        echo 'Listener inventory unavailable: ss failed.' >&2
    fi
else
    echo 'Listener inventory unavailable: ss is not installed.' >&2
fi

printf '%s\n' 'A local listener does not establish a link to Muse. A browser-only deployment can have no local listener.'
