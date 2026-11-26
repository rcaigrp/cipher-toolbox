#!/usr/bin/env bash
set -euo pipefail

usage() {
    printf 'Usage: %s LOCAL_WEB_ROOT\n' "${0##*/}"
    printf 'Lists candidate setup artifacts. Review ingress and application configuration separately to determine reachability.\n'
}

if [[ $# -eq 1 && $1 == --help ]]; then
    usage
    exit 0
fi

if [[ $# -ne 1 || $1 == *://* || ! -d $1 || ! -r $1 || ! -x $1 ]]; then
    usage >&2
    exit 2
fi

root=$1
paths=(install.php core/install.php wp-admin/install.php setup admin/install install bootstrap init)
found=0
for path in "${paths[@]}"; do
    if [[ -L "$root/$path" || -e "$root/$path" ]]; then
        printf 'Candidate setup artifact: %q\n' "$path"
        found=1
    fi
done

if [[ $found -eq 0 ]]; then
    printf 'No candidate setup artifacts found at the checked paths.\n'
fi
