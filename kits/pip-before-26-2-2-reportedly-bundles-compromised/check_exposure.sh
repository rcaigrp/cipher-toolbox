#!/usr/bin/env bash
set -euo pipefail
if (($# == 0)); then set -- python3; fi
status=0
for python_bin in "$@"; do
    result=0
    "$python_bin" -B - <<'PY' || result=$?
import os
import re
import subprocess
import sys
from urllib.parse import urlsplit

print(f'Interpreter: {sys.executable} (Python {sys.version.split()[0]})', flush=True)
try:
    import pip
except ModuleNotFoundError as exc:
    if exc.name != 'pip':
        raise
    print('VERDICT: pip absent for this interpreter.')
    sys.exit(0)

from pip._vendor.packaging.version import Version

version = Version(pip.__version__)
print(f'pip: {version} ({pip.__file__})')
config = subprocess.run([sys.executable, '-B', '-m', 'pip', '--disable-pip-version-check', 'config', 'list'], capture_output=True, text=True)
review = set()
if config.returncode:
    review.add('pip configuration could not be read')
else:
    for line in config.stdout.splitlines():
        key, equals, raw = line.partition('=')
        if not equals:
            continue
        option = key.rsplit('.', 1)[-1].lower()
        value = raw.strip().strip('\'"')
        if option in {'trusted-host', 'cert', 'use-deprecated'} and value:
            review.add(f'pip configuration sets {option}')
        if option in {'index-url', 'extra-index-url', 'find-links'} and re.search(r'\bhttp://', value, re.I):
            review.add(f'pip configuration sets a plaintext URL in {option}')
for key in ('REQUESTS_CA_BUNDLE', 'CURL_CA_BUNDLE', 'SSL_CERT_FILE', 'SSL_CERT_DIR'):
    if os.environ.get(key):
        review.add(f'{key} overrides trust inputs for compatible clients')
for key in ('PIP_INDEX_URL', 'PIP_EXTRA_INDEX_URL', 'PIP_FIND_LINKS'):
    if any(urlsplit(item).scheme.lower() == 'http' for item in os.environ.get(key, '').split()):
        review.add(f'{key} contains a plaintext URL')
for finding in sorted(review):
    print(f'REVIEW: {finding}')
if version < Version('26.2.2'):
    print('VERDICT: potentially exposed. This pip predates 26.2.2. Runtime rejection of the affected intermediates and vendor backports require separate verification.')
    sys.exit(1)
print('VERDICT: pip meets the 26.2.2 version threshold.' + (' Review trust configuration findings above.' if review else ''))
sys.exit(2 if review else 0)
PY
    case "$result" in
        0) ;;
        1) status=1 ;;
        *) if ((status == 0)); then status=2; fi ;;
    esac
done
printf '\nLocal TCP/UDP listeners for review. CVE-2026-133949 concerns outbound pip TLS.\n'
if command -v ss >/dev/null && ss -H -lntu; then
    :
else
    echo 'Listener inventory unavailable.' >&2
    if ((status == 0)); then status=2; fi
fi
exit "$status"
