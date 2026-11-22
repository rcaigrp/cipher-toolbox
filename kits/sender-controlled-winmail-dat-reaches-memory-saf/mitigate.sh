#!/usr/bin/env bash
set -euo pipefail

usage() {
    printf 'Usage: %s [--apply] --stop-unit NAME.service\n' "$0"
    printf 'Select a dedicated systemd TNEF decoding worker. Dry-run is the default.\n'
}

apply=false
if [[ ${1:-} == --help ]]; then
    usage
    exit 0
fi
if [[ ${1:-} == --apply ]]; then
    apply=true
    shift
fi
if [[ $# != 2 || ${1:-} != --stop-unit || ! ${2:-} =~ ^[[:alnum:]_][[:alnum:]_.@-]*\.service$ ]]; then
    usage >&2
    exit 2
fi
unit=$2

if ! $apply; then
    printf 'DRY RUN: would verify %s is a loaded system service, then run systemctl mask --runtime --now %s\n' "$unit" "$unit"
    printf 'Use only for a dedicated TNEF worker. Confirm the mail pipeline queues attachments safely while it is stopped.\n'
    printf 'Runtime masking lasts until reboot or manual removal. For a procmail hook, suspend the decoder in the mail recipe and verify queue delivery.\n'
    exit 0
fi

if [[ $(systemctl show --property=LoadState --value -- "$unit") != loaded ]]; then
    printf 'Expected an existing, loaded service: %s\n' "$unit" >&2
    exit 1
fi
systemctl mask --runtime --now -- "$unit"
state=$(systemctl show --property=ActiveState --value -- "$unit")
if [[ $state != inactive && $state != failed ]]; then
    printf 'Could not verify %s stopped (state: %s). Inspect the unit before resuming mail processing.\n' "$unit" "$state" >&2
    exit 1
fi
printf 'Stopped and runtime-masked %s. Verify queue delivery and recheck after reboot.\n' "$unit"
printf 'After verifying the parser fix, remove the runtime mask with systemctl unmask --runtime -- %s and restore the service if needed.\n' "$unit"
