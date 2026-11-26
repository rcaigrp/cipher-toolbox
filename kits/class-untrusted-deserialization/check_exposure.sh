#!/bin/bash
set -o pipefail

usage() {
    printf 'Usage: %s [DIRECTORY]\nScan a directory for potential .NET deserialization exposure. Defaults to the current directory.\n' "${0##*/}"
}

if [[ $# -eq 1 && ( $1 == --help || $1 == -h ) ]]; then
    usage
    exit 0
fi

if [[ $# -gt 1 || ${1:-} == -* ]]; then
    usage >&2
    exit 2
fi

root=${1:-.}
if [[ ! -d $root ]]; then
    printf 'Directory not found: %s\n' "$root" >&2
    exit 2
fi

for dependency in find grep strings; do
    if ! command -v "$dependency" >/dev/null; then
        printf 'Required command not found: %s\n' "$dependency" >&2
        exit 1
    fi
done

[[ $root == /* || $root == . ]] || root=./$root
serializer='BinaryFormatter|SoapFormatter'

printf 'Checking for untrusted deserialization exposure...\n'
if ! find "$root" -type f \( -iname '*.dll' -o -iname '*.exe' -o -iname 'web.config' -o -iname 'app.config' -o -iname '*.cs' \) -print0 | (
    failed=0
    while IFS= read -r -d '' file; do
        case ${file,,} in
            *.dll|*.exe)
                strings -- "$file" | grep -Ei "$serializer" >/dev/null
                result=("${PIPESTATUS[@]}")
                if (( result[0] != 0 || result[1] > 1 )); then
                    failed=1
                elif (( result[1] == 0 )); then
                    printf 'Potential dangerous serializer found in: %s\n' "$file"
                fi
                ;;
            */web.config|*/app.config)
                grep -Ei "$serializer|System\.Runtime\.Serialization\.Formatters\.(Binary|Soap)" -- "$file" >/dev/null
                case $? in
                    0) printf 'Potential unsafe deserialization configuration found in: %s\n' "$file" ;;
                    2) failed=1 ;;
                esac
                ;;
            *.cs)
                grep -Ei "$serializer" -- "$file" >/dev/null
                case $? in
                    0) printf 'Potential dangerous deserialization method found in: %s\n' "$file" ;;
                    2) failed=1 ;;
                esac
                if grep -Eq '(Deserialize|ReadObject)' -- "$file" && grep -Eiq '\b(request|cookie|cookies|form|session)\b' -- "$file"; then
                    printf 'Potential untrusted deserialization pattern found in: %s\n' "$file"
                fi
                ;;
        esac
    done
    exit "$failed"
); then
    printf 'Scan incomplete. See errors above.\n' >&2
    exit 1
fi
printf 'Check complete.\n'
