#!/usr/bin/env bash
set -euo pipefail

usage() {
    printf 'Usage: %s [--apply] [--pause-unit NAME.service]...\n' "$0"
    printf 'Select only verified unattended OpenPGP receivers. The default previews all actions.\n'
}

apply=0
units=()
while (( $# )); do
    case $1 in
        --apply) apply=1; shift ;;
        --pause-unit)
            if (( $# < 2 )) || [[ ! $2 =~ ^[a-zA-Z0-9_][a-zA-Z0-9_.@-]*\.service$ ]]; then
                usage >&2
                exit 2
            fi
            units+=("$2")
            shift 2
            ;;
        --help|-h) usage; exit 0 ;;
        *) usage >&2; exit 2 ;;
    esac
done

printf 'Deploy GPGME 2.3.1 or a distributor-confirmed T8557 backport through your normal package or application update process. Restart affected consumers after deployment, then verify their mapped libraries.\n'
printf 'Until then, pause unattended processing of untrusted keys and signed data. Check for socket, timer, queue or supervisor activation before relying on a stopped service.\n'
if (( ${#units[@]} == 0 )); then
    printf 'No receiver units selected. No host changes were made.\n'
    if (( apply )); then exit 2; fi
    exit 0
fi

if (( ! apply )); then
    printf 'DRY RUN: would run systemctl stop --'
    printf ' %q' "${units[@]}"
    printf '\n'
    exit 0
fi

for unit in "${units[@]}"; do
    load_state=$(systemctl show --property=LoadState --value -- "$unit")
    if [[ $load_state != loaded ]]; then
        printf 'Cannot stop %s: systemd load state is %s.\n' "$unit" "$load_state" >&2
        exit 2
    fi
done
systemctl stop -- "${units[@]}"
for unit in "${units[@]}"; do
    state=$(systemctl show --property=ActiveState --value -- "$unit")
    if [[ $state != inactive && $state != failed ]]; then
        printf '%s is %s after the stop request. Check its activation sources.\n' "$unit" "$state" >&2
        exit 1
    fi
    printf '%s is %s.\n' "$unit" "$state"
done
