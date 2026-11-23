#!/usr/bin/env bash
set -euo pipefail

usage() {
    printf '%s\n' 'Usage: check_exposure.sh [--version X.Y.Z] [--repo LOCAL_CHECKOUT] [--nginx-include LOCAL_FILE]' 'Run with the deployment Python on PATH, or supply the deployed version explicitly.' 'Pass the deployed checkout and active server-scope guard file when available.'
}

version=''
repo=''
guard=''
while (( $# )); do
    case "$1" in
        -h|--help) usage; exit 0 ;;
        --version|--repo|--nginx-include)
            if (( $# < 2 )) || [[ -z $2 || $2 == --* ]]; then usage >&2; exit 2; fi
            case "$1" in
                --version) version=$2 ;;
                --repo) repo=$2 ;;
                --nginx-include) guard=$2 ;;
            esac
            shift 2 ;;
        *) usage >&2; exit 2 ;;
    esac
done

if [[ -z $version ]]; then
    version=$(python3 - <<'PY'
from importlib.metadata import PackageNotFoundError, version

for name in ('tabbycat-debate', 'tabbycat'):
    try:
        print(version(name))
        break
    except PackageNotFoundError:
        continue
PY
    ) || version=''
fi
printf 'Reported version: %s\n' "${version:-unknown}"

fix=b7f0746ba9cb5a23f94ac169dbe5b68a5fbd1ab2
printf 'Known upstream fix: %s. Fixed tagged release unconfirmed.\n' "$fix"
fix_present=false
if [[ -n $repo ]] && command -v git >/dev/null && GIT_NO_LAZY_FETCH=1 git -C "$repo" merge-base --is-ancestor "$fix" HEAD 2>/dev/null; then
    fix_present=true
    printf '%s\n' 'The supplied checkout includes the upstream fix in its history. Confirm the running build matches this checkout.'
elif [[ -n $repo ]]; then
    printf '%s\n' 'The upstream fix could not be verified in the supplied checkout. Shallow history and backports can obscure this check.'
fi

if [[ -n $guard && -r $guard ]] && awk '
    /^[[:space:]]*if \(\$uri ~ \^\/api\/v1\/tournaments\(\/\|\$\)\) \{[[:space:]]*$/ { found = (getline > 0 && $0 ~ /^[[:space:]]*return 403;[[:space:]]*$/ && getline > 0 && $0 ~ /^[[:space:]]*\}[[:space:]]*$/); if (found) exit }
    END { exit !found }
' "$guard"; then
    printf '%s\n' 'The supplied file contains the kit guard. Verify it is loaded for each Tabbycat host and that clients cannot bypass the proxy.'
else
    printf '%s\n' 'Tournament API restrictions are unverified. Review the active proxy and any direct backend access.'
fi

printf '%s\n' 'Local TCP listeners (review backend port bindings and process ownership):'
if ! command -v ss >/dev/null || ! ss -ltnp; then
    printf '%s\n' 'Local TCP listeners could not be enumerated.'
fi

if [[ $fix_present == true ]]; then
    printf '%s\n' 'VERDICT FIX PRESENT IN SUPPLIED CHECKOUT. Running build and network reachability remain unverified.'
    exit 0
fi

if [[ $version =~ ^2\.(9|10|11)\.(0|[1-9][0-9]*)$ || $version =~ ^2\.12\.[01]$ ]]; then
    printf '%s\n' 'VERDICT POTENTIALLY EXPOSED. Version is in the reported affected range and the running fix and access restrictions are unverified.'
    exit 1
fi

if [[ $version =~ ^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$ ]]; then
    printf '%s\n' 'VERDICT OUTSIDE REPORTED RANGE. Fix status and reachability remain unverified.'
    exit 0
fi

printf '%s\n' 'VERDICT UNKNOWN. Identify the running release and verify the upstream fix and access restrictions.'
exit 2
