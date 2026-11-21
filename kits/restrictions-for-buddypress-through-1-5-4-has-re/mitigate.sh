#!/usr/bin/env bash
set -euo pipefail

usage() {
    echo 'Usage: bash mitigate.sh /absolute/local/wordpress/root [--apply]' >&2
    exit 2
}

(( $# == 1 || $# == 2 )) || usage
root=$1
[[ $root == /* && -f "$root/wp-load.php" && -d "$root/wp-includes" ]] || usage
[[ $# == 1 || $2 == --apply ]] || usage
apply=${2:-}
command -v wp >/dev/null || { echo 'WP-CLI is required.' >&2; exit 2; }

wp_local() {
    wp --path="$root" --skip-plugins --skip-themes "$@"
}

if ! inventory=$(wp_local plugin list --fields=name,status,version --format=csv); then
    echo 'Unable to read plugin inventory. No change made.' >&2
    exit 2
fi
entry=$(awk -F, '$1 == "bp-restrict" { print $2 "," $3 }' <<< "$inventory")
if [[ -z $entry ]]; then
    echo 'bp-restrict is absent from the plugin inventory.'
    exit 0
fi
IFS=, read -r status version <<< "$entry"
if [[ ! $version =~ ^[0-9]+(\.[0-9]+)*$ ]]; then
    echo 'Unrecognized release version. Verify patch status manually.' >&2
    exit 2
fi
if dpkg --compare-versions "$version" ge 1.5.5; then
    echo "bp-restrict $version meets the fixed-version threshold."
    exit 0
fi

case $status in
    active) scope=() ;;
    active-network) scope=(--network) ;;
    inactive)
        echo "bp-restrict $version is inactive in the selected site context. Check other sites separately on multisite."
        exit 0 ;;
    *) echo "Unknown activation status: $status" >&2; exit 2 ;;
esac

printf 'Affected release %s (%s). Update to 1.5.5 or a newer patched release.\n' "$version" "$status"
if [[ -z $apply ]]; then
    printf 'DRY RUN: would deactivate bp-restrict (%s) at %s if an update cannot be applied promptly.\n' "$status" "$root"
    exit 0
fi

wp_local plugin deactivate bp-restrict "${scope[@]}"
updated_status=$(wp_local plugin list --fields=name,status --format=csv | awk -F, '$1 == "bp-restrict" {print $2}')
if [[ $updated_status != inactive ]]; then
    echo "Deactivation could not be verified in the selected site context (status: ${updated_status:-unknown})." >&2
    exit 2
fi
echo 'Verified bp-restrict is inactive in the selected site context.'
