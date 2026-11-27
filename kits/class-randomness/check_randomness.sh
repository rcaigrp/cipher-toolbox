#!/usr/bin/env bash
# Inventory references for source review without printing source lines or executing project code.
set -uo pipefail

if [[ ${1-} == --help && $# -eq 1 ]]; then
    printf 'Usage: %s [SOURCE_DIRECTORY]\n' "${0##*/}"
    exit 0
fi
if (( $# > 1 )); then
    printf 'Usage: %s [SOURCE_DIRECTORY]\n' "${0##*/}" >&2
    exit 2
fi
if ! cd -- "${1:-.}"; then
    exit 2
fi

export LC_ALL=C
find . -type d -name .git -prune -o -type f \( \
    -name '*.pl' -o -name '*.pm' -o -name '*.t' -o -name '*.psgi' -o \
    -name 'cpanfile' -o -name 'cpanfile.snapshot' -o -name 'Makefile.PL' -o \
    -name 'Build.PL' -o -name 'META.json' -o -name 'META.yml' \
\) -print0 |
while IFS= read -r -d '' path; do
    case "$path" in
        */cpanfile|*/cpanfile.snapshot|*/Makefile.PL|*/Build.PL|*/META.json|*/META.yml)
            pattern='(^|[^[:alnum:]_])Strong::Random([^[:alnum:]_:]|$)'
            ;;
        *)
            pattern='(^|[^[:alnum:]_$@%>])((CORE::)?s?rand([[:space:]]*\(|[[:space:]]+|[;),}]|$)|Strong::Random([^[:alnum:]_:]|$))'
            ;;
    esac
    if grep -E -- "$pattern" "$path" >/dev/null; then
        printf 'Review randomness reference in %q\n' "$path"
    else
        status=$?
        if (( status != 1 )); then
            exit "$status"
        fi
    fi
done
