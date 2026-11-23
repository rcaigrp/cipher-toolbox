#!/usr/bin/env bash
set -euo pipefail

usage() {
    cat <<'EOF'
Usage: mitigate.sh --nginx-include /absolute/path/to/tabbycat-guard.conf [--apply]

Preview or install an emergency Nginx block for the tournament API.
The destination must be included at server scope in each Tabbycat virtual host.
This script leaves Nginx validation and reload to the operator.
EOF
}

apply=false
destination=''
while (( $# )); do
    case "$1" in
        --nginx-include)
            if (( $# < 2 )) || [[ $2 != /*.conf ]]; then
                usage >&2
                exit 2
            fi
            destination=$2
            shift
            ;;
        --apply) apply=true ;;
        -h|--help) usage; exit 0 ;;
        *) usage >&2; exit 2 ;;
    esac
    shift
done

if [[ -z $destination ]]; then
    usage >&2
    exit 2
fi

render_config() {
    cat <<'EOF'
# Emergency Tabbycat tournament API restriction.
# Include at server scope in the Tabbycat virtual host.
if ($uri ~ ^/api/v1/tournaments(/|$)) {
    return 403;
}
EOF
}

if [[ $apply == false ]]; then
    printf 'DRY RUN. Would install %s with the following contents.\n' "$destination"
    render_config
    exit 0
fi

staged=$(mktemp -- "$(dirname -- "$destination")/.tabbycat-guard.XXXXXX")
trap 'rm -f -- "$staged"' EXIT
render_config > "$staged"
chmod 0644 -- "$staged"
if ! ln -T -- "$staged" "$destination"; then
    if [[ ! -L $destination && -f $destination ]] && cmp -s -- "$staged" "$destination"; then
        printf 'Guard already installed at %s.\n' "$destination"
    else
        printf 'Could not install the guard at %s. Existing files are preserved.\n' "$destination" >&2
        exit 1
    fi
else
    printf 'Installed guard at %s.\n' "$destination"
fi
printf 'Confirm the server-scope include and run nginx -t before reloading Nginx. Restrict any direct backend access separately.\n'
