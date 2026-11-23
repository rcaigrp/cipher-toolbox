#!/bin/bash
# Check for command injection exposure in bash scripts
# This is a defensive tool only, no execution or modification

set -euo pipefail

usage() {
    printf 'Usage: %s [directory]\nScan shell scripts in directory (default: current directory).\n' "$0"
}

if [[ $# -eq 1 && ( $1 == --help || $1 == -h ) ]]; then
    usage
    exit 0
fi

if [[ $# -gt 1 ]]; then
    usage >&2
    exit 2
fi

target_dir="${1-.}"

if [[ ! -d "$target_dir" ]]; then
    echo "Error: '$target_dir' is not a directory"
    exit 2
fi

# Report candidate locations without executing or printing source code.
cd -- "$target_dir"
pattern='(^|[^[:alnum:]_])(eval|system|exec|shell|backtick)([^[:alnum:]_]|$)|\$\(|\$\{'
find . -type f -name '*.sh' -exec bash -c '
    set -o pipefail
    pattern=$1
    shift
    for path do
        grep -nE -- "$pattern" "$path" | while IFS=: read -r line remainder; do
            printf "%s:%s\n" "$path" "$line"
        done
        statuses=("${PIPESTATUS[@]}")
        if (( statuses[0] > 1 || statuses[1] != 0 )); then
            exit 1
        fi
    done
' bash "$pattern" {} +
