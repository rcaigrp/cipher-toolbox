#!/usr/bin/env bash
set -euo pipefail

usage() {
    printf '%s\n' 'Usage: bash check_exposure.sh [--version RELEASE] [--port PORT] [--shared yes|no|unknown]' 'Supply the running release and port from local deployment records when known.'
}

version=''
port=''
shared=unknown
while (( $# )); do
    case "$1" in
        -h|--help) usage; exit 0 ;;
        --version|--port|--shared)
            if (( $# < 2 )); then usage >&2; exit 2; fi
            case "$1" in
                --version) version=$2 ;;
                --port) port=$2 ;;
                --shared) shared=$2 ;;
            esac
            shift 2 ;;
        *) usage >&2; exit 2 ;;
    esac
done
case "$shared" in yes|no|unknown) ;; *) usage >&2; exit 2 ;; esac
if [[ -n "$port" ]] && { [[ ! "$port" =~ ^[1-9][0-9]{0,4}$ ]] || (( port > 65535 )); }; then
    usage >&2
    exit 2
fi

if [[ -z "$version" ]]; then
    for root in /opt/texera /usr/local/texera "$HOME/texera"; do
        if [[ -r "$root/version.txt" ]]; then
            printf 'Local version marker (verify against active deployment): %s\n' "$root/version.txt"
            IFS= read -r marker < "$root/version.txt" || true
            printf 'Marker version: %q\n' "$marker"
        fi
    done
fi

printf 'Shared access: %s\n' "$shared"
if [[ "$shared" == yes ]]; then
    printf '%s\n' 'Shared access increases cross-user exposure on affected releases.'
fi
if [[ -z "$port" ]]; then
    printf '%s\n' 'Texera listener unknown. Provide the deployment port with --port.'
elif command -v ss >/dev/null && listeners=$(ss -H -lnt "sport = :$port"); then
    if [[ -z "$listeners" ]]; then
        printf 'No TCP listener on port %s in this network namespace.\n' "$port"
    else
        printf 'Local TCP listeners on port %s (confirm service ownership):\n%s\n' "$port" "$listeners"
        while read -r state recvq sendq address peer; do
            case "$address" in
                127.*|\[::1\]:*) ;;
                *) printf 'Review access controls for non-loopback bind %s.\n' "$address" ;;
            esac
        done <<< "$listeners"
    fi
else
    printf '%s\n' 'Local listener check unavailable.'
fi

if [[ "$version" == 1.3.0-incubating ]]; then
    printf '%s\n' 'FIXED RELEASE REPORTED: 1.3.0-incubating. Verify important historical workflow results.'
    exit 0
fi
if [[ "$version" =~ ^(0|1)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(-incubating)?$ ]]; then
    major=${BASH_REMATCH[1]}
    minor=${BASH_REMATCH[2]}
    if [[ "$major" == 0 || "$minor" =~ ^[012]$ ]]; then
        printf 'POTENTIALLY EXPOSED: %s predates the documented fix. Prioritize shared deployments.\n' "$version"
        exit 1
    fi
fi
printf 'UNKNOWN: running release %q has no verified fix status in the supplied material. Confirm the active release and provenance.\n' "$version"
exit 2
