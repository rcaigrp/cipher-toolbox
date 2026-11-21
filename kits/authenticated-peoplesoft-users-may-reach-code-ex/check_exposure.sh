#!/usr/bin/env bash
set -euo pipefail

usage() {
    printf 'Usage: %s [--installed-version VERSION] [--config FILE]\n' "$0"
}

version=''
configs=()
while (($#)); do
    case "$1" in
        --installed-version|--config)
            if (($# < 2)) || [[ -z "$2" || "$2" == --* ]]; then usage >&2; exit 64; fi
            if [[ "$1" == --installed-version ]]; then version=$2; else configs+=("$2"); fi
            shift 2
            ;;
        --help|-h) usage; exit 0 ;;
        *) usage >&2; exit 64 ;;
    esac
done

printf 'Local PeopleTools exposure review for CVE-2026-35273 / ZDI-26-1039\n'
if [[ -n "$version" && ! "$version" =~ ^[0-9]+\.[0-9]+(\.[0-9]+)*$ ]]; then
    printf 'Supply a numeric PeopleTools build, such as 8.61 or a more specific installed build.\n' >&2
    exit 64
fi
case "$version" in
    8.61|8.61.*|8.62|8.62.*)
        printf 'Installed build from operator inventory: %s (Oracle lists this release family as affected).\n' "$version" ;;
    '') printf 'Installed build unknown. Supply the build from local inventory with --installed-version.\n' ;;
    *) printf 'Installed build from operator inventory: %s (outside the supported release families named in the supplied alert).\n' "$version" ;;
esac
printf 'Fixed build for ZDI-26-1039: unconfirmed in supplied material.\n'

for root in "${PS_HOME:-}" "${PS_CFG_HOME:-}"; do
    if [[ -n "$root" && -d "$root" ]]; then
        printf 'Local PeopleTools environment directory: %s\n' "$root"
    fi
done

if ((${#configs[@]} == 0)); then
    printf 'Configuration: supply local domain or listener configuration with --config for review.\n'
fi
for config in "${configs[@]}"; do
    if [[ ! -f "$config" || ! -r "$config" ]]; then
        printf 'Configuration unreadable: %s\n' "$config" >&2
        continue
    fi
    awk '/^[[:space:]]*[^#;=]*=/ && /=[[:space:]]*(0[.]0[.]0[.]0|::|[*])[[:space:]]*([#;].*)?$/ { printf "Review wildcard binding in %s at line %d\n", FILENAME, FNR; found=1 } END { if (!found) printf "No wildcard assignments found by this limited check in %s\n", FILENAME }' "$config"
done

printf 'Local TCP/UDP listeners (check owners and bindings against deployment inventory):\n'
if ! command -v ss >/dev/null || ! ss -H -lntup; then
    printf 'Listener inventory unavailable.\n' >&2
fi
case "$version" in
    8.61|8.61.*|8.62|8.62.*) printf 'Verdict: POTENTIALLY AFFECTED. Verify Oracle fix coverage and management-plane reachability for this build.\n' ;;
    *) printf 'Verdict: INDETERMINATE. Verify installed build, Oracle fix coverage, and management-plane reachability.\n' ;;
esac
exit 2
