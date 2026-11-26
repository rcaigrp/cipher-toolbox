#!/bin/bash
set -eu
cd -- "$(dirname -- "$0")"

output=$(./check_exposure.sh test_files)
grep -Fxq 'WARNING: Idunno.AntiCsrf reference detected' <<< "$output"
grep -F './test_vulnerable_config.xml:' <<< "$output" | grep -Fq 'Idunno.AntiCsrf'
for sample in test_web_config.xml test_vulnerable_config.xml; do
    grep -F "./$sample:" <<< "$output" | grep -Fq 'cookieless="true"'
done
if grep -Eq 'WebForms files detected|BinaryFormatter or SoapFormatter reference detected' <<< "$output"; then
    printf '%s\n' 'Unexpected finding in the XML samples' >&2
    exit 1
fi
printf '%s\n' 'Legacy ASP.NET sample test passed.'
