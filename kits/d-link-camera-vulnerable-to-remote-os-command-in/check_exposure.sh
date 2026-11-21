#!/usr/bin/env bash
set -euo pipefail

if (( $# > 1 )); then
    printf 'Usage: %s [local-camera-inventory.tsv]\n' "$0" >&2
    exit 2
fi

printf 'Local TCP listeners on ports 80 and 443\n'
if command -v ss >/dev/null && listeners=$(ss -H -ltn '( sport = :80 or sport = :443 )'); then
    printf '%s\n' "${listeners:-No matching TCP listeners in this network namespace.}"
else
    printf 'Listener check unavailable.\n'
fi
printf 'Local listeners alone cannot establish camera identity or internet reachability.\n'

if (( $# == 0 )); then
    printf 'Verdict: UNKNOWN. Supply a local inventory export to evaluate camera firmware and recorded exposure.\n'
    exit 0
fi
if [[ ! -f $1 || ! -r $1 ]]; then
    printf 'Inventory must be a readable local regular file.\n' >&2
    exit 2
fi

# Each row contains model, firmware, and management exposure separated by tabs.
# Exposure values are internet, unrestricted, restricted, or unknown.
awk -F '\t' '
    { sub(/\r$/, "") }
    /^[[:space:]]*($|#)/ { next }
    $0 == "model\tfirmware\tmanagement_exposure" { next }
    NF != 3 || $1 == "" || $2 == "" || $3 !~ /^(internet|unrestricted|restricted|unknown)$/ {
        printf "Invalid inventory row %d\n", NR > "/dev/stderr"
        invalid = 1
        next
    }
    toupper($1) == "DCS-935L" {
        cameras++
        if ($2 == "1.10.01") {
            firmware = "affected firmware confirmed by supplied advisory"
            affected++
        } else {
            firmware = "firmware vulnerability status unconfirmed"
        }
        printf "Inventory row %d: DCS-935L %s, %s, recorded management exposure: %s\n", NR, $2, firmware, $3
        if ($3 == "internet" || $3 == "unrestricted") {
            print "Action: isolate this device immediately."
            risky++
        }
    }
    END {
        if (invalid) {
            print "Verdict: INCOMPLETE. Correct invalid rows and rerun."
            exit 2
        }
        if (risky) print "Verdict: ISOLATE NOW. Inventory records unrestricted or internet-facing management."
        else if (affected) print "Verdict: AFFECTED FIRMWARE PRESENT. Verify management isolation and plan replacement."
        else if (cameras) print "Verdict: END-OF-LIFE CAMERAS PRESENT. Firmware vulnerability status is unconfirmed."
        else print "Verdict: NO DCS-935L LISTED. Result depends on inventory completeness."
        if (cameras) print "Fixed firmware version: unconfirmed."
    }
' < "$1"
