#!/usr/bin/env bash
set -u

if (( $# > 1 )); then
    printf 'Usage: %s [source-directory]\n' "$0" >&2
    exit 2
fi
cd -P -- "${1:-.}" || exit 2

# Report candidate locations without executing or printing source code.
pattern='(^|[[:space:]])(eval[[:space:]]+|((ba|da|z|k)?sh)[[:space:]]+-c([[:space:]]|$))|(^|[^[:alnum:]_])(system|shell_exec|popen|execSync)[[:space:]]*\(|shell[[:space:]]*=[[:space:]]*True'
find . -type f \( -name '*.sh' -o -name '*.bash' -o -name '*.py' -o -name '*.js' -o -name '*.ts' -o -name '*.php' -o -name '*.rb' \) -exec bash -c '
    pattern=$1
    shift
    failed=0
    for file do
        if matches=$(LC_ALL=C grep -InE -- "$pattern" "$file"); then
            while IFS=: read -r line remainder; do
                printf "%q:%s\n" "$file" "$line"
            done <<< "$matches"
        else
            status=$?
            if (( status != 1 )); then
                failed=1
            fi
        fi
    done
    exit "$failed"
' bash "$pattern" {} +
