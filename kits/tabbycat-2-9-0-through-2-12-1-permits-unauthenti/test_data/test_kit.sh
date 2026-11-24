#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.."

tmp=$(mktemp -d)
trap 'rm -rf -- "$tmp"' EXIT
guard=$tmp/tabbycat-guard.conf

for script in check_exposure.sh mitigate.sh; do
    bash -n "$script"
    "./$script" --help >/dev/null
done

status=0
./check_exposure.sh --version 2.12.1 >"$tmp/exposure.out" || status=$?
[[ $status == 1 ]]
grep -q 'VERDICT POTENTIALLY EXPOSED' "$tmp/exposure.out"

./mitigate.sh --nginx-include "$guard" >"$tmp/preview"
[[ ! -e $guard ]]
./mitigate.sh --nginx-include "$guard" --apply
sed '1d' "$tmp/preview" | diff - "$guard"
./mitigate.sh --nginx-include "$guard" --apply >"$tmp/reapply.out" 2>"$tmp/reapply.err"
grep -q 'Guard already installed' "$tmp/reapply.out"
[[ ! -s $tmp/reapply.err ]]
printf '%s\n' 'existing config' >"$guard"
status=0
./mitigate.sh --nginx-include "$guard" --apply >"$tmp/conflict.out" 2>"$tmp/conflict.err" || status=$?
[[ $status == 1 ]]
grep -qx 'existing config' "$guard"

# Test log parsing for hunt.md
grep -E '"(POST|PUT|PATCH|DELETE) /api/v1/tournaments([/?][^" ]*)? HTTP/[0-9.]+" [1-5][0-9]{2} ' test_data/access.log | sed -E 's/^[^"]*"([A-Z]+) .*/\1/' >"$tmp/log.methods"
jq -r 'select(((.method // "" | ascii_upcase) | IN("POST", "PUT", "PATCH", "DELETE")) and ((.uri // "") | test("^/api/v1/tournaments([/?]|$)"))) | .method' test_data/access.json >"$tmp/json.methods"
# Both fixtures contain two successful writes, a read, and one blocked write.
# The hunt keeps blocked writes for timeline review.
printf '%s\n' POST POST POST >"$tmp/expected.methods"
diff "$tmp/expected.methods" "$tmp/log.methods"
diff "$tmp/expected.methods" "$tmp/json.methods"
printf '%s\n' 'Tabbycat kit smoke tests passed.'