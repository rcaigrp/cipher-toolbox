#!/usr/bin/env bash
set -euo pipefail

kit_dir=$(cd -- "$(dirname -- "$0")" && pwd)
scanner="$kit_dir/check_exposure.sh"
fixtures=$(mktemp -d)
trap 'rm -rf -- "$fixtures"' EXIT
printf '%s\n' '# eval marker for the static scanner' > "$fixtures/flagged.sh"
printf '%s\n' '# ordinary greeting' > "$fixtures/clean.sh"

help=$("$scanner" --help)
[[ $help == Usage:* ]]
expected='./flagged.sh:1'
[[ $("$scanner" "$fixtures") == "$expected" ]]
[[ $(cd -- "$fixtures" && "$scanner") == "$expected" ]]
status=0
"$scanner" "$fixtures/missing" >/dev/null 2>&1 || status=$?
[[ $status == 2 ]]
printf 'Scanner tests passed\n'
