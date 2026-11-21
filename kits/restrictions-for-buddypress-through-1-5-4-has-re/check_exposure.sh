#!/usr/bin/env bash
set -euo pipefail

unknown() {
    printf 'UNKNOWN: %s\n' "$1" >&2
    exit 2
}

# Listener inventory is local. Proxies, NAT, and firewalls affect public reachability.
if command -v ss >/dev/null && listeners=$(ss -lnt); then
    printf 'Local TCP listeners (bind addresses alone do not establish internet reachability):\n%s\n' "$listeners"
else
    echo 'Local listener inventory unavailable.' >&2
fi

(( $# == 1 )) || unknown 'Usage: bash check_exposure.sh /absolute/local/wordpress/root'
root=$1
[[ $root == /* && -f "$root/wp-load.php" && -d "$root/wp-includes" ]] || unknown 'Provide the absolute path to a local WordPress root.'
command -v wp >/dev/null || unknown 'WP-CLI is unavailable.'
command -v dpkg >/dev/null || unknown 'dpkg is required for version comparison.'

inventory=$(wp --path="$root" --skip-plugins --skip-themes plugin list --fields=name,status,version --format=csv) || unknown 'Could not read local plugin inventory.'
[[ ${inventory%%$'\n'*} == name,status,version ]] || unknown 'Unexpected WP-CLI inventory format.'

plugin_entry() {
    awk -F, -v plugin="$1" '$1 == plugin {print $2 "," $3}' <<< "$inventory"
}

entry=$(plugin_entry bp-restrict)
if [[ -z $entry ]]; then
    echo 'NO AFFECTED PLUGIN FOUND in the selected WordPress inventory.'
    exit 0
fi
IFS=, read -r status version <<< "$entry"
printf 'bp-restrict: %s (%s)\n' "$version" "$status"
[[ $version =~ ^[0-9]+(\.[0-9]+)*$ ]] || unknown 'Version is outside the supported numeric release format.'
if dpkg --compare-versions "$version" ge 1.5.5; then
    echo 'MEETS FIXED VERSION THRESHOLD (1.5.5).'
    exit 0
fi
if ! dpkg --compare-versions "$version" le 1.5.4; then
    unknown 'Version falls between the reported affected and fixed releases.'
fi

active=0
for plugin in bp-restrict buddypress paid-memberships-pro; do
    entry=$(plugin_entry "$plugin")
    state=${entry%%,*}
    printf '%s activation: %s\n' "$plugin" "${state:-absent}"
    case "$state" in
        active|active-network) active=$((active + 1)) ;;
        inactive|'') ;;
        *) unknown "Unrecognized activation status for $plugin." ;;
    esac
done

if (( active == 3 )); then
    echo 'POTENTIALLY EXPOSED: affected release and all three plugins active in the selected site context.'
    echo 'The reported risky conditions are enabled by default. Site-specific settings and public reachability require separate verification.'
    exit 1
fi
echo 'AFFECTED VERSION PRESENT: the reported activation prerequisites are incomplete in the selected site context. Review other multisite sites separately and update the installed copy.'
