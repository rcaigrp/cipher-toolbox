#!/bin/bash
set -eu
cd -- "$(dirname -- "$0")"

output=$(./check_exposure.sh test_files)
grep -Fxq 'Potential unsafe deserialization configuration found in: ./test_files/web.config' <<< "$output"
grep -Fxq 'Potential dangerous deserialization method found in: ./test_files/test_vulnerable_code.cs' <<< "$output"
if grep -Fq 'test_safe_code.cs' <<< "$output"; then
    printf '%s\n' 'Unexpected finding for the safe C# sample' >&2
    exit 1
fi
printf '%s\n' 'Untrusted deserialization sample test passed.'
