#!/usr/bin/env bash
set -euo pipefail

usage() {
    printf '%s\n' 'Usage: mitigate.sh [--apply] UNIT.service CPU_PERCENT MEMORY_MIB TASKS' \
        'Use only for a dedicated parser worker that needs no network access.' \
        'Set limits from measured workload. TASKS includes threads.'
}

apply=false
case ${1:-} in
    --apply) apply=true; shift ;;
    --help|-h) usage; exit 0 ;;
esac
if [[ $# != 4 ]]; then usage >&2; exit 2; fi
unit=$1
cpu=$2
memory=$3
tasks=$4
if [[ ! $unit =~ ^[a-zA-Z0-9_][a-zA-Z0-9_.@-]*\.service$ ||
      ! $cpu =~ ^[1-9][0-9]{0,5}$ || ! $memory =~ ^[1-9][0-9]{0,8}$ ||
      ! $tasks =~ ^[1-9][0-9]{0,8}$ ]]; then
    usage >&2
    exit 2
fi

dir="/etc/systemd/system/$unit.d"
target="$dir/90-parser-isolation.conf"
config=$(printf '[Service]\nNoNewPrivileges=yes\nPrivateNetwork=yes\nRestrictAddressFamilies=AF_UNIX\nCPUQuota=%s%%\nMemoryMax=%sM\nTasksMax=%s\n' "$cpu" "$memory" "$tasks")
printf 'Drop-in for %s\n%s\n\n%s\n' "$unit" "$target" "$config"
printf '%s\n' 'Verify the worker uses a non-root service identity and needs no IP sockets.' \
    'Set per-message CPU time, parser concurrency, MIME depth, header and decoded-pixel limits in the application.' \
    'Patch affected MIME parser deployments to 3.0.6 or 4.0.2 on the appropriate branch and affected Mailpit deployments to 1.30.4 or later.' \
    'Review existing drop-ins and inherited sockets. Restart the worker during a maintenance window after reloading systemd.'
if ! $apply; then
    printf '%s\n' 'Dry run. No files were written.'
    exit 0
fi

if (( EUID != 0 )); then printf '%s\n' 'Apply requires root.' >&2; exit 2; fi
settings=$(systemctl show --property=LoadState,User,DynamicUser -- "$unit")
if ! grep -qx 'LoadState=loaded' <<< "$settings"; then
    printf '%s\n' 'The system service must already exist and load successfully.' >&2
    exit 2
fi
if ! grep -qx 'DynamicUser=yes' <<< "$settings" &&
   { ! grep -q '^User=.' <<< "$settings" || grep -Eq '^User=(root|0+)$' <<< "$settings"; }; then
    printf '%s\n' 'Configure a non-root service identity before applying this drop-in.' >&2
    exit 2
fi
install -d -m 0755 -- "$dir"
tmp=$(mktemp -- "$dir/.parser-isolation.XXXXXXXX")
trap 'rm -f -- "$tmp"' EXIT
printf '%s\n' "$config" > "$tmp"
chmod 0644 -- "$tmp"
if ! ln -T -- "$tmp" "$target"; then
    if [[ -L $target || ! -f $target ]] || ! cmp -s -- "$tmp" "$target"; then
        printf 'Could not install %s. Review the path and any existing drop-in.\n' "$target" >&2
        exit 2
    fi
fi
printf 'Installed %s. Run systemctl daemon-reload and restart %s when ready.\n' "$target" "$unit"
