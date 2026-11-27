#!/usr/bin/env bash
set -euo pipefail

kit_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
checker="$kit_dir/check_randomness.sh"
fixture=$(mktemp -d)
trap 'rm -rf -- "$fixture"' EXIT

mkdir -- "$fixture/.git" "$fixture/clean"
printf '%s\n' 'my $sample = CORE::rand(100);' > "$fixture/weak sample.pm"
printf '%s\n' 'requires "Strong::Random";' > "$fixture/cpanfile"
printf '%s\n' 'my $random_value = 1;' > "$fixture/clean/identifier.pl"
printf '%s\n' 'my $sample = rand(100);' > "$fixture/.git/ignored.pl"

actual=$("$checker" "$fixture" | LC_ALL=C sort)
expected=$(printf 'Review randomness reference in %q\n' './cpanfile' './weak sample.pm')
if [[ $actual != "$expected" ]]; then
    printf 'Unexpected findings.\nExpected:\n%s\nActual:\n%s\n' "$expected" "$actual" >&2
    exit 1
fi

[[ -z $("$checker" "$fixture/clean") ]]
"$checker" --help >/dev/null
status=0
"$checker" "$fixture/missing" >/dev/null 2>&1 || status=$?
[[ $status -eq 2 ]]
printf 'PASS: expected findings, clean directory, Git exclusion, help, and invalid directory\n'
