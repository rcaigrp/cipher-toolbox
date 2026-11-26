#!/bin/bash

usage() {
    echo 'Usage: check_exposure.sh [DIRECTORY]'
    echo 'Scan local ASP.NET project files for exposure indicators. Defaults to the current directory.'
}

case ${1-} in
    -h|--help)
        usage
        exit 0
        ;;
    -*)
        usage >&2
        exit 2
        ;;
esac
if (( $# > 1 )); then
    usage >&2
    exit 2
fi
cd -- "${1-.}" || exit 2

scan() {
    local message=$1 matches status
    shift
    if matches=$(grep -rn "$@" .); then
        printf '%s\n' "$message" "$matches"
    else
        status=$?
        if (( status != 1 )); then
            exit "$status"
        fi
    fi
}

printf '%s\n' 'Checking local files for legacy ASP.NET exposure indicators...'
scan 'WARNING: Idunno.AntiCsrf reference detected' \
    -F -e 'Idunno.AntiCsrf' --include='*.csproj' --include='*.xml' --include='*.config' --include='*.props'

webforms=$(find . -type f \( -iname '*.aspx' -o -iname '*.ascx' \) -print) || exit 2
if [[ -n $webforms ]]; then
    printf '%s\n' 'INFO: Legacy ASP.NET WebForms files detected'
    head -n 5 <<< "$webforms"
fi

scan 'WARNING: BinaryFormatter or SoapFormatter reference detected' \
    -E -w -e 'BinaryFormatter|SoapFormatter' --include='*.cs'
scan 'INFO: Cookieless session state indicator detected' \
    -Ei -e "<sessionState[[:space:]][^>]*[[:space:]]cookieless[[:space:]]*=[[:space:]]*(\"(true|UseUri)\"|'(true|UseUri)')" \
    --include='*.xml' --include='*.config'

printf '%s\n' 'Check complete.'
