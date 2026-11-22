#!/usr/bin/env bash
set -euo pipefail

usage() {
    printf '%s\n' 'Usage: bash mitigate.sh [--upgrade-script /absolute/path] [--apply]' \
        'The optional script must be your reviewed, credential-free procedure for upgrading this local Texera deployment to 1.3.0-incubating.' \
        'By default this command prints the plan. --apply requires an explicit upgrade script.'
}

apply=false
upgrade_script=''
while (( $# > 0 )); do
    case "$1" in
        --apply) apply=true; shift ;;
        --upgrade-script)
            if (( $# < 2 )) || [[ "$2" != /* ]]; then
                usage >&2
                exit 2
            fi
            upgrade_script=$2
            shift 2
            ;;
        -h|--help) usage; exit 0 ;;
        *) usage >&2; exit 2 ;;
    esac
done

printf '%s\n' 'Upgrade the local Texera deployment to the fixed release, 1.3.0-incubating.' \
    'After upgrading, verify the running release and compare important workflow results against trusted copies or rerun the workflows from trusted inputs.'
if [[ -n "$upgrade_script" ]]; then
    if [[ ! -f "$upgrade_script" || ! -x "$upgrade_script" ]]; then
        printf 'Upgrade script must be an executable regular file: %s\n' "$upgrade_script" >&2
        exit 2
    fi
    printf 'Local upgrade command: %q\n' "$upgrade_script"
fi

if [[ "$apply" == false ]]; then
    printf '%s\n' 'Dry run. No changes made.'
    exit 0
fi
if [[ -z "$upgrade_script" ]]; then
    printf '%s\n' '--apply requires --upgrade-script with a reviewed local upgrade procedure.' >&2
    exit 2
fi
"$upgrade_script"
printf '%s\n' 'Upgrade command completed. Verify the running release and important workflow results.'
